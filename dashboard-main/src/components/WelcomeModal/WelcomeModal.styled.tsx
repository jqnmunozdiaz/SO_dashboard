'use client';

import type { ReactNode } from 'react';
import classNames from 'classnames';
import { Image } from 'vizonomy';

interface ChildrenProps {
  children: ReactNode;
}

export function ModalContent({
  children,
  className,
}: ChildrenProps & { className?: string }) {
  const containerClasses = classNames(
    'bg-white box-border content-stretch flex flex-col gap-2.5 items-start justify-start overflow-clip px-8 py-[41px] relative rounded-xl size-full',
    className
  );
  return <div className={containerClasses}>{children}</div>;
}

export function ContentWrapper({
  children,
  className,
}: ChildrenProps & { className?: string }) {
  const wrapperClasses = classNames(
    'content-stretch flex gap-8 items-center justify-start relative size-full',
    className
  );
  return <div className={wrapperClasses}>{children}</div>;
}

export function TextSection({
  children,
  className,
}: ChildrenProps & { className?: string }) {
  const sectionClasses = classNames(
    'content-stretch flex flex-col gap-6 items-start justify-start relative shrink-0 w-[400px]',
    className
  );
  return <div className={sectionClasses}>{children}</div>;
}

export function TextContainer({
  children,
  className,
}: ChildrenProps & { className?: string }) {
  const containerClasses = classNames(
    'content-stretch flex flex-col font-normal gap-2 items-start justify-start leading-[0] relative shrink-0 text-[#295e84] w-full',
    className
  );
  return <div className={containerClasses}>{children}</div>;
}

export function TitleContainer({
  children,
  className,
}: ChildrenProps & { className?: string }) {
  const containerClasses = classNames(
    'content-stretch flex flex-col items-start justify-start relative shrink-0 w-full',
    className
  );
  return <div className={containerClasses}>{children}</div>;
}

export function DisclaimerText({
  children,
  className,
}: ChildrenProps & { className?: string }) {
  const textClasses = classNames(
    'font-["Inter:Regular",_sans-serif] not-italic relative shrink-0 text-[12px] tracking-[-0.15px] w-[356px] leading-[18px]',
    className
  );
  return <div className={textClasses}>{children}</div>;
}

export function WelcomeTitle({
  children,
  className,
}: ChildrenProps & { className?: string }) {
  const titleClasses = classNames(
    'font-["Roboto:Bold",_sans-serif] font-bold leading-[40px] text-[32px] text-[#295e84]',
    className
  );
  return <div className={titleClasses}>{children}</div>;
}

export function DescriptionText({
  children,
  className,
}: ChildrenProps & { className?: string }) {
  const textClasses = classNames(
    'font-["Inter:Regular",_sans-serif] not-italic relative shrink-0 text-[14px] tracking-[-0.15px] w-full leading-[21px] text-[#295e84]',
    className
  );
  return <div className={textClasses}>{children}</div>;
}

export function EnterButton({
  children,
  onClick,
  className,
}: ChildrenProps & { onClick: () => void; className?: string }) {
  const buttonClasses = classNames(
    'bg-[#295e84] box-border content-stretch flex gap-2.5 items-center justify-center overflow-clip px-6 py-[13px] relative rounded-[99px] shrink-0 w-[116px] cursor-pointer hover:bg-[#1e4a6b] transition-colors',
    className
  );
  return (
    <div className={buttonClasses} onClick={onClick}>
      {children}
    </div>
  );
}

export function ButtonText({
  children,
  className,
}: ChildrenProps & { className?: string }) {
  const textClasses = classNames(
    'font-["Inter:Bold",_sans-serif] font-bold leading-[0] not-italic relative shrink-0 text-[#ffffff] text-[14px] text-nowrap tracking-[-0.15px]',
    className
  );
  return <div className={textClasses}>{children}</div>;
}

export function LogoSection({
  children,
  className,
}: ChildrenProps & { className?: string }) {
  const sectionClasses = classNames(
    'relative flex-1 h-full flex flex-col justify-center',
    className
  );
  return <div className={sectionClasses}>{children}</div>;
}

export function LogoGrid({
  children,
  className,
}: ChildrenProps & { className?: string }) {
  const gridClasses = classNames('flex flex-col', className);
  return <div className={gridClasses}>{children}</div>;
}

export function LogoRow({
  children,
  className,
}: ChildrenProps & { className?: string }) {
  const rowClasses = classNames('flex items-start gap-4 mb-4', className);
  return <div className={rowClasses}>{children}</div>;
}

export function LogoItem({
  children,
  className,
}: ChildrenProps & { className?: string }) {
  const itemClasses = classNames('flex-shrink-0', className);
  return <div className={itemClasses}>{children}</div>;
}

export function LogoBottomRow({
  children,
  className,
}: ChildrenProps & { className?: string }) {
  const rowClasses = classNames('flex justify-start', className);
  return <div className={rowClasses}>{children}</div>;
}

export function LogoImage({
  src,
  alt,
  className,
}: {
  src: string;
  alt: string;
  className?: string;
}) {
  const imageClasses = classNames('h-auto w-auto object-contain', className);
  return <Image src={src} alt={alt} className={imageClasses} />;
}

export function ButtonContainer({
  children,
  className,
}: ChildrenProps & { className?: string }) {
  const containerClasses = classNames('flex justify-center', className);
  return <div className={containerClasses}>{children}</div>;
}
