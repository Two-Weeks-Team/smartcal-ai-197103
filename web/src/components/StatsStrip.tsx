"use client";
import { SparklesIcon, BoltIcon, ChatBubbleOvalLeftEllipsisIcon } from '@heroicons/react/24/outline';

const stats = [
  { label: 'AI Accuracy', value: '≈ 92%', icon: SparklesIcon },
  { label: 'Log Speed', value: '< 2s', icon: BoltIcon },
  { label: 'User Love', value: '4.9/5 ★', icon: ChatBubbleOvalLeftEllipsisIcon }
];

export default function StatsStrip() {
  return (
    <div className="flex justify-between border-t border-b border-muted py-4 mt-6">
      {stats.map((stat, i) => (
        <div key={i} className="flex items-center gap-2 text-sm">
          <stat.icon className="h-5 w-5 text-primary" />
          <span className="font-medium">{stat.label}:</span>
          <span>{stat.value}</span>
        </div>
      ))}
    </div>
  );
}
