'use client';

import {
  DashboardContainer,
  DashboardWrapper,
  MainDashboardSection,
} from './Welcome.styled';
import { DashboardHero } from '@/components/Dashboard/DashboardHero';
import { CatDDOTabs } from '@/components/CatDDO';

export function Welcome() {
  return (
    <DashboardContainer>
      <DashboardWrapper>
        <MainDashboardSection>
          <DashboardHero />
        </MainDashboardSection>
      </DashboardWrapper>
      <CatDDOTabs />
    </DashboardContainer>
  );
}
