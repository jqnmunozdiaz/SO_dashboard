import type { ReactNode } from 'react';

interface ChildrenProps {
  children: ReactNode;
}

export function LayoutContainer({ children }: ChildrenProps) {
  return (
    <div className="flex h-screen bg-gray-50 overflow-hidden">{children}</div>
  );
}

export function Sidebar({ children }: ChildrenProps) {
  return (
    <aside className="w-64 bg-white shadow-sm border-r border-gray-200 flex-shrink-0 h-full overflow-y-auto">
      {children}
    </aside>
  );
}

export function SidebarContent({ children }: ChildrenProps) {
  return <div className="p-6">{children}</div>;
}

export function HeaderContainer({ children }: ChildrenProps) {
  return <div className="flex items-center mb-8">{children}</div>;
}

export function LogoContainer({ children }: ChildrenProps) {
  return (
    <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center mr-3">
      {children}
    </div>
  );
}

export function LogoText({ children }: ChildrenProps) {
  return <span className="text-white text-sm font-bold">{children}</span>;
}

export function TitleContainer({ children }: ChildrenProps) {
  return <div>{children}</div>;
}

export function MainTitle({ children }: ChildrenProps) {
  return <h1 className="text-sm font-semibold text-gray-900">{children}</h1>;
}

export function Subtitle({ children }: ChildrenProps) {
  return <p className="text-xs text-gray-500">{children}</p>;
}

export function Navigation({ children }: ChildrenProps) {
  return <nav className="space-y-6">{children}</nav>;
}

export function FilterSection({ children }: ChildrenProps) {
  return <div>{children}</div>;
}

export function FilterTitle({ children }: ChildrenProps) {
  return <h3 className="text-sm font-medium text-gray-700 mb-3">{children}</h3>;
}

export function FilterList({ children }: ChildrenProps) {
  return <div className="space-y-2">{children}</div>;
}

export function CheckboxLabel({ children }: ChildrenProps) {
  return <label className="flex items-center">{children}</label>;
}

export function CheckboxInput() {
  return <input type="checkbox" className="mr-2" />;
}

export function CheckboxText({ children }: ChildrenProps) {
  return <span className="text-sm text-gray-600">{children}</span>;
}

export function BlueFilterList({ children }: ChildrenProps) {
  return <div className="space-y-2 text-sm text-blue-600">{children}</div>;
}

export function FilterItem({ children }: ChildrenProps) {
  return <div>{children}</div>;
}

export function MainContent({ children }: ChildrenProps) {
  return <main className="flex-1 overflow-y-auto">{children}</main>;
}
