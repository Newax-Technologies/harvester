import { AlertCircle } from "lucide-react";
import type { ReactNode } from "react";

interface DataPanelProps {
  isLoading: boolean;
  isError: boolean;
  error: unknown;
  isEmpty: boolean;
  loadingLabel: string;
  errorLabel: string;
  emptyLabel: string;
  children: ReactNode;
}

/**
 * Wraps the loading/error/empty tri-state + card panel every list page
 * (InstitutionsExplorer, ResolutionQueue, ReadinessGate, ...) previously
 * re-pasted verbatim. Table markup (columns/cells) stays page-specific --
 * pass your <table> as children once data is confirmed present and non-empty.
 */
export function DataPanel({
  isLoading,
  isError,
  error,
  isEmpty,
  loadingLabel,
  errorLabel,
  emptyLabel,
  children,
}: DataPanelProps) {
  return (
    <div className="bg-card border border-border rounded-lg overflow-hidden">
      {isLoading ? (
        <div className="p-8 text-center text-muted-foreground">
          {loadingLabel}
        </div>
      ) : isError ? (
        <div className="p-8 text-center text-destructive flex flex-col items-center">
          <AlertCircle className="mb-2" />
          {errorLabel}:{" "}
          {error instanceof Error ? error.message : "Unknown error"}
        </div>
      ) : isEmpty ? (
        <div className="p-8 text-center text-muted-foreground">
          {emptyLabel}
        </div>
      ) : (
        children
      )}
    </div>
  );
}

export function Table({ children }: { children: ReactNode }) {
  return <table className="w-full text-sm text-left">{children}</table>;
}

export function TableHead({ children }: { children: ReactNode }) {
  return (
    <thead className="bg-secondary/50 text-muted-foreground border-b border-border">
      <tr>{children}</tr>
    </thead>
  );
}

export function TableBody({ children }: { children: ReactNode }) {
  return <tbody className="divide-y divide-border">{children}</tbody>;
}

export function Th({
  children,
  align,
}: {
  children: ReactNode;
  align?: "right";
}) {
  return (
    <th
      className={`px-6 py-4 font-medium ${align === "right" ? "text-right" : ""}`}
    >
      {children}
    </th>
  );
}

export function Tr({ children }: { children: ReactNode }) {
  return (
    <tr className="hover:bg-secondary/20 transition-colors">{children}</tr>
  );
}

export function Td({
  children,
  align,
}: {
  children: ReactNode;
  align?: "right";
}) {
  return (
    <td className={`px-6 py-4 ${align === "right" ? "text-right" : ""}`}>
      {children}
    </td>
  );
}
