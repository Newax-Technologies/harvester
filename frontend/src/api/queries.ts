import { queryOptions } from "@tanstack/react-query";
import { apiClient, handleApiResponse } from "./client";

export const queryKeys = {
  dashboard: {
    summary: () => ["dashboard", "summary"],
    activity: () => ["dashboard", "activity"],
  },
  institutions: {
    list: (filters: any) => ["institutions", "list", filters],
    detail: (id: string) => ["institutions", "detail", id],
  },
  drafts: {
    list: () => ["drafts", "list"],
    detail: (id: string) => ["drafts", "detail", id],
  },
  resolutions: {
    list: () => ["resolutions", "list"],
    detail: (id: string) => ["resolutions", "detail", id],
  },
  leadProfiles: {
    list: (filters: any) => ["lead-profiles", "list", filters],
    detail: (institutionId: string) => [
      "lead-profiles",
      "detail",
      institutionId,
    ],
    scoreHistory: (institutionId: string) => [
      "lead-profiles",
      "score-history",
      institutionId,
    ],
  },
  dailySelection: {
    list: (filters: any) => ["daily-selection", "list", filters],
  },
  verification: {
    flags: (filters: any) => ["verification", "flags", filters],
  },
  compliance: {
    suppressions: (limit: number) => ["compliance", "suppressions", limit],
    deletionRequests: (status?: string) => [
      "compliance",
      "deletion-requests",
      status,
    ],
  },
  operations: {
    health: () => ["operations", "health"],
    metrics: () => ["operations", "metrics"],
    sourceRuns: (filters: any) => ["operations", "source-runs", filters],
    sourceRunDetail: (id: string) => ["operations", "source-runs", id],
    sourceHealth: () => ["operations", "source-health"],
    strandedRecords: () => ["operations", "stranded-records"],
    auditLog: (filters: any) => ["operations", "audit-log", filters],
    config: () => ["operations", "config"],
  },
  outbox: {
    list: (status?: string) => ["outbox", "list", status],
  },
};

export const dashboardQueries = {
  summary: () =>
    queryOptions({
      queryKey: queryKeys.dashboard.summary(),
      queryFn: () =>
        apiClient.GET("/api/v1/dashboard/summary").then(handleApiResponse),
    }),
  activity: () =>
    queryOptions({
      queryKey: queryKeys.dashboard.activity(),
      queryFn: () =>
        apiClient.GET("/api/v1/dashboard/activity").then(handleApiResponse),
    }),
};

export const institutionQueries = {
  list: (limit: number, offset: number, city?: string) =>
    queryOptions({
      queryKey: queryKeys.institutions.list({ limit, offset, city }),
      queryFn: () =>
        apiClient
          .GET("/api/v1/institutions", {
            params: { query: { limit, offset, city } },
          })
          .then(handleApiResponse),
    }),
  detail: (id: string) =>
    queryOptions({
      queryKey: queryKeys.institutions.detail(id),
      queryFn: () =>
        apiClient
          .GET("/api/v1/institutions/{institution_id}", {
            params: { path: { institution_id: id } },
          })
          .then(handleApiResponse),
    }),
};

export const draftQueries = {
  list: () =>
    queryOptions({
      queryKey: queryKeys.drafts.list(),
      queryFn: () => apiClient.GET("/api/v1/drafts").then(handleApiResponse),
    }),
  detail: (id: string) =>
    queryOptions({
      queryKey: queryKeys.drafts.detail(id),
      queryFn: () =>
        apiClient
          .GET("/api/v1/drafts/{draft_id}", {
            params: { path: { draft_id: id } },
          })
          .then(handleApiResponse),
    }),
};

export const resolutionQueries = {
  list: () =>
    queryOptions({
      queryKey: queryKeys.resolutions.list(),
      queryFn: () =>
        apiClient.GET("/api/v1/resolution-reviews").then(handleApiResponse),
    }),
  detail: (id: string) =>
    queryOptions({
      queryKey: queryKeys.resolutions.detail(id),
      queryFn: () =>
        apiClient
          .GET("/api/v1/resolution-reviews/{review_id}", {
            params: { path: { review_id: id } },
          })
          .then(handleApiResponse),
    }),
};

export const leadProfileQueries = {
  list: (limit: number, offset: number, minScore?: number) =>
    queryOptions({
      queryKey: queryKeys.leadProfiles.list({ limit, offset, minScore }),
      queryFn: () =>
        apiClient
          .GET("/api/v1/lead-profiles", {
            params: { query: { limit, offset, min_score: minScore } },
          })
          .then(handleApiResponse),
    }),
  detail: (institutionId: string) =>
    queryOptions({
      queryKey: queryKeys.leadProfiles.detail(institutionId),
      queryFn: () =>
        apiClient
          .GET("/api/v1/lead-profiles/{institution_id}", {
            params: { path: { institution_id: institutionId } },
          })
          .then(handleApiResponse),
      // A brand-new institution may not have a profile computed yet --
      // 404 is an expected, non-error state here (see EntityDossier's
      // Score tab), not something to retry.
      retry: false,
    }),
  scoreHistory: (institutionId: string, limit = 50) =>
    queryOptions({
      queryKey: queryKeys.leadProfiles.scoreHistory(institutionId),
      queryFn: () =>
        apiClient
          .GET("/api/v1/lead-profiles/{institution_id}/score-history", {
            params: {
              path: { institution_id: institutionId },
              query: { limit },
            },
          })
          .then(handleApiResponse),
    }),
};

export const dailySelectionQueries = {
  list: (status?: string, limit = 100) =>
    queryOptions({
      queryKey: queryKeys.dailySelection.list({ status, limit }),
      queryFn: () =>
        apiClient
          .GET("/api/v1/daily-selection", {
            params: { query: { status: status as any, limit } },
          })
          .then(handleApiResponse),
    }),
};

export const verificationQueries = {
  flags: (status?: string, flagType?: string, limit = 100) =>
    queryOptions({
      queryKey: queryKeys.verification.flags({ status, flagType, limit }),
      queryFn: () =>
        apiClient
          .GET("/api/v1/verification/flags", {
            params: {
              query: {
                status: status as any,
                flag_type: flagType as any,
                limit,
              },
            },
          })
          .then(handleApiResponse),
    }),
};

export const complianceQueries = {
  suppressions: (limit = 100) =>
    queryOptions({
      queryKey: queryKeys.compliance.suppressions(limit),
      queryFn: () =>
        apiClient
          .GET("/api/v1/compliance/suppressions", {
            params: { query: { limit } },
          })
          .then(handleApiResponse),
    }),
  deletionRequests: (status?: string, limit = 100) =>
    queryOptions({
      queryKey: queryKeys.compliance.deletionRequests(status),
      queryFn: () =>
        apiClient
          .GET("/api/v1/compliance/deletion-requests", {
            params: { query: { status: status as any, limit } },
          })
          .then(handleApiResponse),
    }),
};

export const operationsQueries = {
  health: () =>
    queryOptions({
      queryKey: queryKeys.operations.health(),
      queryFn: () =>
        apiClient.GET("/api/v1/operations/health").then(handleApiResponse),
    }),
  metrics: () =>
    queryOptions({
      queryKey: queryKeys.operations.metrics(),
      queryFn: () =>
        apiClient.GET("/api/v1/operations/metrics").then(handleApiResponse),
    }),
  sourceRuns: (sourceType?: string, status?: string, limit = 50) =>
    queryOptions({
      queryKey: queryKeys.operations.sourceRuns({ sourceType, status, limit }),
      queryFn: () =>
        apiClient
          .GET("/api/v1/operations/source-runs", {
            params: {
              query: {
                source_type: sourceType as any,
                status: status as any,
                limit,
              },
            },
          })
          .then(handleApiResponse),
    }),
  sourceRunDetail: (runId: string) =>
    queryOptions({
      queryKey: queryKeys.operations.sourceRunDetail(runId),
      queryFn: () =>
        apiClient
          .GET("/api/v1/operations/source-runs/{run_id}", {
            params: { path: { run_id: runId } },
          })
          .then(handleApiResponse),
      enabled: !!runId,
    }),
  sourceHealth: () =>
    queryOptions({
      queryKey: queryKeys.operations.sourceHealth(),
      queryFn: () =>
        apiClient
          .GET("/api/v1/operations/source-health")
          .then(handleApiResponse),
    }),
  strandedRecords: (limit = 100) =>
    queryOptions({
      queryKey: queryKeys.operations.strandedRecords(),
      queryFn: () =>
        apiClient
          .GET("/api/v1/operations/stranded-records", {
            params: { query: { limit } },
          })
          .then(handleApiResponse),
    }),
  auditLog: (entityType?: string, actor?: string, limit = 100) =>
    queryOptions({
      queryKey: queryKeys.operations.auditLog({ entityType, actor, limit }),
      queryFn: () =>
        apiClient
          .GET("/api/v1/operations/audit-log", {
            params: {
              query: { entity_type: entityType, actor, limit },
            },
          })
          .then(handleApiResponse),
    }),
  config: () =>
    queryOptions({
      queryKey: queryKeys.operations.config(),
      queryFn: () =>
        apiClient.GET("/api/v1/operations/config").then(handleApiResponse),
    }),
};

export const outboxQueries = {
  list: (status?: string, limit = 100) =>
    queryOptions({
      queryKey: queryKeys.outbox.list(status),
      queryFn: () =>
        apiClient
          .GET("/api/v1/outbox", {
            params: { query: { status: status as any, limit } },
          })
          .then(handleApiResponse),
    }),
};
