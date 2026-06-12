export const LIFECYCLE_FLOW = [
  'new_site',
  'relationship_building',
  'showroom_visit_scheduled',
  'showroom_visit_done',
  'selection_done',
  'quotation_sent',
  'negotiation',
  'order_confirmed',
] as const;

export const MARKETING_STAGES = ['relationship_building', 'showroom_visit_scheduled'] as const;
export const SALES_STAGES = [
  'showroom_visit_done',
  'selection_done',
  'quotation_sent',
  'negotiation',
  'order_confirmed',
] as const;

export function formatStatus(status: string) {
  return status.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());
}

/** Demo-friendly transition options per role */
export function getDemoTransitionOptions(current: string, role: string): string[] {
  const idx = LIFECYCLE_FLOW.indexOf(current as (typeof LIFECYCLE_FLOW)[number]);

  if (role === 'manager' || role === 'administrator') {
    return [...LIFECYCLE_FLOW, 'lost'];
  }

  if (role === 'marketing_executive') {
    const opts: string[] = [current];
    for (const stage of LIFECYCLE_FLOW) {
      const stageIdx = LIFECYCLE_FLOW.indexOf(stage);
      if (stageIdx > idx && (MARKETING_STAGES as readonly string[]).includes(stage)) {
        opts.push(stage);
      }
    }
    if (idx < LIFECYCLE_FLOW.indexOf('showroom_visit_scheduled')) {
      opts.push('showroom_visit_scheduled');
    }
    opts.push('lost');
    return [...new Set(opts)];
  }

  if (role === 'sales_executive') {
    const opts: string[] = [current];
    const salesStartIdx = LIFECYCLE_FLOW.indexOf('showroom_visit_done');
    // Show full sales pipeline from current position (or from showroom_visit_done if still at marketing stage)
    const fromIdx = idx < salesStartIdx ? salesStartIdx : idx;
    for (let i = fromIdx + 1; i < LIFECYCLE_FLOW.length; i++) {
      opts.push(LIFECYCLE_FLOW[i]);
    }
    if (idx < salesStartIdx) {
      opts.push('showroom_visit_done');
    }
    opts.push('lost');
    return [...new Set(opts)];
  }

  return [current];
}

export function getRecommendedNext(current: string, role: string): string | null {
  const options = getDemoTransitionOptions(current, role).filter((s) => s !== current && s !== 'lost');
  return options[0] || null;
}

export function canTransitionLifecycle(role: string): boolean {
  return ['marketing_executive', 'sales_executive', 'manager', 'administrator'].includes(role);
}
