import {AutocompleteComponent} from '../../../components/autocomplete/autocomplete';
import {LinkComponent} from '../../../components/link/link';
import {HtmlComponent} from '../../../components/html/html';
import {UploaderComponent} from '../../../components/uploader/uploader';
import {EmbedComponent} from '../../../components/embed/embed';
import {TableComponent} from '../../../components/table/table';
import {SidenavComponent} from '../../../components/sidenav/sidenav';
import {VideoComponent} from '../../../components/video/video';
import {AudioComponent} from '../../../components/audio/audio';
import {ImageComponent} from '../../../components/image/image';
import {SliderComponent} from '../../../components/slider/slider';
import {SelectComponent} from '../../../components/select/select';
import {RadioComponent} from '../../../components/radio/radio';
import {SlideToggleComponent} from '../../../components/slide_toggle/slide_toggle';
import {ProgressSpinnerComponent} from '../../../components/progress_spinner/progress_spinner';
import {ProgressBarComponent} from '../../../components/progress_bar/progress_bar';
import {IconComponent} from '../../../components/icon/icon';
import {DividerComponent} from '../../../components/divider/divider';
import {BadgeComponent} from '../../../components/badge/badge';
import {TooltipComponent} from '../../../components/tooltip/tooltip';
import {InputComponent} from '../../../components/input/input';
import {
  Key,
  Style,
  Type,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';

import {CheckboxComponent} from '../../../components/checkbox/checkbox';
import {ButtonComponent} from '../../../components/button/button';
import {TextComponent} from '../../../components/text/text';
import {MarkdownComponent} from '../../../components/markdown/markdown';
import {Component, Input} from '@angular/core';

export interface BaseComponent {
  key: Key;
  type: Type;
  style?: Style;

  ngOnChanges(): void;
}

export interface TypeToComponent {
  [typeName: string]: new (...rest: any[]) => BaseComponent;
}

@Component({
  template: '<ng-content></ng-content>',
  standalone: true,
})
export class UserDefinedComponent implements BaseComponent {
  @Input() key!: Key;
  @Input() type!: Type;
  ngOnChanges() {
    // Placeholder function since the
  }
}

export const typeToComponent = {
  'autocomplete': AutocompleteComponent,
  'link': LinkComponent,
  'html': HtmlComponent,
  'uploader': UploaderComponent,
  'embed': EmbedComponent,
  'table': TableComponent,
  'sidenav': SidenavComponent,
  'video': VideoComponent,
  'audio': AudioComponent,
  'image': ImageComponent,
  'slider': SliderComponent,
  'select': SelectComponent,
  'radio': RadioComponent,
  'content_slide_toggle': SlideToggleComponent,
  'progress_spinner': ProgressSpinnerComponent,
  'progress_bar': ProgressBarComponent,
  'icon': IconComponent,
  'divider': DividerComponent,
  'badge': BadgeComponent,
  'tooltip': TooltipComponent,
  'input': InputComponent,
  // Textarea is a special case where it's exposed as a separate
  // component / API, but the implementation is almost identical as Input.
  'textarea': InputComponent,
  'content_button': ButtonComponent,
  'content_checkbox': CheckboxComponent,
  'text': TextComponent,
  'markdown': MarkdownComponent,
} as TypeToComponent;

export function registerCustomComponent(
  name: string,
  component: new (...rest: any[]) => UserDefinedComponent,
) {
  // Prefix with <custom> to ensure there's never any overlap.
  typeToComponent[`<custom>${name}`] = component;
}
