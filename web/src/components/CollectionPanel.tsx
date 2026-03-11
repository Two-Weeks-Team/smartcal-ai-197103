"use client";
import { ClockIcon } from '@heroicons/react/24/outline';
import clsx from 'clsx';

type CollectionPanelProps = {
  items: any[];
};

export default function CollectionPanel({ items }: CollectionPanelProps) {
  return (
    <ul className="space-y-4">
      {items.map((item, idx) => (
        <li key={idx} className={clsx('card flex items-center gap-3')}> 
          <ClockIcon className="h-5 w-5 text-primary" />
          <div>
            <p className="font-medium text-foreground">{item.name ?? 'Unnamed entry'}</p>
            {item.calories && <p className="text-sm text-muted">{item.calories} kcal</p>}
          </div>
        </li>
      ))}
    </ul>
  );
}
