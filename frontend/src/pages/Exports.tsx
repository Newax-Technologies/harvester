import { useState } from "react";
import { Download } from "lucide-react";
import { authHeaders } from "../api/client";
import { useToast } from "../components/Toast";

const FORMAT_OPTIONS = ["csv", "json"];
const OPERATING_STATUS_OPTIONS = [
  "",
  "operational",
  "closed_temporarily",
  "closed_permanently",
  "unknown",
];
const QUALIFICATION_OPTIONS = [
  "",
  "pending",
  "qualified",
  "disqualified",
  "needs_review",
];

export function Exports() {
  const [format, setFormat] = useState("csv");
  const [status, setStatus] = useState("");
  const [minScore, setMinScore] = useState<number | undefined>(undefined);
  const [qualificationStatus, setQualificationStatus] = useState("");
  const [limit, setLimit] = useState(1000);
  const [downloading, setDownloading] = useState(false);
  const { showToast } = useToast();

  const handleDownload = async () => {
    setDownloading(true);
    try {
      const params = new URLSearchParams();
      params.set("format", format);
      if (status) params.set("status", status);
      if (minScore !== undefined) params.set("min_score", String(minScore));
      if (qualificationStatus)
        params.set("qualification_status", qualificationStatus);
      params.set("limit", String(limit));

      const response = await fetch(
        `http://localhost:8000/api/v1/exports/leads?${params.toString()}`,
        { headers: authHeaders() },
      );
      if (!response.ok) {
        throw new Error(`Export failed with status ${response.status}`);
      }
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `leads-export.${format}`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
      showToast("Export downloaded.", true);
    } catch (err) {
      showToast(
        `Export failed: ${err instanceof Error ? err.message : "Unknown error"}`,
        false,
      );
    } finally {
      setDownloading(false);
    }
  };

  return (
    <div className="space-y-6 max-w-3xl mx-auto">
      <div>
        <h2 className="text-3xl font-bold tracking-tight text-foreground">
          Exports
        </h2>
        <p className="text-muted-foreground mt-1">
          Download lead contact points as a CSV or JSON file, filtered as
          needed.
        </p>
      </div>

      <div className="bg-card p-6 rounded-lg border border-border space-y-5">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-xs text-muted-foreground mb-1">
              Format
            </label>
            <select
              className="w-full bg-background border border-border rounded-md py-2 px-4 text-sm uppercase"
              value={format}
              onChange={(e) => setFormat(e.target.value)}
            >
              {FORMAT_OPTIONS.map((f) => (
                <option key={f} value={f} className="uppercase">
                  {f}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-xs text-muted-foreground mb-1">
              Limit
            </label>
            <input
              type="number"
              min={1}
              className="w-full bg-background border border-border rounded-md py-2 px-4 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50"
              value={limit}
              onChange={(e) => setLimit(Number(e.target.value) || 1000)}
            />
          </div>
          <div>
            <label className="block text-xs text-muted-foreground mb-1">
              Operating status
            </label>
            <select
              className="w-full bg-background border border-border rounded-md py-2 px-4 text-sm capitalize"
              value={status}
              onChange={(e) => setStatus(e.target.value)}
            >
              {OPERATING_STATUS_OPTIONS.map((s) => (
                <option key={s || "all"} value={s} className="capitalize">
                  {s ? s.replace(/_/g, " ") : "Any"}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-xs text-muted-foreground mb-1">
              Qualification status
            </label>
            <select
              className="w-full bg-background border border-border rounded-md py-2 px-4 text-sm capitalize"
              value={qualificationStatus}
              onChange={(e) => setQualificationStatus(e.target.value)}
            >
              {QUALIFICATION_OPTIONS.map((s) => (
                <option key={s || "all"} value={s} className="capitalize">
                  {s ? s.replace(/_/g, " ") : "Any"}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-xs text-muted-foreground mb-1">
              Minimum score
            </label>
            <input
              type="number"
              min={0}
              max={100}
              placeholder="0"
              className="w-full bg-background border border-border rounded-md py-2 px-4 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50"
              value={minScore ?? ""}
              onChange={(e) =>
                setMinScore(e.target.value ? Number(e.target.value) : undefined)
              }
            />
          </div>
        </div>

        <button
          onClick={handleDownload}
          disabled={downloading}
          className="inline-flex items-center gap-2 px-4 py-2 text-sm font-semibold rounded-md text-primary-foreground bg-primary hover:bg-primary/90 disabled:opacity-50"
        >
          <Download size={16} />
          {downloading ? "Preparing download..." : "Download Export"}
        </button>
      </div>
    </div>
  );
}
