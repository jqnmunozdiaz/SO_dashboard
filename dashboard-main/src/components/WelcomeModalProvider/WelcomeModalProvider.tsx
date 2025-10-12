'use client';

import React from 'react';
import WelcomeModal from '../WelcomeModal';
import { useWelcomeModal } from '@/hooks/useWelcomeModal';

interface WelcomeModalProviderProps {
  children: React.ReactNode;
}

const WelcomeModalProvider: React.FC<WelcomeModalProviderProps> = ({
  children,
}) => {
  const { isOpen, onClose } = useWelcomeModal();

  return (
    <>
      {children}
      <WelcomeModal isOpen={isOpen} onClose={onClose} />
    </>
  );
};

export default WelcomeModalProvider;
