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
  WebComponentType,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {ComponentLoader} from './component_loader';
import {BoxType} from 'mesop/mesop/components/box/box_jspb_proto_pb/mesop/components/box/box_pb';
import {
  BaseComponent,
  UserDefinedComponent,
  typeToComponent,
} from './type_to_component';
import {Channel} from '../services/channel';
import {EditorService, SelectionMode} from '../services/editor_service';
import {
  Overlay,
  OverlayConfig,
  OverlayModule,
  OverlayRef,
} from '@angular/cdk/overlay';
import {MatButtonModule} from '@angular/material/button';
import {MatIconModule} from '@angular/material/icon';
import {MatDividerModule} from '@angular/material/divider';
import {formatStyle} from '../utils/styles';
import {isComponentNameEquals} from '../utils/proto';
import {MatTooltipModule} from '@angular/material/tooltip';
import {TemplatePortal} from '@angular/cdk/portal';
import {jsonParse} from '../utils/strict_types';

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
    MatTooltipModule,
  ],
})
export class ComponentRenderer {
  @ViewChild('childrenTemplate', {static: true})
  childrenTemplate!: TemplateRef<any>;

  @ViewChild('insertion', {read: ViewContainerRef, static: true})
  insertionRef!: ViewContainerRef;

  @ViewChild('editorOverlay') editorOverlay!: TemplateRef<any>;

  @Input() component!: ComponentProto;
  private _boxType: BoxType | undefined;
  private _componentRef!: ComponentRef<BaseComponent>;
  isEditorMode: boolean;
  isEditorOverlayOpen = false;
  overlayRef?: OverlayRef;
  customElement: HTMLElement | undefined;

  constructor(
    private channel: Channel,
    private applicationRef: ApplicationRef,
    private editorService: EditorService,
    private elementRef: ElementRef,
    private overlay: Overlay,
    private viewContainerRef: ViewContainerRef,
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

  getKey() {
    return this.component.getKey()?.getKey();
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
    if (this.customElement) {
      this.updateCustomElement(this.customElement);
      return;
    }
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

  updateCustomElement(customElement: HTMLElement) {
    const webComponentType = WebComponentType.deserializeBinary(
      this.component.getType()!.getValue() as unknown as Uint8Array,
    );
    const jsonObj = jsonParse(webComponentType.getPropertiesJson()!) as object;
    for (const key of Object.keys(jsonObj)) {
      customElement.setAttribute(key, (jsonObj as any)[key]);
    }
    const style = this.component.getStyle()!;
    if (style) {
      (customElement as any)['style'] = formatStyle(style);
    }
    customElement.removeEventListener(
      'mesop-event',
      this.dispatchCustomUserEvent,
    );
    customElement.addEventListener('mesop-event', this.dispatchCustomUserEvent);
    // TODO: clean up event listener
  }

  ngDoCheck() {
    // Only need to re-compute styles in editor mode to properly
    // show focused component highlight.
    if (this.isEditorMode) {
      this.computeStyles();
      this.renderOverlay();
    }
  }

  renderOverlay() {
    if (this.isEditorFocusedComponent()) {
      if (this.overlayRef) return;
      const overlayConfig = new OverlayConfig({
        positionStrategy: this.overlay
          .position()
          .flexibleConnectedTo(this.viewContainerRef.element)
          .withPositions([
            {
              originX: 'start',
              originY: 'bottom',
              overlayX: 'start',
              overlayY: 'top',
            },
          ]),
      });

      this.overlayRef = this.overlay.create(overlayConfig);
      const portal = new TemplatePortal(
        this.editorOverlay,
        this.viewContainerRef,
      );
      this.overlayRef.attach(portal);
    } else {
      if (this.overlayRef) {
        this.overlayRef.detach();
        this.overlayRef = undefined;
      }
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
      ? typeToComponent[typeName.getFnName()!] || UserDefinedComponent // Some core modules rely on UserDefinedComponent
      : UserDefinedComponent;
    if (typeName.getFnName()?.startsWith('<web>')) {
      console.log('**TYPENAME', typeName);
      const customElementName = typeName.getFnName()!.slice('<web>'.length);
      const customElement = document.createElement(customElementName);
      (customElement as any)['$$trustedHTMLFromStringBypass$$'] =
        trustedHTMLFromStringBypass;
      this.customElement = customElement;
      this.updateCustomElement(customElement);

      this.insertionRef.element.nativeElement.parentElement.appendChild(
        customElement,
      );
    } else {
      // Need to insert at insertionRef and *not* viewContainerRef, otherwise
      // the component (e.g. <mesop-text> will not be properly nested inside <component-renderer>).
      this._componentRef = this.insertionRef.createComponent(
        componentClass, // If it's an unrecognized type, we assume it's a user-defined component
        options,
      );
      this.updateComponentRef();
    }
  }

  dispatchCustomUserEvent = (event: Event) => {
    const customEvent = event as CustomEvent;
    const userEvent = new UserEvent();
    userEvent.setStringValue(JSON.stringify(customEvent.detail['payload']));
    userEvent.setHandlerId(customEvent.detail['handlerId']);
    userEvent.setKey(this.component.getKey());
    this.channel.dispatch(userEvent);

    // this.channel.dispatch();
  };

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
          ['divider', 'text', 'markdown', 'progress_bar'].includes(
            name.getFnName()!,
          )
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

  canAddChildComponent(): boolean {
    return Boolean(
      this.channel
        .getComponentConfigs()
        .find((c) =>
          isComponentNameEquals(
            c.getComponentName()!,
            this.component.getType()?.getName(),
          ),
        )
        ?.getAcceptsChild(),
    );
  }

  addChildComponent(): void {
    this.editorService.addComponentChild(this.component);
  }

  addSiblingComponent(): void {
    this.editorService.addComponentSibling(this.component);
  }

  SelectionMode = SelectionMode;

  getComponentName(): string {
    return this.type()?.getName()?.getFnName() ?? '[root]';
  }

  shouldShowOverlay(): boolean {
    return (
      this.isEditorFocusedComponent() &&
      this.getSelectionMode() === SelectionMode.SELECTING
    );
  }
}

function isRegularComponent(component: ComponentProto) {
  const typeName = component.getType()?.getName()!;
  return (
    component.getType() &&
    !(typeName.getCoreModule() && typeName.getFnName() === 'box')
  );
}

// Copied from:
// https://github.com/angular/angular/blob/567c2f6d904667263a8657df7023c46d4979a23d/packages/core/src/util/security/trusted_types_bypass.ts#L29

/**
 * The Trusted Types policy, or null if Trusted Types are not
 * enabled/supported, or undefined if the policy has not been created yet.
 */
let policy: TrustedTypePolicy | null | undefined;

/**
 * Returns the Trusted Types policy, or null if Trusted Types are not
 * enabled/supported. The first call to this function will create the policy.
 */
function getPolicy(): TrustedTypePolicy | null {
  if (policy === undefined) {
    policy = null;
    if ((window as any).trustedTypes) {
      try {
        policy = (
          (window as any).trustedTypes as TrustedTypePolicyFactory
        ).createPolicy('mesop#custom-web-components', {
          createHTML: (s: string) => s,
          createScript: (s: string) => s,
          createScriptURL: (s: string) => s,
        });
      } catch {
        // trustedTypes.createPolicy throws if called with a name that is
        // already registered, even in report-only mode. Until the API changes,
        // catch the error not to break the applications functionally. In such
        // cases, the code will fall back to using strings.
      }
    }
  }
  return policy;
}

/**
 * Unsafely promote a string to a TrustedHTML, falling back to strings when
 * Trusted Types are not available.
 * @security This is a security-sensitive function; any use of this function
 * must go through security review. In particular, it must be assured that it
 * is only passed strings that come directly from custom sanitizers or the
 * bypassSecurityTrust* functions.
 */
export function trustedHTMLFromStringBypass(
  html: string,
): TrustedHTML | string {
  return getPolicy()?.createHTML(html) || html;
}

(window as any)['trustedHTMLFromStringBypass'] = trustedHTMLFromStringBypass;

// copied from: https://github.com/angular/angular/blob/567c2f6d904667263a8657df7023c46d4979a23d/packages/core/src/util/security/trusted_type_defs.ts#L28

export type TrustedHTML = string & {
  __brand__: 'TrustedHTML';
};
export type TrustedScript = string & {
  __brand__: 'TrustedScript';
};
export type TrustedScriptURL = string & {
  __brand__: 'TrustedScriptURL';
};

export interface TrustedTypePolicyFactory {
  createPolicy(
    policyName: string,
    policyOptions: {
      createHTML?: (input: string) => string;
      createScript?: (input: string) => string;
      createScriptURL?: (input: string) => string;
    },
  ): TrustedTypePolicy;
  getAttributeType(tagName: string, attribute: string): string | null;
}

export interface TrustedTypePolicy {
  createHTML(input: string): TrustedHTML;
  createScript(input: string): TrustedScript;
  createScriptURL(input: string): TrustedScriptURL;
}
