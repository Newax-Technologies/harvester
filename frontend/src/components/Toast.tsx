import {
  createContext,
  useCallback,
  useContext,
  useState,
  type ReactNode,
} from "react";

interface ToastMessage {
  id: number;
  msg: string;
  ok: boolean;
}

interface ToastContextValue {
  showToast: (msg: string, ok: boolean) => void;
}

const ToastContext = createContext<ToastContextValue | null>(null);

/**
 * Generalizes ManualLeadDrawer's original local toast state (a single
 * message, `absolute bottom-20` positioned relative to the drawer) into a
 * fixed-position, stackable, app-wide toast so every new mutation
 * (Compliance, Verification, Daily Selection, Outbox, ...) can report
 * success/error without re-inventing this per page. Mount once at the app
 * root (see App.tsx).
 */
export function ToastProvider({ children }: { children: ReactNode }) {
  const [toasts, setToasts] = useState<ToastMessage[]>([]);

  const showToast = useCallback((msg: string, ok: boolean) => {
    const id = Date.now() + Math.random();
    setToasts((prev) => [...prev, { id, msg, ok }]);
    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id));
    }, 4000);
  }, []);

  return (
    <ToastContext.Provider value={{ showToast }}>
      {children}
      <div className="fixed bottom-6 right-6 z-[100] flex flex-col gap-2 max-w-sm">
        {toasts.map((t) => (
          <div
            key={t.id}
            className={`px-4 py-3 rounded-lg text-sm font-medium border shadow-xl animate-in slide-in-from-bottom-2 duration-200 ${
              t.ok
                ? "bg-green-950 border-green-600/50 text-green-300"
                : "bg-red-950 border-red-600/50 text-red-300"
            }`}
          >
            {t.msg}
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
}

export function useToast(): ToastContextValue {
  const ctx = useContext(ToastContext);
  if (!ctx) throw new Error("useToast must be used within a ToastProvider");
  return ctx;
}
