// Maps every status/enum value returned by the backend to one of the six
// semantic tokens defined in index.css (verified/inference/hypothesis/
// conflict/stale/approved) -- most of those tokens were defined but unused
// until the compliance/verification/daily-selection/outbox pages needed
// them. Falls back to a neutral muted badge for anything unmapped so a
// backend enum this doesn't know about yet, rather than crashing.
const STATUS_STYLES: Record<string, string> = {
  // Compliance: SuppressionReason / DeletionRequestStatus
  opt_out: "bg-conflict/10 text-conflict",
  bounced: "bg-conflict/10 text-conflict",
  legal_request: "bg-conflict/10 text-conflict",
  manual: "bg-stale/10 text-stale",
  pending: "bg-inference/10 text-inference",
  completed: "bg-verified/10 text-verified",
  rejected: "bg-conflict/10 text-conflict",

  // Daily Selection: ReservationStatus
  reserved: "bg-approved/10 text-approved",
  consumed: "bg-verified/10 text-verified",
  expired: "bg-stale/10 text-stale",
  released: "bg-stale/10 text-stale",

  // Verification: FlagStatus / FlagType
  open: "bg-inference/10 text-inference",
  resolved: "bg-verified/10 text-verified",
  dismissed: "bg-stale/10 text-stale",
  confidence_drift: "bg-hypothesis/10 text-hypothesis",
  conflicting_field: "bg-conflict/10 text-conflict",
  stale_evidence: "bg-stale/10 text-stale",
  unreachable_contact: "bg-conflict/10 text-conflict",

  // Event Outbox: OutboxStatus
  delivered: "bg-verified/10 text-verified",
  failed: "bg-conflict/10 text-conflict",
  dead_letter: "bg-conflict/10 text-conflict",

  // Qualification / Operating status (reused across Institutions/Lead Profiles)
  qualified: "bg-verified/10 text-verified",
  disqualified: "bg-conflict/10 text-conflict",
  needs_review: "bg-inference/10 text-inference",
  operational: "bg-verified/10 text-verified",
  closed_temporarily: "bg-inference/10 text-inference",
  closed_permanently: "bg-conflict/10 text-conflict",
  unknown: "bg-stale/10 text-stale",
};

interface StatusBadgeProps {
  status: string;
  label?: string;
}

export function StatusBadge({ status, label }: StatusBadgeProps) {
  const classes = STATUS_STYLES[status] ?? "bg-muted text-muted-foreground";
  const text = label ?? status.replace(/_/g, " ");
  return (
    <span
      className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium capitalize whitespace-nowrap ${classes}`}
    >
      {text}
    </span>
  );
}
