# UrbanRupee Admin Payout Micro Dashboard — Design Reference

Stitch project: `13644661613890610533`  
Screen: UrbanRupee Admin — Payout Micro Dashboard (`513a62d003004f629282b9c36c9f4953`)

> Stitch MCP was not available in the implementation environment. This document captures
> design tokens and layout from the implementation spec. Add `code.html` and `screen.png`
> from Stitch when available.

## Layout (desktop ~1440px)

- **Top bar:** wordmark + "Admin Dashboard" | LIVE pill + last updated | Logout
- **Main grid:** ~62% left / ~38% right
  - **Left:** India transaction map (~70% height) + live transactions table (~30%)
  - **Right:** Payout KPI cards + top providers + Payin placeholder (Phase 2)

## Design tokens

```css
--ur-primary: #1a3a7a;
--ur-accent: #3bdef7;
--ur-bg-dark: #1e293b;
--ur-card-bg: #162528;
--ur-card-border: #1e3538;
--ur-text: #f0fafb;
--ur-muted: #4a8890;
--ur-success: #05a34a;
--ur-warning: #fbbc06;
--ur-danger: #ff3366;
```

## Typography & spacing

- Card radius: 12–16px
- Subtle borders, no heavy gradients
- INR formatting: `en-IN` locale with Indian grouping
