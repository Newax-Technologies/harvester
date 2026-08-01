import { useState } from "react";
import { Link } from "react-router";
import {
  ShieldAlert,
  CheckCircle2,
  XCircle,
  Sparkles,
  Clock,
} from "lucide-react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { verificationQueries } from "../api/queries";
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

const STATUS_OPTIONS = ["", "open", "resolved", "dismissed"];
const TYPE_OPTIONS = [
  "",
  "confidence_drift",
  "conflicting_field",
  "stale_evidence",
  "unreachable_contact",
];

interface PendingAction {
  flagId: string;
  action: "resolve" | "dismiss";
}

export function DataQuality() {
  const [status, setStatus] = useState("open");
  const [flagType, setFlagType] = useState("");
  const [note, setNote] = useState("");
  const [pending, setPending] = useState<PendingAction | null>(null);
  const [sweeping, setSweeping] = useState(false);

  const queryClient = useQueryClient();
  const { showToast } = useToast();

  const {
    data: flags,
    isLoading,
    isError,
    error,
  } = useQuery(
    verificationQueries.flags(status || undefined, flagType || undefined),
  );

  const invalidateFlags = () =>
    queryClient.invalidateQueries({ queryKey: ["verification", "flags"] });

  const actionMutation = useMutation({
    mutationFn: ({ flagId, action }: PendingAction) => {
      const request =
        action === "resolve"
          ? apiClient.POST("/api/v1/verification/flags/{flag_id}/resolve", {
              params: { path: { flag_id: flagId } },
              body: { note },
            })
          : apiClient.POST("/api/v1/verification/flags/{flag_id}/dismiss", {
              params: { path: { flag_id: flagId } },
              body: { note },
            });
      return request.then(handleApiResponse);
    },
    onSuccess: (_data, variables) => {
      showToast(
        `Flag ${variables.action === "resolve" ? "resolved" : "dismissed"}.`,
        true,
      );
      setPending(null);
      setNote("");
      invalidateFlags();
    },
    onError: (err: unknown) =>
      showToast(
        `Failed to update flag: ${err instanceof Error ? err.message : "Unknown error"}`,
        false,
      ),
  });

  const runSweep = async () => {
    setSweeping(true);
    try {
      const result = await apiClient
        .POST("/api/v1/verification/sweep", { body: {} })
        .then(handleApiResponse);
      showToast(
        `Sweep complete -- ${(result as any).flags_created} flag(s) created.`,
        true,
      );
      invalidateFlags();
    } catch (err) {
      showToast(
        `Sweep failed: ${err instanceof Error ? err.message : "Unknown error"}`,
        false,
      );
    } finally {
      setSweeping(false);
    }
  };

  const items = flags ?? [];

  return (
    <div className="space-y-6 max-w-6xl mx-auto relative">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold tracking-tight text-foreground">
            Data Quality
          </h2>
          <p className="text-muted-foreground mt-1">
            Confidence drift, conflicting evidence, and stale/unreachable
            contacts, flagged for review.
          </p>
        </div>
        <button
          onClick={runSweep}
          disabled={sweeping}
          className="inline-flex items-center gap-2 px-4 py-2 text-sm font-semibold rounded-md text-primary-foreground bg-primary hover:bg-primary/90 disabled:opacity-50"
        >
          <Sparkles size={16} />
          {sweeping ? "Running sweep..." : "Run Sweep"}
        </button>
      </div>

      <div className="flex flex-wrap gap-4 items-center bg-card p-4 rounded-lg border border-border">
        <div className="flex gap-2">
          {STATUS_OPTIONS.map((s) => (
            <button
              key={s || "all"}
              onClick={() => setStatus(s)}
              className={`px-3 py-1.5 rounded-full text-xs font-medium border transition-all capitalize ${
                status === s
                  ? "border-primary text-primary bg-primary/10"
                  : "border-border text-muted-foreground hover:border-muted-foreground"
              }`}
            >
              {s || "All statuses"}
            </button>
          ))}
        </div>
        <select
          className="bg-background border border-border rounded-md py-2 px-4 text-sm capitalize"
          value={flagType}
          onChange={(e) => setFlagType(e.target.value)}
        >
          <option value="">All types</option>
          {TYPE_OPTIONS.filter(Boolean).map((t) => (
            <option key={t} value={t} className="capitalize">
              {t.replace(/_/g, " ")}
            </option>
          ))}
        </select>
      </div>

      <DataPanel
        isLoading={isLoading}
        isError={isError}
        error={error}
        isEmpty={items.length === 0}
        loadingLabel="Loading data quality flags..."
        errorLabel="Error loading flags"
        emptyLabel="No flags match these filters."
      >
        <Table>
          <TableHead>
            <Th>Institution</Th>
            <Th>Type</Th>
            <Th>Status</Th>
            <Th>Detected</Th>
            <Th align="right">Actions</Th>
          </TableHead>
          <TableBody>
            {items.map((flag: any) => (
              <Tr key={flag.id}>
                <Td>
                  <Link
                    to={`/institutions/${flag.institution_id}`}
                    className="font-medium text-foreground hover:text-primary transition-colors inline-flex items-center gap-2"
                  >
                    <ShieldAlert size={15} className="text-muted-foreground" />
                    {flag.field_name || flag.institution_id}
                  </Link>
                </Td>
                <Td>
                  <StatusBadge status={flag.flag_type} />
                </Td>
                <Td>
                  <StatusBadge status={flag.status} />
                </Td>
                <Td>
                  <div className="flex items-center gap-2 text-muted-foreground text-xs">
                    <Clock size={13} />
                    {new Date(flag.detected_at).toLocaleString()}
                  </div>
                </Td>
                <Td align="right">
                  {flag.status === "open" && (
                    <div className="flex justify-end gap-2">
                      <button
                        onClick={() =>
                          setPending({ flagId: flag.id, action: "dismiss" })
                        }
                        className="inline-flex items-center gap-1 px-3 py-1.5 text-xs font-medium border border-border text-muted-foreground hover:border-destructive hover:text-destructive rounded-md"
                      >
                        <XCircle size={13} />
                        Dismiss
                      </button>
                      <button
                        onClick={() =>
                          setPending({ flagId: flag.id, action: "resolve" })
                        }
                        className="inline-flex items-center gap-1 px-3 py-1.5 text-xs font-medium rounded-md text-primary-foreground bg-primary hover:bg-primary/90"
                      >
                        <CheckCircle2 size={13} />
                        Resolve
                      </button>
                    </div>
                  )}
                </Td>
              </Tr>
            ))}
          </TableBody>
        </Table>
      </DataPanel>

      {pending && (
        <div className="fixed inset-0 z-[110] bg-background/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-card border border-border rounded-xl shadow-lg max-w-md w-full p-6 animate-in fade-in zoom-in-95 duration-200">
            <h3 className="text-lg font-semibold text-foreground mb-4 capitalize">
              {pending.action} flag
            </h3>
            <textarea
              placeholder="Note (optional)..."
              className="w-full bg-background border border-border rounded-md p-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50 mb-4"
              rows={3}
              value={note}
              onChange={(e) => setNote(e.target.value)}
            />
            <div className="flex justify-end gap-3">
              <button
                onClick={() => {
                  setPending(null);
                  setNote("");
                }}
                className="inline-flex items-center justify-center px-4 py-2 text-sm font-medium rounded-md bg-secondary text-secondary-foreground hover:bg-secondary/80"
              >
                Cancel
              </button>
              <button
                onClick={() => actionMutation.mutate(pending)}
                disabled={actionMutation.isPending}
                className="inline-flex items-center justify-center px-4 py-2 text-sm font-medium rounded-md text-primary-foreground bg-primary hover:bg-primary/90 disabled:opacity-50 capitalize"
              >
                {actionMutation.isPending ? "Saving..." : pending.action}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
