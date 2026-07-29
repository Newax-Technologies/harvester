import { useState, useCallback } from "react";
import {
  X,
  Plus,
  Trash2,
  Building2,
  MapPin,
  Phone,
  Loader2,
  CheckCircle2,
} from "lucide-react";

// ─── Types ───────────────────────────────────────────────────────────────────

interface ContactEntry {
  contact_type: string;
  contact_value: string;
  person_name: string;
  role: string;
}

interface ManualLeadPayload {
  institution_name: string;
  institution_type: string;
  website: string | null;
  operating_status: string;
  address: string;
  city: string;
  country: string;
  contacts: ContactEntry[];
  notes: string | null;
  lead_source_note: string | null;
}

const CONTACT_TYPES = [
  { value: "phone", label: "📞 Phone" },
  { value: "email", label: "📧 Email" },
  { value: "whatsapp", label: "💬 WhatsApp" },
  { value: "linkedin", label: "🔗 LinkedIn" },
  { value: "other", label: "· Other" },
];

const INSTITUTION_TYPES = [
  "school",
  "college",
  "university",
  "academy",
  "clinic",
  "hospital",
  "ngo",
  "company",
  "other",
];

const STATUS_OPTIONS = [
  {
    value: "operational",
    label: "Operational",
    color: "text-green-400  border-green-500/40  bg-green-500/10",
  },
  {
    value: "closed_temporarily",
    label: "Temp. Closed",
    color: "text-yellow-400 border-yellow-500/40 bg-yellow-500/10",
  },
  {
    value: "closed_permanently",
    label: "Closed",
    color: "text-red-400    border-red-500/40    bg-red-500/10",
  },
  {
    value: "unknown",
    label: "Unknown",
    color: "text-zinc-400   border-zinc-600      bg-zinc-800",
  },
];

const API_URL = "http://localhost:8000/api/v1/leads/manual";
const DEV_TOKEN = "secret-reviewer-token";

function emptyContact(): ContactEntry {
  return {
    contact_type: "phone",
    contact_value: "",
    person_name: "",
    role: "",
  };
}

// ─── Main drawer component ────────────────────────────────────────────────────

interface ManualLeadDrawerProps {
  open: boolean;
  onClose: () => void;
  onSuccess?: (name: string) => void;
}

export function ManualLeadDrawer({
  open,
  onClose,
  onSuccess,
}: ManualLeadDrawerProps) {
  // Form state
  const [name, setName] = useState("");
  const [type, setType] = useState("school");
  const [website, setWebsite] = useState("");
  const [status, setStatus] = useState("operational");
  const [address, setAddress] = useState("");
  const [city, setCity] = useState("");
  const [contacts, setContacts] = useState<ContactEntry[]>([emptyContact()]);
  const [sourceNote, setSourceNote] = useState("");
  const [notes, setNotes] = useState("");

  // UI state
  const [submitting, setSubmitting] = useState(false);
  const [toast, setToast] = useState<{ msg: string; ok: boolean } | null>(null);

  const showToast = (msg: string, ok: boolean) => {
    setToast({ msg, ok });
    setTimeout(() => setToast(null), 4000);
  };

  const resetForm = useCallback(() => {
    setName("");
    setType("school");
    setWebsite("");
    setStatus("operational");
    setAddress("");
    setCity("");
    setSourceNote("");
    setNotes("");
    setContacts([emptyContact()]);
  }, []);

  const handleClose = () => {
    resetForm();
    onClose();
  };

  // Contact helpers
  const updateContact = (i: number, field: keyof ContactEntry, val: string) =>
    setContacts((prev) =>
      prev.map((c, idx) => (idx === i ? { ...c, [field]: val } : c)),
    );

  const removeContact = (i: number) =>
    setContacts((prev) =>
      prev.length > 1 ? prev.filter((_, idx) => idx !== i) : prev,
    );

  // Submit
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const validContacts = contacts.filter((c) => c.contact_value.trim());
    if (!name.trim()) {
      showToast("Institution name is required.", false);
      return;
    }
    if (!validContacts.length) {
      showToast("Add at least one contact.", false);
      return;
    }

    const payload: ManualLeadPayload = {
      institution_name: name.trim(),
      institution_type: type,
      website: website.trim() || null,
      operating_status: status,
      address: address.trim(),
      city: city.trim(),
      country: "Pakistan",
      contacts: validContacts.map((c) => ({
        contact_type: c.contact_type,
        contact_value: c.contact_value.trim(),
        person_name: c.person_name.trim() || (null as any),
        role: c.role.trim() || (null as any),
      })),
      notes: notes.trim() || null,
      lead_source_note: sourceNote.trim() || null,
    };

    setSubmitting(true);
    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${DEV_TOKEN}`,
        },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      if (res.ok) {
        showToast(`✓ "${data.institution_name}" saved!`, true);
        onSuccess?.(data.institution_name);
        resetForm();
      } else {
        showToast(
          data?.error?.message || data?.detail || "Server error.",
          false,
        );
      }
    } catch (err: any) {
      showToast(`Network error: ${err.message}`, false);
    } finally {
      setSubmitting(false);
    }
  };

  // ── Render ──────────────────────────────────────────────────────────────────
  return (
    <>
      {/* Backdrop */}
      <div
        className={`fixed inset-0 z-40 bg-black/60 backdrop-blur-sm transition-opacity duration-300 ${
          open
            ? "opacity-100 pointer-events-auto"
            : "opacity-0 pointer-events-none"
        }`}
        onClick={handleClose}
      />

      {/* Drawer panel */}
      <aside
        className={`fixed top-0 right-0 z-50 h-full w-full max-w-[600px] bg-zinc-950 border-l border-zinc-800
          shadow-2xl flex flex-col transition-transform duration-300 ease-out ${
            open ? "translate-x-0" : "translate-x-full"
          }`}
      >
        {/* Header */}
        <div className="flex items-center gap-3 px-6 py-4 border-b border-zinc-800 shrink-0">
          <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-blue-500 to-violet-600 flex items-center justify-center shadow-lg shadow-blue-500/20">
            <Plus size={18} className="text-white" />
          </div>
          <div>
            <h2 className="text-base font-semibold text-white">
              Add Lead Manually
            </h2>
            <p className="text-xs text-zinc-500">
              Saves to the same pipeline as scrapers
            </p>
          </div>
          <button
            onClick={handleClose}
            className="ml-auto p-1.5 rounded-md text-zinc-500 hover:text-white hover:bg-zinc-800 transition-colors"
          >
            <X size={18} />
          </button>
        </div>

        {/* Scrollable form body */}
        <form
          onSubmit={handleSubmit}
          className="flex-1 overflow-y-auto p-6 space-y-6"
        >
          {/* ── Institution ── */}
          <section>
            <div className="flex items-center gap-2 mb-4">
              <Building2 size={14} className="text-zinc-500" />
              <span className="text-xs font-semibold tracking-widest uppercase text-zinc-500">
                Institution
              </span>
              <div className="flex-1 h-px bg-zinc-800" />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="col-span-2">
                <label className="block text-xs font-medium text-zinc-400 mb-1.5">
                  Name <span className="text-blue-400">*</span>
                </label>
                <input
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="e.g. Beacon House School, DHA Phase 5"
                  className="w-full bg-zinc-900 border border-zinc-700 rounded-md px-3 py-2 text-sm text-white
                    placeholder:text-zinc-600 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500/30
                    transition-colors"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-zinc-400 mb-1.5">
                  Type
                </label>
                <select
                  value={type}
                  onChange={(e) => setType(e.target.value)}
                  className="w-full bg-zinc-900 border border-zinc-700 rounded-md px-3 py-2 text-sm text-white
                    focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500/30 transition-colors capitalize"
                >
                  {INSTITUTION_TYPES.map((t) => (
                    <option key={t} value={t} className="capitalize">
                      {t}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-xs font-medium text-zinc-400 mb-1.5">
                  Website
                </label>
                <input
                  value={website}
                  onChange={(e) => setWebsite(e.target.value)}
                  placeholder="https://..."
                  type="url"
                  className="w-full bg-zinc-900 border border-zinc-700 rounded-md px-3 py-2 text-sm text-white
                    placeholder:text-zinc-600 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500/30
                    transition-colors"
                />
              </div>
              <div className="col-span-2">
                <label className="block text-xs font-medium text-zinc-400 mb-2">
                  Status
                </label>
                <div className="flex gap-2 flex-wrap">
                  {STATUS_OPTIONS.map((s) => (
                    <button
                      key={s.value}
                      type="button"
                      onClick={() => setStatus(s.value)}
                      className={`px-3 py-1.5 rounded-full text-xs font-medium border transition-all ${
                        status === s.value
                          ? s.color
                          : "text-zinc-500 border-zinc-700 bg-transparent hover:border-zinc-500"
                      }`}
                    >
                      {s.label}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </section>

          {/* ── Location ── */}
          <section>
            <div className="flex items-center gap-2 mb-4">
              <MapPin size={14} className="text-zinc-500" />
              <span className="text-xs font-semibold tracking-widest uppercase text-zinc-500">
                Location
              </span>
              <div className="flex-1 h-px bg-zinc-800" />
            </div>
            <div className="grid grid-cols-3 gap-4">
              <div className="col-span-2">
                <label className="block text-xs font-medium text-zinc-400 mb-1.5">
                  Street Address
                </label>
                <input
                  value={address}
                  onChange={(e) => setAddress(e.target.value)}
                  placeholder="Plot 12, Block B, Gulshan-e-Iqbal"
                  className="w-full bg-zinc-900 border border-zinc-700 rounded-md px-3 py-2 text-sm text-white
                    placeholder:text-zinc-600 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500/30
                    transition-colors"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-zinc-400 mb-1.5">
                  City
                </label>
                <input
                  value={city}
                  onChange={(e) => setCity(e.target.value)}
                  placeholder="Karachi"
                  className="w-full bg-zinc-900 border border-zinc-700 rounded-md px-3 py-2 text-sm text-white
                    placeholder:text-zinc-600 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500/30
                    transition-colors"
                />
              </div>
            </div>
          </section>

          {/* ── Contacts ── */}
          <section>
            <div className="flex items-center gap-2 mb-4">
              <Phone size={14} className="text-zinc-500" />
              <span className="text-xs font-semibold tracking-widest uppercase text-zinc-500">
                Contacts
              </span>
              <span className="text-xs text-blue-400 font-medium ml-1">
                · at least one
              </span>
              <div className="flex-1 h-px bg-zinc-800" />
            </div>
            <div className="space-y-3">
              {contacts.map((c, i) => (
                <div
                  key={i}
                  className="grid grid-cols-[130px_1fr_1fr_auto] gap-2 p-3 bg-zinc-900 rounded-lg border border-zinc-800
                    hover:border-zinc-700 transition-colors"
                >
                  <select
                    value={c.contact_type}
                    onChange={(e) =>
                      updateContact(i, "contact_type", e.target.value)
                    }
                    className="bg-zinc-800 border border-zinc-700 rounded px-2 py-1.5 text-xs text-white
                      focus:outline-none focus:border-blue-500 transition-colors"
                  >
                    {CONTACT_TYPES.map((t) => (
                      <option key={t.value} value={t.value}>
                        {t.label}
                      </option>
                    ))}
                  </select>
                  <input
                    value={c.contact_value}
                    onChange={(e) =>
                      updateContact(i, "contact_value", e.target.value)
                    }
                    placeholder="+92 300 1234567"
                    className="bg-zinc-800 border border-zinc-700 rounded px-2 py-1.5 text-xs text-white
                      placeholder:text-zinc-600 focus:outline-none focus:border-blue-500 transition-colors"
                  />
                  <input
                    value={c.person_name}
                    onChange={(e) =>
                      updateContact(i, "person_name", e.target.value)
                    }
                    placeholder="Name & Role (optional)"
                    className="bg-zinc-800 border border-zinc-700 rounded px-2 py-1.5 text-xs text-white
                      placeholder:text-zinc-600 focus:outline-none focus:border-blue-500 transition-colors"
                  />
                  <button
                    type="button"
                    onClick={() => removeContact(i)}
                    className="p-1.5 rounded text-zinc-600 hover:text-red-400 hover:bg-red-500/10 transition-colors"
                  >
                    <Trash2 size={13} />
                  </button>
                </div>
              ))}
              <button
                type="button"
                onClick={() => setContacts((prev) => [...prev, emptyContact()])}
                className="w-full flex items-center justify-center gap-2 py-2.5 rounded-lg border border-dashed
                  border-zinc-700 text-zinc-500 hover:text-blue-400 hover:border-blue-500/50 hover:bg-blue-500/5
                  text-xs font-medium transition-all"
              >
                <Plus size={13} /> Add another contact
              </button>
            </div>
          </section>

          {/* ── Notes ── */}
          <section>
            <div className="flex items-center gap-2 mb-4">
              <span className="text-xs font-semibold tracking-widest uppercase text-zinc-500">
                Notes
              </span>
              <div className="flex-1 h-px bg-zinc-800" />
            </div>
            <div className="space-y-3">
              <div>
                <label className="block text-xs font-medium text-zinc-400 mb-1.5">
                  Source
                </label>
                <input
                  value={sourceNote}
                  onChange={(e) => setSourceNote(e.target.value)}
                  placeholder="How did you find this? e.g. Cold call, Referral from Ahmed, Field visit"
                  className="w-full bg-zinc-900 border border-zinc-700 rounded-md px-3 py-2 text-sm text-white
                    placeholder:text-zinc-600 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500/30
                    transition-colors"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-zinc-400 mb-1.5">
                  Additional Notes
                </label>
                <textarea
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  placeholder="Decision-maker info, budget signals, pain points, next steps..."
                  rows={3}
                  className="w-full bg-zinc-900 border border-zinc-700 rounded-md px-3 py-2 text-sm text-white
                    placeholder:text-zinc-600 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500/30
                    resize-none transition-colors"
                />
              </div>
            </div>
          </section>

          {/* Spacer so last field isn't hidden behind the footer */}
          <div className="h-4" />
        </form>

        {/* Footer */}
        <div className="px-6 py-4 border-t border-zinc-800 bg-zinc-950 shrink-0 flex items-center gap-3">
          <button
            type="submit"
            form="" // handled via onSubmit on the form
            onClick={handleSubmit}
            disabled={submitting}
            className="flex items-center gap-2 px-5 py-2.5 rounded-lg text-sm font-semibold text-white
              bg-gradient-to-r from-blue-600 to-violet-600 hover:from-blue-500 hover:to-violet-500
              disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg shadow-blue-500/20
              hover:shadow-blue-500/30 hover:-translate-y-px active:translate-y-0"
          >
            {submitting ? (
              <>
                <Loader2 size={15} className="animate-spin" /> Saving…
              </>
            ) : (
              <>
                <CheckCircle2 size={15} /> Save Lead
              </>
            )}
          </button>
          <button
            type="button"
            onClick={resetForm}
            className="px-4 py-2.5 rounded-lg text-sm font-medium text-zinc-400 border border-zinc-700
              hover:border-zinc-500 hover:text-white transition-colors"
          >
            Clear
          </button>
          <span className="text-xs text-zinc-600 ml-auto">
            Saves to canonical pipeline
          </span>
        </div>

        {/* Toast */}
        {toast && (
          <div
            className={`absolute bottom-20 left-6 right-6 px-4 py-3 rounded-lg text-sm font-medium
            border shadow-xl animate-in slide-in-from-bottom-2 duration-200 ${
              toast.ok
                ? "bg-green-950 border-green-600/50 text-green-300"
                : "bg-red-950  border-red-600/50  text-red-300"
            }`}
          >
            {toast.msg}
          </div>
        )}
      </aside>
    </>
  );
}
