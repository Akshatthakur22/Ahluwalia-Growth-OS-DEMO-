import React from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

export const Input: React.FC<InputProps> = ({ label, error, className = '', ...props }) => (
  <div className="flex flex-col gap-1.5">
    {label && <label className="text-sm font-medium text-gray-700">{label}</label>}
    <input
      className={`demo-input ${error ? 'border-red-400' : ''} ${className}`}
      {...props}
    />
    {error && <span className="text-sm text-red-600">{error}</span>}
  </div>
);
