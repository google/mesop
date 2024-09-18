import {
  MatDatepickerModule,
  MatDatepickerInputEvent,
  DateRange,
} from '@angular/material/datepicker';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatInputModule} from '@angular/material/input';
import {Component, Input} from '@angular/core';
import {
  FormControl,
  FormGroup,
  FormsModule,
  ReactiveFormsModule,
} from '@angular/forms';
import {
  DateRangePickerEvent,
  UserEvent,
  Key,
  Type,
  Style,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {DatepickerType} from 'mesop/mesop/components/datepicker/datepicker_jspb_proto_pb/mesop/components/datepicker/datepicker_pb';
import {CommonModule} from '@angular/common';
import {Channel} from '../../web/src/services/channel';
import {formatStyle} from '../../web/src/utils/styles';
import {provideNativeDateAdapter} from '@angular/material/core';
import {debounceTime} from 'rxjs/operators';
import {Subject} from 'rxjs';

@Component({
  selector: 'mesop-datepicker',
  templateUrl: 'datepicker.ng.html',
  standalone: true,
  providers: [provideNativeDateAdapter()],
  imports: [
    MatDatepickerModule,
    MatFormFieldModule,
    MatInputModule,
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
  ],
})
export class DatepickerComponent {
  @Input({required: true}) type!: Type;
  @Input() key!: Key;
  @Input() style!: Style;
  private _config!: DatepickerType;

  // Date picker specific
  readonly date = new FormControl();
  private initialDate = '';
  // Date Range specific
  readonly dateRange = new FormGroup({
    start: new FormControl(),
    end: new FormControl(),
  });
  private initialStartDate = '';
  private initialEndDate = '';
  private dateRangeChangeSubject = new Subject<
    MatDatepickerInputEvent<string | undefined, DateRange<string | undefined>>
  >();

  constructor(private readonly channel: Channel) {
    this.dateRangeChangeSubject
      .pipe(debounceTime(30))
      .subscribe((event) => this.onDateRangeChangeDebounced(event));
  }

  ngOnChanges() {
    this._config = DatepickerType.deserializeBinary(
      this.type.getValue() as unknown as Uint8Array,
    );

    // Override date range inputs if set.
    if (this._config.getIsDateRange()) {
      const startDateString = this._config.getValue1() || '';
      const endDateString = this._config.getValue2() || '';

      let dateInputUpdated = false;
      if (this.initialStartDate !== startDateString) {
        this.initialStartDate = startDateString;
        dateInputUpdated = true;
      }
      if (this.initialEndDate !== endDateString) {
        this.initialEndDate = endDateString;
        this.initialEndDate = endDateString;
        dateInputUpdated = true;
      }

      if (dateInputUpdated) {
        this.dateRange.setValue({
          start: this.makeDate(startDateString),
          end: this.makeDate(endDateString),
        });
      }
    } else {
      const initialDate = this._config.getValue1() || '';
      if (this.initialDate !== initialDate) {
        this.initialDate = initialDate;
        this.date.setValue(this.makeDate(initialDate));
      }
    }
  }

  // For Date picker
  onDateChange(event: MatDatepickerInputEvent<Date>): void {
    if (this.date.value) {
      const userEvent = new UserEvent();
      userEvent.setHandlerId(this.config().getOnChangeHandlerId()!);
      userEvent.setStringValue(this.makeDateString(this.date.value));
      userEvent.setKey(this.key);
      this.channel.dispatch(userEvent);
    }
  }

  // For Date range picker
  onDateRangeChange(
    event: MatDatepickerInputEvent<
      string | undefined,
      DateRange<string | undefined>
    >,
  ): void {
    this.dateRangeChangeSubject.next(event);
  }

  // We debounce the date range change event to avoid an issue where two change events
  // are fired consecutively when resetting the date range.
  //
  // If we send both events, this can cause issues if the value parameters are set on
  // the component. What will happen is the end date will not get reset, which is why
  // we only want to send the second event.
  //
  // The other reason we need debounce is to handle the case where the user edits the
  // start date directly. On blur, only one event will fire. And we need to send this
  // event if the end date is also set.
  onDateRangeChangeDebounced(
    event: MatDatepickerInputEvent<
      string | undefined,
      DateRange<string | undefined>
    >,
  ): void {
    if (this.dateRange.value.start && this.dateRange.value.end) {
      const userEvent = new UserEvent();
      userEvent.setHandlerId(this.config().getOnChangeHandlerId()!);
      const dateRangeEvent = new DateRangePickerEvent();
      dateRangeEvent.setStartDate(
        this.makeDateString(this.dateRange.value.start),
      );
      dateRangeEvent.setEndDate(this.makeDateString(this.dateRange.value.end));
      userEvent.setDateRangePickerEvent(dateRangeEvent);
      userEvent.setKey(this.key);
      this.channel.dispatch(userEvent);
    }
  }

  private makeDate(date_input: string): Date | null {
    if (date_input) {
      const [year, month, date] = date_input.split('-').map((e) => parseInt(e));
      return new Date(year, month - 1, date);
    }
    return null;
  }

  private makeDateString(date: Date | null): string {
    return date
      ? `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`
      : '';
  }

  config(): DatepickerType {
    return this._config;
  }

  getStyle(): string {
    return formatStyle(this.style);
  }

  getColor(): 'primary' | 'accent' | 'warn' {
    return this.config().getColor() as 'primary' | 'accent' | 'warn';
  }

  getFloatLabel(): 'always' | 'auto' {
    return this.config().getFloatLabel() as 'always' | 'auto';
  }

  getAppearance(): 'fill' | 'outline' {
    return this.config().getAppearance() as 'fill' | 'outline';
  }

  getSubscriptSizing(): 'fixed' | 'dynamic' {
    return this.config().getSubscriptSizing() as 'fixed' | 'dynamic';
  }
}
