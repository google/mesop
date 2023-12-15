import {
  ApplicationRef,
  Component,
  ComponentRef,
  HostBinding,
  Input,
  TemplateRef,
  ViewChild,
  ViewContainerRef,
} from '@angular/core';
import {CommonModule} from '@angular/common';
import {Component as ComponentProto} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {ComponentLoader} from './component_loader';
import {BoxType} from 'mesop/mesop/components/box/box_jspb_proto_pb/mesop/components/box/box_pb';
import {BaseComponent, typeToComponent} from './type_to_component';

@Component({
  selector: 'component-renderer',
  templateUrl: 'component_renderer.ng.html',
  standalone: true,
  imports: [CommonModule, ComponentLoader],
})
export class ComponentRenderer {
  @ViewChild('childrenTemplate', {static: true})
  childrenTemplate!: TemplateRef<any>;

  @Input() component!: ComponentProto;
  private _boxType: BoxType | undefined;
  private _componentRef!: ComponentRef<BaseComponent>;

  constructor(
    private viewContainerRef: ViewContainerRef,
    private applicationRef: ApplicationRef,
  ) {}

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
    let options = {};
    if (this.component.getChildrenList().length) {
      const projectedViewRef = this.childrenTemplate.createEmbeddedView(this);
      // Need to attach view or it doesn't render.
      // View automatically detaches when it is destroyed.
      // Template will destroy each ViewRef when it is destroyed.
      const index = this.component.getType()?.getVariantIndex() ?? 0;
      this.applicationRef.attachView(projectedViewRef);
      const projectableNodes = [];
      projectableNodes[index] = projectedViewRef.rootNodes;
      options = {
        projectableNodes,
      };
    }
    this._componentRef = this.viewContainerRef.createComponent(
      typeToComponent[typeName],
      options,
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
