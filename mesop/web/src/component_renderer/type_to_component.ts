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
  Type,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';

import {CheckboxComponent} from '../../../components/checkbox/checkbox';
import {ButtonComponent} from '../../../components/button/button';
import {TextComponent} from '../../../components/text/text';
import {MarkdownComponent} from '../../../components/markdown/markdown';

export interface BaseComponent {
  key: Key;
  type: Type;

  ngOnChanges(): void;
}

export interface TypeToComponent {
  [typeName: string]: new (...rest: any[]) => BaseComponent;
}

export const typeToComponent = {
  'slider': SliderComponent,
  'select': SelectComponent,
  'radio': RadioComponent,
  'slide_toggle': SlideToggleComponent,
  'progress_spinner': ProgressSpinnerComponent,
  'progress_bar': ProgressBarComponent,
  'icon': IconComponent,
  'divider': DividerComponent,
  'badge': BadgeComponent,
  'tooltip': TooltipComponent,
  'input': InputComponent,
  'button': ButtonComponent,
  'checkbox': CheckboxComponent,
  'text': TextComponent,
  'markdown': MarkdownComponent,
} as TypeToComponent;
