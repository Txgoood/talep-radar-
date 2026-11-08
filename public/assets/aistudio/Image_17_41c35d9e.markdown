---
name: Talep Radari Native Desktop
colors:
  surface: '#0c1321'
  surface-dim: '#0c1321'
  surface-bright: '#323949'
  surface-container-lowest: '#070e1c'
  surface-container-low: '#151b2a'
  surface-container: '#19202e'
  surface-container-high: '#232a39'
  surface-container-highest: '#2e3544'
  on-surface: '#dce2f6'
  on-surface-variant: '#c1c7d3'
  inverse-surface: '#dce2f6'
  inverse-on-surface: '#2a3040'
  outline: '#8b919d'
  outline-variant: '#414751'
  surface-tint: '#a4c9ff'
  primary: '#a4c9ff'
  on-primary: '#00315d'
  primary-container: '#60a5fa'
  on-primary-container: '#003a6b'
  inverse-primary: '#0060ac'
  secondary: '#ddb7ff'
  on-secondary: '#490080'
  secondary-container: '#6f00be'
  on-secondary-container: '#d6a9ff'
  tertiary: '#4ae176'
  on-tertiary: '#003915'
  tertiary-container: '#06bb56'
  on-tertiary-container: '#00431a'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#d4e3ff'
  primary-fixed-dim: '#a4c9ff'
  on-primary-fixed: '#001c39'
  on-primary-fixed-variant: '#004883'
  secondary-fixed: '#f0dbff'
  secondary-fixed-dim: '#ddb7ff'
  on-secondary-fixed: '#2c0051'
  on-secondary-fixed-variant: '#6900b3'
  tertiary-fixed: '#6bff8f'
  tertiary-fixed-dim: '#4ae176'
  on-tertiary-fixed: '#002109'
  on-tertiary-fixed-variant: '#005321'
  background: '#0c1321'
  on-background: '#dce2f6'
  surface-variant: '#2e3544'
typography:
  headline-lg:
    fontFamily: Segoe UI
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 26px
  headline-md:
    fontFamily: Segoe UI
    fontSize: 16px
    fontWeight: '600'
    lineHeight: 22px
  headline-sm:
    fontFamily: Segoe UI
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 18px
  body-default:
    fontFamily: Segoe UI
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
  body-strong:
    fontFamily: Segoe UI
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
  caption:
    fontFamily: Segoe UI
    fontSize: 11px
    fontWeight: '400'
    lineHeight: 14px
  label-dense:
    fontFamily: Segoe UI
    fontSize: 10px
    fontWeight: '700'
    lineHeight: 12px
  code-default:
    fontFamily: Cascadia Code
    fontSize: 11px
    fontWeight: '400'
    lineHeight: 15px
  code-compact:
    fontFamily: Cascadia Code
    fontSize: 10px
    fontWeight: '400'
    lineHeight: 14px
  code-strong:
    fontFamily: Cascadia Code
    fontSize: 11px
    fontWeight: '600'
    lineHeight: 15px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  gutter: 0.5rem
  margin: 0.5rem
  space-xs: 0.25rem
  space-sm: 0.375rem
  space-md: 0.5rem
  space-lg: 0.75rem
  space-xl: 1rem
---

## Brand & Style
The design system establishes a high-density, mission-critical operations cockpit built for Windows 11 x64 execution via PySide6 and Qt Widgets. Designed for continuous monitoring, intelligence extraction, and live command execution, the aesthetic moves away from breezy, web-influenced consumer patterns and embraces the discipline of high-reliability desktop engineering.

The visual style blends Windows 11 Sun Valley precision with mission-critical systems monitoring: 1px structural framing, subdued cold-slate background steps, dense typography, and high-legibility status indicators. The environment prioritizes information throughput, deterministic layout behavior, and instant state legibility. The interface minimizes non-functional ornamentation, relying on tonal contrast, micro-radii, and precise alignment to give operators immediate confidence during fast triage operations.

## Colors
The color hierarchy is engineered for long-shift legibility under low-light ambient office environments, eliminating eye strain while retaining crisp semantic signals.

### Surface System
- `canvas-base`: `#0B1220` — Master window canvas, background of split panes, and docking area borders.
- `surface-default`: `#142033` — Primary workspace containers, data tables, search filter panels, and log viewports.
- `surface-elevated`: `#1C2B41` — Popovers, context menus, toolbars, modal dialogs, and active tab heads.
- `surface-highlight`: `#24354D` — Selected table row states, item hover treatments, and pressed button surfaces.
- `border-subtle`: `#24354D` — Canonical 1px divider for table cells, docking separators, and widget perimeters.
- `border-strong`: `#3B5170` — Focused input rings, active splitters, and modal borders.

### Text & Readability
- `text-primary`: `#E8EEF7` — High-contrast white-ice for titles, active fields, table cell values, and key metrics.
- `text-secondary`: `#A6B4C8` — Neutral blue-gray for field labels, descriptive captions, and secondary parameters.
- `text-muted`: `#64748B` — Low-emphasis slate for column headers, deactivated options, and static syntax punctuation.

### Semantic & Operational Accents
- `accent-info`: `#60A5FA` — Primary interactive emphasis, Telegram poller indicators, and hyperlinked IDs.
- `accent-success`: `#22C55E` — Engine running state, active connections, confirmed matches, and valid health checks.
- `accent-warning`: `#FBBF24` — Ambiguous parse alerts, throttled API rates, and items awaiting operator review.
- `accent-danger`: `#F87171` — Emergency stop triggers, disconnected state, fatal parser panics, and lockouts.
- `accent-ai`: `#A855F7` — Local model inference engine, vector matching results, and extraction confidence badges.

## Typography
Typographic scale and vertical rhythm are calibrated for fixed physical screen monitors (1080p to 4K at 100%-150% DPI scaling).

- **Proportional Stack:** `Segoe UI`, `-apple-system`, `sans-serif` serves as the primary system engine. It delivers rapid glanceability across dense layouts.
- **Monospaced Stack:** `Cascadia Code`, `Consolas`, `monospace` is mandated for strict spatial data: telegram record identifiers, raw payloads, IP addresses, memory addresses, parsing logs, and timestamps. Tabular numeric data within tables must apply tabular figures (`font-variant-numeric: tabular-nums`) to preserve column vertical tracking.
- **Hierarchy:** No body text in the interface exceeds 12px; desktop productivity relies on maximizing row count over oversized typography. Status indicators leverage 10px uppercase tracking for rapid identification without screen crowding.

## Layout & Spacing
The layout adheres strictly to an absolute 4px/8px engineering grid. Screen space is preserved by default; there are no empty margin voids, oversized mobile hero containers, or decorative white buffers.

### Spatial Architecture
- **Master Canvas Structure:** Structured using `QSplitter` containers with persistent pixel sizing, allowing users to dock and resize the Telegram channel tree, target feed table, inspector view, and real-time execution log.
- **Panel Insets:** Outer pane boundaries use `margin: 0.5rem` (8px), preventing window-edge crowding while maximizing horizontal and vertical payload acreage.
- **Inner Spacing:** Component internal padding uses `space-xs` (4px) vertically and `space-sm` (6px) or `space-md` (8px) horizontally for standard inputs and compact pushbuttons.
- **Table Grids:** Standard row height is fixed to 26px for high-density listing and 32px for expandable multi-attribute entries. Cell internal horizontal padding is strictly 6px.

## Elevation & Depth
In this native dark desktop environment, depth is established via tonal layering and crisp 1px structural boundary lines (`#24354D`), rather than large blurred drop shadows.

- **Level 0 (Application Floor):** `#0B1220` — Master window canvas and inactive splitter tracks.
- **Level 1 (Dock & Panel Surfaces):** `#142033` — Content panels, main tables, and filter sidebars bounded by a 1px solid `#24354D` border.
- **Level 2 (Active Controls & Headers):** `#1C2B41` — Panel headers, toolbars, and inactive button baselines.
- **Level 3 (Overlays & Menus):** `#1C2B41` surrounded by a 1px `#3B5170` border with a subtle desktop ambient drop shadow: `0 4px 12px rgba(0, 0, 0, 0.45)`. Reserved strictly for context menus, combobox dropdown popups, and floating tooltip notifications.

## Shapes
The shape system mirrors native Windows 11 desktop geometry with constrained corner rounding:

- **Interactive Controls (Inputs, Buttons, ComboBoxes):** 6px radius (`0.25rem` to `0.375rem`), balancing modern aesthetic softness with dense horizontal packing.
- **Embedded Badges & Status Chips:** 4px radius, preserving a tight, tag-like look.
- **Application Panels & Windows:** 6px radius for internal dock frames; outer main window uses default OS window frame rounding.
- **Context Menus & Dialog Windows:** 8px radius with a 1px solid stroke (`#3B5170`).
- **Tabs:** 4px on top corners, square at base when locked to dock bars.

## Components

### Buttons
- **Standard Button:** Background `#1C2B41`, border 1px solid `#24354D`, text `#E8EEF7`. Height 26px, padding 0 10px. Hover: background `#24354D`, border `#3B5170`. Pressed: background `#142033`.
- **Primary / Action Button:** Background `#60A5FA`, text `#0B1220` (high-contrast navy), font weight 600. Hover: background `#93C5FD`.
- **Emergency Kill-Switch Button:** Background `#F87171` (or transparent with 1px solid `#F87171`), text `#F87171` (filled: `#0B1220` with bold text), with an icon prefix. Active emergency state flashes a solid `#F87171` fill with immediate lockout confirmation.

### Status Badges
Engineered with an icon glyph (8x8px) followed by uppercase 10px text:
- **Read-Only:** Background `rgba(100, 116, 139, 0.15)`, text `#A6B4C8`, border 1px solid `rgba(100, 116, 139, 0.3)`.
- **Confirmed:** Background `rgba(34, 197, 94, 0.15)`, text `#22C55E`, border 1px solid `rgba(34, 197, 94, 0.35)`.
- **Uncertain / Low Confidence:** Background `rgba(251, 191, 36, 0.15)`, text `#FBBF24`, border 1px solid `rgba(251, 191, 36, 0.35)`.
- **Awaiting Approval:** Background `rgba(96, 165, 250, 0.15)`, text `#60A5FA`, border 1px solid `rgba(96, 165, 250, 0.35)`.
- **Emergency Lock:** Background `rgba(248, 113, 113, 0.2)`, text `#F87171`, border 1px solid `#F87171`.

### Data Tables & Lists (`QTableView` / `QTreeView`)
- Alternating row styling: alternate background `#101928` on primary `#142033`.
- Row height: 26px compact mode, 32px regular.
- Header view: background `#0B1220`, border bottom 1px solid `#24354D`, font size 11px uppercase, text `#64748B`.
- Selection: background `rgba(96, 165, 250, 0.2)`, cell outline 1px solid `#60A5FA`.

### Input Fields & Controls
- **Line Edit / Spin Box:** Height 24px, background `#0B1220`, border 1px solid `#24354D`, text `#E8EEF7`, padding 2px 6px. Focus: border 1px solid `#60A5FA`.
- **Checkbox / Radio:** Size 14x14px, background `#0B1220`, border 1px solid `#3B5170`, checked background `#60A5FA` with dark tick mark.

### Windows Native Scrollbars (`QScrollBar`)
- Width / Height: 8px.
- Track: `#0B1220` with no borders.
- Thumb: `#24354D`, border-radius 4px. Hover: thumb becomes `#3B5170`. No arrow buttons on track terminals.

### Splitters (`QSplitter`)
- Handle width: 4px.
- Color: `#0B1220` with a 1px centered accent guide of `#24354D`. Hover color shifts to `#60A5FA` to signal interactivity.

### Bottom Status Bar (`QStatusBar`)
- Height: 24px fixed.
- Background: `#0B1220`, top border 1px solid `#24354D`.
- Layout: Horizontal distribution of compartmentalized system status blocks separated by 1px vertical slate dividers:
  - `Engine`: Status pill + ping time (`24ms`).
  - `Telegram Poller`: Channel count + queue size (`12 pending`).
  - `Local Model`: GPU/CPU badge + VRAM usage (`Ollama: 3.2 GB`).
  - `Build`: Right-aligned monospaced version string (`v1.0.0-x64`).