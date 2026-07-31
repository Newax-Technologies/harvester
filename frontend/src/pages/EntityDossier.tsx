import { useState } from "react";
import { useParams, Link } from "react-router";
import {
  ArrowLeft,
  Building2,
  Phone,
  MapPin,
  Globe,
  CheckCircle2,
  AlertTriangle,
  FileText,
  AlertCircle,
  TrendingUp,
} from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import { institutionQueries, leadProfileQueries } from "../api/queries";
import { StatusBadge } from "../components/StatusBadge";

export function EntityDossier() {
  const { id } = useParams<{ id: string }>();
  const [activeTab, setActiveTab] = useState("overview");

  const {
    data: dossier,
    isLoading,
    isError,
    error,
  } = useQuery(institutionQueries.detail(id!));

  // Only fetched once the Score tab is opened -- a brand-new institution
  // may not have a profile computed yet at all (404, not an error state).
  const { data: profile, isLoading: profileLoading } = useQuery({
    ...leadProfileQueries.detail(id!),
    enabled: activeTab === "score",
  });
  const { data: scoreHistory } = useQuery({
    ...leadProfileQueries.scoreHistory(id!),
    enabled: activeTab === "score",
  });

  if (isLoading)
    return (
      <div className="p-8 text-center text-muted-foreground">
        Loading dossier...
      </div>
    );
  if (isError || !dossier)
    return (
      <div className="p-8 text-center text-destructive flex flex-col items-center">
        <AlertCircle className="mb-2" />
        Error loading dossier:{" "}
        {error instanceof Error ? error.message : "Unknown error"}
      </div>
    );

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      {/* Header */}
      <div>
        <Link
          to="/institutions"
          className="inline-flex items-center text-sm text-muted-foreground hover:text-foreground mb-4 transition-colors"
        >
          <ArrowLeft size={16} className="mr-2" />
          Back to Explorer
        </Link>
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 rounded-xl bg-secondary flex items-center justify-center shrink-0">
              <Building2 size={32} className="text-primary" />
            </div>
            <div>
              <h2 className="text-3xl font-bold tracking-tight text-foreground flex items-center gap-3">
                {dossier.canonical_name}
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-verified/10 text-verified">
                  {dossier.confidence_score}% Confidence
                </span>
              </h2>
              <div className="flex items-center gap-4 text-sm text-muted-foreground mt-2">
                <span className="flex items-center gap-1">
                  <MapPin size={14} />{" "}
                  {dossier.branches?.[0]?.address || "Unknown"}
                </span>
                <span className="flex items-center gap-1">
                  <Globe size={14} /> {dossier.domain}
                </span>
              </div>
            </div>
          </div>
          <Link
            to={`/readiness/${id}`}
            className="inline-flex items-center justify-center px-4 py-2 text-sm font-medium transition-colors rounded-md bg-primary hover:bg-primary/90 text-primary-foreground"
          >
            Generate Outreach
          </Link>
        </div>
      </div>

      {/* Tabs */}
      <div className="border-b border-border">
        <nav className="flex space-x-8">
          {[
            "Overview",
            "Score",
            "Branches",
            "Contacts",
            "Research Findings",
            "Evidence",
          ].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab.toLowerCase().replace(" ", "-"))}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeTab === tab.toLowerCase().replace(" ", "-")
                  ? "border-primary text-primary"
                  : "border-transparent text-muted-foreground hover:text-foreground hover:border-border"
              }`}
            >
              {tab}
            </button>
          ))}
        </nav>
      </div>

      {/* Tab Content */}
      <div className="mt-6">
        {activeTab === "overview" && (
          <div className="grid grid-cols-3 gap-6">
            <div className="col-span-2 space-y-6">
              <div className="bg-card border border-border rounded-lg p-6">
                <h3 className="text-lg font-semibold mb-4">Research Summary</h3>
                <div className="space-y-4">
                  {(dossier as any).findings?.map((item: any) => (
                    <div
                      key={item.id}
                      className="flex gap-4 p-4 rounded-md border border-border bg-background/50"
                    >
                      <div className="shrink-0 mt-1">
                        {item.confidence_score > 80 ? (
                          <CheckCircle2 className="text-verified" size={20} />
                        ) : (
                          <AlertTriangle className="text-inference" size={20} />
                        )}
                      </div>
                      <div>
                        <div className="font-medium text-foreground">
                          {item.finding_value}
                        </div>
                        <div className="text-sm text-muted-foreground mt-1 flex items-center gap-2">
                          <span className="capitalize text-xs font-semibold px-2 py-0.5 rounded bg-secondary">
                            {item.finding_type}
                          </span>
                          <span>· {item.confidence_score}% confidence</span>
                        </div>
                      </div>
                    </div>
                  ))}
                  {(!(dossier as any).findings ||
                    (dossier as any).findings.length === 0) && (
                    <div className="text-muted-foreground text-sm">
                      No research findings available.
                    </div>
                  )}
                </div>
              </div>
            </div>
            <div className="space-y-6">
              <div className="bg-card border border-border rounded-lg p-6">
                <h3 className="text-lg font-semibold mb-4">Quick Contacts</h3>
                <div className="space-y-3">
                  {(dossier as any).contacts?.map((contact: any) => (
                    <div
                      key={contact.id}
                      className="flex items-center gap-3 text-sm"
                    >
                      <div className="w-8 h-8 rounded-full bg-secondary flex items-center justify-center text-muted-foreground">
                        {contact.contact_type === "phone" ? (
                          <Phone size={14} />
                        ) : (
                          <FileText size={14} />
                        )}
                      </div>
                      <div>
                        <div className="font-medium text-foreground">
                          {contact.contact_value}
                        </div>
                        <div className="text-xs text-muted-foreground">
                          {contact.role}
                        </div>
                      </div>
                    </div>
                  ))}
                  {(!(dossier as any).contacts ||
                    (dossier as any).contacts.length === 0) && (
                    <div className="text-muted-foreground text-sm">
                      No contacts available.
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === "score" && (
          <div className="grid grid-cols-3 gap-6">
            {profileLoading ? (
              <div className="col-span-3 p-8 text-center text-muted-foreground">
                Loading score...
              </div>
            ) : !profile ? (
              <div className="col-span-3 bg-card border border-border rounded-lg p-8 text-center text-muted-foreground">
                No score has been computed for this institution yet.
              </div>
            ) : (
              <>
                <div className="col-span-2 space-y-6">
                  <div className="bg-card border border-border rounded-lg p-6">
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="text-lg font-semibold">Score Breakdown</h3>
                      <div className="flex items-center gap-3">
                        {(profile as any).qualification_status && (
                          <StatusBadge
                            status={(profile as any).qualification_status}
                          />
                        )}
                        <span className="font-mono text-2xl font-bold text-verified">
                          {(profile as any).overall_score}
                        </span>
                        <span className="text-muted-foreground">/100</span>
                      </div>
                    </div>
                    <div className="space-y-3">
                      {Object.entries(
                        (profile as any).score_breakdown as Record<
                          string,
                          number
                        >,
                      )
                        .sort((a, b) => b[1] - a[1])
                        .map(([key, value]) => (
                          <div key={key}>
                            <div className="flex justify-between text-sm mb-1">
                              <span className="capitalize text-muted-foreground">
                                {key.replace(/_/g, " ")}
                              </span>
                              <span className="font-mono">{value}</span>
                            </div>
                            <div className="h-1.5 rounded-full bg-secondary overflow-hidden">
                              <div
                                className="h-full bg-verified"
                                style={{
                                  width: `${Math.min(100, Math.max(0, value))}%`,
                                }}
                              />
                            </div>
                          </div>
                        ))}
                    </div>
                  </div>

                  {scoreHistory && (scoreHistory as any[]).length > 0 && (
                    <div className="bg-card border border-border rounded-lg p-6">
                      <h3 className="text-lg font-semibold mb-4">
                        Score History
                      </h3>
                      <div className="space-y-2">
                        {(scoreHistory as any[]).map((point, i) => (
                          <div
                            key={i}
                            className="flex items-center justify-between text-sm py-2 border-b border-border last:border-0"
                          >
                            <span className="text-muted-foreground">
                              {new Date(point.computed_at).toLocaleString()}
                            </span>
                            <span className="font-mono font-medium">
                              {point.overall_score}/100
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>

                <div className="space-y-6">
                  <div className="bg-card border border-border rounded-lg p-6">
                    <h3 className="text-lg font-semibold mb-4">Signals</h3>
                    <div className="space-y-3 text-sm">
                      <div className="flex items-center justify-between">
                        <span className="text-muted-foreground">
                          Evidence points
                        </span>
                        <span className="font-mono">
                          {(profile as any).evidence_count}
                        </span>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-muted-foreground">
                          Has phone
                        </span>
                        <TrendingUp
                          size={14}
                          className={
                            (profile as any).has_phone
                              ? "text-verified"
                              : "text-stale"
                          }
                        />
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-muted-foreground">
                          Has email
                        </span>
                        <TrendingUp
                          size={14}
                          className={
                            (profile as any).has_email
                              ? "text-verified"
                              : "text-stale"
                          }
                        />
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-muted-foreground">
                          Named contact
                        </span>
                        <TrendingUp
                          size={14}
                          className={
                            (profile as any).has_named_contact
                              ? "text-verified"
                              : "text-stale"
                          }
                        />
                      </div>
                    </div>
                    {(profile as any).organization_summary && (
                      <>
                        <div className="h-px bg-border my-4" />
                        <p className="text-sm text-muted-foreground">
                          {(profile as any).organization_summary}
                        </p>
                      </>
                    )}
                  </div>
                </div>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
