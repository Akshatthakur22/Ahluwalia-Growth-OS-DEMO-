export const MET_WITH_OPTIONS = [
  { value: 'owner', label: 'Owner' },
  { value: 'builder', label: 'Builder' },
  { value: 'architect', label: 'Architect' },
  { value: 'designer', label: 'Designer' },
];

export const MEETING_CATEGORIES = [
  { value: 'A', label: 'A — Key Decision Maker' },
  { value: 'B', label: 'B — Influencer' },
  { value: 'C', label: 'C — Site Contact' },
  { value: 'D', label: 'D — Peripheral' },
];

export const RELATIONSHIP_STAGES = [
  { value: 'new', label: 'New Contact' },
  { value: 'introductory', label: 'Introductory' },
  { value: 'rapport_building', label: 'Rapport Building' },
  { value: 'active_engagement', label: 'Active Engagement' },
  { value: 'trusted', label: 'Trusted Relationship' },
  { value: 'strategic', label: 'Strategic Partner' },
];

export function metWithLabel(value?: string) {
  return MET_WITH_OPTIONS.find((o) => o.value === value)?.label || value || '—';
}

export function relationshipStageLabel(value?: string) {
  return RELATIONSHIP_STAGES.find((s) => s.value === value)?.label || value?.replace(/_/g, ' ') || '—';
}

export function meetingTypeLabel(value?: string) {
  if (!value) return 'meeting';
  return value.replace(/_/g, ' ');
}
