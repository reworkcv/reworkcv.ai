const API_BASE = '/api';

export interface ProcessResponse {
  success: boolean;
  message: string;
  pdf_url?: string;
  latex_content?: string;
  tailored_json?: Record<string, unknown>;
}

export async function processResume(
  resumeFile: File,
  jobDescription: string,
  templateFile?: File
): Promise<ProcessResponse> {
  const formData = new FormData();
  formData.append('resume', resumeFile);
  formData.append('job_description', jobDescription);
  
  if (templateFile) {
    formData.append('template', templateFile);
  }

  const response = await fetch(`${API_BASE}/process`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to process resume');
  }

  return response.json();
}

export async function healthCheck(): Promise<{ status: string; message: string }> {
  const response = await fetch(`${API_BASE}/health`);
  return response.json();
}

export function getPdfPreviewUrl(requestId: string): string {
  return `${API_BASE}/preview/${requestId}`;
}

export function getPdfDownloadUrl(requestId: string): string {
  return `${API_BASE}/download/${requestId}`;
}
