import {Component, HostBinding, Input} from '@angular/core';
import {CommonModule} from '@angular/common';
import {Component as ComponentProto} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {CheckboxComponent} from '../../../components/checkbox/checkbox';
import {ButtonComponent} from '../../../components/button/button';
import {TextComponent} from '../../../components/text/text';
// REF(//scripts/gen_component.py):insert_ts_import
import {MarkdownComponent} from '../../../components/markdown/markdown';
import {TextInputComponent} from '../../../components/text_input/text_input';
import {ComponentLoader} from './component_loader';
import {BoxType} from 'mesop/mesop/components/box/box_jspb_proto_pb/mesop/components/box/box_pb';

@Component({
  selector: 'component-renderer',
  templateUrl: 'component_renderer.ng.html',
  standalone: true,
  imports: [
    // REF(//scripts/gen_component.py):insert_ng_import
    MarkdownComponent,
    TextInputComponent,
    TextComponent,
    CheckboxComponent,
    ButtonComponent,
    CommonModule,
    ComponentLoader,
  ],
})
export class ComponentRenderer {
  @Input() component!: ComponentProto;
  private _boxType: BoxType | undefined;

  trackByFn(index: any, item: ComponentProto) {
    const key = item.getKey()?.getKey();
    if (key) {
      return key;
    }
    return index;
  }

  type() {
    return this.component.getType();
  }

  key() {
    return this.component.getKey()!;
  }

  ngOnChanges() {
    if (this.component.getType()?.getName() !== 'box') {
      return;
    }
    this._boxType = BoxType.deserializeBinary(
      this.component.getType()!.getValue() as unknown as Uint8Array,
    );
  }

  @HostBinding('style') get style(): string {
    if (!this._boxType) {
      return '';
    }

    return this._boxType.getStyles().trim();
  }
}
