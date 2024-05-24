import {
  ChangeDetectorRef,
  Component,
  ElementRef,
  Input,
  ViewChild,
} from '@angular/core';
import {
  Key,
  Style,
  Type,
  UserEvent,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {MarkdownType} from 'mesop/mesop/components/markdown/markdown_jspb_proto_pb/mesop/components/markdown/markdown_pb';
import {formatStyle} from '../../web/src/utils/styles';
import {Channel} from '../../web/src/services/channel';
import {MatIconModule} from '@angular/material/icon';

@Component({
  selector: 'mesop-markdown',
  templateUrl: 'markdown.ng.html',
  standalone: true,
  styleUrl: 'markdown.css',
  imports: [MatIconModule],
})
export class MarkdownComponent {
  @ViewChild('menu', {read: ElementRef}) menu!: ElementRef;
  @Input({required: true}) type!: Type;
  @Input() key!: Key;
  @Input() style!: Style;
  items: string[] = [];

  private _config!: MarkdownType;

  constructor(
    readonly changeDetectorRef: ChangeDetectorRef,
    private channel: Channel,
  ) {}

  async ngOnChanges() {
    this._config = MarkdownType.deserializeBinary(
      this.type.getValue() as unknown as Uint8Array,
    );
  }

  config(): MarkdownType {
    return this._config;
  }

  getStyle(): string {
    return formatStyle(this.style);
  }

  onClick(event: Event) {
    const target = event.target as HTMLElement;
    if (target.tagName === 'A') {
      console.log('clicked', target);
      const items = target.className.split(',');
      this.items = items;
      const rect = target.getBoundingClientRect();
      const menuElement = this.menu.nativeElement;
      menuElement.style.position = 'absolute';
      menuElement.style.top = `${rect.top + window.scrollY + 24}px`; // Adjust for scrolling
      menuElement.style.left = `${rect.left + window.scrollX + 24}px`; // Adjust for scrolling
      menuElement.style.display = 'flex';
      event.stopPropagation(); // Prevent the click from immediately closing the menu
      this.listenForOutsideClicks();
    }
  }

  listenForOutsideClicks() {
    document.addEventListener(
      'click',
      this.closeMenuOnClickOutside.bind(this),
      {once: true},
    );
  }

  closeMenuOnClickOutside(event: MouseEvent) {
    const target = event.target as HTMLElement;
    const menuElement = this.menu.nativeElement;
    if (!menuElement.contains(target)) {
      menuElement.style.display = 'none';
    } else {
      // If the click is inside the menu, listen for the next click outside
      this.listenForOutsideClicks();
    }
  }

  clickMenuItem(event: Event) {
    const menuElement = this.menu.nativeElement;
    menuElement.style.display = 'none';
    const userEvent = new UserEvent();
    userEvent.setKey(this.key);
    userEvent.setHandlerId(this.config().getOnSelectEventHandlerId()!);
    userEvent.setStringValue(
      (event.target as HTMLElement).getAttribute('data-item')!,
    );
    this.channel.dispatch(userEvent);
  }
}
