import {Component, Inject, Injectable, Input} from '@angular/core';
import {MatButtonModule} from '@angular/material/button';
import {
  MAT_DIALOG_DATA,
  MatDialog,
  MatDialogModule,
} from '@angular/material/dialog';

@Injectable({
  providedIn: 'root',
})
export class ErrorDialogService {
  constructor(private dialog: MatDialog) {}

  showError(error: any): void {
    console.error(error);
    this.dialog.open(ErrorDialogComponent, {
      width: '400px',
      data: {error: error},
    });
  }
}

@Component({
  selector: 'mesop-error-dialog',
  template: `
    <h3 mat-dialog-title>Mesop Developer Error</h3>
    <mat-dialog-content class="mat-typography">
      <div class="error-content">{{ data.error }}</div>
    </mat-dialog-content>
    <mat-dialog-actions align="end">
      <button mat-button color="warn" [mat-dialog-close]="true" cdkFocusInitial>
        OK
      </button>
    </mat-dialog-actions>
  `,
  styles: `
    :host {
      display: block;
      background: #f6dfe3;
      --mdc-dialog-supporting-text-size: 16px;
      --mdc-dialog-supporting-text-line-height: 1.5;
    }

    .error-content {
      white-space: break-spaces;
    }
  `,
  standalone: true,
  imports: [MatDialogModule, MatButtonModule],
})
export class ErrorDialogComponent {
  constructor(@Inject(MAT_DIALOG_DATA) public data: {error: Error}) {}
}
