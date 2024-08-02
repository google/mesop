import {Injectable} from '@angular/core';
import {
  ThemeMode,
  SetThemeMode,
  ThemeSettings,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';

// Default to light theme because many Mesop apps only support
// light theme, but eventually we will want to default to THEME_MODE_AUTO.
const DEFAULT_THEME_MODE = new SetThemeMode();
DEFAULT_THEME_MODE.setThemeMode(ThemeMode.THEME_MODE_LIGHT);

@Injectable({
  providedIn: 'root',
})
export class ThemeService {
  private prefersDarkColorSchemeMediaQuery = window.matchMedia(
    '(prefers-color-scheme: dark)',
  );

  // Use SetThemeMode instead of ThemeMode directly because the TS type
  // of proto enum differs between upstream and downstream.
  mode = DEFAULT_THEME_MODE;
  onChangePrefersColorScheme!: () => void;
  previousDensityClass: string | undefined;

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
    settings.setThemeMode(this.mode.getThemeMode()!);
    return settings;
  }

  setThemeMode(mode: SetThemeMode) {
    this.mode = mode;
    this.updateTheme();
  }

  setDensity(density: number) {
    const densityClass = `theme-density-${density}`;
    if (this.previousDensityClass) {
      document.body.classList.remove(this.previousDensityClass);
    }
    document.body.classList.add(densityClass);
    this.previousDensityClass = densityClass;
  }

  private updateTheme(): void {
    if (this.isUsingDarkTheme()) {
      document.body.classList.add('dark-theme');
    } else {
      document.body.classList.remove('dark-theme');
    }
  }

  private isUsingDarkTheme(): boolean {
    if (this.mode.getThemeMode() === ThemeMode.THEME_MODE_DARK) {
      return true;
    }
    if (this.mode.getThemeMode() === ThemeMode.THEME_MODE_LIGHT) {
      return false;
    }

    return this.prefersDarkColorSchemeMediaQuery.matches;
  }
}
