import { createTheme as createMuiTheme } from "@mui/material";
import { createPalette } from "./create-palette";
import { createComponents } from "./create-components";
import { createShadows } from "./create-shadows";
import { createTypography } from "./create-typography";
import { zhCN } from "@mui/material/locale";

export function createTheme(themeColor) {
  const palette = createPalette(themeColor);
  const components = createComponents({ palette });
  const shadows = createShadows();
  const typography = createTypography();

  return createMuiTheme({
    spacing: 10,
    breakpoints: {
      values: {
        xs: 0,
        sm: 600,
        md: 900,
        lg: 1200,
        xl: 1440,
      },
    },
    components,
    palette,
    shadows,
    shape: {
      borderRadius: 4,
    },
    typography,
    zhCN,
  });
}
