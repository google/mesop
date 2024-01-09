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
  UserEvent,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {ComponentLoader} from './component_loader';
import {BoxType} from 'mesop/mesop/components/box/box_jspb_proto_pb/mesop/components/box/box_pb';
import {BaseComponent, typeToComponent} from './type_to_component';
import {Channel} from '../services/channel';
import {EditorService} from '../services/editor_service';
import {OverlayModule} from '@angular/cdk/overlay';
import {MatButtonModule} from '@angular/material/button';
import {MatIconModule} from '@angular/material/icon';
import {MatDividerModule} from '@angular/material/divider';

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
    (this.elementRef.nativeElement as HTMLElement).addEventListener(
      'click',
      this.onContainerClick,
      {capture: true},
    );
  }

  ngOnDestroy() {
    (this.elementRef.nativeElement as HTMLElement).removeEventListener(
      'click',
      this.onContainerClick,
      {capture: true},
    );
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
    // Need to insert at insertionRef and *not* viewContainerRef, otherwise
    // the component (e.g. <mesop-text> will not be properly nested inside <component-renderer>).
    this._componentRef = this.insertionRef.createComponent(
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

  //////////////
  // Box-specific implementation:
  //////////////

  getStyle(): string {
    if (!this._boxType) {
      if (this.isEditorFocusedComponent()) {
        return `display: block; ${this.getFocusedStyle()}`;
      }
      return '';
    }

    // `display: block` because box should have "div"-like semantics.
    // Custom elements like Angular component tags are treated as inline by default.
    let style = 'display: block;';

    const styleObj = this.component.getStyle();
    if (!styleObj) {
      return style;
    }
    if (styleObj.getBackground()) {
      style += `background: ${styleObj.getBackground()};`;
    }
    if (styleObj.getColor()) {
      style += `color: ${styleObj.getColor()};`;
    }
    if (styleObj.getHeight()) {
      style += `height: ${styleObj.getHeight()};`;
    }
    if (styleObj.getWidth()) {
      style += `width: ${styleObj.getWidth()};`;
    }
    if (styleObj.getDisplay()) {
      style += `display: ${styleObj.getDisplay()};`;
    }
    if (styleObj.getFlexDirection()) {
      style += `flex-direction: ${styleObj.getFlexDirection()};`;
    }
    if (styleObj.getFlexGrow()) {
      style += `flex-grow: ${styleObj.getFlexGrow()};`;
    }
    if (styleObj.getAlignItems()) {
      style += `align-items: ${styleObj.getAlignItems()};`;
    }
    if (styleObj.getPosition()) {
      style += `position: ${styleObj.getPosition()};`;
    }
    if (styleObj.getTextAlign()) {
      style += `text-align: ${styleObj.getTextAlign()};`;
    }
    if (styleObj.getBorder()) {
      const border = styleObj.getBorder()!;
      const top = border.getTop();
      if (top) {
        style += `border-top: ${top.getWidth()} ${top.getStyle()} ${top.getColor()};`;
      }
      const bottom = border.getBottom();
      if (bottom) {
        style += `border-bottom: ${bottom.getWidth()} ${bottom.getStyle()} ${bottom.getColor()};`;
      }
      const left = border.getLeft();
      if (left) {
        style += `border-left: ${left.getWidth()} ${left.getStyle()} ${left.getColor()};`;
      }
      const right = border.getRight();
      if (right) {
        style += `border-right: ${right.getWidth()} ${right.getStyle()} ${right.getColor()};`;
      }
    }
    if (styleObj.getMargin()) {
      const margin = styleObj.getMargin()!;
      style += `margin: ${margin.getTop()} ${margin.getRight()} ${margin.getBottom()} ${margin.getLeft()};`;
    }
    if (styleObj.getPadding()) {
      const padding = styleObj.getPadding()!;
      style += `padding: ${padding.getTop()} ${padding.getRight()} ${padding.getBottom()} ${padding.getLeft()};`;
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
    userEvent.setHandlerId(this._boxType.getOnClickHandlerId());
    userEvent.setKey(this.component.getKey());
    this.channel.dispatch(userEvent);
  }

  //////////////
  // Editor-specific implementation:
  //////////////

  getFocusedStyle(): string {
    return `
    background: rgb(119 166 245);
    opacity: 0.7;
    border-radius: 2px;
    `;
  }

  onContainerClick = () => {
    if (!this.isEditorMode) {
      return;
    }

    this.editorService.setFocusedComponent(this.component);
  };

  isEditorFocusedComponent() {
    return this.editorService.getFocusedComponent() === this.component;
  }
}

function isRegularComponent(component: ComponentProto) {
  return component.getType() && component.getType()!.getName() !== 'box';
}
