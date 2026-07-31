import { useState } from "react";
import type { ReactNode } from "react";
import { BrowserRouter, Routes, Route, Outlet, Link } from "react-router";
import {
  LayoutDashboard,
  Building2,
  Merge,
  CheckCircle2,
  AlertCircle,
  Plus,
  TrendingUp,
  Sparkles,
  ShieldAlert,
} from "lucide-react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { dashboardQueries } from "./api/queries";
import { InstitutionsExplorer } from "./pages/InstitutionsExplorer";
import { EntityDossier } from "./pages/EntityDossier";
import { ReadinessGate } from "./pages/ReadinessGate";
import { ReadinessGateDetail } from "./pages/ReadinessGateDetail";
import { ResolutionQueue } from "./pages/ResolutionQueue";
import { ResolutionDetail } from "./pages/ResolutionDetail";
import { LeadProfiles } from "./pages/LeadProfiles";
import { DailyQueue } from "./pages/DailyQueue";
import { DataQuality } from "./pages/DataQuality";
import { ManualLeadDrawer } from "./components/ManualLeadDrawer";

function NavSection({
  label,
  children,
}: {
  label: string;
  children: ReactNode;
}) {
  return (
    <div className="space-y-1">
      <div className="px-3 pt-3 pb-1 text-xs font-semibold uppercase tracking-wider text-muted-foreground/70">
        {label}
      </div>
      {children}
    </div>
  );
}

function NavLink({
  to,
  icon,
  children,
}: {
  to: string;
  icon: ReactNode;
  children: ReactNode;
}) {
  return (
    <Link
      to={to}
      className="flex items-center space-x-3 px-3 py-2 rounded-md hover:bg-secondary transition-colors"
    >
      {icon}
      <span>{children}</span>
    </Link>
  );
}

// Layout Component
function Layout() {
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [successBanner, setSuccessBanner] = useState<string | null>(null);
  const queryClient = useQueryClient();

  const handleSuccess = (name: string) => {
    setSuccessBanner(`"${name}" added to database`);
    queryClient.invalidateQueries({ queryKey: ["dashboard"] });
    setTimeout(() => setSuccessBanner(null), 5000);
  };

  return (
    <div className="flex h-screen bg-background text-foreground">
      {/* Sidebar */}
      <aside className="w-64 border-r border-border bg-card flex flex-col">
        <div className="p-4 border-b border-border">
          <h1 className="text-xl font-semibold text-primary">Lead Harvester</h1>
          <p className="text-xs text-muted-foreground mt-1">
            v0.1.0 · Dashboard
          </p>
        </div>
        <nav className="p-4 flex-1 overflow-y-auto">
          <NavSection label="Pipeline">
            <NavLink to="/" icon={<LayoutDashboard size={18} />}>
              Command Center
            </NavLink>
            <NavLink to="/institutions" icon={<Building2 size={18} />}>
              Explorer
            </NavLink>
            <NavLink to="/leads" icon={<TrendingUp size={18} />}>
              Lead Profiles
            </NavLink>
            <NavLink to="/daily-queue" icon={<Sparkles size={18} />}>
              Daily Queue
            </NavLink>
          </NavSection>
          <NavSection label="Review">
            <NavLink to="/resolution" icon={<Merge size={18} />}>
              Resolution Queue
            </NavLink>
            <NavLink to="/readiness" icon={<CheckCircle2 size={18} />}>
              Readiness Gate
            </NavLink>
            <NavLink to="/data-quality" icon={<ShieldAlert size={18} />}>
              Data Quality
            </NavLink>
          </NavSection>
        </nav>

        {/* Add Lead button pinned to bottom of sidebar */}
        <div className="p-4 border-t border-border">
          <button
            onClick={() => setDrawerOpen(true)}
            className="w-full flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg text-sm font-semibold
              text-white bg-gradient-to-r from-blue-600 to-violet-600
              hover:from-blue-500 hover:to-violet-500
              shadow-lg shadow-blue-500/20 hover:shadow-blue-500/30
              hover:-translate-y-px active:translate-y-0
              transition-all duration-150"
          >
            <Plus size={16} />
            Add Lead Manually
          </button>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col overflow-hidden">
        <header className="h-14 border-b border-border bg-card/50 backdrop-blur-sm flex items-center px-6 shrink-0 gap-3">
          {/* Success banner in header */}
          {successBanner && (
            <div
              className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-green-500/10 border border-green-500/30
              text-green-400 text-xs font-medium animate-in slide-in-from-top-1 duration-200"
            >
              <CheckCircle2 size={13} />
              {successBanner}
            </div>
          )}
          <div className="ml-auto flex items-center gap-3">
            {/* Header quick-add button */}
            <button
              onClick={() => setDrawerOpen(true)}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-semibold
                text-blue-400 border border-blue-500/30 bg-blue-500/10
                hover:bg-blue-500/20 hover:border-blue-500/50 transition-all"
            >
              <Plus size={13} />
              Add Lead
            </button>
            <span className="text-sm text-muted-foreground">
              Logged in as Dev Admin
            </span>
          </div>
        </header>
        <div className="flex-1 overflow-auto p-6">
          <Outlet />
        </div>
      </main>

      {/* Drawer */}
      <ManualLeadDrawer
        open={drawerOpen}
        onClose={() => setDrawerOpen(false)}
        onSuccess={handleSuccess}
      />
    </div>
  );
}

// Temporary Placeholder Views
function CommandCenter() {
  const {
    data: summary,
    isLoading,
    isError,
    error,
  } = useQuery(dashboardQueries.summary());

  if (isLoading)
    return (
      <div className="p-8 text-center text-muted-foreground">
        Loading dashboard...
      </div>
    );
  if (isError || !summary)
    return (
      <div className="p-8 text-center text-destructive flex flex-col items-center">
        <AlertCircle className="mb-2" />
        Error loading dashboard:{" "}
        {error instanceof Error ? error.message : "Unknown error"}
      </div>
    );

  return (
    <div className="space-y-6">
      <h2 className="text-3xl font-bold tracking-tight">Command Center</h2>
      <div className="grid grid-cols-4 gap-4">
        {[
          {
            title: "Canonical Leads",
            value: String((summary as any).total_canonical_institutions || "0"),
          },
          {
            title: "Pending Resolution",
            value: String(
              (summary as any).pending_resolution_candidates || "0",
            ),
          },
          {
            title: "Drafts to Review",
            value: String((summary as any).pending_outreach_drafts || "0"),
          },
          {
            title: "Target Accounts",
            value: String((summary as any).total_target_accounts || "0"),
          },
        ].map((stat) => (
          <div
            key={stat.title}
            className="bg-card border border-border p-6 rounded-lg shadow-sm"
          >
            <h3 className="text-sm font-medium text-muted-foreground mb-2">
              {stat.title}
            </h3>
            <p className="text-3xl font-semibold">{stat.value}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<CommandCenter />} />
          <Route path="institutions" element={<InstitutionsExplorer />} />
          <Route path="institutions/:id" element={<EntityDossier />} />
          <Route path="leads" element={<LeadProfiles />} />
          <Route path="daily-queue" element={<DailyQueue />} />
          <Route path="resolution" element={<ResolutionQueue />} />
          <Route path="resolution/:id" element={<ResolutionDetail />} />
          <Route path="readiness" element={<ReadinessGate />} />
          <Route path="readiness/:id" element={<ReadinessGateDetail />} />
          <Route path="data-quality" element={<DataQuality />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
