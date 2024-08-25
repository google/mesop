import {Injectable} from '@angular/core';

export interface PromptOption {
  prompt: string;
  icon: string;
}

const HISTORY_OPTIONS_KEY = 'MESOP://PROMPT_HISTORY';

@Injectable({
  providedIn: 'root',
})
export class EditorToolbarAutocompleteService {
  private allOptions: PromptOption[] = [
    {prompt: 'Add text to the bottom', icon: 'prompt_suggestion'},
    {prompt: 'Create a card', icon: 'prompt_suggestion'},
    {prompt: 'Make it prettier', icon: 'prompt_suggestion'},
    {prompt: 'Add a button', icon: 'prompt_suggestion'},
    {prompt: 'Create a 3x3 grid', icon: 'prompt_suggestion'},
    {prompt: 'Create a side-by-side layout', icon: 'prompt_suggestion'},
  ];
  filteredOptions: PromptOption[];

  constructor() {
    this.loadHistoryOptions();
    this.filteredOptions = this.allOptions;
  }

  private loadHistoryOptions() {
    const historyOptions = sessionStorage.getItem(HISTORY_OPTIONS_KEY);
    if (historyOptions) {
      const parsedOptions = JSON.parse(historyOptions) as string[];
      parsedOptions.forEach((option) => {
        this.allOptions.push({prompt: option, icon: 'history'});
      });
    }
  }

  getFilteredOptions(): PromptOption[] {
    return this.filteredOptions;
  }

  addHistoryOption(option: string) {
    this.allOptions.push({prompt: option, icon: 'history'});
    this.saveHistoryOptions();
  }

  updateFilteredOptions(prompt: string) {
    this.filteredOptions = this.allOptions.filter((opt) =>
      opt.prompt.toLowerCase().includes(prompt.toLowerCase()),
    );
  }

  private saveHistoryOptions() {
    const historyOptions = this.allOptions
      .filter((opt) => opt.icon === 'history')
      .map((opt) => opt.prompt)
      .slice(-100); // Keep only the 100 most recent options
    sessionStorage.setItem(HISTORY_OPTIONS_KEY, JSON.stringify(historyOptions));
  }
}
