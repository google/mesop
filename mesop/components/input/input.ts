import {MatFormFieldModule} from '@angular/material/form-field';
import {MatInputModule} from '@angular/material/input';
import {Component, Input} from '@angular/core';
import {
  UserEvent,
  Key,
  Type,
  Style,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {InputType} from 'mesop/mesop/components/input/input_jspb_proto_pb/mesop/components/input/input_pb';
import {Channel} from '../../web/src/services/channel';
import {formatStyle} from '../../web/src/utils/styles';
import {Subject} from 'rxjs';
import {debounceTime} from 'rxjs/operators';
import {CommonModule} from '@angular/common';

@Component({
  templateUrl: 'input.ng.html',
  standalone: true,
  imports: [MatInputModule, MatFormFieldModule, CommonModule],
})
export class InputComponent {
  @Input({required: true}) type!: Type;
  @Input() key!: Key;
  @Input() style!: Style;
  private _config!: InputType;
  private inputSubject = new Subject<Event>();

  constructor(private readonly channel: Channel) {
    this.inputSubject
      .pipe(
        // Setting this to a short duration to avoid having the user trigger another event
        // during this debounce time period:
        // https://github.com/google/mesop/issues/171
        debounceTime(150),
      )
      .subscribe((event) => this.onInputDebounced(event));
  }

  ngOnDestroy(): void {
    this.inputSubject.unsubscribe();
  }

  ngOnChanges() {
    this._config = InputType.deserializeBinary(
      this.type.getValue() as unknown as Uint8Array,
    );
  }

  config(): InputType {
    return this._config;
  }

  getStyle(): string {
    return formatStyle(this.style);
  }

  getColor(): 'primary' | 'accent' | 'warn' {
    return this.config().getColor() as 'primary' | 'accent' | 'warn';
  }

  getFloatLabel(): 'always' | 'auto' {
    return this.config().getFloatLabel() as 'always' | 'auto';
  }

  getAppearance(): 'fill' | 'outline' {
    return this.config().getAppearance() as 'fill' | 'outline';
  }

  getSubscriptSizing(): 'fixed' | 'dynamic' {
    return this.config().getSubscriptSizing() as 'fixed' | 'dynamic';
  }

  onInput(event: Event): void {
    this.inputSubject.next(event);
  }

  onInputDebounced(event: Event): void {
    const userEvent = new UserEvent();
    userEvent.setHandlerId(this.config().getOnInputHandlerId()!);
    userEvent.setStringValue((event.target as HTMLInputElement).value);
    userEvent.setKey(this.key);
    this.channel.dispatch(userEvent);
  }

  onKeyUp(event: Event): void {
    if ((event as KeyboardEvent).key === 'Enter') {
      const userEvent = new UserEvent();
      userEvent.setHandlerId(this.config().getOnEnterHandlerId()!);
      userEvent.setKey(this.key);
      this.channel.dispatch(userEvent);
    }
  }

  onBlur(event: Event): void {
    const userEvent = new UserEvent();
    userEvent.setHandlerId(this.config().getOnBlurHandlerId()!);
    userEvent.setStringValue((event.target as HTMLInputElement).value);
    userEvent.setKey(this.key);
    this.channel.dispatch(userEvent);
  }
}
