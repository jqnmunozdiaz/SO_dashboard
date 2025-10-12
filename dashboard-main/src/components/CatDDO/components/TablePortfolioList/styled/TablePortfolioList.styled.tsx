import type { ReactNode } from 'react';

interface TableLinkProps {
  href: string;
  children: ReactNode;
}

export function TableLink({ href, children }: TableLinkProps) {
  return (
    <a
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      className="text-[#1890ff] underline hover:text-[#40a9ff] transition-colors duration-200 cursor-pointer font-['Inter:Regular',_sans-serif] font-normal text-[14px] leading-normal tracking-[-0.154px] break-all"
    >
      {children}
    </a>
  );
}
