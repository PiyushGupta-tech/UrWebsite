# Urbanrupee PNG logos

| File | Use |
|------|-----|
| **urwhite.png** | Full wordmark on **dark** backgrounds (nav, footer, checkout) — “rupee” in white |
| **urblack.png** | Full wordmark on **light** backgrounds — “rupee” in black |
| **urlogo.png** | Shield icon only (favicon, compact UI, dashboard bar) |

## In Vue

```vue
<BrandLogo variant="on-dark" />   <!-- urwhite.png -->
<BrandLogo variant="on-light" />  <!-- urblack.png -->
<BrandLogo variant="icon" />        <!-- urlogo.png -->
```

Paths are defined in `frontend/src/constants/logos.js`.

## Merchant logos

Upload partner marks to `logos/merchants/` — see `logos/merchants/README.md` for filenames. Used on the Payment Orchestration hero (and can be wired elsewhere via `MERCHANT_LOGOS` / `ORCHESTRATION_MERCHANTS`).
