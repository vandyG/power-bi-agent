# Accessibility

Aligned to WCAG 2.1 AA and Microsoft Power BI accessibility guidance.

## Audit checklist

### Color & contrast
- [ ] Text vs background ≥ **4.5:1** (or 3:1 for ≥18 pt / 14 pt bold)
- [ ] Graphical objects (axis, marks) ≥ **3:1** vs background
- [ ] Color is **never** the only channel: pair with icon, label, pattern, or position
- [ ] Palette tested with a color-blindness simulator (deuteranopia, protanopia, tritanopia)
- [ ] Red/green only used for delta semantics (negative/positive), with `▲`/`▼` icons

### Keyboard & focus
- [ ] Every interactive element reachable by Tab
- [ ] Tab order set explicitly via Selection pane (top-left → bottom-right by default)
- [ ] Focus indicator visible on all interactive elements (don't disable it via theme)
- [ ] No keyboard trap — `Esc` always returns to the page

### Screen readers
- [ ] Every visual has Alt text (Format → General → Alt text)
- [ ] Alt text describes what the chart shows, not just the title
- [ ] Title text is unique per page
- [ ] Decorative images marked as decorative

### Content & language
- [ ] Page has a single H1 equivalent (the page title)
- [ ] Acronyms expanded on first use
- [ ] Reading order matches visual order
- [ ] Don't rely on hover-only tooltips for critical info — also surface in alt text or a label

### Motion
- [ ] No flashing > 3 Hz
- [ ] Animations can be disabled (Power BI animations respect Windows reduce-motion settings)

## Power BI-specific

- Use the **Show data as table** option (Alt+Shift+F11) for visuals — non-sighted users rely on this.
- Use **Selection pane** to verify and order screen-reader traversal.
- Custom visuals: only use ones marked **Microsoft-certified accessible**. Many community visuals fail screen-reader tests.
- For embedded reports, ensure the host page also conforms to WCAG and the iframe has a meaningful title.

## Testing tools

- **Power BI Accessibility Checker**: built into the View ribbon (Insert → Accessibility Checker).
- **axe DevTools** browser extension on the published report.
- **NVDA** (Windows) or **VoiceOver** (macOS) for actual screen-reader walkthroughs.
- **Stark** or **Adobe Color Contrast Analyzer** for theme JSON validation.
