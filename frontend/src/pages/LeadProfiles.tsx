import { useState } from "react";
import { Link } from "react-router";
import { TrendingUp, Phone, Mail, User } from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import { leadProfileQueries } from "../api/queries";
import { StatusBadge } from "../components/StatusBadge";
import {
  DataPanel,
  Table,
  TableHead,
  TableBody,
  Th,
  Tr,
  Td,
} from "../components/DataTable";

function scoreColor(score: number): string {
  if (score >= 80) return "text-verified";
  if (score >= 50) return "text-inference";
  return "text-stale";
}

export function LeadProfiles() {
  const [minScore, setMinScore] = useState<number | undefined>(undefined);

  const {
    data: profiles,
    isLoading,
    isError,
    error,
  } = useQuery(leadProfileQueries.list(50, 0, minScore));

  const items = profiles?.items ?? [];

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold tracking-tight text-foreground">
            Lead Profiles
          </h2>
          <p className="text-muted-foreground mt-1">
            Institutions ranked by score -- who to work first.
          </p>
        </div>
      </div>

      <div className="flex gap-4 items-center bg-card p-4 rounded-lg border border-border">
        <label className="text-sm text-muted-foreground shrink-0">
          Minimum score
        </label>
        <input
          type="number"
          min={0}
          max={100}
          placeholder="0"
          className="w-32 bg-background border border-border rounded-md py-2 px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50"
          value={minScore ?? ""}
          onChange={(e) =>
            setMinScore(e.target.value ? Number(e.target.value) : undefined)
          }
        />
      </div>

      <DataPanel
        isLoading={isLoading}
        isError={isError}
        error={error}
        isEmpty={items.length === 0}
        loadingLabel="Loading lead profiles..."
        errorLabel="Error loading lead profiles"
        emptyLabel="No lead profiles found."
      >
        <Table>
          <TableHead>
            <Th>Institution</Th>
            <Th>Score</Th>
            <Th>Qualification</Th>
            <Th>Contactability</Th>
            <Th align="right">Actions</Th>
          </TableHead>
          <TableBody>
            {items.map((profile: any) => (
              <Tr key={profile.id}>
                <Td>
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-md bg-secondary flex items-center justify-center shrink-0">
                      <TrendingUp
                        size={20}
                        className={scoreColor(profile.overall_score)}
                      />
                    </div>
                    <div>
                      <div className="font-medium text-foreground">
                        {profile.canonical_name}
                      </div>
                      <div className="text-xs text-muted-foreground line-clamp-1 max-w-xs">
                        {profile.organization_summary || "No summary yet."}
                      </div>
                    </div>
                  </div>
                </Td>
                <Td>
                  <span
                    className={`font-mono font-semibold ${scoreColor(profile.overall_score)}`}
                  >
                    {profile.overall_score}
                  </span>
                  <span className="text-muted-foreground">/100</span>
                </Td>
                <Td>
                  {profile.qualification_status ? (
                    <StatusBadge status={profile.qualification_status} />
                  ) : (
                    <span className="text-muted-foreground text-xs">
                      Not assessed
                    </span>
                  )}
                </Td>
                <Td>
                  <div className="flex items-center gap-3 text-muted-foreground">
                    <Phone
                      size={14}
                      className={profile.has_phone ? "text-verified" : ""}
                    />
                    <Mail
                      size={14}
                      className={profile.has_email ? "text-verified" : ""}
                    />
                    <User
                      size={14}
                      className={
                        profile.has_named_contact ? "text-verified" : ""
                      }
                    />
                  </div>
                </Td>
                <Td align="right">
                  <Link
                    to={`/institutions/${profile.institution_id}`}
                    className="inline-flex items-center justify-center px-4 py-2 text-sm font-medium transition-colors rounded-md bg-secondary hover:bg-secondary/80 text-secondary-foreground"
                  >
                    View Dossier
                  </Link>
                </Td>
              </Tr>
            ))}
          </TableBody>
        </Table>
      </DataPanel>
    </div>
  );
}
