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
    detail: (institutionId: string) => ["lead-profiles", "detail", institutionId],
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
            params: { path: { institution_id: institutionId }, query: { limit } },
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
