import { BrowserRouter, Routes, Route, Outlet, Link } from 'react-router'
import { LayoutDashboard, Building2, Merge, CheckCircle2, AlertCircle } from 'lucide-react'
import { useQuery } from '@tanstack/react-query'
import { dashboardQueries } from './api/queries'
import { InstitutionsExplorer } from './pages/InstitutionsExplorer'
import { EntityDossier } from './pages/EntityDossier'
import { ReadinessGate } from './pages/ReadinessGate'
import { ReadinessGateDetail } from './pages/ReadinessGateDetail'
import { ResolutionQueue } from './pages/ResolutionQueue'
import { ResolutionDetail } from './pages/ResolutionDetail'

// Layout Component
function Layout() {
  return (
    <div className="flex h-screen bg-background text-foreground">
      {/* Sidebar */}
      <aside className="w-64 border-r border-border bg-card">
        <div className="p-4 border-b border-border">
          <h1 className="text-xl font-semibold text-primary">Lead Harvester</h1>
          <p className="text-xs text-muted-foreground mt-1">v0.1.0 · Dashboard</p>
        </div>
        <nav className="p-4 space-y-2">
          <Link to="/" className="flex items-center space-x-3 px-3 py-2 rounded-md hover:bg-secondary transition-colors">
            <LayoutDashboard size={18} />
            <span>Command Center</span>
          </Link>
          <Link to="/institutions" className="flex items-center space-x-3 px-3 py-2 rounded-md hover:bg-secondary transition-colors">
            <Building2 size={18} />
            <span>Explorer</span>
          </Link>
          <Link to="/resolution" className="flex items-center space-x-3 px-3 py-2 rounded-md hover:bg-secondary transition-colors">
            <Merge size={18} />
            <span>Resolution Queue</span>
          </Link>
          <Link to="/readiness" className="flex items-center space-x-3 px-3 py-2 rounded-md hover:bg-secondary transition-colors">
            <CheckCircle2 size={18} />
            <span>Readiness Gate</span>
          </Link>
        </nav>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col overflow-hidden">
        <header className="h-14 border-b border-border bg-card/50 backdrop-blur-sm flex items-center px-6 shrink-0">
          <div className="ml-auto text-sm text-muted-foreground">Logged in as Dev Admin</div>
        </header>
        <div className="flex-1 overflow-auto p-6">
          <Outlet />
        </div>
      </main>
    </div>
  )
}

// Temporary Placeholder Views
function CommandCenter() {
  const { data: summary, isLoading, isError, error } = useQuery(dashboardQueries.summary())

  if (isLoading) return <div className="p-8 text-center text-muted-foreground">Loading dashboard...</div>
  if (isError || !summary) return (
    <div className="p-8 text-center text-destructive flex flex-col items-center">
      <AlertCircle className="mb-2" />
      Error loading dashboard: {error instanceof Error ? error.message : "Unknown error"}
    </div>
  )

  return (
    <div className="space-y-6">
      <h2 className="text-3xl font-bold tracking-tight">Command Center</h2>
      <div className="grid grid-cols-4 gap-4">
        {[
          { title: "Canonical Leads", value: String((summary as any).total_canonical_institutions || "0") },
          { title: "Pending Resolution", value: String((summary as any).pending_resolution_candidates || "0") },
          { title: "Drafts to Review", value: String((summary as any).pending_outreach_drafts || "0") },
          { title: "Target Accounts", value: String((summary as any).total_target_accounts || "0") }
        ].map(stat => (
          <div key={stat.title} className="bg-card border border-border p-6 rounded-lg shadow-sm">
            <h3 className="text-sm font-medium text-muted-foreground mb-2">{stat.title}</h3>
            <p className="text-3xl font-semibold">{stat.value}</p>
          </div>
        ))}
      </div>
    </div>
  )
}



function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<CommandCenter />} />
          <Route path="institutions" element={<InstitutionsExplorer />} />
          <Route path="institutions/:id" element={<EntityDossier />} />
          <Route path="resolution" element={<ResolutionQueue />} />
          <Route path="resolution/:id" element={<ResolutionDetail />} />
          <Route path="readiness" element={<ReadinessGate />} />
          <Route path="readiness/:id" element={<ReadinessGateDetail />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
