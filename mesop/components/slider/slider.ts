import {MatSliderModule} from '@angular/material/slider';
import {Component, Input} from '@angular/core';
import {
  UserEvent,
  Key,
  Type,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {SliderType} from 'mesop/mesop/components/slider/slider_jspb_proto_pb/mesop/components/slider/slider_pb';
import {Channel} from '../../web/src/services/channel';
import {debounceTime} from 'rxjs/operators';
import {Subject} from 'rxjs';

@Component({
  templateUrl: 'slider.ng.html',
  standalone: true,
  imports: [MatSliderModule],
})
export class SliderComponent {
  @Input({required: true}) type!: Type;
  @Input() key!: Key;
  private _config!: SliderType;
  private changeSubject = new Subject<number>();

  constructor(private readonly channel: Channel) {
    this.changeSubject
      .pipe(debounceTime(300))
      .subscribe((number) => this.onValueChangeDebounced(number));
  }

  ngOnChanges() {
    this._config = SliderType.deserializeBinary(
      this.type.getValue() as unknown as Uint8Array,
    );
  }

  config(): SliderType {
    return this._config;
  }

  getColor(): 'primary' | 'accent' | 'warn' {
    return this.config().getColor() as 'primary' | 'accent' | 'warn';
  }

  onValueChange(value: number): void {
    this.changeSubject.next(value);
  }

  onValueChangeDebounced(value: number) {
    const userEvent = new UserEvent();

    userEvent.setHandlerId(this.config().getOnValueChangeHandlerId()!);
    userEvent.setDoubleValue(value);
    userEvent.setKey(this.key);
    this.channel.dispatch(userEvent);
  }
}
