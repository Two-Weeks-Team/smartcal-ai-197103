"use client";
import { ArrowPathIcon, ExclamationTriangleIcon, CheckCircleIcon } from '@heroicons/react/24/outline';

type StatePanelProps = {
  state: 'loading' | 'empty' | 'error' | 'success';
  message?: string;
};

export default function StatePanel({ state, message }: StatePanelProps) {
  const icons = {
    loading: <ArrowPathIcon className="animate-spin h-6 w-6 text-primary" />, 
    empty: <ExclamationTriangleIcon className="h-6 w-6 text-muted" />, 
    error: <ExclamationTriangleIcon className="h-6 w-6 text-warning" />, 
    success: <CheckCircleIcon className="h-6 w-6 text-success" />
  };

  const defaultMessages: Record<string, string> = {
    loading: 'Processing…',
    empty: 'No data available.',
    error: 'Something went wrong.',
    success: 'Action completed successfully.'
  };

  return (
    <div className="flex items-center gap-2 text-foreground p-4">
      {icons[state]}
      <span>{message ?? defaultMessages[state]}</span>
    </div>
  );
}
