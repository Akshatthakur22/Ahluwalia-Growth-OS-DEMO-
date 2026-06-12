import { ReactNode } from 'react';

export function FormSection({ title, children }: { title: string; children: ReactNode }) {
  return (
    <div className="space-y-3 pt-2 first:pt-0">
      <h4 className="text-xs font-semibold text-gray-400 uppercase tracking-wider border-b border-gray-100 pb-2">
        {title}
      </h4>
      {children}
    </div>
  );
}
