import React from 'react';
import { useTab } from '@/contexts/TabContext';
import { PortfolioContent } from './PortfolioContent';
import { PolicyProgramContent } from './PolicyProgramContent';
import { DisbursementTriggersContent } from './DisbursementTriggersContent';
import {
  TabTextContainer,
  TabsWrapper,
  TabsInnerContainer,
  TabStyledWrapper,
  TabTextParagraph,
} from './styled';

export function TabText({ children }: { children: React.ReactNode }) {
  return (
    <TabTextContainer>
      <TabTextParagraph>{children}</TabTextParagraph>
    </TabTextContainer>
  );
}

export function CatDDOTabs() {
  const { activeTab, setActiveTab } = useTab();

  const tabs = [
    {
      id: 'portfolio',
      label: <TabText>DPF Cat DDO Portfolio</TabText>,
      content: <PortfolioContent />,
    },
    {
      id: 'policy',
      label: <TabText>DPF Cat DDO Policy Program</TabText>,
      content: <PolicyProgramContent />,
    },
    {
      id: 'triggers',
      label: <TabText>DPF Cat DDO Disbursement Triggers</TabText>,
      content: <DisbursementTriggersContent />,
    },
  ];

  return (
    <TabsWrapper>
      <TabsInnerContainer>
        <TabStyledWrapper
          tabs={tabs}
          defaultActiveTabId="portfolio"
          activeTabId={activeTab}
          onTabChange={setActiveTab}
        />
      </TabsInnerContainer>
    </TabsWrapper>
  );
}

export default CatDDOTabs;
