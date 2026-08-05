import { useState } from "react";
import { ShieldOff, Trash2, CheckCircle2, XCircle, Plus } from "lucide-react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { complianceQueries } from "../api/queries";
import { apiClient, handleApiResponse } from "../api/client";
import { useToast } from "../components/Toast";
import { StatusBadge } from "../components/StatusBadge";
import { ConfirmDialog } from "../components/ConfirmDialog";
import {
  DataPanel,
  Table,
  TableHead,
  TableBody,
  Th,
  Tr,
  Td,
} from "../components/DataTable";

const SUPPRESSION_REASONS = ["opt_out", "bounced", "legal_request", "manual"];
const DELETION_STATUS_OPTIONS = ["", "pending", "completed", "rejected"];

function SuppressionsTab() {
  const [showForm, setShowForm] = useState(false);
  const [contactValue, setContactValue] = useState("");
  const [reason, setReason] = useState("opt_out");
  const [channel, setChannel] = useState("");
  const [note, setNote] = useState("");
  const [deleteId, setDeleteId] = useState<string | null>(null);

  const queryClient = useQueryClient();
  const { showToast } = useToast();

  const {
    data: suppressions,
    isLoading,
    isError,
    error,
  } = useQuery(complianceQueries.suppressions());

  const invalidate = () =>
    queryClient.invalidateQueries({ queryKey: ["compliance", "suppressions"] });

  const addMutation = useMutation({
    mutationFn: () =>
      apiClient
        .POST("/api/v1/compliance/suppressions", {
          body: {
            contact_value: contactValue,
            reason: reason as any,
            channel: channel || null,
            note,
            suppressed_by: "Dev Admin",
          },
        })
        .then(handleApiResponse),
    onSuccess: () => {
      showToast("Suppression added.", true);
      setShowForm(false);
      setContactValue("");
      setChannel("");
      setNote("");
      invalidate();
    },
    onError: (err: unknown) =>
      showToast(
        `Failed to add suppression: ${err instanceof Error ? err.message : "Unknown error"}`,
        false,
      ),
  });

  const deleteMutation = useMutation({
    mutationFn: (id: string) =>
      apiClient
        .DELETE("/api/v1/compliance/suppressions/{suppression_id}", {
          params: { path: { suppression_id: id } },
        })
        .then(handleApiResponse),
    onSuccess: () => {
      showToast("Suppression removed.", true);
      setDeleteId(null);
      invalidate();
    },
    onError: (err: unknown) =>
      showToast(
        `Failed to remove suppression: ${err instanceof Error ? err.message : "Unknown error"}`,
        false,
      ),
  });

  const items = suppressions ?? [];

  return (
    <div className="space-y-6">
      <div className="flex justify-end">
        <button
          onClick={() => setShowForm((v) => !v)}
          className="inline-flex items-center gap-2 px-4 py-2 text-sm font-semibold rounded-md text-primary-foreground bg-primary hover:bg-primary/90"
        >
          <Plus size={16} />
          Add Suppression
        </button>
      </div>

      {showForm && (
        <div className="bg-card p-4 rounded-lg border border-border flex flex-wrap items-end gap-4">
          <div className="flex-1 min-w-[200px]">
            <label className="block text-xs text-muted-foreground mb-1">
              Contact value
            </label>
            <input
              type="text"
              placeholder="phone, email, etc."
              className="w-full bg-background border border-border rounded-md py-2 px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50"
              value={contactValue}
              onChange={(e) => setContactValue(e.target.value)}
            />
          </div>
          <div>
            <label className="block text-xs text-muted-foreground mb-1">
              Reason
            </label>
            <select
              className="bg-background border border-border rounded-md py-2 px-4 text-sm capitalize"
              value={reason}
              onChange={(e) => setReason(e.target.value)}
            >
              {SUPPRESSION_REASONS.map((r) => (
                <option key={r} value={r} className="capitalize">
                  {r.replace(/_/g, " ")}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-xs text-muted-foreground mb-1">
              Channel (optional)
            </label>
            <input
              type="text"
              placeholder="phone / email"
              className="w-36 bg-background border border-border rounded-md py-2 px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50"
              value={channel}
              onChange={(e) => setChannel(e.target.value)}
            />
          </div>
          <div className="flex-1 min-w-[200px]">
            <label className="block text-xs text-muted-foreground mb-1">
              Note
            </label>
            <input
              type="text"
              className="w-full bg-background border border-border rounded-md py-2 px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50"
              value={note}
              onChange={(e) => setNote(e.target.value)}
            />
          </div>
          <button
            onClick={() => addMutation.mutate()}
            disabled={!contactValue || addMutation.isPending}
            className="inline-flex items-center gap-2 px-4 py-2 text-sm font-semibold rounded-md text-primary-foreground bg-primary hover:bg-primary/90 disabled:opacity-50"
          >
            {addMutation.isPending ? "Saving..." : "Save"}
          </button>
        </div>
      )}

      <DataPanel
        isLoading={isLoading}
        isError={isError}
        error={error}
        isEmpty={items.length === 0}
        loadingLabel="Loading suppressions..."
        errorLabel="Error loading suppressions"
        emptyLabel="No suppressed contacts."
      >
        <Table>
          <TableHead>
            <Th>Contact</Th>
            <Th>Reason</Th>
            <Th>Channel</Th>
            <Th>Suppressed by</Th>
            <Th>Suppressed at</Th>
            <Th align="right">Actions</Th>
          </TableHead>
          <TableBody>
            {items.map((s: any) => (
              <Tr key={s.id}>
                <Td>
                  <div className="flex items-center gap-2 font-medium text-foreground">
                    <ShieldOff size={15} className="text-muted-foreground" />
                    {s.normalized_contact_value}
                  </div>
                </Td>
                <Td>
                  <StatusBadge status={s.reason} />
                </Td>
                <Td>
                  <span className="text-muted-foreground text-xs">
                    {s.channel || "-"}
                  </span>
                </Td>
                <Td>
                  <span className="text-muted-foreground text-xs">
                    {s.suppressed_by}
                  </span>
                </Td>
                <Td>
                  <span className="text-muted-foreground text-xs">
                    {new Date(s.suppressed_at).toLocaleString()}
                  </span>
                </Td>
                <Td align="right">
                  <button
                    onClick={() => setDeleteId(s.id)}
                    className="inline-flex items-center gap-1 px-3 py-1.5 text-xs font-medium border border-border text-muted-foreground hover:border-destructive hover:text-destructive rounded-md"
                  >
                    <Trash2 size={13} />
                    Remove
                  </button>
                </Td>
              </Tr>
            ))}
          </TableBody>
        </Table>
      </DataPanel>

      <ConfirmDialog
        open={deleteId !== null}
        title="Remove suppression"
        description="This contact will become reachable again by outreach. This cannot be undone from here."
        confirmLabel="Remove"
        onConfirm={() => deleteId && deleteMutation.mutate(deleteId)}
        onCancel={() => setDeleteId(null)}
      />
    </div>
  );
}

function DeletionRequestsTab() {
  const [status, setStatus] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [subjectType, setSubjectType] = useState<
    "institution" | "contact_point"
  >("institution");
  const [subjectId, setSubjectId] = useState("");
  const [note, setNote] = useState("");
  const [fulfillId, setFulfillId] = useState<string | null>(null);
  const [rejectId, setRejectId] = useState<string | null>(null);
  const [rejectReason, setRejectReason] = useState("");

  const queryClient = useQueryClient();
  const { showToast } = useToast();

  const {
    data: requests,
    isLoading,
    isError,
    error,
  } = useQuery(complianceQueries.deletionRequests(status || undefined));

  const invalidate = () =>
    queryClient.invalidateQueries({
      queryKey: ["compliance", "deletion-requests"],
    });

  const createMutation = useMutation({
    mutationFn: () =>
      apiClient
        .POST("/api/v1/compliance/deletion-requests", {
          body: { subject_type: subjectType, subject_id: subjectId, note },
        })
        .then(handleApiResponse),
    onSuccess: () => {
      showToast("Deletion request recorded.", true);
      setShowForm(false);
      setSubjectId("");
      setNote("");
      invalidate();
    },
    onError: (err: unknown) =>
      showToast(
        `Failed to create request: ${err instanceof Error ? err.message : "Unknown error"}`,
        false,
      ),
  });

  const fulfillMutation = useMutation({
    mutationFn: (id: string) =>
      apiClient
        .POST("/api/v1/compliance/deletion-requests/{request_id}/fulfill", {
          params: { path: { request_id: id } },
        })
        .then(handleApiResponse),
    onSuccess: () => {
      showToast("Deletion request fulfilled -- subject data erased.", true);
      setFulfillId(null);
      invalidate();
    },
    onError: (err: unknown) =>
      showToast(
        `Failed to fulfill request: ${err instanceof Error ? err.message : "Unknown error"}`,
        false,
      ),
  });

  const rejectMutation = useMutation({
    mutationFn: () =>
      apiClient
        .POST("/api/v1/compliance/deletion-requests/{request_id}/reject", {
          params: { path: { request_id: rejectId! } },
          body: { reason: rejectReason },
        })
        .then(handleApiResponse),
    onSuccess: () => {
      showToast("Deletion request rejected.", true);
      setRejectId(null);
      setRejectReason("");
      invalidate();
    },
    onError: (err: unknown) =>
      showToast(
        `Failed to reject request: ${err instanceof Error ? err.message : "Unknown error"}`,
        false,
      ),
  });

  const items = requests ?? [];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex gap-2">
          {DELETION_STATUS_OPTIONS.map((s) => (
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
        <button
          onClick={() => setShowForm((v) => !v)}
          className="inline-flex items-center gap-2 px-4 py-2 text-sm font-semibold rounded-md text-primary-foreground bg-primary hover:bg-primary/90"
        >
          <Plus size={16} />
          New Request
        </button>
      </div>

      {showForm && (
        <div className="bg-card p-4 rounded-lg border border-border flex flex-wrap items-end gap-4">
          <div>
            <label className="block text-xs text-muted-foreground mb-1">
              Subject type
            </label>
            <select
              className="bg-background border border-border rounded-md py-2 px-4 text-sm capitalize"
              value={subjectType}
              onChange={(e) => setSubjectType(e.target.value as any)}
            >
              <option value="institution">Institution</option>
              <option value="contact_point">Contact point</option>
            </select>
          </div>
          <div className="flex-1 min-w-[240px]">
            <label className="block text-xs text-muted-foreground mb-1">
              Subject ID
            </label>
            <input
              type="text"
              placeholder="uuid"
              className="w-full bg-background border border-border rounded-md py-2 px-3 text-sm font-mono focus:outline-none focus:ring-2 focus:ring-primary/50"
              value={subjectId}
              onChange={(e) => setSubjectId(e.target.value)}
            />
          </div>
          <div className="flex-1 min-w-[200px]">
            <label className="block text-xs text-muted-foreground mb-1">
              Note
            </label>
            <input
              type="text"
              className="w-full bg-background border border-border rounded-md py-2 px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50"
              value={note}
              onChange={(e) => setNote(e.target.value)}
            />
          </div>
          <button
            onClick={() => createMutation.mutate()}
            disabled={!subjectId || createMutation.isPending}
            className="inline-flex items-center gap-2 px-4 py-2 text-sm font-semibold rounded-md text-primary-foreground bg-primary hover:bg-primary/90 disabled:opacity-50"
          >
            {createMutation.isPending ? "Saving..." : "Save"}
          </button>
        </div>
      )}

      <DataPanel
        isLoading={isLoading}
        isError={isError}
        error={error}
        isEmpty={items.length === 0}
        loadingLabel="Loading deletion requests..."
        errorLabel="Error loading deletion requests"
        emptyLabel="No deletion requests match these filters."
      >
        <Table>
          <TableHead>
            <Th>Subject</Th>
            <Th>Status</Th>
            <Th>Note</Th>
            <Th>Requested at</Th>
            <Th align="right">Actions</Th>
          </TableHead>
          <TableBody>
            {items.map((r: any) => (
              <Tr key={r.id}>
                <Td>
                  <div className="font-medium text-foreground capitalize">
                    {r.subject_type.replace(/_/g, " ")}
                  </div>
                  <div className="text-xs text-muted-foreground font-mono">
                    {r.subject_id}
                  </div>
                </Td>
                <Td>
                  <StatusBadge status={r.status} />
                </Td>
                <Td>
                  <span className="text-muted-foreground text-xs">
                    {r.status === "rejected"
                      ? r.rejection_reason
                      : r.requestor_note || "-"}
                  </span>
                </Td>
                <Td>
                  <span className="text-muted-foreground text-xs">
                    {new Date(r.requested_at).toLocaleString()}
                  </span>
                </Td>
                <Td align="right">
                  {r.status === "pending" && (
                    <div className="flex justify-end gap-2">
                      <button
                        onClick={() => setRejectId(r.id)}
                        className="inline-flex items-center gap-1 px-3 py-1.5 text-xs font-medium border border-border text-muted-foreground hover:border-destructive hover:text-destructive rounded-md"
                      >
                        <XCircle size={13} />
                        Reject
                      </button>
                      <button
                        onClick={() => setFulfillId(r.id)}
                        className="inline-flex items-center gap-1 px-3 py-1.5 text-xs font-medium rounded-md text-destructive-foreground bg-destructive hover:bg-destructive/90"
                      >
                        <CheckCircle2 size={13} />
                        Fulfill
                      </button>
                    </div>
                  )}
                </Td>
              </Tr>
            ))}
          </TableBody>
        </Table>
      </DataPanel>

      <ConfirmDialog
        open={fulfillId !== null}
        title="Fulfill deletion request"
        description="This permanently erases the subject's data. This action is irreversible."
        confirmLabel="Erase permanently"
        onConfirm={() => fulfillId && fulfillMutation.mutate(fulfillId)}
        onCancel={() => setFulfillId(null)}
      />

      {rejectId && (
        <div className="fixed inset-0 z-[110] bg-background/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-card border border-border rounded-xl shadow-lg max-w-md w-full p-6 animate-in fade-in zoom-in-95 duration-200">
            <h3 className="text-lg font-semibold text-foreground mb-4">
              Reject deletion request
            </h3>
            <textarea
              placeholder="Reason..."
              className="w-full bg-background border border-border rounded-md p-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50 mb-4"
              rows={3}
              value={rejectReason}
              onChange={(e) => setRejectReason(e.target.value)}
            />
            <div className="flex justify-end gap-3">
              <button
                onClick={() => {
                  setRejectId(null);
                  setRejectReason("");
                }}
                className="inline-flex items-center justify-center px-4 py-2 text-sm font-medium rounded-md bg-secondary text-secondary-foreground hover:bg-secondary/80"
              >
                Cancel
              </button>
              <button
                onClick={() => rejectMutation.mutate()}
                disabled={!rejectReason || rejectMutation.isPending}
                className="inline-flex items-center justify-center px-4 py-2 text-sm font-medium rounded-md text-primary-foreground bg-primary hover:bg-primary/90 disabled:opacity-50"
              >
                {rejectMutation.isPending ? "Saving..." : "Reject"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export function Compliance() {
  const [tab, setTab] = useState<"suppressions" | "deletions">("suppressions");

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      <div>
        <h2 className="text-3xl font-bold tracking-tight text-foreground">
          Compliance
        </h2>
        <p className="text-muted-foreground mt-1">
          Contact suppressions and data-subject deletion requests.
        </p>
      </div>

      <div className="border-b border-border">
        <nav className="flex space-x-8">
          {[
            { key: "suppressions", label: "Suppressions" },
            { key: "deletions", label: "Deletion Requests" },
          ].map((t) => (
            <button
              key={t.key}
              onClick={() => setTab(t.key as any)}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                tab === t.key
                  ? "border-primary text-primary"
                  : "border-transparent text-muted-foreground hover:text-foreground hover:border-border"
              }`}
            >
              {t.label}
            </button>
          ))}
        </nav>
      </div>

      {tab === "suppressions" ? <SuppressionsTab /> : <DeletionRequestsTab />}
    </div>
  );
}
