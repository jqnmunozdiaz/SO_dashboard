import type { ReactNode } from 'react';

interface ChildrenProps {
  children: ReactNode;
}

export function DashboardContainer({ children }: ChildrenProps) {
  return <main className="w-full min-h-screen flex flex-col">{children}</main>;
}

export function DashboardWrapper({ children }: ChildrenProps) {
  return <div className="w-full flex-shrink-0">{children}</div>;
}

export function MainDashboardSection({ children }: ChildrenProps) {
  return <div className="w-full bg-white">{children}</div>;
}

export function DashboardInnerContainer({ children }: ChildrenProps) {
  return <div className="max-w-7xl mx-auto px-8">{children}</div>;
}

export function HeroWrapper({ children }: ChildrenProps) {
  return (
    <div className="w-full flex flex-col lg:flex-row min-h-[400px]">
      {children}
    </div>
  );
}

export function TextContentSection({ children }: ChildrenProps) {
  return (
    <div className="flex-1 lg:flex-[0_0_50%] p-8 lg:p-16 flex flex-col justify-center">
      {children}
    </div>
  );
}

export function TitleSection({ children }: ChildrenProps) {
  return <div className="mb-6">{children}</div>;
}

export function DashboardTitle({ children }: ChildrenProps) {
  return (
    <h1 className="font-semibold text-2xl md:text-3xl lg:text-[40px] leading-tight lg:leading-[48px] text-[#295e84] tracking-[-0.64px]">
      {children}
    </h1>
  );
}

export function DescriptionSection({ children }: ChildrenProps) {
  return <div>{children}</div>;
}

export function DescriptionParagraph({ children }: ChildrenProps) {
  return (
    <p className="font-normal text-sm lg:text-[14px] leading-relaxed lg:leading-[24px] text-[#295e84] mb-3.5">
      {children}
    </p>
  );
}

export function DescriptionParagraphLast({ children }: ChildrenProps) {
  return (
    <p className="font-normal text-sm lg:text-[14px] leading-relaxed lg:leading-[24px] text-[#295e84]">
      {children}
    </p>
  );
}

export function ItalicText({ children }: ChildrenProps) {
  return <span className="font-normal italic">{children}</span>;
}

export function BoldText({ children }: ChildrenProps) {
  return <span className="font-bold">{children}</span>;
}

export function MapVisualizationSection({ children }: ChildrenProps) {
  return (
    <div className="flex-1 lg:flex-[0_0_50%] relative min-h-[250px] md:min-h-[300px] lg:min-h-[400px] overflow-hidden">
      {children}
    </div>
  );
}

export function BackgroundMapContainer() {
  return (
    <div
      className="absolute inset-0 w-full h-full bg-center bg-contain md:bg-cover bg-no-repeat opacity-[0.08] scale-110"
      style={{
        backgroundImage: "url('/world-map-dashboard.png')",
      }}
    />
  );
}

export function MainMapContainer() {
  return (
    <div
      className="absolute inset-2 md:inset-4 lg:inset-8 bg-center bg-contain md:bg-cover bg-no-repeat"
      style={{
        backgroundImage: "url('/world-map-dashboard.png')",
      }}
    />
  );
}
