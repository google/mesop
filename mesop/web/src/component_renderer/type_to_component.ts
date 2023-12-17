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
import {TextInputComponent} from '../../../components/text_input/text_input';

export interface BaseComponent {
  key: Key;
  type: Type;

  ngOnChanges(): void;
}

export interface TypeToComponent {
  [typeName: string]: new (...rest: any[]) => BaseComponent;
}

export const typeToComponent = {
  'divider': DividerComponent,
  'badge': BadgeComponent,
  'tooltip': TooltipComponent,
  'input': InputComponent,
  'button': ButtonComponent,
  'checkbox': CheckboxComponent,
  'text': TextComponent,
  'markdown': MarkdownComponent,
  'text_input': TextInputComponent,
} as TypeToComponent;
