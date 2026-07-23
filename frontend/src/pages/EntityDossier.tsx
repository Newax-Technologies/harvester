import { useState } from 'react'
import { useParams, Link } from 'react-router'
import { ArrowLeft, Building2, Phone, MapPin, Globe, CheckCircle2, AlertTriangle, FileText, AlertCircle } from 'lucide-react'
import { useQuery } from '@tanstack/react-query'
import { institutionQueries } from '../api/queries'

export function EntityDossier() {
  const { id } = useParams<{ id: string }>()
  const [activeTab, setActiveTab] = useState('overview')

  const { data: dossier, isLoading, isError, error } = useQuery(institutionQueries.detail(id!))

  if (isLoading) return <div className="p-8 text-center text-muted-foreground">Loading dossier...</div>
  if (isError || !dossier) return (
    <div className="p-8 text-center text-destructive flex flex-col items-center">
      <AlertCircle className="mb-2" />
      Error loading dossier: {error instanceof Error ? error.message : "Unknown error"}
    </div>
  )

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      {/* Header */}
      <div>
        <Link to="/institutions" className="inline-flex items-center text-sm text-muted-foreground hover:text-foreground mb-4 transition-colors">
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
                <span className="flex items-center gap-1"><MapPin size={14}/> {dossier.branches?.[0]?.address || 'Unknown'}</span>
                <span className="flex items-center gap-1"><Globe size={14}/> {dossier.domain}</span>
              </div>
            </div>
          </div>
          <Link to={`/readiness/${id}`} className="inline-flex items-center justify-center px-4 py-2 text-sm font-medium transition-colors rounded-md bg-primary hover:bg-primary/90 text-primary-foreground">
            Generate Outreach
          </Link>
        </div>
      </div>

      {/* Tabs */}
      <div className="border-b border-border">
        <nav className="flex space-x-8">
          {['Overview', 'Branches', 'Contacts', 'Research Findings', 'Evidence'].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab.toLowerCase().replace(' ', '-'))}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeTab === tab.toLowerCase().replace(' ', '-')
                  ? 'border-primary text-primary'
                  : 'border-transparent text-muted-foreground hover:text-foreground hover:border-border'
              }`}
            >
              {tab}
            </button>
          ))}
        </nav>
      </div>

      {/* Tab Content */}
      <div className="mt-6">
        {activeTab === 'overview' && (
          <div className="grid grid-cols-3 gap-6">
            <div className="col-span-2 space-y-6">
              <div className="bg-card border border-border rounded-lg p-6">
                <h3 className="text-lg font-semibold mb-4">Research Summary</h3>
                <div className="space-y-4">
                  {(dossier as any).findings?.map((item: any) => (
                    <div key={item.id} className="flex gap-4 p-4 rounded-md border border-border bg-background/50">
                      <div className="shrink-0 mt-1">
                        {item.confidence_score > 80 ? (
                          <CheckCircle2 className="text-verified" size={20} />
                        ) : (
                          <AlertTriangle className="text-inference" size={20} />
                        )}
                      </div>
                      <div>
                        <div className="font-medium text-foreground">{item.finding_value}</div>
                        <div className="text-sm text-muted-foreground mt-1 flex items-center gap-2">
                          <span className="capitalize text-xs font-semibold px-2 py-0.5 rounded bg-secondary">{item.finding_type}</span>
                          <span>· {item.confidence_score}% confidence</span>
                        </div>
                      </div>
                    </div>
                  ))}
                  {(!(dossier as any).findings || (dossier as any).findings.length === 0) && (
                    <div className="text-muted-foreground text-sm">No research findings available.</div>
                  )}
                </div>
              </div>
            </div>
            <div className="space-y-6">
              <div className="bg-card border border-border rounded-lg p-6">
                <h3 className="text-lg font-semibold mb-4">Quick Contacts</h3>
                <div className="space-y-3">
                  {(dossier as any).contacts?.map((contact: any) => (
                    <div key={contact.id} className="flex items-center gap-3 text-sm">
                      <div className="w-8 h-8 rounded-full bg-secondary flex items-center justify-center text-muted-foreground">
                        {contact.contact_type === 'phone' ? <Phone size={14}/> : <FileText size={14}/>}
                      </div>
                      <div>
                        <div className="font-medium text-foreground">{contact.contact_value}</div>
                        <div className="text-xs text-muted-foreground">{contact.role}</div>
                      </div>
                    </div>
                  ))}
                  {(!(dossier as any).contacts || (dossier as any).contacts.length === 0) && (
                    <div className="text-muted-foreground text-sm">No contacts available.</div>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
