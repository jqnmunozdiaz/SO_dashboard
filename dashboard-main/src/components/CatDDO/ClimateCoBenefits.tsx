import * as React from 'react';
import { StandaloneChart, MixedDPOChart } from './components';
import {
  ClimateWrapper,
  ClimateContainer,
  ClimateTitle,
  ClimateContentWrapper,
  ClimateBulletPointsContainer,
  ClimateBulletPoint,
  ClimateSubBulletPointsContainer,
  ClimateSubBulletPoint,
  ClimateChartsContainer,
} from './styled';
import { SemiboldText } from './styled';

export const ClimateCoBenefits = () => {
  return (
    <ClimateWrapper>
      <ClimateContainer>
        <ClimateTitle>Climate Co-Benefits</ClimateTitle>

        <ClimateContentWrapper>
          <ClimateBulletPointsContainer>
            <ClimateBulletPoint>
              On average, DPF Cat DDO financing achieves{' '}
              <SemiboldText>63% climate co-benefits</SemiboldText>, driven
              predominantly by adaptation.
              <ClimateSubBulletPointsContainer>
                <ClimateSubBulletPoint>
                  When implemented as standalone contingent-financing
                  operations, DPF Cat DDOs are significantly more effective,
                  achieving an average of{' '}
                  <SemiboldText>81% climate co-benefits</SemiboldText>.
                </ClimateSubBulletPoint>
                <ClimateSubBulletPoint>
                  In comparison, operations attain only{' '}
                  <SemiboldText>36%</SemiboldText> when integrating a DPF DPF
                  Cat DDO into a DPO ("mixed DPO") that combines upfront budget
                  support with catastrophe-contingent financing.
                </ClimateSubBulletPoint>
              </ClimateSubBulletPointsContainer>
            </ClimateBulletPoint>
          </ClimateBulletPointsContainer>

          <ClimateChartsContainer>
            <StandaloneChart />
            <MixedDPOChart />
          </ClimateChartsContainer>
        </ClimateContentWrapper>
      </ClimateContainer>
    </ClimateWrapper>
  );
};

export default ClimateCoBenefits;
