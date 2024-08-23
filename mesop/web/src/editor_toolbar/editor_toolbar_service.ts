import {Injectable} from '@angular/core';

export interface PromptInteraction extends PromptResponse {
  prompt: string;
  path: string;
}

export interface PromptResponse {
  beforeCode: string;
  afterCode: string;
  diff: string;
}

const CANNED_HISTORY = [
  {
    path: '/',
    prompt: 'Add a button to the home page - some extremely long prompt',
    beforeCode: 'def fo1o():\n  return "bar"',
    afterCode: 'def fo4o():\n  return "bar"\n\nprint(foo())',
    diff: '<==== def foo2():\n  return "bar"\n\nprint(foo())',
  },
  {
    path: '/',
    prompt: 'Add a 22button to the home page',
    beforeCode: 'def foo22():\n  return "bar"',
    afterCode: 'def111 foo():\n  return "bar"\n\nprint(foo())',
    diff: '<==== def foo():\n  return "bar"\n\nprint(foo())',
  },
  {
    path: '/',
    prompt: 'Add a 33button to the home page',
    beforeCode: 'def foo33():\n  return "bar"',
    afterCode: 'def foo44():\n  return "bar"\n\nprint(foo())',
    diff: '<==== def foo():\n  return "bar"\n\nprint(foo())',
  },
];

@Injectable({
  providedIn: 'root',
})
export class EditorToolbarService {
  history: PromptInteraction[] = [];

  getHistory(): readonly PromptInteraction[] {
    return this.history;
  }

  async sendPrompt(prompt: string): Promise<PromptResponse> {
    console.debug('sendPrompt', prompt);
    const path = window.location.pathname;
    const response = await fetch('/__editor__/page-generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({prompt, path}),
    });
    if (!response.ok) {
      console.error('Commit error:', response.status, response.statusText);
      let error = '';
      try {
        error = await response.text();
      } catch (e) {}
      throw new Error(`${response.status} ${response.statusText} ${error}`);
    }
    const json = (await response.json()) as PromptResponse;
    // Insert at the top of the history so we display the most recent interactions first.
    this.history.unshift({
      path,
      prompt,
      ...json,
    });
    return json;
  }

  async commit(code: string): Promise<PromptResponse> {
    console.debug('commit', prompt);
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
