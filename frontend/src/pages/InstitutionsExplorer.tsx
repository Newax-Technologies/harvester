import { useState } from "react";
import { Link } from "react-router";
import {
  Search,
  Building2,
  MapPin,
  Activity,
  ShieldCheck,
  AlertCircle,
} from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import { institutionQueries } from "../api/queries";

export function InstitutionsExplorer() {
  const [searchTerm, setSearchTerm] = useState("");
  const [cityFilter, setCityFilter] = useState("");

  const {
    data: institutions,
    isLoading,
    isError,
    error,
  } = useQuery(institutionQueries.list(50, 0, cityFilter || undefined));

  const filteredInstitutions =
    institutions?.items?.filter((inst: any) =>
      inst.canonical_name.toLowerCase().includes(searchTerm.toLowerCase()),
    ) || [];

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold tracking-tight text-foreground">
            Institution Explorer
          </h2>
          <p className="text-muted-foreground mt-1">
            Browse and filter resolved canonical entities.
          </p>
        </div>
      </div>

      {/* Filters and Search */}
      <div className="flex gap-4 items-center bg-card p-4 rounded-lg border border-border">
        <div className="relative flex-1">
          <Search
            className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground"
            size={18}
          />
          <input
            type="text"
            placeholder="Search institutions..."
            className="w-full bg-background border border-border rounded-md py-2 pl-10 pr-4 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        <select className="bg-background border border-border rounded-md py-2 px-4 text-sm">
          <option value="">All Types</option>
          <option value="clinic">Clinic</option>
          <option value="rehab">Rehabilitation</option>
        </select>
        <select
          className="bg-background border border-border rounded-md py-2 px-4 text-sm"
          value={cityFilter}
          onChange={(e) => setCityFilter(e.target.value)}
        >
          <option value="">All Cities</option>
          <option value="Islamabad">Islamabad</option>
          <option value="Rawalpindi">Rawalpindi</option>
        </select>
      </div>

      {/* Table */}
      <div className="bg-card border border-border rounded-lg overflow-hidden">
        {isLoading ? (
          <div className="p-8 text-center text-muted-foreground">
            Loading institutions...
          </div>
        ) : isError ? (
          <div className="p-8 text-center text-destructive flex flex-col items-center">
            <AlertCircle className="mb-2" />
            Error loading institutions:{" "}
            {error instanceof Error ? error.message : "Unknown error"}
          </div>
        ) : (
          <table className="w-full text-sm text-left">
            <thead className="bg-secondary/50 text-muted-foreground border-b border-border">
              <tr>
                <th className="px-6 py-4 font-medium">Institution</th>
                <th className="px-6 py-4 font-medium">Location</th>
                <th className="px-6 py-4 font-medium">Domain</th>
                <th className="px-6 py-4 font-medium">Confidence</th>
                <th className="px-6 py-4 font-medium text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border">
              {filteredInstitutions.length === 0 ? (
                <tr>
                  <td
                    colSpan={5}
                    className="px-6 py-8 text-center text-muted-foreground"
                  >
                    No institutions found.
                  </td>
                </tr>
              ) : (
                filteredInstitutions.map((inst: any) => (
                  <tr
                    key={inst.id}
                    className="hover:bg-secondary/20 transition-colors"
                  >
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-md bg-secondary flex items-center justify-center shrink-0">
                          <Building2
                            size={20}
                            className="text-muted-foreground"
                          />
                        </div>
                        <div>
                          <div className="font-medium text-foreground">
                            {inst.canonical_name}
                          </div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-2 text-muted-foreground">
                        <MapPin size={14} />
                        <span>
                          {(inst.branches && inst.branches[0]?.address) ||
                            "Unknown"}
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-2">
                        <Activity size={14} className="text-muted-foreground" />
                        <span>{inst.domain}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-2">
                        <ShieldCheck
                          size={14}
                          className={
                            inst.confidence_score > 80
                              ? "text-verified"
                              : "text-inference"
                          }
                        />
                        <span>{inst.confidence_score}%</span>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <Link
                        to={`/institutions/${inst.id}`}
                        className="inline-flex items-center justify-center px-4 py-2 text-sm font-medium transition-colors rounded-md bg-secondary hover:bg-secondary/80 text-secondary-foreground"
                      >
                        View Dossier
                      </Link>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
