import {Injectable, Renderer2, RendererFactory2} from '@angular/core';
import {BehaviorSubject} from 'rxjs';
import {Channel} from './channel';
import {
  ChangePrefersColorScheme,
  ResizeEvent,
  ThemeMode,
  SetThemeMode,
  UserEvent,
  ThemeModeMap,
  ThemeSettings,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';

@Injectable({
  providedIn: 'root',
})
export class ThemeService {
  private prefersDarkColorSchemeMediaQuery = window.matchMedia(
    '(prefers-color-scheme: dark)',
  );

  // Default to light theme because many Mesop apps only support
  // light theme, but eventually we will want to default to THEME_MODE_AUTO.
  mode: ThemeModeMap[keyof ThemeModeMap] = ThemeMode.THEME_MODE_LIGHT;
  onChangePrefersColorScheme!: () => void;

  constructor() {
    this.prefersDarkColorSchemeMediaQuery.addEventListener('change', (e) => {
      this.updateTheme();
      this.onChangePrefersColorScheme();
    });
  }

  setOnChangePrefersColorScheme(onChangePrefersColorScheme: () => void) {
    this.onChangePrefersColorScheme = onChangePrefersColorScheme;
  }

  getThemeSettings(): ThemeSettings {
    const settings = new ThemeSettings();
    settings.setPrefersDarkTheme(
      window.matchMedia('(prefers-color-scheme: dark)').matches,
    );
    settings.setThemeMode(this.mode);
    return settings;
  }

  setThemeMode(mode: ThemeModeMap[keyof ThemeModeMap]) {
    this.mode = mode;
    this.updateTheme();
  }

  private updateTheme(): void {
    if (this.isUsingDarkTheme()) {
      document.body.classList.add('dark-theme');
    } else {
      document.body.classList.remove('dark-theme');
    }
  }

  private isUsingDarkTheme(): boolean {
    if (this.mode == ThemeMode.THEME_MODE_DARK) {
      return true;
    }
    if (this.mode == ThemeMode.THEME_MODE_LIGHT) {
      return false;
    }

    return this.prefersDarkColorSchemeMediaQuery.matches;
  }
}
