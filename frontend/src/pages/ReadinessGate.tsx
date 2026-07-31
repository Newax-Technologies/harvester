import { Link } from "react-router";
import { FileText, Clock, AlertCircle } from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import { draftQueries } from "../api/queries";

export function ReadinessGate() {
  const {
    data: drafts,
    isLoading,
    isError,
    error,
  } = useQuery(draftQueries.list());

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold tracking-tight text-foreground">
            Readiness Gate
          </h2>
          <p className="text-muted-foreground mt-1">
            Review, edit, and approve AI-generated outreach drafts.
          </p>
        </div>
      </div>

      <div className="bg-card border border-border rounded-lg overflow-hidden">
        {isLoading ? (
          <div className="p-8 text-center text-muted-foreground">
            Loading drafts...
          </div>
        ) : isError ? (
          <div className="p-8 text-center text-destructive flex flex-col items-center">
            <AlertCircle className="mb-2" />
            Error loading drafts:{" "}
            {error instanceof Error ? error.message : "Unknown error"}
          </div>
        ) : !drafts || drafts.length === 0 ? (
          <div className="p-8 text-center text-muted-foreground">
            No drafts pending review.
          </div>
        ) : (
          <table className="w-full text-sm text-left">
            <thead className="bg-secondary/50 text-muted-foreground border-b border-border">
              <tr>
                <th className="px-6 py-4 font-medium">Target & Institution</th>
                <th className="px-6 py-4 font-medium">Generated</th>
                <th className="px-6 py-4 font-medium text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border">
              {drafts.map((draft: any) => (
                <tr
                  key={draft.id}
                  className="hover:bg-secondary/20 transition-colors"
                >
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-md bg-secondary flex items-center justify-center shrink-0">
                        <FileText size={20} className="text-muted-foreground" />
                      </div>
                      <div>
                        <div className="font-medium text-foreground">
                          {draft.target_name}
                        </div>
                        <div className="text-xs text-muted-foreground">
                          {draft.target_role}
                        </div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2 text-muted-foreground">
                      <Clock size={14} />
                      <span>
                        {new Date(draft.created_at as string).toLocaleString()}
                      </span>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <Link
                      to={`/readiness/${draft.id}`}
                      className="inline-flex items-center justify-center px-4 py-2 text-sm font-medium transition-colors rounded-md bg-primary hover:bg-primary/90 text-primary-foreground"
                    >
                      Review Draft
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
