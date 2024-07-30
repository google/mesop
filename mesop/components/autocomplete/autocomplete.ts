import {MatFormFieldModule} from '@angular/material/form-field';
import {MatInputModule} from '@angular/material/input';
import {Component, Input, OnInit} from '@angular/core';
import {
  Key,
  Type,
  UserEvent,
  Style,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {
  AutocompleteType,
  AutocompleteOptionSet,
  AutocompleteOptionGroup,
} from 'mesop/mesop/components/autocomplete/autocomplete_jspb_proto_pb/mesop/components/autocomplete/autocomplete_pb';
import {Channel} from '../../web/src/services/channel';
import {formatStyle} from '../../web/src/utils/styles';
import {Subject} from 'rxjs';
import {debounceTime, startWith} from 'rxjs/operators';
import {AsyncPipe, CommonModule} from '@angular/common';
import {Observable} from 'rxjs';
import {map} from 'rxjs/operators';
import {FormControl, FormsModule, ReactiveFormsModule} from '@angular/forms';
import {
  MatAutocompleteModule,
  MatAutocompleteSelectedEvent,
} from '@angular/material/autocomplete';

@Component({
  selector: 'mesop-autocomplete',
  templateUrl: 'autocomplete.ng.html',
  standalone: true,
  imports: [
    MatInputModule,
    MatFormFieldModule,
    CommonModule,
    MatAutocompleteModule,
    ReactiveFormsModule,
    AsyncPipe,
  ],
})
export class AutocompleteComponent implements OnInit {
  @Input({required: true}) type!: Type;
  @Input() key!: Key;
  @Input() style!: Style;
  private _config!: AutocompleteType;
  filteredOptions: Observable<AutocompleteOptionSet[]> = new Observable<
    AutocompleteOptionSet[]
  >();
  private inputSubject = new Subject<Event>();
  autocompleteControl = new FormControl('');
  constructor(private readonly channel: Channel) {
    this.inputSubject
      .pipe(
        // Setting this to a short duration to avoid having the user trigger another event
        // during this debounce time period:
        // https://github.com/google/mesop/issues/171
        debounceTime(150),
      )
      .subscribe((event) => this.onInputDebounced(event));
  }

  ngOnInit(): void {
    this.filteredOptions = this.autocompleteControl.valueChanges.pipe(
      startWith(''),
      map((value) => {
        return this._filter(value || '', this._config.getOptionsList());
      }),
    );
  }

  ngOnDestroy(): void {
    this.inputSubject.unsubscribe();
  }

  ngOnChanges() {
    this._config = AutocompleteType.deserializeBinary(
      this.type.getValue() as unknown as Uint8Array,
    );
  }

  config(): AutocompleteType {
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

  onInput(event: Event): void {
    this.inputSubject.next(event);
  }

  onInputDebounced(event: Event): void {
    const userEvent = new UserEvent();
    userEvent.setHandlerId(this.config().getOnInputHandlerId()!);
    userEvent.setStringValue((event.target as HTMLInputElement).value);
    userEvent.setKey(this.key);
    this.channel.dispatch(userEvent);
  }

  onKeyUp(event: Event): void {
    const keyboardEvent = event as KeyboardEvent;
    if (keyboardEvent.key === 'Enter') {
      const userEvent = new UserEvent();
      userEvent.setHandlerId(this.config().getOnEnterHandlerId()!);
      userEvent.setStringValue(this.autocompleteControl.value || '');
      userEvent.setKey(this.key);
      this.channel.dispatch(userEvent);
    }
  }

  onAutocompleteSelectEvent(event: MatAutocompleteSelectedEvent): void {
    const userEvent = new UserEvent();
    userEvent.setHandlerId(this.config().getOnSelectionChangeHandlerId()!);
    userEvent.setStringValue(this.autocompleteControl.value || '');
    userEvent.setKey(this.key);
    this.channel.dispatch(userEvent);
  }

  private _filter(
    value: string,
    options: AutocompleteOptionSet[],
  ): AutocompleteOptionSet[] {
    if (!value) {
      return options;
    }
    const filterValue = value.toLowerCase();
    const filteredOptions = new Array<AutocompleteOptionSet>();
    for (const option of options) {
      if (option.getOptionGroup()) {
        const filteredOptionGroup = new AutocompleteOptionGroup();
        filteredOptionGroup.setLabel(option.getOptionGroup()?.getLabel()!);
        for (const subOption of option.getOptionGroup()?.getOptionsList()!) {
          if (subOption?.getValue()?.toLowerCase().includes(filterValue)) {
            filteredOptionGroup.addOptions(subOption);
          }
        }
        if (filteredOptionGroup.getOptionsList().length > 0) {
          const optionSet = new AutocompleteOptionSet();
          optionSet.setOptionGroup(filteredOptionGroup);
          filteredOptions.push(optionSet);
        }
      } else {
        if (
          option.getOption()?.getValue()?.toLowerCase().includes(filterValue)
        ) {
          filteredOptions.push(option);
        }
      }
    }
    return filteredOptions;
  }
}
