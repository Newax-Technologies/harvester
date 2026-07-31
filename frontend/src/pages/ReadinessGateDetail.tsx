import { useState, useEffect } from "react";
import { useParams, Link, useNavigate } from "react-router";
import {
  ArrowLeft,
  Save,
  CheckCircle,
  XCircle,
  AlertCircle,
} from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import { draftQueries } from "../api/queries";
import { apiClient, handleApiResponse } from "../api/client";
import { useVersionedMutation } from "../hooks/useVersionedMutation";
import { ConflictModal } from "../components/ConflictModal";

export function ReadinessGateDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const {
    data: draft,
    isLoading,
    isError,
    error,
  } = useQuery(draftQueries.detail(id!));

  const [draftBody, setDraftBody] = useState("");
  const [feedback, setFeedback] = useState("");

  // Update local state when draft loads
  useEffect(() => {
    if (draft) {
      setDraftBody(draft.body);
    }
  }, [draft]);

  const editMutation = useVersionedMutation({
    mutationFn: (newBody: string) =>
      apiClient
        .PATCH("/api/v1/drafts/{draft_id}", {
          params: { path: { draft_id: id! } },
          body: { message: newBody, expected_version: draft!.version },
        })
        .then(handleApiResponse),
    invalidateKey: draftQueries.detail(id!).queryKey,
    currentVersion: draft?.version ?? 0,
  });

  const decisionMutation = useVersionedMutation({
    mutationFn: (decision: "approved" | "rejected") =>
      apiClient
        .POST("/api/v1/drafts/{draft_id}/decision", {
          params: { path: { draft_id: id! } },
          body: { decision, feedback, expected_version: draft!.version },
        })
        .then(handleApiResponse),
    invalidateKey: draftQueries.detail(id!).queryKey,
    currentVersion: draft?.version ?? 0,
    onSuccess: () => navigate("/readiness"),
  });

  const conflict = editMutation.conflict ?? decisionMutation.conflict;
  const resolveConflict = editMutation.conflict
    ? editMutation.resolveConflict
    : decisionMutation.resolveConflict;

  if (isLoading)
    return (
      <div className="p-8 text-center text-muted-foreground">
        Loading draft details...
      </div>
    );
  if (isError || !draft)
    return (
      <div className="p-8 text-center text-destructive flex flex-col items-center">
        <AlertCircle className="mb-2" />
        Error loading draft:{" "}
        {error instanceof Error ? error.message : "Unknown error"}
      </div>
    );

  return (
    <div className="h-full flex flex-col relative">
      {/* Header */}
      <div className="mb-6 shrink-0">
        <Link
          to="/readiness"
          className="inline-flex items-center text-sm text-muted-foreground hover:text-foreground mb-4 transition-colors"
        >
          <ArrowLeft size={16} className="mr-2" />
          Back to Readiness Queue
        </Link>
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-3xl font-bold tracking-tight text-foreground">
              Draft Review Workspace
            </h2>
            <p className="text-muted-foreground mt-1">
              Reviewing outreach for {draft.target_name}
            </p>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={() => editMutation.mutate(draftBody)}
              disabled={editMutation.isPending || draftBody === draft.body}
              className="inline-flex items-center justify-center px-4 py-2 text-sm font-medium transition-colors rounded-md bg-secondary text-secondary-foreground hover:bg-secondary/80 disabled:opacity-50"
            >
              <Save size={16} className="mr-2" />
              {editMutation.isPending ? "Saving..." : "Save Edit"}
            </button>
          </div>
        </div>
      </div>

      {/* 3-Column Layout */}
      <div className="flex-1 grid grid-cols-12 gap-6 min-h-0">
        {/* LEFT: Context */}
        <div className="col-span-3 bg-card border border-border rounded-lg p-5 overflow-auto">
          <h3 className="font-semibold text-sm text-muted-foreground uppercase tracking-wider mb-4">
            Target Context
          </h3>
          <div className="space-y-4">
            <div>
              <div className="text-sm font-medium text-foreground">
                {draft.target_name}
              </div>
              <div className="text-xs text-muted-foreground">
                {draft.target_role}
              </div>
            </div>
            <div className="h-px bg-border my-2"></div>
            <div>
              <div className="text-xs text-muted-foreground">Version</div>
              <div className="text-sm font-medium text-foreground">
                v{draft.version}
              </div>
            </div>
          </div>
        </div>

        {/* CENTER: Editable Draft */}
        <div className="col-span-6 bg-card border border-border rounded-lg flex flex-col overflow-hidden">
          <div className="p-4 border-b border-border bg-muted/20">
            <div className="text-sm text-muted-foreground mb-1">Subject</div>
            <div className="font-medium">{draft.subject_line}</div>
          </div>
          <div className="flex-1 p-4 bg-background">
            <textarea
              className="w-full h-full bg-transparent resize-none outline-none text-foreground font-sans"
              value={draftBody}
              onChange={(e) => setDraftBody(e.target.value)}
            />
          </div>

          {/* Action Bar */}
          <div className="p-4 border-t border-border bg-card flex flex-col gap-3">
            <textarea
              placeholder="Leave feedback for AI if rejecting..."
              className="w-full bg-background border border-border rounded-md p-2 text-sm focus:outline-none focus:ring-1 focus:ring-primary/50"
              rows={2}
              value={feedback}
              onChange={(e) => setFeedback(e.target.value)}
            />
            <div className="flex items-center justify-end gap-3">
              <button
                onClick={() => decisionMutation.mutate("rejected")}
                disabled={decisionMutation.isPending}
                className="inline-flex items-center px-4 py-2 text-sm font-medium text-destructive-foreground bg-destructive hover:bg-destructive/90 rounded-md disabled:opacity-50"
              >
                <XCircle size={16} className="mr-2" />
                Reject & Request Fix
              </button>
              <button
                onClick={() => decisionMutation.mutate("approved")}
                disabled={decisionMutation.isPending}
                className="inline-flex items-center px-4 py-2 text-sm font-medium text-primary-foreground bg-primary hover:bg-primary/90 rounded-md disabled:opacity-50"
              >
                <CheckCircle size={16} className="mr-2" />
                Approve Draft
              </button>
            </div>
          </div>
        </div>

        {/* RIGHT: Readiness Checks */}
        <div className="col-span-3 bg-card border border-border rounded-lg p-5 overflow-auto">
          <h3 className="font-semibold text-sm text-muted-foreground uppercase tracking-wider mb-4">
            Readiness Checks
          </h3>
          <div className="text-sm text-muted-foreground italic">
            Check evaluation goes here...
          </div>
        </div>
      </div>

      {conflict && (
        <ConflictModal
          expected={conflict.expected}
          current={conflict.current}
          description="Another reviewer has modified or approved this draft while you were viewing it."
          onReload={resolveConflict}
        />
      )}
    </div>
  );
}
