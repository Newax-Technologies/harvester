import { Link } from 'react-router'
import { Merge, AlertCircle } from 'lucide-react'
import { useQuery } from '@tanstack/react-query'
import { resolutionQueries } from '../api/queries'

export function ResolutionQueue() {
  const { data: resolutions, isLoading, isError, error } = useQuery(resolutionQueries.list())

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold tracking-tight text-foreground">Resolution Queue</h2>
          <p className="text-muted-foreground mt-1">Review ambiguous source matches and canonicalize entities.</p>
        </div>
      </div>

      <div className="bg-card border border-border rounded-lg overflow-hidden">
        {isLoading ? (
          <div className="p-8 text-center text-muted-foreground">Loading resolutions...</div>
        ) : isError ? (
          <div className="p-8 text-center text-destructive flex flex-col items-center">
             <AlertCircle className="mb-2" />
             Error loading resolutions: {error instanceof Error ? error.message : "Unknown error"}
          </div>
        ) : !resolutions || resolutions.length === 0 ? (
          <div className="p-8 text-center text-muted-foreground">No resolutions pending review.</div>
        ) : (
          <table className="w-full text-sm text-left">
            <thead className="bg-secondary/50 text-muted-foreground border-b border-border">
              <tr>
                <th className="px-6 py-4 font-medium">Candidate Match</th>
                <th className="px-6 py-4 font-medium">Strategy</th>
                <th className="px-6 py-4 font-medium">Confidence Score</th>
                <th className="px-6 py-4 font-medium text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border">
              {resolutions.map((res: any) => (
                <tr key={res.id} className="hover:bg-secondary/20 transition-colors">
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-md bg-secondary flex items-center justify-center shrink-0">
                        <Merge size={20} className="text-muted-foreground" />
                      </div>
                      <div>
                        <div className="font-medium text-foreground">{res.candidateName}</div>
                        <div className="text-xs text-muted-foreground">Matches: {res.targetName}</div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-muted-foreground font-mono text-xs">
                    {res.strategy}
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2">
                      <AlertCircle size={14} className={res.score > 80 ? 'text-verified' : 'text-inference'} />
                      <span>{res.score}% Match</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <Link 
                      to={`/resolution/${res.id}`}
                      className="inline-flex items-center justify-center px-4 py-2 text-sm font-medium transition-colors rounded-md bg-primary hover:bg-primary/90 text-primary-foreground"
                    >
                      Compare Evidence
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}
