import {
  Component,
  ComponentRef,
  HostBinding,
  Input,
  ViewContainerRef,
} from '@angular/core';
import {CommonModule} from '@angular/common';
import {
  Component as ComponentProto,
  Key,
  Type,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {CheckboxComponent} from '../../../components/checkbox/checkbox';
import {ButtonComponent} from '../../../components/button/button';
import {TextComponent} from '../../../components/text/text';
// REF(//scripts/gen_component.py):insert_ts_import
import {MarkdownComponent} from '../../../components/markdown/markdown';
import {TextInputComponent} from '../../../components/text_input/text_input';
import {ComponentLoader} from './component_loader';
import {BoxType} from 'mesop/mesop/components/box/box_jspb_proto_pb/mesop/components/box/box_pb';

interface BaseComponent {
  key: Key;
  type: Type;

  ngOnChanges(): void;
}

interface TypeToComponent {
  [typeName: string]: new (...rest: any[]) => BaseComponent;
}

const typeToComponent = {
  'button': ButtonComponent,
  'checkbox': CheckboxComponent,
  'text': TextComponent,
  'markdown': MarkdownComponent,
  'text_input': TextInputComponent,
} as TypeToComponent;

@Component({
  selector: 'component-renderer',
  templateUrl: 'component_renderer.ng.html',
  standalone: true,
  imports: [CommonModule, ComponentLoader],
})
export class ComponentRenderer {
  @Input() component!: ComponentProto;
  private _boxType: BoxType | undefined;
  private _componentRef!: ComponentRef<BaseComponent>;

  constructor(private viewContainerRef: ViewContainerRef) {}

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

  ngOnInit() {
    if (isRegularComponent(this.component)) {
      this.createComponentRef();
    }
  }

  ngOnChanges() {
    if (isRegularComponent(this.component)) {
      this.updateComponentRef();
      return;
    }
    if (this.component.getType()?.getName() === 'box') {
      this._boxType = BoxType.deserializeBinary(
        this.component.getType()!.getValue() as unknown as Uint8Array,
      );
    }
  }

  createComponentRef() {
    const typeName = this.component.getType()?.getName()!;
    this._componentRef = this.viewContainerRef.createComponent(
      typeToComponent[typeName],
    );
    this.updateComponentRef();
  }

  updateComponentRef() {
    if (this._componentRef) {
      const instance = this._componentRef.instance;
      instance.type = this.component.getType()!;
      instance.key = this.component.getKey()!;
      instance.ngOnChanges();
    }
  }

  @HostBinding('style') get style(): string {
    if (!this._boxType) {
      return '';
    }

    return this._boxType.getStyles().trim();
  }
}

function isRegularComponent(component: ComponentProto) {
  return component.getType() && component.getType()!.getName() !== 'box';
}
