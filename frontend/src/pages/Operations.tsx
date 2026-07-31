import { useState } from "react";
import {
  Activity,
  AlertCircle,
  CheckCircle2,
  Clock,
  RefreshCw,
  Settings,
  ShieldAlert,
  Sparkles,
} from "lucide-react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { operationsQueries, outboxQueries } from "../api/queries";
import { apiClient, handleApiResponse } from "../api/client";
import { useToast } from "../components/Toast";
import { StatusBadge } from "../components/StatusBadge";
import {
  DataPanel,
  Table,
  TableHead,
  TableBody,
  Th,
  Tr,
  Td,
} from "../components/DataTable";

const TABS = [
  "Health",
  "Metrics",
  "Source Runs",
  "Source Health",
  "Stranded Records",
  "Audit Log",
  "Config",
  "Outbox",
];

function HealthTab() {
  const { data, isLoading, isError, error } = useQuery(
    operationsQueries.health(),
  );

  if (isLoading)
    return (
      <div className="p-8 text-center text-muted-foreground">
        Checking health...
      </div>
    );
  if (isError || !data)
    return (
      <div className="p-8 text-center text-destructive flex flex-col items-center">
        <AlertCircle className="mb-2" />
        {error instanceof Error ? error.message : "Unknown error"}
      </div>
    );

  const health = data as any;

  return (
    <div className="grid grid-cols-3 gap-4">
      <div className="bg-card border border-border rounded-lg p-6 flex items-center gap-4">
        {health.healthy ? (
          <CheckCircle2 className="text-verified" size={28} />
        ) : (
          <AlertCircle className="text-conflict" size={28} />
        )}
        <div>
          <div className="text-sm text-muted-foreground">Overall</div>
          <div className="text-lg font-semibold">
            {health.healthy ? "Healthy" : "Unhealthy"}
          </div>
        </div>
      </div>
      <div className="bg-card border border-border rounded-lg p-6 flex items-center gap-4">
        {health.database_ok ? (
          <CheckCircle2 className="text-verified" size={28} />
        ) : (
          <AlertCircle className="text-conflict" size={28} />
        )}
        <div>
          <div className="text-sm text-muted-foreground">Database</div>
          <div className="text-lg font-semibold">
            {health.database_ok ? "Connected" : "Unreachable"}
          </div>
        </div>
      </div>
      <div className="bg-card border border-border rounded-lg p-6 flex items-center gap-4">
        <Clock
          className={health.stuck_run_count > 0 ? "text-inference" : "text-verified"}
          size={28}
        />
        <div>
          <div className="text-sm text-muted-foreground">Stuck runs</div>
          <div className="text-lg font-semibold">{health.stuck_run_count}</div>
        </div>
      </div>
      {health.stuck_run_ids?.length > 0 && (
        <div className="col-span-3 bg-card border border-border rounded-lg p-4">
          <div className="text-sm text-muted-foreground mb-2">
            Stuck run IDs
          </div>
          <div className="space-y-1 font-mono text-xs text-foreground">
            {health.stuck_run_ids.map((id: string) => (
              <div key={id}>{id}</div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function MetricsTab() {
  const { data, isLoading, isError, error } = useQuery(
    operationsQueries.metrics(),
  );

  if (isLoading)
    return (
      <div className="p-8 text-center text-muted-foreground">
        Loading metrics...
      </div>
    );
  if (isError || !data)
    return (
      <div className="p-8 text-center text-destructive flex flex-col items-center">
        <AlertCircle className="mb-2" />
        {error instanceof Error ? error.message : "Unknown error"}
      </div>
    );

  const metrics = data as any;
  const stats = [
    { title: "Canonical Leads", value: metrics.total_canonical_institutions },
    { title: "Pending Resolution", value: metrics.pending_resolution_candidates },
    { title: "Drafts to Review", value: metrics.pending_outreach_drafts },
    { title: "Target Accounts", value: metrics.total_target_accounts },
    { title: "Outbox Pending", value: metrics.outbox_pending },
    { title: "Outbox Dead Letter", value: metrics.outbox_dead_letter },
    { title: "Open Data Quality Flags", value: metrics.open_data_quality_flags },
    { title: "Suppressed Contacts", value: metrics.suppressed_contacts },
  ];

  return (
    <div className="grid grid-cols-4 gap-4">
      {stats.map((stat) => (
        <div
          key={stat.title}
          className="bg-card border border-border p-6 rounded-lg shadow-sm"
        >
          <h3 className="text-sm font-medium text-muted-foreground mb-2">
            {stat.title}
          </h3>
          <p className="text-3xl font-semibold">{String(stat.value ?? "0")}</p>
        </div>
      ))}
    </div>
  );
}

const SOURCE_TYPE_OPTIONS = [
  "",
  "google_places",
  "website",
  "telegram",
  "linkedin",
  "yandex",
  "apple_maps",
  "manual",
  "authorized_import",
];
const RUN_STATUS_OPTIONS = ["", "started", "completed", "failed"];

function SourceRunsTab() {
  const [sourceType, setSourceType] = useState("");
  const [status, setStatus] = useState("");
  const [selectedRunId, setSelectedRunId] = useState<string | null>(null);

  const { data: runs, isLoading, isError, error } = useQuery(
    operationsQueries.sourceRuns(sourceType || undefined, status || undefined),
  );
  const { data: detail } = useQuery({
    ...operationsQueries.sourceRunDetail(selectedRunId ?? ""),
    enabled: !!selectedRunId,
  });

  const items = runs ?? [];

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap gap-4 items-center bg-card p-4 rounded-lg border border-border">
        <select
          className="bg-background border border-border rounded-md py-2 px-4 text-sm capitalize"
          value={sourceType}
          onChange={(e) => setSourceType(e.target.value)}
        >
          {SOURCE_TYPE_OPTIONS.map((t) => (
            <option key={t || "all"} value={t} className="capitalize">
              {t ? t.replace(/_/g, " ") : "All sources"}
            </option>
          ))}
        </select>
        <select
          className="bg-background border border-border rounded-md py-2 px-4 text-sm capitalize"
          value={status}
          onChange={(e) => setStatus(e.target.value)}
        >
          {RUN_STATUS_OPTIONS.map((s) => (
            <option key={s || "all"} value={s} className="capitalize">
              {s || "All statuses"}
            </option>
          ))}
        </select>
      </div>

      <DataPanel
        isLoading={isLoading}
        isError={isError}
        error={error}
        isEmpty={items.length === 0}
        loadingLabel="Loading source runs..."
        errorLabel="Error loading source runs"
        emptyLabel="No source runs match these filters."
      >
        <Table>
          <TableHead>
            <Th>Source</Th>
            <Th>Status</Th>
            <Th>Started</Th>
            <Th>Completed</Th>
            <Th align="right">Actions</Th>
          </TableHead>
          <TableBody>
            {items.map((run: any) => (
              <Tr key={run.id}>
                <Td>
                  <span className="capitalize font-medium text-foreground">
                    {run.source_type.replace(/_/g, " ")}
                  </span>
                </Td>
                <Td>
                  <StatusBadge status={run.status} />
                </Td>
                <Td>
                  <span className="text-muted-foreground text-xs">
                    {new Date(run.started_at).toLocaleString()}
                  </span>
                </Td>
                <Td>
                  <span className="text-muted-foreground text-xs">
                    {run.completed_at
                      ? new Date(run.completed_at).toLocaleString()
                      : "-"}
                  </span>
                </Td>
                <Td align="right">
                  <button
                    onClick={() => setSelectedRunId(run.id)}
                    className="inline-flex items-center gap-1 px-3 py-1.5 text-xs font-medium border border-border text-muted-foreground hover:border-primary hover:text-primary rounded-md"
                  >
                    Details
                  </button>
                </Td>
              </Tr>
            ))}
          </TableBody>
        </Table>
      </DataPanel>

      {selectedRunId && (
        <div className="fixed inset-0 z-[110] bg-background/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-card border border-border rounded-xl shadow-lg max-w-2xl w-full p-6 max-h-[80vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-foreground">
                Source run detail
              </h3>
              <button
                onClick={() => setSelectedRunId(null)}
                className="text-muted-foreground hover:text-foreground text-sm"
              >
                Close
              </button>
            </div>
            {!detail ? (
              <div className="text-muted-foreground text-sm">Loading...</div>
            ) : (
              <div className="space-y-4 text-sm">
                <div className="flex items-center gap-3">
                  <StatusBadge status={(detail as any).run.status} />
                  <span className="text-muted-foreground">
                    {(detail as any).record_count} record(s)
                  </span>
                </div>
                <div>
                  <div className="text-xs text-muted-foreground mb-1">
                    Unresolved records
                  </div>
                  <pre className="bg-background border border-border rounded-md p-3 text-xs overflow-x-auto">
                    {JSON.stringify(
                      (detail as any).unresolved_records,
                      null,
                      2,
                    )}
                  </pre>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

function SourceHealthTab() {
  const { data, isLoading, isError, error } = useQuery(
    operationsQueries.sourceHealth(),
  );
  const items = (data as any[]) ?? [];

  return (
    <DataPanel
      isLoading={isLoading}
      isError={isError}
      error={error}
      isEmpty={items.length === 0}
      loadingLabel="Loading source health..."
      errorLabel="Error loading source health"
      emptyLabel="No source runs recorded yet."
    >
      <Table>
        <TableHead>
          <Th>Source</Th>
          <Th>Last run</Th>
          <Th>Last status</Th>
          <Th>Last success</Th>
          <Th align="right">Failures (7d)</Th>
        </TableHead>
        <TableBody>
          {items.map((h) => (
            <Tr key={h.source_type}>
              <Td>
                <span className="capitalize font-medium text-foreground">
                  {h.source_type.replace(/_/g, " ")}
                </span>
              </Td>
              <Td>
                <span className="text-muted-foreground text-xs">
                  {new Date(h.last_run_at).toLocaleString()}
                </span>
              </Td>
              <Td>
                <StatusBadge status={h.last_run_status} />
              </Td>
              <Td>
                <span className="text-muted-foreground text-xs">
                  {h.last_successful_run_at
                    ? new Date(h.last_successful_run_at).toLocaleString()
                    : "Never"}
                </span>
              </Td>
              <Td align="right">
                <span
                  className={
                    h.failed_run_count_last_7d > 0
                      ? "text-conflict font-mono"
                      : "text-muted-foreground font-mono"
                  }
                >
                  {h.failed_run_count_last_7d}
                </span>
              </Td>
            </Tr>
          ))}
        </TableBody>
      </Table>
    </DataPanel>
  );
}

function StrandedRecordsTab() {
  const { data, isLoading, isError, error } = useQuery(
    operationsQueries.strandedRecords(),
  );
  const items = (data as any[]) ?? [];

  return (
    <DataPanel
      isLoading={isLoading}
      isError={isError}
      error={error}
      isEmpty={items.length === 0}
      loadingLabel="Loading stranded records..."
      errorLabel="Error loading stranded records"
      emptyLabel="No stranded records -- every extracted record has been resolved."
    >
      <Table>
        <TableHead>
          <Th>Source</Th>
          <Th>Source ID</Th>
          <Th>Extracted at</Th>
        </TableHead>
        <TableBody>
          {items.map((r) => (
            <Tr key={r.id}>
              <Td>
                <div className="flex items-center gap-2 capitalize font-medium text-foreground">
                  <ShieldAlert size={14} className="text-inference" />
                  {r.source_type.replace(/_/g, " ")}
                </div>
              </Td>
              <Td>
                <span className="text-muted-foreground text-xs font-mono">
                  {r.source_id}
                </span>
              </Td>
              <Td>
                <span className="text-muted-foreground text-xs">
                  {new Date(r.extracted_at).toLocaleString()}
                </span>
              </Td>
            </Tr>
          ))}
        </TableBody>
      </Table>
    </DataPanel>
  );
}

function AuditLogTab() {
  const [entityType, setEntityType] = useState("");
  const [actor, setActor] = useState("");

  const { data, isLoading, isError, error } = useQuery(
    operationsQueries.auditLog(entityType || undefined, actor || undefined),
  );
  const items = (data as any[]) ?? [];

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap gap-4 items-center bg-card p-4 rounded-lg border border-border">
        <input
          type="text"
          placeholder="Entity type"
          className="w-40 bg-background border border-border rounded-md py-2 px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50"
          value={entityType}
          onChange={(e) => setEntityType(e.target.value)}
        />
        <input
          type="text"
          placeholder="Actor"
          className="w-40 bg-background border border-border rounded-md py-2 px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50"
          value={actor}
          onChange={(e) => setActor(e.target.value)}
        />
      </div>

      <DataPanel
        isLoading={isLoading}
        isError={isError}
        error={error}
        isEmpty={items.length === 0}
        loadingLabel="Loading audit log..."
        errorLabel="Error loading audit log"
        emptyLabel="No audit events match these filters."
      >
        <Table>
          <TableHead>
            <Th>Action</Th>
            <Th>Entity</Th>
            <Th>Actor</Th>
            <Th>Timestamp</Th>
          </TableHead>
          <TableBody>
            {items.map((event) => (
              <Tr key={event.id}>
                <Td>
                  <span className="font-medium text-foreground">
                    {event.action}
                  </span>
                  {event.feedback && (
                    <div className="text-xs text-muted-foreground mt-0.5">
                      {event.feedback}
                    </div>
                  )}
                </Td>
                <Td>
                  <div className="text-xs">
                    <span className="capitalize">{event.entity_type}</span>
                    <div className="text-muted-foreground font-mono">
                      {event.entity_id}
                    </div>
                  </div>
                </Td>
                <Td>
                  <span className="text-muted-foreground text-xs">
                    {event.actor}
                  </span>
                </Td>
                <Td>
                  <span className="text-muted-foreground text-xs">
                    {new Date(event.timestamp).toLocaleString()}
                  </span>
                </Td>
              </Tr>
            ))}
          </TableBody>
        </Table>
      </DataPanel>
    </div>
  );
}

function ConfigTab() {
  const { data, isLoading, isError, error } = useQuery(
    operationsQueries.config(),
  );

  if (isLoading)
    return (
      <div className="p-8 text-center text-muted-foreground">
        Loading config...
      </div>
    );
  if (isError || !data)
    return (
      <div className="p-8 text-center text-destructive flex flex-col items-center">
        <AlertCircle className="mb-2" />
        {error instanceof Error ? error.message : "Unknown error"}
      </div>
    );

  const entries = Object.entries(data as Record<string, unknown>);

  return (
    <div className="bg-card border border-border rounded-lg overflow-hidden">
      <div className="px-6 py-3 border-b border-border flex items-center gap-2 text-sm text-muted-foreground">
        <Settings size={15} />
        Read-only, allowlisted configuration
      </div>
      <Table>
        <TableHead>
          <Th>Key</Th>
          <Th>Value</Th>
        </TableHead>
        <TableBody>
          {entries.map(([key, value]) => (
            <Tr key={key}>
              <Td>
                <span className="font-mono text-xs">{key}</span>
              </Td>
              <Td>
                <span className="font-mono text-xs text-muted-foreground">
                  {typeof value === "object"
                    ? JSON.stringify(value)
                    : String(value)}
                </span>
              </Td>
            </Tr>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}

function OutboxTab() {
  const [status, setStatus] = useState("");
  const [processing, setProcessing] = useState(false);
  const queryClient = useQueryClient();
  const { showToast } = useToast();

  const { data, isLoading, isError, error } = useQuery(
    outboxQueries.list(status || undefined),
  );

  const invalidate = () =>
    queryClient.invalidateQueries({ queryKey: ["outbox"] });

  const requeueMutation = useMutation({
    mutationFn: (id: string) =>
      apiClient
        .POST("/api/v1/outbox/{outbox_id}/requeue", {
          params: { path: { outbox_id: id } },
        })
        .then(handleApiResponse),
    onSuccess: () => {
      showToast("Entry requeued.", true);
      invalidate();
    },
    onError: (err: unknown) =>
      showToast(
        `Failed to requeue: ${err instanceof Error ? err.message : "Unknown error"}`,
        false,
      ),
  });

  const processPending = async () => {
    setProcessing(true);
    try {
      const result = await apiClient
        .POST("/api/v1/outbox/process", { params: { query: {} } })
        .then(handleApiResponse);
      showToast(
        `Processed ${(result as any).processed ?? 0} pending deliveries.`,
        true,
      );
      invalidate();
    } catch (err) {
      showToast(
        `Failed to process pending: ${err instanceof Error ? err.message : "Unknown error"}`,
        false,
      );
    } finally {
      setProcessing(false);
    }
  };

  const items = (data as any[]) ?? [];

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex gap-2">
          {["", "pending", "delivered", "failed", "dead_letter"].map((s) => (
            <button
              key={s || "all"}
              onClick={() => setStatus(s)}
              className={`px-3 py-1.5 rounded-full text-xs font-medium border transition-all capitalize ${
                status === s
                  ? "border-primary text-primary bg-primary/10"
                  : "border-border text-muted-foreground hover:border-muted-foreground"
              }`}
            >
              {s ? s.replace(/_/g, " ") : "All"}
            </button>
          ))}
        </div>
        <button
          onClick={processPending}
          disabled={processing}
          className="inline-flex items-center gap-2 px-4 py-2 text-sm font-semibold rounded-md text-primary-foreground bg-primary hover:bg-primary/90 disabled:opacity-50"
        >
          <Sparkles size={16} />
          {processing ? "Processing..." : "Process Pending"}
        </button>
      </div>

      <DataPanel
        isLoading={isLoading}
        isError={isError}
        error={error}
        isEmpty={items.length === 0}
        loadingLabel="Loading outbox..."
        errorLabel="Error loading outbox"
        emptyLabel="No outbox entries match these filters."
      >
        <Table>
          <TableHead>
            <Th>Event</Th>
            <Th>Status</Th>
            <Th>Attempts</Th>
            <Th>Next attempt</Th>
            <Th>Last error</Th>
            <Th align="right">Actions</Th>
          </TableHead>
          <TableBody>
            {items.map((entry) => (
              <Tr key={entry.id}>
                <Td>
                  <span className="font-medium text-foreground">
                    {entry.event_type}
                  </span>
                  <div className="text-xs text-muted-foreground font-mono">
                    {entry.institution_id}
                  </div>
                </Td>
                <Td>
                  <StatusBadge status={entry.status} />
                </Td>
                <Td>
                  <span className="font-mono">{entry.attempt_count}</span>
                </Td>
                <Td>
                  <span className="text-muted-foreground text-xs">
                    {new Date(entry.next_attempt_at).toLocaleString()}
                  </span>
                </Td>
                <Td>
                  <span className="text-conflict text-xs line-clamp-1 max-w-xs">
                    {entry.last_error || "-"}
                  </span>
                </Td>
                <Td align="right">
                  {entry.status === "dead_letter" && (
                    <button
                      onClick={() => requeueMutation.mutate(entry.id)}
                      disabled={requeueMutation.isPending}
                      className="inline-flex items-center gap-1 px-3 py-1.5 text-xs font-medium rounded-md text-primary-foreground bg-primary hover:bg-primary/90 disabled:opacity-50"
                    >
                      <RefreshCw size={13} />
                      Requeue
                    </button>
                  )}
                </Td>
              </Tr>
            ))}
          </TableBody>
        </Table>
      </DataPanel>
    </div>
  );
}

export function Operations() {
  const [tab, setTab] = useState("Health");

  const renderTab = () => {
    switch (tab) {
      case "Health":
        return <HealthTab />;
      case "Metrics":
        return <MetricsTab />;
      case "Source Runs":
        return <SourceRunsTab />;
      case "Source Health":
        return <SourceHealthTab />;
      case "Stranded Records":
        return <StrandedRecordsTab />;
      case "Audit Log":
        return <AuditLogTab />;
      case "Config":
        return <ConfigTab />;
      case "Outbox":
        return <OutboxTab />;
      default:
        return null;
    }
  };

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      <div>
        <h2 className="text-3xl font-bold tracking-tight text-foreground flex items-center gap-3">
          <Activity className="text-primary" size={28} />
          Operations
        </h2>
        <p className="text-muted-foreground mt-1">
          System health, pipeline metrics, source runs, and delivery
          internals.
        </p>
      </div>

      <div className="border-b border-border">
        <nav className="flex space-x-6 overflow-x-auto">
          {TABS.map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`py-4 px-1 border-b-2 font-medium text-sm whitespace-nowrap transition-colors ${
                tab === t
                  ? "border-primary text-primary"
                  : "border-transparent text-muted-foreground hover:text-foreground hover:border-border"
              }`}
            >
              {t}
            </button>
          ))}
        </nav>
      </div>

      <div>{renderTab()}</div>
    </div>
  );
}
