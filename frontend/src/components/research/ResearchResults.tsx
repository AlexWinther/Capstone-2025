import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { BookmarkPlus, ExternalLink, Users, Calendar } from "lucide-react";

const mockPapers = [
  {
    id: 1,
    title: "Attention Is All You Need",
    authors: "Vaswani et al.",
    year: 2017,
    venue: "NeurIPS",
    citations: 98234,
    relevance: 0.98,
    summary: "Introduces the Transformer architecture, relying entirely on self-attention mechanisms.",
    tags: ["Transformers", "Attention", "NLP"],
  },
  {
    id: 2,
    title: "BERT: Pre-training of Deep Bidirectional Transformers",
    authors: "Devlin et al.",
    year: 2019,
    venue: "NAACL",
    citations: 67891,
    relevance: 0.92,
    summary: "Proposes bidirectional training of Transformers for language understanding tasks.",
    tags: ["BERT", "Pre-training", "NLP"],
  },
  {
    id: 3,
    title: "An Image is Worth 16x16 Words: Transformers for Image Recognition",
    authors: "Dosovitskiy et al.",
    year: 2021,
    venue: "ICLR",
    citations: 45123,
    relevance: 0.87,
    summary: "Applies pure transformer architecture to computer vision tasks with minimal modifications.",
    tags: ["Vision Transformers", "Computer Vision", "Attention"],
  },
];

export const ResearchResults = () => {
  return (
    <div className="space-y-4 rounded-lg border bg-card p-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-xl font-semibold text-card-foreground">Research Results</h3>
          <p className="text-sm text-muted-foreground">
            Found {mockPapers.length} highly relevant papers
          </p>
        </div>
        <Button variant="outline" size="sm">
          Export Results
        </Button>
      </div>

      <div className="space-y-4">
        {mockPapers.map((paper) => (
          <Card key={paper.id} className="transition-shadow hover:shadow-md">
            <CardHeader>
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1">
                  <CardTitle className="text-lg">{paper.title}</CardTitle>
                  <CardDescription className="mt-2 flex flex-wrap items-center gap-3 text-sm">
                    <span className="flex items-center gap-1">
                      <Users className="h-3 w-3" />
                      {paper.authors}
                    </span>
                    <span className="flex items-center gap-1">
                      <Calendar className="h-3 w-3" />
                      {paper.year}
                    </span>
                    <span>·</span>
                    <span>{paper.venue}</span>
                    <span>·</span>
                    <span className="font-medium">{paper.citations.toLocaleString()} citations</span>
                  </CardDescription>
                </div>
                <Badge variant="secondary" className="shrink-0">
                  {Math.round(paper.relevance * 100)}% match
                </Badge>
              </div>
            </CardHeader>
            <CardContent>
              <p className="mb-4 text-sm text-muted-foreground">{paper.summary}</p>
              <div className="flex flex-wrap items-center justify-between gap-3">
                <div className="flex flex-wrap gap-2">
                  {paper.tags.map((tag) => (
                    <Badge key={tag} variant="outline">
                      {tag}
                    </Badge>
                  ))}
                </div>
                <div className="flex gap-2">
                  <Button variant="ghost" size="sm" className="gap-2">
                    <BookmarkPlus className="h-4 w-4" />
                    Save
                  </Button>
                  <Button variant="ghost" size="sm" className="gap-2">
                    <ExternalLink className="h-4 w-4" />
                    Open
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};

