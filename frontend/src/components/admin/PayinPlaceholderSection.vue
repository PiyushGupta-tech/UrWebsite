<template>
  <div class="payin-section">
    <div class="payin-section__header">
      <h2 class="payin-section__title">Payin</h2>
      <span class="payin-section__badge">Phase 2</span>
    </div>

    <div class="payin-grid">
      <article class="payin-card">
        <p class="payin-card__label">Today success</p>
        <p class="payin-card__value payin-card__value--placeholder">—</p>
      </article>

      <article class="payin-card">
        <p class="payin-card__label">Earnings</p>
        <div class="payin-card__dual">
          <div class="payin-card__metric">
            <p class="payin-card__sub-label">Today</p>
            <p class="payin-card__value payin-card__value--placeholder">—</p>
          </div>
          <span class="payin-card__sep" aria-hidden="true">/</span>
          <div class="payin-card__metric">
            <p class="payin-card__sub-label">Total</p>
            <p class="payin-card__value payin-card__value--placeholder">—</p>
          </div>
        </div>
      </article>

      <article class="payin-card payin-card--warning">
        <p class="payin-card__label">Pending today</p>
        <div class="payin-card__dual">
          <div class="payin-card__metric">
            <p class="payin-card__sub-label">Txns</p>
            <p class="payin-card__value payin-card__value--placeholder">—</p>
          </div>
          <span class="payin-card__sep" aria-hidden="true">/</span>
          <div class="payin-card__metric">
            <p class="payin-card__sub-label">Amount</p>
            <p class="payin-card__value payin-card__value--placeholder">—</p>
          </div>
        </div>
      </article>

      <article class="payin-card">
        <p class="payin-card__label">Overall successful amount</p>
        <p class="payin-card__value payin-card__value--placeholder">—</p>
      </article>
    </div>

    <div class="payin-providers">
      <h3 class="payin-providers__title">Top providers today</h3>
      <p class="payin-providers__empty">Coming soon</p>
    </div>
  </div>
</template>

<style scoped>
.payin-section {
  display: flex;
  flex-direction: column;
  min-height: 0;
  overflow: hidden;
}

.payin-section__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 12px;
}

.payin-section__title {
  margin: 0;
  font-size: 16px;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: #fff;
  text-transform: uppercase;
  text-shadow:
    0 0 8px rgba(255, 255, 255, 0.55),
    0 0 18px rgba(240, 250, 251, 0.28);
}

.payin-section__badge {
  padding: 3px 8px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.08);
  color: var(--ur-muted);
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.04em;
}

.payin-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
  flex-shrink: 0;
}

.payin-card__label {
  margin: 0 0 6px;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.05em;
  color: #fff;
  text-transform: uppercase;
  text-shadow:
    0 0 8px rgba(255, 255, 255, 0.55),
    0 0 18px rgba(240, 250, 251, 0.28);
}

.payin-card__value {
  margin: 0;
  font-size: 20px;
  font-weight: 700;
  color: var(--ur-text);
}

.payin-card__value--placeholder {
  color: rgba(240, 250, 251, 0.4);
}

.payin-card__dual {
  display: flex;
  align-items: flex-end;
  gap: 6px;
}

.payin-card__metric {
  flex: 1;
  min-width: 0;
}

.payin-card__sub-label {
  margin: 0 0 4px;
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.04em;
  color: var(--ur-muted);
  text-transform: uppercase;
}

.payin-card__dual .payin-card__value {
  font-size: 18px;
}

.payin-card__sep {
  flex-shrink: 0;
  padding-bottom: 3px;
  color: var(--ur-muted);
  font-size: 18px;
  font-weight: 400;
}

.payin-card--warning .payin-card__value {
  color: rgba(251, 188, 6, 0.45);
}

.payin-providers {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid var(--ur-card-border);
  flex: 1 1 auto;
  min-height: 0;
  overflow: auto;
}

.payin-providers__title {
  margin: 0 0 8px;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--ur-muted);
}

.payin-providers__empty {
  margin: 0;
  padding: 8px;
  font-size: 11px;
  color: var(--ur-muted);
  text-align: center;
  border-radius: 8px;
  background: var(--ur-surface-raised);
  border: 1px solid var(--ur-card-border);
}
</style>
