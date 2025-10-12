'use client';

import React, { createContext, useContext, useState, ReactNode } from 'react';

export type TabId = 'portfolio' | 'policy' | 'triggers';

interface TabContextType {
  activeTab: TabId;
  setActiveTab: (tab: TabId) => void;
}

const TabContext = createContext<TabContextType | undefined>(undefined);

interface TabProviderProps {
  children: ReactNode;
}

export function TabProvider({ children }: TabProviderProps) {
  const [activeTab, setActiveTab] = useState<TabId>('portfolio');

  const value: TabContextType = {
    activeTab,
    setActiveTab,
  };

  return <TabContext.Provider value={value}>{children}</TabContext.Provider>;
}

export function useTab() {
  const context = useContext(TabContext);
  if (context === undefined) {
    throw new Error('useTab must be used within a TabProvider');
  }
  return context;
}
