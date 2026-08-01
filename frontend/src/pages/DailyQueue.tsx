import { useState } from "react";
import { Link } from "react-router";
import { Sparkles, Clock, CheckCircle2, XCircle } from "lucide-react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { dailySelectionQueries } from "../api/queries";
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

const STATUS_OPTIONS = ["", "reserved", "consumed", "expired", "released"];

export function DailyQueue() {
  const [status, setStatus] = useState("");
  const [limit, setLimit] = useState(25);
  const [minScore, setMinScore] = useState<number | undefined>(undefined);
  const [batchLabel, setBatchLabel] = useState("");
  const queryClient = useQueryClient();
  const { showToast } = useToast();

  const {
    data: reservations,
    isLoading,
    isError,
    error,
  } = useQuery(dailySelectionQueries.list(status || undefined));

  const invalidateList = () =>
    queryClient.invalidateQueries({ queryKey: ["daily-selection"] });

  const selectBatchMutation = useMutation({
    mutationFn: () =>
      apiClient
        .POST("/api/v1/daily-selection", {
          body: {
            limit,
            min_score: minScore ?? null,
            batch_label: batchLabel || null,
          },
        })
        .then(handleApiResponse),
    onSuccess: (data: any) => {
      showToast(`Selected ${data.length} lead(s) for today's batch.`, true);
      invalidateList();
    },
    onError: (err: unknown) =>
      showToast(
        `Failed to select batch: ${err instanceof Error ? err.message : "Unknown error"}`,
        false,
      ),
  });

  const consumeMutation = useMutation({
    mutationFn: (reservationId: string) =>
      apiClient
        .POST("/api/v1/daily-selection/{reservation_id}/consume", {
          params: { path: { reservation_id: reservationId } },
        })
        .then(handleApiResponse),
    onSuccess: () => {
      showToast("Reservation marked consumed.", true);
      invalidateList();
    },
    onError: (err: unknown) =>
      showToast(
        `Failed to consume: ${err instanceof Error ? err.message : "Unknown error"}`,
        false,
      ),
  });

  const releaseMutation = useMutation({
    mutationFn: (reservationId: string) =>
      apiClient
        .POST("/api/v1/daily-selection/{reservation_id}/release", {
          params: { path: { reservation_id: reservationId } },
        })
        .then(handleApiResponse),
    onSuccess: () => {
      showToast("Reservation released.", true);
      invalidateList();
    },
    onError: (err: unknown) =>
      showToast(
        `Failed to release: ${err instanceof Error ? err.message : "Unknown error"}`,
        false,
      ),
  });

  const items = reservations ?? [];

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold tracking-tight text-foreground">
            Daily Queue
          </h2>
          <p className="text-muted-foreground mt-1">
            Claim today's highest-scoring eligible leads for outreach.
          </p>
        </div>
      </div>

      {/* Select batch */}
      <div className="bg-card p-4 rounded-lg border border-border flex flex-wrap items-end gap-4">
        <div>
          <label className="block text-xs text-muted-foreground mb-1">
            Limit
          </label>
          <input
            type="number"
            min={1}
            className="w-24 bg-background border border-border rounded-md py-2 px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50"
            value={limit}
            onChange={(e) => setLimit(Number(e.target.value) || 25)}
          />
        </div>
        <div>
          <label className="block text-xs text-muted-foreground mb-1">
            Minimum score
          </label>
          <input
            type="number"
            min={0}
            max={100}
            placeholder="0"
            className="w-28 bg-background border border-border rounded-md py-2 px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50"
            value={minScore ?? ""}
            onChange={(e) =>
              setMinScore(e.target.value ? Number(e.target.value) : undefined)
            }
          />
        </div>
        <div className="flex-1 min-w-[180px]">
          <label className="block text-xs text-muted-foreground mb-1">
            Batch label
          </label>
          <input
            type="text"
            placeholder="e.g. 2026-07-31-morning"
            className="w-full bg-background border border-border rounded-md py-2 px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50"
            value={batchLabel}
            onChange={(e) => setBatchLabel(e.target.value)}
          />
        </div>
        <button
          onClick={() => selectBatchMutation.mutate()}
          disabled={selectBatchMutation.isPending}
          className="inline-flex items-center gap-2 px-4 py-2 text-sm font-semibold rounded-md text-primary-foreground bg-primary hover:bg-primary/90 disabled:opacity-50"
        >
          <Sparkles size={16} />
          {selectBatchMutation.isPending
            ? "Selecting..."
            : "Select Today's Batch"}
        </button>
      </div>

      {/* Status filter */}
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
            {s || "All"}
          </button>
        ))}
      </div>

      <DataPanel
        isLoading={isLoading}
        isError={isError}
        error={error}
        isEmpty={items.length === 0}
        loadingLabel="Loading reservations..."
        errorLabel="Error loading reservations"
        emptyLabel="No reservations yet -- select today's batch above."
      >
        <Table>
          <TableHead>
            <Th>Institution</Th>
            <Th>Status</Th>
            <Th>Score</Th>
            <Th>Batch</Th>
            <Th>Expires</Th>
            <Th align="right">Actions</Th>
          </TableHead>
          <TableBody>
            {items.map((res: any) => (
              <Tr key={res.id}>
                <Td>
                  <Link
                    to={`/institutions/${res.institution_id}`}
                    className="font-medium text-foreground hover:text-primary transition-colors"
                  >
                    {res.canonical_name}
                  </Link>
                </Td>
                <Td>
                  <StatusBadge status={res.status} />
                </Td>
                <Td>
                  <span className="font-mono">{res.score_at_reservation}</span>
                </Td>
                <Td>
                  <span className="text-muted-foreground text-xs">
                    {res.batch_label || "-"}
                  </span>
                </Td>
                <Td>
                  <div className="flex items-center gap-2 text-muted-foreground text-xs">
                    <Clock size={13} />
                    {new Date(res.expires_at).toLocaleString()}
                  </div>
                </Td>
                <Td align="right">
                  {res.status === "reserved" && (
                    <div className="flex justify-end gap-2">
                      <button
                        onClick={() => releaseMutation.mutate(res.id)}
                        disabled={releaseMutation.isPending}
                        className="inline-flex items-center gap-1 px-3 py-1.5 text-xs font-medium border border-border text-muted-foreground hover:border-destructive hover:text-destructive rounded-md disabled:opacity-50"
                      >
                        <XCircle size={13} />
                        Release
                      </button>
                      <button
                        onClick={() => consumeMutation.mutate(res.id)}
                        disabled={consumeMutation.isPending}
                        className="inline-flex items-center gap-1 px-3 py-1.5 text-xs font-medium rounded-md text-primary-foreground bg-primary hover:bg-primary/90 disabled:opacity-50"
                      >
                        <CheckCircle2 size={13} />
                        Consume
                      </button>
                    </div>
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
