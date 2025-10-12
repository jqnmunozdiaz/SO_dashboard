import { useState, useEffect } from 'react';

const WELCOME_MODAL_KEY = 'welcome-modal-dismissed';

export const useWelcomeModal = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true);

    const hasSeenModal = localStorage.getItem(WELCOME_MODAL_KEY);

    if (!hasSeenModal) {
      setIsOpen(true);
    }
  }, []);

  const handleClose = () => {
    setIsOpen(false);
    if (isClient) {
      localStorage.setItem(WELCOME_MODAL_KEY, 'true');
    }
  };

  const resetModal = () => {
    if (isClient) {
      localStorage.removeItem(WELCOME_MODAL_KEY);
      setIsOpen(true);
    }
  };

  return {
    isOpen,
    onClose: handleClose,
    resetModal,
  };
};
