import {
  ApplicationRef,
  Component,
  ComponentRef,
  ElementRef,
  HostListener,
  Input,
  TemplateRef,
  ViewChild,
  ViewContainerRef,
} from '@angular/core';
import {CommonModule} from '@angular/common';
import {
  Component as ComponentProto,
  Key,
  Type,
  UserEvent,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {ComponentLoader} from './component_loader';
import {BoxType} from 'mesop/mesop/components/box/box_jspb_proto_pb/mesop/components/box/box_pb';
import {BaseComponent, typeToComponent} from './type_to_component';
import {Channel} from '../services/channel';
import {EditorService, SelectionMode} from '../services/editor_service';
import {OverlayModule} from '@angular/cdk/overlay';
import {MatButtonModule} from '@angular/material/button';
import {MatIconModule} from '@angular/material/icon';
import {MatDividerModule} from '@angular/material/divider';
import {formatStyle} from '../utils/styles';

const CORE_NAMESPACE = 'me';

@Component({
  selector: 'component-renderer',
  templateUrl: 'component_renderer.ng.html',
  styleUrl: 'component_renderer.css',
  standalone: true,
  imports: [
    CommonModule,
    ComponentLoader,
    OverlayModule,
    MatButtonModule,
    MatIconModule,
    MatDividerModule,
  ],
})
export class ComponentRenderer {
  @ViewChild('childrenTemplate', {static: true})
  childrenTemplate!: TemplateRef<any>;

  @ViewChild('insertion', {read: ViewContainerRef, static: true})
  insertionRef!: ViewContainerRef;

  @Input() component!: ComponentProto;
  private _boxType: BoxType | undefined;
  private _componentRef!: ComponentRef<BaseComponent>;
  isEditorMode: boolean;
  isEditorOverlayOpen = false;

  constructor(
    private channel: Channel,
    private applicationRef: ApplicationRef,
    private editorService: EditorService,
    private elementRef: ElementRef,
  ) {
    this.isEditorMode = this.editorService.isEditorMode();
  }

  ngAfterViewInit() {
    if (this.isEditorMode) {
      (this.elementRef.nativeElement as HTMLElement).addEventListener(
        'mouseover',
        this.onEditorHover,
        {capture: true},
      );
      (this.elementRef.nativeElement as HTMLElement).addEventListener(
        'click',
        this.onEditorClick,
        {capture: true},
      );
    }
  }

  ngOnDestroy() {
    if (this.isEditorMode) {
      (this.elementRef.nativeElement as HTMLElement).removeEventListener(
        'mouseover',
        this.onEditorHover,
        {capture: true},
      );
      (this.elementRef.nativeElement as HTMLElement).removeEventListener(
        'click',
        this.onEditorClick,
        {capture: true},
      );
    }
  }

  trackByFn(index: any, item: ComponentProto) {
    const key = item.getKey()?.getKey();
    if (key) {
      return key;
    }
    // Include the component type so that Angular
    // knows that it's a new child, otherwise it gets confused
    // and tries to pass in the new component properties into the
    // old component and we get an error.
    return `${index}___${item.getType()?.getName()}`;
  }

  isBoxType() {
    const typeName = this.component.getType()?.getName();
    return typeName?.getCoreModule() && typeName.getFnName() === 'box';
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
    if (this.isBoxType()) {
      this._boxType = BoxType.deserializeBinary(
        this.component.getType()!.getValue() as unknown as Uint8Array,
      );
    }

    this.computeStyles();
  }

  ngDoCheck() {
    // Only need to re-compute styles in editor mode to properly
    // show focused component highlight.
    if (this.isEditorMode) {
      this.computeStyles();
    }
  }

  computeStyles() {
    this.elementRef.nativeElement.style = this.getStyle();
  }

  createComponentRef() {
    const typeName = this.component.getType()?.getName()!;
    let options = {};
    if (this.component.getChildrenList().length) {
      const projectedViewRef = this.childrenTemplate.createEmbeddedView(this);
      // Need to attach view or it doesn't render.
      // View automatically detaches when it is destroyed.
      // Template will destroy each ViewRef when it is destroyed.
      const index = this.component.getType()?.getTypeIndex() ?? 0;
      this.applicationRef.attachView(projectedViewRef);
      const projectableNodes = [];
      projectableNodes[index] = projectedViewRef.rootNodes;
      options = {
        projectableNodes,
      };
    }
    const componentClass = typeName.getCoreModule()
      ? typeToComponent[typeName.getFnName()!]
      : UserDefinedComponent;
    // Need to insert at insertionRef and *not* viewContainerRef, otherwise
    // the component (e.g. <mesop-text> will not be properly nested inside <component-renderer>).
    this._componentRef = this.insertionRef.createComponent(
      componentClass, // If it's an unrecognized type, we assume it's a user-defined component
      options,
    );
    this.updateComponentRef();
  }

  updateComponentRef() {
    if (this._componentRef) {
      const instance = this._componentRef.instance;
      instance.type = this.component.getType()!;
      instance.key = this.component.getKey()!;
      instance.style = this.component.getStyle()!;
      instance.ngOnChanges();
    }
  }

  //////////////
  // Box-specific implementation:
  //////////////

  getStyle(): string {
    if (!this._boxType) {
      if (this.isEditorFocusedComponent()) {
        let display = 'inline-block';
        const name = this.component.getType()?.getName();
        // Might be root component which doesn't have a name.
        if (!name) {
          return '';
        }
        // Preserve existing display semantics.
        if (
          name.getCoreModule() &&
          ['text', 'markdown'].includes(name.getFnName()!)
        ) {
          display = 'block';
        }
        return `display: ${display}; ${this.getFocusedStyle()}`;
      }
      return '';
    }

    // `display: block` because box should have "div"-like semantics.
    // Custom elements like Angular component tags are treated as inline by default.
    let style = 'display: block;';

    if (this.component.getStyle()) {
      style += formatStyle(this.component.getStyle()!);
    }
    return (
      style + (this.isEditorFocusedComponent() ? this.getFocusedStyle() : '')
    );
  }

  @HostListener('click', ['$event'])
  onClick(event: Event) {
    if (!this._boxType) {
      return;
    }
    const userEvent = new UserEvent();
    userEvent.setHandlerId(this._boxType.getOnClickHandlerId()!);
    userEvent.setKey(this.component.getKey());
    this.channel.dispatch(userEvent);
  }

  //////////////
  // Editor-specific implementation:
  //////////////

  getFocusedStyle(): string {
    if (this.editorService.getSelectionMode() === SelectionMode.SELECTING) {
      return `
    background: rgb(119 166 245);
    opacity: 0.7;
    border-radius: 2px;
    `;
    }
    return `border: 1px solid #1c6ef3;
      border-radius: 4px;`;
  }

  onEditorHover = () => {
    if (this.editorService.getSelectionMode() === SelectionMode.SELECTING) {
      this.editorService.setFocusedComponent(this.component);
    }
  };

  onEditorClick = () => {
    if (this.editorService.getSelectionMode() === SelectionMode.SELECTING) {
      this.editorService.setSelectionMode(SelectionMode.SELECTED);
    }
  };

  isEditorFocusedComponent() {
    return this.editorService.getFocusedComponent() === this.component;
  }

  getSelectionMode(): SelectionMode {
    return this.editorService.getSelectionMode();
  }

  SelectionMode = SelectionMode;

  getComponentName(): string {
    return this.type()?.getName()?.getFnName() ?? '[root]';
  }
}

function isRegularComponent(component: ComponentProto) {
  const typeName = component.getType()?.getName()!;
  return (
    component.getType() &&
    !(typeName.getCoreModule() && typeName.getFnName() === 'box')
  );
}

@Component({
  template: '<ng-content></ng-content>',
  standalone: true,
})
class UserDefinedComponent implements BaseComponent {
  @Input() key!: Key;
  @Input() type!: Type;
  ngOnChanges() {
    // Placeholder function since the
  }
}
