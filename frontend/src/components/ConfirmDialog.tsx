import { AlertTriangle } from "lucide-react";

interface ConfirmDialogProps {
  open: boolean;
  title: string;
  description: string;
  confirmLabel?: string;
  destructive?: boolean;
  onConfirm: () => void;
  onCancel: () => void;
}

/** For irreversible actions (e.g. Compliance's deletion-request fulfillment). */
export function ConfirmDialog({
  open,
  title,
  description,
  confirmLabel = "Confirm",
  destructive = true,
  onConfirm,
  onCancel,
}: ConfirmDialogProps) {
  if (!open) return null;

  return (
    <div className="fixed inset-0 z-[110] bg-background/80 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-card border border-border rounded-xl shadow-lg max-w-md w-full p-6 animate-in fade-in zoom-in-95 duration-200">
        <div
          className={`flex items-center gap-3 mb-4 ${destructive ? "text-destructive" : "text-foreground"}`}
        >
          <AlertTriangle size={24} />
          <h3 className="text-lg font-semibold text-foreground">{title}</h3>
        </div>
        <p className="text-sm text-muted-foreground mb-6">{description}</p>
        <div className="flex justify-end gap-3">
          <button
            onClick={onCancel}
            className="inline-flex items-center justify-center px-4 py-2 text-sm font-medium rounded-md bg-secondary text-secondary-foreground hover:bg-secondary/80"
          >
            Cancel
          </button>
          <button
            onClick={onConfirm}
            className={`inline-flex items-center justify-center px-4 py-2 text-sm font-medium rounded-md ${
              destructive
                ? "bg-destructive text-destructive-foreground hover:bg-destructive/90"
                : "bg-primary text-primary-foreground hover:bg-primary/90"
            }`}
          >
            {confirmLabel}
          </button>
        </div>
      </div>
    </div>
  );
}
