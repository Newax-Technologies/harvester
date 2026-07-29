import { useState } from "react";
import { useParams, Link, useNavigate } from "react-router";
import {
  ArrowLeft,
  Check,
  X,
  MapPin,
  Building2,
  ExternalLink,
  AlertTriangle,
  AlertCircle,
} from "lucide-react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { resolutionQueries } from "../api/queries";
import { apiClient, ApiError } from "../api/client";

export function ResolutionDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const [feedback, setFeedback] = useState("");
  const [conflictError, setConflictError] = useState<{
    expected: number;
    current: number;
  } | null>(null);

  const {
    data: resolution,
    isLoading,
    isError,
    error,
  } = useQuery(resolutionQueries.detail(id!));

  const decisionMutation = useMutation({
    mutationFn: async (decision: "merge" | "separate" | "branch") => {
      const res = await apiClient.POST(
        "/api/v1/resolution-reviews/{review_id}/decision",
        {
          params: { path: { review_id: id! } },
          body: { decision, feedback, expected_version: resolution!.version },
        },
      );
      if (res.error)
        throw new ApiError(
          (res.error as any).error?.message || "Error",
          (res.error as any).error?.code,
          (res.error as any).error?.details,
        );
      return res.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: resolutionQueries.detail(id!).queryKey,
      });
      navigate("/resolution");
    },
    onError: (err: any) => {
      if (err instanceof ApiError && err.code === "stale_resource") {
        setConflictError({
          expected: resolution!.version,
          current: err.details?.current_version || resolution!.version + 1,
        });
      } else {
        alert("Failed to save decision: " + err.message);
      }
    },
  });

  if (isLoading)
    return (
      <div className="p-8 text-center text-muted-foreground">
        Loading resolution details...
      </div>
    );
  if (isError || !resolution)
    return (
      <div className="p-8 text-center text-destructive flex flex-col items-center">
        <AlertCircle className="mb-2" />
        Error loading resolution:{" "}
        {error instanceof Error ? error.message : "Unknown error"}
      </div>
    );

  const candidate = (resolution as any).incoming_data || {};

  return (
    <div className="h-full flex flex-col max-w-6xl mx-auto relative">
      <div className="mb-6 shrink-0">
        <Link
          to="/resolution"
          className="inline-flex items-center text-sm text-muted-foreground hover:text-foreground mb-4 transition-colors"
        >
          <ArrowLeft size={16} className="mr-2" />
          Back to Queue
        </Link>
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-3xl font-bold tracking-tight text-foreground">
              Evidence Comparison
            </h2>
            <p className="text-muted-foreground mt-1">
              Determine if these records represent the same entity.
            </p>
          </div>
          <div className="bg-secondary px-4 py-2 rounded-md font-mono text-sm border border-border">
            Score:{" "}
            <span className="font-bold text-foreground">
              {(resolution as any).confidence_score || 0}
            </span>
            /100
          </div>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-8 flex-1">
        {/* Record A */}
        <div className="bg-card border border-border rounded-lg p-6 space-y-6">
          <div className="flex items-center justify-between border-b border-border pb-4">
            <h3 className="font-semibold text-lg flex items-center gap-2">
              <Building2 size={20} className="text-primary" /> Record A
            </h3>
            <span className="text-xs uppercase tracking-wider text-muted-foreground font-semibold">
              Incoming Source
            </span>
          </div>

          <div className="space-y-4">
            <div>
              <div className="text-sm text-muted-foreground mb-1">Name</div>
              <div className="font-medium">{candidate.name || "Unknown"}</div>
            </div>
            <div>
              <div className="text-sm text-muted-foreground mb-1">Address</div>
              <div className="flex items-center gap-2 font-medium">
                <MapPin size={16} className="text-muted-foreground" />
                {candidate.address || "Unknown"}
              </div>
            </div>
            <div>
              <div className="text-sm text-muted-foreground mb-1">Phone</div>
              <div className="font-medium">{candidate.phone || "Unknown"}</div>
            </div>
            <div>
              <div className="text-sm text-muted-foreground mb-1">Website</div>
              <div className="font-medium flex items-center gap-2 text-primary">
                {candidate.website || "Unknown"}
                <ExternalLink size={14} />
              </div>
            </div>
          </div>
        </div>

        {/* Record B */}
        <div className="bg-card border border-border rounded-lg p-6 space-y-6">
          <div className="flex items-center justify-between border-b border-border pb-4">
            <h3 className="font-semibold text-lg flex items-center gap-2">
              <Building2 size={20} className="text-verified" /> Record B
            </h3>
            <span className="text-xs uppercase tracking-wider text-muted-foreground font-semibold">
              Canonical Target
            </span>
          </div>

          <div className="space-y-4">
            <div>
              <div className="text-sm text-muted-foreground mb-1">Name</div>
              <div className="font-medium">
                Unknown (Need to fetch Canonical Institution details)
              </div>
            </div>
            <div>
              <div className="text-sm text-muted-foreground mb-1">Address</div>
              <div className="flex items-center gap-2 font-medium">
                <MapPin size={16} className="text-muted-foreground" />
                Unknown
              </div>
            </div>
            <div>
              <div className="text-sm text-muted-foreground mb-1">Phone</div>
              <div className="font-medium">Unknown</div>
            </div>
            <div>
              <div className="text-sm text-muted-foreground mb-1">Website</div>
              <div className="font-medium flex items-center gap-2 text-primary">
                Unknown
                <ExternalLink size={14} />
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Decision Bar */}
      <div className="mt-8 bg-card border border-border p-6 rounded-lg shadow-sm space-y-4">
        <textarea
          placeholder="Reasoning for decision (optional but recommended)..."
          className="w-full bg-background border border-border rounded-md p-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50"
          rows={2}
          value={feedback}
          onChange={(e) => setFeedback(e.target.value)}
        />

        <div className="flex items-center justify-end gap-3">
          <button
            onClick={() => decisionMutation.mutate("separate")}
            disabled={decisionMutation.isPending}
            className="inline-flex items-center px-4 py-2 text-sm font-medium border border-destructive text-destructive hover:bg-destructive/10 rounded-md disabled:opacity-50"
          >
            <X size={16} className="mr-2" />
            Keep Separate
          </button>
          <button
            onClick={() => decisionMutation.mutate("branch")}
            disabled={decisionMutation.isPending}
            className="inline-flex items-center px-4 py-2 text-sm font-medium border border-primary text-primary hover:bg-primary/10 rounded-md disabled:opacity-50"
          >
            Shared Parent (Branches)
          </button>
          <button
            onClick={() => decisionMutation.mutate("merge")}
            disabled={decisionMutation.isPending}
            className="inline-flex items-center px-4 py-2 text-sm font-medium text-primary-foreground bg-primary hover:bg-primary/90 rounded-md disabled:opacity-50"
          >
            <Check size={16} className="mr-2" />
            Merge Entities
          </button>
        </div>
      </div>

      {/* Conflict Modal */}
      {conflictError && (
        <div className="absolute inset-0 z-50 bg-background/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-card border border-border rounded-xl shadow-lg max-w-md w-full p-6 animate-in fade-in zoom-in-95 duration-200">
            <div className="flex items-center gap-3 text-destructive mb-4">
              <AlertTriangle size={24} />
              <h3 className="text-lg font-semibold text-foreground">
                Update Conflict Detected
              </h3>
            </div>

            <div className="space-y-4 mb-6 text-sm text-muted-foreground">
              <p>
                Another reviewer has modified or decided on this candidate while
                you were viewing it.
              </p>
              <div className="bg-muted p-3 rounded-md border border-border space-y-2">
                <div className="flex justify-between">
                  <span>Your version:</span>
                  <span className="font-mono bg-background px-1.5 py-0.5 rounded text-foreground">
                    v{conflictError.expected}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span>Current server version:</span>
                  <span className="font-mono bg-background px-1.5 py-0.5 rounded text-foreground">
                    v{conflictError.current}
                  </span>
                </div>
              </div>
              <p>
                To prevent overwriting someone else's work, your changes have
                been blocked. Please refresh to see the latest version before
                taking action.
              </p>
            </div>

            <div className="flex justify-end gap-3">
              <button
                onClick={() => {
                  setConflictError(null);
                  queryClient.invalidateQueries({
                    queryKey: resolutionQueries.detail(id!).queryKey,
                  });
                }}
                className="inline-flex items-center justify-center px-4 py-2 text-sm font-medium transition-colors rounded-md bg-primary hover:bg-primary/90 text-primary-foreground"
              >
                Reload Latest Version
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
