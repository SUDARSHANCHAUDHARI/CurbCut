// CurbCut web enforcement — ESLint 9 flat config.
// Install:  npm i -D eslint eslint-plugin-jsx-a11y
// Use:      import curbcut from "./enforce/rules/eslint/eslint.config.mjs";
//           export default [ ...curbcut ];           // spread into your flat config
// Or lint directly:
//           npx eslint -c enforce/rules/eslint/eslint.config.mjs "**/*.{jsx,tsx}"
import jsxA11y from "eslint-plugin-jsx-a11y";

/** @type {import("eslint").Linter.Config[]} */
export default [
  jsxA11y.flatConfigs.strict,
  {
    files: ["**/*.{jsx,tsx}"],
    rules: {
      // Mirrors the CurbCut hook's 🟢 AUTO web rules.
      "jsx-a11y/no-static-element-interactions": "error", // WEB_CLICKABLE_DIV
      "jsx-a11y/click-events-have-key-events": "error",   // keyboard parity
      "jsx-a11y/alt-text": "error",                       // WEB_IMG_NO_ALT
      "jsx-a11y/label-has-associated-control": "error",   // labels
      "jsx-a11y/anchor-is-valid": "error",
      "jsx-a11y/no-noninteractive-tabindex": "error",
      "jsx-a11y/tabindex-no-positive": "error",           // WEB_POSITIVE_TABINDEX
      "jsx-a11y/aria-role": "error",
      "jsx-a11y/no-redundant-roles": "error",             // WEB_REDUNDANT_ROLE (ARIA soup)
      "jsx-a11y/no-autofocus": "warn",
      "jsx-a11y/media-has-caption": "warn",
    },
  },
];
