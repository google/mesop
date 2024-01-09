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

@Component({
  templateUrl: 'input.ng.html',
  standalone: true,
  imports: [MatInputModule, MatFormFieldModule],
})
export class InputComponent {
  @Input({required: true}) type!: Type;
  @Input() key!: Key;
  @Input() style!: Style;
  private _config!: InputType;

  constructor(private readonly channel: Channel) {}

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
    const userEvent = new UserEvent();
    userEvent.setHandlerId(this.config().getOnInputHandlerId());
    userEvent.setStringValue((event.target as HTMLInputElement).value);
    userEvent.setKey(this.key);
    this.channel.dispatch(userEvent);
  }
}
