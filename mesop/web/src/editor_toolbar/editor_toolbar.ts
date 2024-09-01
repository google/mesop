import {
  Component,
  ElementRef,
  HostListener,
  Inject,
  OnInit,
  ViewChild,
} from '@angular/core';
import {FormsModule} from '@angular/forms';
import {CdkDrag, CdkDragEnd} from '@angular/cdk/drag-drop';
import {MatButtonModule} from '@angular/material/button';
import {MatIconModule} from '@angular/material/icon';
import {
  EditorToolbarService,
  PromptInteraction,
  PromptResponse,
} from './editor_toolbar_service';
import {
  MAT_DIALOG_DATA,
  MatDialog,
  MatDialogModule,
} from '@angular/material/dialog';
import {
  CodeMirrorDiffComponent,
  CodeMirrorRawComponent,
} from './code_mirror_component';
import {interval, Subscription} from 'rxjs';
import {MatSnackBar, MatSnackBarModule} from '@angular/material/snack-bar';
import {CommonModule} from '@angular/common';
import {ErrorDialogService} from '../services/error_dialog_service';
import {MatTooltipModule} from '@angular/material/tooltip';
import {
  MAT_AUTOCOMPLETE_SCROLL_STRATEGY,
  MatAutocomplete,
  MatAutocompleteModule,
  MatAutocompleteTrigger,
} from '@angular/material/autocomplete';
import {EditorToolbarAutocompleteService} from './editor_toolbar_autocomplete_service';
import {Overlay} from '@angular/cdk/overlay';
import {HighlightPipe} from './highlight_pipe';
import {EditorService, SelectionMode} from '../services/editor_service';
import {isMac} from '../utils/platform';
import {Component as ComponentProto} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {MatProgressBarModule} from '@angular/material/progress-bar';

interface PromptOption {
  prompt: string;
  icon: string;
}

const IS_TOOLBAR_MINIMIZED_KEY = 'MESOP://IS_TOOLBAR_MINIMIZED';

@Component({
  selector: 'mesop-editor-toolbar',
  templateUrl: 'editor_toolbar.ng.html',
  standalone: true,
  styleUrl: 'editor_toolbar.css',
  imports: [
    MatIconModule,
    MatButtonModule,
    FormsModule,
    MatSnackBarModule,
    CommonModule,
    CdkDrag,
    MatAutocompleteModule,
    MatTooltipModule,
    HighlightPipe,
  ],
  providers: [
    {
      provide: MAT_AUTOCOMPLETE_SCROLL_STRATEGY,
      useFactory: (overlay: Overlay) => () => overlay.scrollStrategies.close(),
      deps: [Overlay],
    },
  ],
})
export class EditorToolbar implements OnInit {
  prompt = '';
  responseTime = 0;
  isLoading = false;
  private timerSubscription: Subscription | null = null;
  isToolbarMinimized = false;
  position: {x: number | null; y: number | null} = {x: null, y: null};
  @ViewChild('toolbar', {static: true}) toolbar!: ElementRef;
  @ViewChild(MatAutocompleteTrigger)
  autocompleteTrigger!: MatAutocompleteTrigger;
  @ViewChild(MatAutocomplete)
  autocomplete!: MatAutocomplete;
  @ViewChild('textarea', {static: false}) textarea!: ElementRef;

  constructor(
    private editorToolbarService: EditorToolbarService,
    private dialog: MatDialog,
    private snackBar: MatSnackBar,
    private errorDialogService: ErrorDialogService,
    private autocompleteService: EditorToolbarAutocompleteService,
    private editorService: EditorService,
  ) {
    const savedState = localStorage.getItem(IS_TOOLBAR_MINIMIZED_KEY);
    this.isToolbarMinimized = savedState === 'true';

    this.editorService.setOnSelectedComponent(() => {
      this.textarea.nativeElement.focus();
    });
  }

  ngOnInit() {
    this.loadSavedPosition();
  }

  ngAfterViewInit() {
    this.setupAutocompleteScrolling();
  }

  getSelectComponentTooltip(): string {
    if (isMac()) {
      return 'Select component - ⌘ ⇧ E';
    }
    return 'Select component - Ctrl ⇧ E';
  }

  @HostListener('window:keydown', ['$event'])
  handleKeyDown(event: KeyboardEvent) {
    // Hotkey for focusing on editor toolbar textarea
    //
    // Binds:
    // cmd + k (MacOs)
    // ctrl + k (Other platforms)
    if (event.key === 'k' && (isMac() ? event.metaKey : event.ctrlKey)) {
      this.textarea.nativeElement.focus();
      event.preventDefault();
      return;
    }
  }

  getToolbarShortcutText(): string {
    if (isMac()) {
      return '⌘ K';
    }
    return 'Ctrl K';
  }

  isSelectingMode(): boolean {
    return this.editorService.getSelectionMode() === SelectionMode.SELECTING;
  }

  toggleSelectingMode(): void {
    switch (this.editorService.getSelectionMode()) {
      case SelectionMode.DISABLED:
      case SelectionMode.SELECTED:
        this.editorService.setSelectionMode(SelectionMode.SELECTING);
        break;
      case SelectionMode.SELECTING:
        this.editorService.setSelectionMode(SelectionMode.DISABLED);
        break;
    }
  }

  setupAutocompleteScrolling() {
    this.autocomplete.opened.subscribe(() => {
      setTimeout(() => {
        if (this.autocomplete?.panel) {
          this.autocomplete.panel.nativeElement.scrollTop =
            this.autocomplete.panel.nativeElement.scrollHeight;
        }
      });
    });
  }

  get filteredOptions(): PromptOption[] {
    return this.autocompleteService.getFilteredOptions();
  }

  toggleToolbar() {
    this.isToolbarMinimized = !this.isToolbarMinimized;
    localStorage.setItem(
      IS_TOOLBAR_MINIMIZED_KEY,
      this.isToolbarMinimized.toString(),
    );
    if (this.isToolbarMinimized) {
      this.position = {x: null, y: null};
    }
    if (!this.isToolbarMinimized) {
      this.loadSavedPosition();
    }
  }

  async onEnter(event: Event) {
    event.preventDefault();

    if (this.autocompleteTrigger.panelOpen) {
      this.autocompleteTrigger.closePanel();
    }
    await this.sendPrompt();
  }

  getSelectedComponent(): ComponentProto | undefined {
    if (this.editorService.getSelectionMode() === SelectionMode.SELECTED) {
      return this.editorService.getFocusedComponent();
    }
    return undefined;
  }

  async sendPrompt() {
    if (this.prompt.length < 4) {
      this.snackBar.open(
        'Please enter a prompt at least 4 characters long',
        'Close',
        {
          duration: 5000,
        },
      );
      return;
    }
    const prompt = this.prompt;
    this.autocompleteService.addHistoryOption(prompt);
    this.prompt = '';
    this.isLoading = true;
    this.responseTime = 0;

    const startTime = performance.now();
    this.startTimer(startTime);
    let progressDialogRef;
    try {
      const responsePromise = this.editorToolbarService.sendPrompt(
        prompt,
        this.getSelectedComponent()?.getSourceCodeLocation(),
      );
      progressDialogRef = this.dialog.open(EditorSendPromptProgressDialog, {
        width: '90%',
      });
      const response = await responsePromise;
      progressDialogRef.afterClosed().subscribe(() => {
        this.autocompleteTrigger.closePanel();
      });
      progressDialogRef.close();

      const dialogRef = this.dialog.open(EditorPromptResponseDialog, {
        data: {response: response, responseTime: this.responseTime},
        width: '90%',
      });

      dialogRef.afterClosed().subscribe(async (result) => {
        if (result) {
          await this.editorToolbarService.commit(response.afterCode);
        }
        this.autocompleteTrigger.closePanel();
      });
    } catch (error) {
      console.error('Error:', error);
      if (progressDialogRef) {
        progressDialogRef.close();
      }
      const snackBarRef = this.snackBar.open(
        'Oops, there was an error',
        'Details',
        {
          duration: 5000,
        },
      );

      snackBarRef.onAction().subscribe(() => {
        this.errorDialogService.showError(error);
      });
    } finally {
      this.stopTimer();
      this.isLoading = false;
    }
  }

  get history() {
    return this.editorToolbarService.getHistory();
  }

  openHistory() {
    const dialogRef = this.dialog.open(EditorHistoryDialog, {
      data: {},
      width: '90%',
    });
    dialogRef.afterClosed().subscribe((result) => {
      if (Number.isInteger(result)) {
        const interaction = this.editorToolbarService.getHistory()[result];
        this.editorToolbarService.commit(interaction.beforeCode);
        this.editorToolbarService.addHistoryEntry({
          prompt: `Revert: ${interaction.prompt}`,
          path: interaction.path,
          // Swap before and after code to represent the revert
          beforeCode: interaction.afterCode,
          afterCode: interaction.beforeCode,
          diff: '<revert>',
          lineNumber: undefined,
        });
      }
    });
  }

  private startTimer(startTime: number) {
    this.timerSubscription = interval(100).subscribe(() => {
      this.responseTime = Number(
        ((performance.now() - startTime) / 1000).toFixed(1),
      );
    });
  }

  private stopTimer() {
    if (this.timerSubscription) {
      this.timerSubscription.unsubscribe();
      this.timerSubscription = null;
    }
  }

  ngOnDestroy() {
    this.stopTimer();
  }

  onDragEnded(event: CdkDragEnd) {
    // Get position relative to the viewport
    const element = event.source.element.nativeElement;
    const rect = element.getBoundingClientRect();
    const x = rect.left;
    const y = rect.top;

    this.position = {x, y};
    this.savePosition();
  }

  private loadSavedPosition() {
    const savedPosition = localStorage.getItem('editorToolbarPosition');
    if (!savedPosition) {
      return;
    }
    this.position = JSON.parse(savedPosition);

    // Ensure the toolbar stays within the viewport
    const viewportWidth = window.innerWidth;
    const viewportHeight = window.innerHeight;
    const toolbarRect = this.toolbar.nativeElement.getBoundingClientRect();

    const left = Math.max(0, Math.min(this.position.x!, viewportWidth - 600));
    const top = Math.max(
      0,
      Math.min(this.position.y!, viewportHeight - toolbarRect.height),
    );

    this.toolbar.nativeElement.style.left = `${left}px`;
    this.toolbar.nativeElement.style.top = `${top}px`;
  }

  private savePosition() {
    localStorage.setItem(
      'editorToolbarPosition',
      JSON.stringify(this.position),
    );
  }

  onPromptChange(newValue: string) {
    this.autocompleteService.updateFilteredOptions(newValue);
  }
}

@Component({
  templateUrl: 'editor_send_prompt_progress_dialog.ng.html',
  standalone: true,
  imports: [
    MatDialogModule,
    MatButtonModule,
    CommonModule,
    CodeMirrorRawComponent,
    MatProgressBarModule,
  ],
})
class EditorSendPromptProgressDialog {
  constructor(private editorToolbarService: EditorToolbarService) {}

  get progress$() {
    return this.editorToolbarService.generationProgress$;
  }
}

@Component({
  templateUrl: 'editor_response_dialog.ng.html',
  standalone: true,
  imports: [MatDialogModule, MatButtonModule, CodeMirrorDiffComponent],
})
class EditorPromptResponseDialog {
  constructor(
    @Inject(MAT_DIALOG_DATA)
    public data: {response: PromptResponse; responseTime: number},
  ) {}
}

@Component({
  templateUrl: './editor_history_dialog.ng.html',
  standalone: true,
  imports: [
    MatDialogModule,
    MatButtonModule,
    CodeMirrorDiffComponent,
    MatIconModule,
    MatSnackBarModule,
    MatTooltipModule,
  ],
  styles: [
    `
      mat-dialog-content {
        overflow: hidden;
      }
      .history-container {
        display: flex;
        flex-direction: row;
        gap: 16px;
      }
      .prompt-list {
        display: flex;
        flex-direction: column;
        gap: 12px;
        max-height: 65vh;
        overflow-y: auto;
      }
      .prompt-item {
        cursor: pointer;
        background: var(--sys-inverse-on-surface);
        padding: 8px;
        border-radius: 12px;
      }
      .prompt-item-text {
        width: 280px;
        padding-bottom: 4px;
      }
      .code-display {
        flex: 1;
        max-height: 65vh;
        overflow-y: auto;
      }
      .save-interaction-button {
        position: absolute;
        top: 16px;
        right: 32px;
      }
    `,
  ],
})
export class EditorHistoryDialog implements OnInit {
  history: readonly PromptInteraction[] = [];
  selectedInteraction = 0;

  constructor(
    private editorToolbarService: EditorToolbarService,
    private snackBar: MatSnackBar,
  ) {}

  ngOnInit() {
    this.history = this.editorToolbarService.getHistory();
  }

  selectInteraction(index: number) {
    this.selectedInteraction = index;
  }

  async saveSelectedInteraction() {
    const interaction = this.history[this.selectedInteraction];
    const folder = await this.editorToolbarService.saveInteraction(interaction);
    this.snackBar.open(`Saved interaction to ${folder}`, 'Close', {
      duration: 5000,
    });
  }
}
