import createClient from "openapi-fetch";
import type { paths } from "./schema";

const DEV_AUTH_TOKEN = "secret-reviewer-token"; // Using reviewer role for testing UI

export const apiClient = createClient<paths>({
  baseUrl: "http://localhost:8000",
  headers: {
    Authorization: `Bearer ${DEV_AUTH_TOKEN}`,
  },
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
