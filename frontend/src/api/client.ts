import createClient from "openapi-fetch";
import type { paths } from "./schema";

// Read from a gitignored .env.local (see .env.local.example) -- never a
// literal here. The mock-auth backend (api/dependencies.py::get_current_user)
// accepts a fixed set of tokens for local development only; shipping one of
// those values in the committed bundle would let anyone who reads the
// repository or the built frontend invoke reviewer-only endpoints.
const DEV_AUTH_TOKEN = import.meta.env.VITE_DEV_AUTH_TOKEN as
  string | undefined;

export const apiClient = createClient<paths>({
  baseUrl: "http://localhost:8000",
  headers: DEV_AUTH_TOKEN ? { Authorization: `Bearer ${DEV_AUTH_TOKEN}` } : {},
});

// Helper for extracting exactly the error schema structure from the backend
export class ApiError extends Error {
  public code: string;
  public details: any;

  constructor(message: string, code: string, details?: any) {
    super(message);
    this.name = "ApiError";
    this.code = code;
    this.details = details || {};
  }
}

export async function handleApiResponse<T>(response: {
  data?: T;
  error?: any;
  response: Response;
}): Promise<T> {
  if (response.error) {
    if (response.error.error) {
      throw new ApiError(
        response.error.error.message,
        response.error.error.code,
        response.error.error.details,
      );
    }
    throw new Error("An unexpected error occurred");
  }
  return response.data as T;
}
