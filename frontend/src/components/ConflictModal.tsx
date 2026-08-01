import { AlertTriangle } from "lucide-react";

interface ConflictModalProps {
  expected: number;
  current: number;
  description: string;
  onReload: () => void;
}

/** Pairs with hooks/useVersionedMutation.ts -- see its docstring. */
export function ConflictModal({
  expected,
  current,
  description,
  onReload,
}: ConflictModalProps) {
  return (
    <div className="absolute inset-0 z-50 bg-background/80 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-card border border-border rounded-xl shadow-lg max-w-md w-full p-6 animate-in fade-in zoom-in-95 duration-200">
        <div className="flex items-center gap-3 text-destructive mb-4">
          <AlertTriangle size={24} />
          <h3 className="text-lg font-semibold text-foreground">
            Update Conflict Detected
          </h3>
        </div>

        <div className="space-y-4 mb-6 text-sm text-muted-foreground">
          <p>{description}</p>
          <div className="bg-muted p-3 rounded-md border border-border space-y-2">
            <div className="flex justify-between">
              <span>Your version:</span>
              <span className="font-mono bg-background px-1.5 py-0.5 rounded text-foreground">
                v{expected}
              </span>
            </div>
            <div className="flex justify-between">
              <span>Current server version:</span>
              <span className="font-mono bg-background px-1.5 py-0.5 rounded text-foreground">
                v{current}
              </span>
            </div>
          </div>
          <p>
            To prevent overwriting someone else's work, your changes have been
            blocked. Please refresh to see the latest version before taking
            action.
          </p>
        </div>

        <div className="flex justify-end gap-3">
          <button
            onClick={onReload}
            className="inline-flex items-center justify-center px-4 py-2 text-sm font-medium transition-colors rounded-md bg-primary hover:bg-primary/90 text-primary-foreground"
          >
            Reload Latest Version
          </button>
        </div>
      </div>
    </div>
  );
}
