/**
 * API Client for Capstone Backend
 * All API endpoints are proxied through Vite dev server to http://localhost:5000
 */

const API_BASE = '/api';

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const errorText = await response.text();
    let errorMessage = `HTTP ${response.status}: ${errorText}`;
    try {
      const errorJson = JSON.parse(errorText);
      errorMessage = errorJson.error || errorJson.message || errorMessage;
    } catch {
      // If not JSON, use the text as-is
    }
    throw new Error(errorMessage);
  }
  return response.json();
}

// Projects API
export const projectsApi = {
  /**
   * Get all projects for the current user
   */
  async getAll(): Promise<{ success: boolean; projects?: any[]; error?: string }> {
    const response = await fetch(`${API_BASE}/getProjects`, {
      credentials: 'include',
    });
    return handleResponse(response);
  },

  /**
   * Get a single project by ID
   */
  async getById(projectId: string): Promise<{ title: string; description: string; project_id: string }> {
    const response = await fetch(`${API_BASE}/project/${projectId}`, {
      credentials: 'include',
    });
    return handleResponse(response);
  },

  /**
   * Create a new project
   */
  async create(data: { title: string; description: string }): Promise<{ projectId: string }> {
    const response = await fetch(`${API_BASE}/projects`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
      credentials: 'include',
    });
    return handleResponse(response);
  },

  /**
   * Update project prompt/description
   */
  async updatePrompt(projectId: string, prompt: string): Promise<{ description: string }> {
    const response = await fetch(`${API_BASE}/project/${projectId}/update_prompt`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt }),
      credentials: 'include',
    });
    return handleResponse(response);
  },
};

// PDF Extraction API
export const pdfApi = {
  /**
   * Extract text from uploaded PDF
   */
  async extractText(file: File): Promise<{ success: boolean; extracted_text?: string; error?: string }> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_BASE}/extract-pdf-text`, {
      method: 'POST',
      body: formData,
      credentials: 'include',
    });
    return handleResponse(response);
  },
};

// Paper Rating API
export const ratingApi = {
  /**
   * Rate a paper (1-5 stars)
   * Returns rating status and replacement info if applicable
   */
  async ratePaper(data: {
    paper_hash: string;
    rating: number;
    project_id: string;
  }): Promise<{
    status: string;
    message?: string;
    replacement?: {
      status: string;
      replacement_title?: string;
      replacement_paper_hash?: string;
      replacement_url?: string;
      replacement_summary?: string;
    };
  }> {
    const response = await fetch(`${API_BASE}/rate_paper`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
      credentials: 'include',
    });
    return handleResponse(response);
  },
};

// PubSub/Newsletter API
export const pubsubApi = {
  /**
   * Update newsletter papers for a project
   */
  async updateNewsletterPapers(projectId: string): Promise<{ success?: boolean; error?: string }> {
    const response = await fetch(`${API_BASE}/pubsub/update_newsletter_papers`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ projectId }),
      credentials: 'include',
    });
    return handleResponse(response);
  },

  /**
   * Get newsletter papers for a project
   */
  async getNewsletterPapers(projectId: string): Promise<any[]> {
    const response = await fetch(`${API_BASE}/pubsub/get_newsletter_papers?projectId=${projectId}`, {
      credentials: 'include',
    });
    return handleResponse(response);
  },
};
