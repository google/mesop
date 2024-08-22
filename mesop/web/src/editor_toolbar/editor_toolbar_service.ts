import {Injectable} from '@angular/core';

export interface PromptResponse {
  message: string;
  beforeCode: string;
  afterCode: string;
}

@Injectable({
  providedIn: 'root',
})
export class EditorToolbarService {
  async sendPrompt(prompt: string): Promise<PromptResponse> {
    console.log('sendPrompt', prompt);
    const response = await fetch('/__editor__/page-generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({prompt, path: window.location.pathname}),
    });
    return response.json() as Promise<PromptResponse>;
  }

  async commit(code: string): Promise<PromptResponse> {
    console.log('commit', prompt);
    const response = await fetch('/__editor__/page-commit', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({code, path: window.location.pathname}),
    });
    return response.json() as Promise<PromptResponse>;
  }
}
