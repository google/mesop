import {Component, Input} from '@angular/core';
import {CommonModule} from '@angular/common';
import {Component as ComponentProto} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {CheckboxComponent} from '../../../components/checkbox/checkbox';
import {ButtonComponent} from '../../../components/button/button';
import {TextComponent} from '../../../components/text/text';
// REF(//scripts/gen_component.py):insert_ts_import
import {MarkdownComponent} from '../../../components/markdown/markdown';
import {TextInputComponent} from '../../../components/text_input/text_input';
import {BoxComponent} from '../../../components/box/box';
import {ComponentLoader} from './component_loader';

@Component({
  selector: 'component-renderer',
  templateUrl: 'component_renderer.ng.html',
  standalone: true,
  imports: [
    // REF(//scripts/gen_component.py):insert_ng_import
    MarkdownComponent,
    TextInputComponent,
    BoxComponent,
    TextComponent,
    CheckboxComponent,
    ButtonComponent,
    CommonModule,
    ComponentLoader,
  ],
})
export class ComponentRenderer {
  @Input() component!: ComponentProto;

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
}
