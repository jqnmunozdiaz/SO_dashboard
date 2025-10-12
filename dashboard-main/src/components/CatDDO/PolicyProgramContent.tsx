import React from 'react';
import {
  PolicyProgramContainer,
  PolicyProgramTitle,
  ContentContainer,
  DescriptionContainer,
  DescriptionText,
  LinkText,
  DiagramContainer,
  PillarsRow,
  PillarColumn,
  PillarBox,
  SubPillarBox,
  PillarText,
  SubPillarText,
} from './styled';
import PriorActionsResultIndicators from './PriorActionsResultIndicators';
import { WORLD_BANK_DOCUMENT_URL } from './constants/PolicyProgramContent.constants';

export const PolicyProgramContent = () => {
  const pillars = [
    {
      id: 1,
      name: 'Legal and Institutional DRM Framework',
      color: '#e4a3a3',
      lightColor: 'rgba(228, 163, 163, 0.4)',
      subPillars: [
        'DRM policies and institutions',
        'Mainstreaming DRM into national development plans',
      ],
    },
    {
      id: 2,
      name: 'Risk Identification',
      color: '#e4e4a3',
      lightColor: 'rgba(228, 228, 163, 0.4)',
      subPillars: [],
    },
    {
      id: 3,
      name: 'Risk Reduction',
      color: '#a3e4a3',
      lightColor: 'rgba(163, 228, 163, 0.4)',
      subPillars: [
        'Territorial and urban planning',
        'Public investment at the central level',
        'Sector-specific risk reduction measures',
      ],
    },
    {
      id: 4,
      name: 'Preparedness',
      color: '#a3e4e4',
      lightColor: 'rgba(163, 228, 228, 0.4)',
      subPillars: [
        'Early Warning Systems',
        'Emergency Preparedness and Response',
        'Adaptive Social Protection',
      ],
    },
    {
      id: 5,
      name: 'Financial Protection',
      color: '#a3a3e4',
      lightColor: 'rgba(163, 163, 228, 0.4)',
      subPillars: [
        'Fiscal risk',
        'Disaster Risk Financing strategies and instruments',
      ],
    },
    {
      id: 6,
      name: 'Resilient Reconstruction',
      color: '#e4a3e4',
      lightColor: 'rgba(228, 163, 228, 0.4)',
      subPillars: [],
    },
  ];

  return (
    <PolicyProgramContainer>
      <PolicyProgramTitle>The DRM Policy Pillars</PolicyProgramTitle>

      <ContentContainer>
        <DescriptionContainer>
          <DescriptionText>
            To analyze trends and distribution patterns in policy reforms
            supported by DPF Cat DDOs, Prior Actions were classified according
            to the World Bank's DRM framework. Originally proposed by{' '}
            <LinkText href={WORLD_BANK_DOCUMENT_URL}>
              Ghesquiere et al. (2012)
            </LinkText>{' '}
            and fully aligned with the Sendai Framework for DRR, this framework
            comprises six pillars that reflect the key areas of engagement
            typically supported through DPF Cat DDOs. Where relevant, the
            pillars are further disaggregated into sub-pillars to provide
            greater analytical granularity.
          </DescriptionText>

          <DescriptionText>
            The DRM framework offers a standardized structure to map reforms,
            track progress, and identify policy gaps across critical dimensions
            of resilience-building. It also serves as a practical tool to inform
            the design of DRM policy programs that adopt a systems-based
            approach to strengthening resilience. While individual PAs may
            contribute to multiple pillars, a simplifying assumption was applied
            for classification purposes: each DRM-related PA was assigned to a
            single pillar based on predefined keywords and expert judgment.
          </DescriptionText>
        </DescriptionContainer>

        <DiagramContainer>
          <PillarsRow>
            {pillars.map((pillar) => (
              <PillarColumn key={pillar.id}>
                <PillarBox backgroundColor={pillar.color}>
                  <PillarText>{pillar.name}</PillarText>
                </PillarBox>

                {pillar.subPillars.map((subPillar, index) => (
                  <SubPillarBox key={index} backgroundColor={pillar.lightColor}>
                    <SubPillarText>{subPillar}</SubPillarText>
                  </SubPillarBox>
                ))}
              </PillarColumn>
            ))}
          </PillarsRow>
        </DiagramContainer>
      </ContentContainer>

      <PriorActionsResultIndicators />
    </PolicyProgramContainer>
  );
};

export default PolicyProgramContent;
