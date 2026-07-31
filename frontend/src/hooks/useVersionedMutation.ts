import { useMutation, useQueryClient, type QueryKey } from "@tanstack/react-query";
import { useState } from "react";
import { ApiError } from "../api/client";

export interface ConflictState {
  expected: number;
  current: number;
}

interface UseVersionedMutationOptions<TVariables, TData> {
  mutationFn: (variables: TVariables) => Promise<TData>;
  /** Query key to invalidate after a successful write or a conflict reload. */
  invalidateKey: QueryKey;
  /** The version this mutation believes it's writing on top of (resource.version). */
  currentVersion: number;
  onSuccess?: (data: TData) => void;
}

/**
 * Every optimistic-locking write in this app (ResolutionDetail's decision,
 * ReadinessGateDetail's edit + decision) sends `expected_version` and, on a
 * `stale_resource` ApiError, needs to show the same "someone else changed
 * this" conflict modal instead of a generic alert. This was previously
 * duplicated inline in each mutation; centralizing it here means a 5th/6th/
 * 7th versioned write (Compliance, Daily Selection, ...) gets the same
 * behavior for free instead of re-copying the onError branching.
 */
export function useVersionedMutation<TVariables, TData>({
  mutationFn,
  invalidateKey,
  currentVersion,
  onSuccess,
}: UseVersionedMutationOptions<TVariables, TData>) {
  const queryClient = useQueryClient();
  const [conflict, setConflict] = useState<ConflictState | null>(null);

  const mutation = useMutation({
    mutationFn,
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: invalidateKey });
      setConflict(null);
      onSuccess?.(data);
    },
    onError: (err: unknown) => {
      if (err instanceof ApiError && err.code === "stale_resource") {
        const details = err.details as { current_version?: number } | undefined;
        setConflict({
          expected: currentVersion,
          current: details?.current_version ?? currentVersion + 1,
        });
      } else {
        const message = err instanceof Error ? err.message : "Unknown error";
        alert("Failed to save: " + message);
      }
    },
  });

  const resolveConflict = () => {
    setConflict(null);
    queryClient.invalidateQueries({ queryKey: invalidateKey });
  };

  return { ...mutation, conflict, resolveConflict };
}
