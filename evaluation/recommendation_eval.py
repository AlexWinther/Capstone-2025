import os
import sys
import pandas as pd
from sklearn.metrics import precision_score, recall_score, accuracy_score
import numpy as np
import uuid
import json

# Set CHROMA_HOST to localhost for local execution
os.environ["CHROMA_HOST"] = "localhost"

# Setup paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from llm.LLMDefinition import set_default_llm, get_available_models
from llm.StategraphAgent import input_node, out_of_scope_check_node, quality_control_node
from paper_handling.paper_handler import fetch_works_multiple_queries
from llm.Embeddings import embed_paper_text
from chroma_db.chroma_vector_db import CHROMA_HOST, CHROMA_PORT

import chromadb

# --- Configuration ---
MODELS_TO_TEST = ["gpt-5-nano"]
SEARCH_RESULTS_TO_CHECK_LIST = [100]
EVALUATION_DATASET = "evaluation/data/paper_pairs.csv"
RESULTS_FILENAME = "recommendation_evaluation_results.txt"
EVAL_SET_SIZE = 50

def calculate_mrr(ranks):
    """Calculates the Mean Reciprocal Rank."""
    if not ranks:
        return 0.0
    reciprocal_ranks = [1.0 / rank for rank in ranks if rank > 0]
    if not reciprocal_ranks:
        return 0.0
    return np.mean(reciprocal_ranks)

def run_full_pipeline_evaluation(row, model_name, search_results_count) -> tuple:
    """
    Performs a single round-trip evaluation of the full recommendation pipeline.
    """
    try:
        set_default_llm(model_name)

        paper1_title = row["title_first"]
        paper1_abstract = row["abstract_first"]
        paper2_id = row["openalexid_second"]

        query_text = f"Title: {paper1_title}. Abstract: {paper1_abstract}"

    except Exception as e:
        print(f"ERROR setting up paper: {e}")
        return "ERROR", None, None

    # 1. Keyword Generation using the correct agent flow
    try:
        state = input_node({"user_query": query_text})
        state = out_of_scope_check_node(state)
        state = quality_control_node(state)

        generated_keywords = state.get("keywords", [])
        if not generated_keywords:
            print("WARNING: No keywords generated. Aborting run.")
            return "ERROR", None, None
    except Exception as e:
        print(f"ERROR in keyword generation: {e}")
        return "ERROR", None, None

    # 2. Fetch Candidate Papers
    try:
        candidate_papers, status = fetch_works_multiple_queries(
            queries=generated_keywords, per_page=search_results_count
        )
        if not candidate_papers:
            print("WARNING: Keyword search failed or returned no results.")
            return "ERROR", None, None

        # De-duplicate candidate papers based on their ID
        unique_papers = {}
        for paper in candidate_papers:
            paper_id = paper.get('id')
            if paper_id and paper_id not in unique_papers:
                unique_papers[paper_id] = paper
        candidate_papers = list(unique_papers.values())

    except Exception as e:
        print(f"ERROR fetching and de-duplicating candidate papers: {e}")
        return "ERROR", None, None

    # 3. Embeddings and In-Memory ChromaDB evaluation
    temp_collection_name = f"eval_{uuid.uuid4().hex}"
    chroma_client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
    prediction = 0
    rank = 0

    try:
        temp_collection = chroma_client.create_collection(name=temp_collection_name)

        paper_texts = [f"{p.get('title', '')} {p.get('abstract', '')}" for p in candidate_papers]
        if not paper_texts:
            print("WARNING: No paper texts to embed. Aborting run.")
            return "ERROR", None, None

        embeddings = [embed_paper_text(text) for text in paper_texts]
        paper_ids = [p.get('id') for p in candidate_papers]

        valid_indices = [i for i, pid in enumerate(paper_ids) if pid is not None and embeddings[i] is not None]
        if not valid_indices:
            print("WARNING: No valid papers after filtering for IDs and embeddings. Aborting run.")
            return "ERROR", None, None

        temp_collection.add(
            ids=[paper_ids[i] for i in valid_indices],
            embeddings=[embeddings[i] for i in valid_indices],
            documents=[paper_texts[i] for i in valid_indices]
        )

        query_embedding = embed_paper_text(query_text)
        if query_embedding is None:
            print("WARNING: Could not generate embedding for query. Aborting run.")
            return "ERROR", None, None

        results = temp_collection.query(
            query_embeddings=[query_embedding],
            n_results=search_results_count,
            include=['documents']
        )

        ranked_ids = results.get('ids', [[]])[0]
        if paper2_id in ranked_ids:
            rank = ranked_ids.index(paper2_id) + 1
            prediction = 1

        return "SUCCESS", prediction, rank

    except Exception as e:
        print(f"ERROR during ChromaDB interaction/embedding generation: {e}")
        return "ERROR", None, None
    finally:
        try:
            client_for_cleanup = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
            if temp_collection_name in [c.name for c in client_for_cleanup.list_collections()]:
                client_for_cleanup.delete_collection(name=temp_collection_name)
        except Exception as e:
            print(f"ERROR during cleanup of temporary ChromaDB collection: {e}")


def main():
    """Main function to orchestrate the recommendation system evaluation."""
    print("Starting full pipeline recommendation system evaluation...")

    try:
        df = pd.read_csv(EVALUATION_DATASET)
        if EVAL_SET_SIZE > 0:
            df = df.head(EVAL_SET_SIZE)
    except FileNotFoundError:
        print(f"Error: Dataset '{EVALUATION_DATASET}' not found.")
        return

    available_models = get_available_models()
    models_to_run = [m for m in MODELS_TO_TEST if m in available_models]
    if not models_to_run:
        print(f"Models {MODELS_TO_TEST} not found in available models: {available_models}.")
        return

    results_summary = {}

    for model in models_to_run:
        for search_count in SEARCH_RESULTS_TO_CHECK_LIST:
            print(f"\n--- Testing Model: {model}, Candidate Pool Size: {search_count} ---")

            predictions = []
            ground_truths = []
            ranks = []

            for i, row in df.iterrows():
                print(f"\n--- Running Evaluation for paper pair {i + 1}/{len(df)} ---")
                status, prediction, rank = run_full_pipeline_evaluation(
                    row, model, search_count
                )

                if status == "SUCCESS":
                    predictions.append(prediction)
                    ground_truths.append(row["label"])
                    if prediction == 1:
                        ranks.append(rank)
                        print(f"Result: Recommended (Rank: {rank}), Ground Truth: {row['label']}")
                    else:
                        ranks.append(0)
                        print(f"Result: Not Recommended, Ground Truth: {row['label']}")
                else:
                    print("Result: ERROR - Run was invalid and will be skipped.")

            if not ground_truths:
                print("No valid runs completed. Cannot calculate metrics.")
                continue

            precision = precision_score(ground_truths, predictions, zero_division=0)
            recall = recall_score(ground_truths, predictions, zero_division=0)
            accuracy = accuracy_score(ground_truths, predictions)
            mrr = calculate_mrr(ranks)

            results_summary[(model, search_count)] = {
                "precision": precision,
                "recall": recall,
                "accuracy": accuracy,
                "mrr": mrr,
                "valid_runs": len(ground_truths),
                "successful_recommendations": sum(1 for r in ranks if r > 0)
            }

    print("\n--- Evaluation Complete ---")
    print("\n--- Results Summary ---")

    with open(RESULTS_FILENAME, "w") as f:
        f.write("--- Full Recommendation Pipeline Evaluation ---\n\n")
        for (model, search_count), metrics in results_summary.items():
            f.write(f"Model: {model}, Candidate Pool Size: {search_count}\n")
            f.write(f"  Valid Runs: {metrics['valid_runs']}\n")
            f.write(f"  Successful Recommendations: {metrics['successful_recommendations']}\n")
            f.write(f"  Precision: {metrics['precision']:.4f}\n")
            f.write(f"  Recall: {metrics['recall']:.4f}\n")
            f.write(f"  Accuracy: {metrics['accuracy']:.4f}\n")
            f.write(f"  Mean Reciprocal Rank (MRR): {metrics['mrr']:.4f}\n\n")

    print(f"Results saved to {RESULTS_FILENAME}")


if __name__ == "__main__":
    main()
