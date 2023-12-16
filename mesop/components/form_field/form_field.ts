import {
  MatFormField,
  MatFormFieldControl,
  MatFormFieldModule,
} from '@angular/material/form-field';
import {Component, ContentChild, Input, ViewChild} from '@angular/core';
import {
  UserEvent,
  Key,
  Type,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {FormFieldType} from 'mesop/mesop/components/form_field/form_field_jspb_proto_pb/mesop/components/form_field/form_field_pb';
import {Channel} from '../../web/src/services/channel';
import {MatInputModule} from '@angular/material/input';

@Component({
  templateUrl: 'form_field.ng.html',
  standalone: true,
  imports: [MatFormFieldModule, MatInputModule],
})
export class FormFieldComponent {
  @Input({required: true}) type!: Type;
  @Input() key!: Key;
  private _config!: FormFieldType;

  @ContentChild(MatFormFieldControl) _control!: MatFormFieldControl<any>;
  @ViewChild(MatFormField) _matFormField!: MatFormField;

  ngOnInit() {
    this._matFormField._control = this._control;
  }

  constructor(private readonly channel: Channel) {}

  ngOnChanges() {
    this._config = FormFieldType.deserializeBinary(
      this.type.getValue() as unknown as Uint8Array,
    );
  }

  config(): FormFieldType {
    return this._config;
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
}
