import * as React from 'react';
import { TableFundingDDO } from './components';
import {
  OverViewWrapper,
  OverViewContainer,
  OverViewTitle,
  ContentWrapper,
  BulletPointsContainer,
  BulletPoint,
  SemiboldText,
} from './styled/OverViewCatDDO.styled';

export const OverViewCatDDO = () => {
  return (
    <OverViewWrapper>
      <OverViewContainer>
        <OverViewTitle>
          Financial overview of DPF Cat DDOs per funding source (US$ million)
        </OverViewTitle>

        <ContentWrapper>
          <TableFundingDDO />

          <BulletPointsContainer>
            <BulletPoint>
              DPF Cat DDOs have disbursed a total of{' '}
              <SemiboldText>US$4.9 billion.</SemiboldText>
            </BulletPoint>
            <BulletPoint>
              There is an undisbursed balance of{' '}
              <SemiboldText>US$1.5 billion</SemiboldText> available for
              responding to catastrophes including public health-related
              emergencies. Of the undisbursed amount,{' '}
              <SemiboldText>US$589 million (38%)</SemiboldText> is allocated to
              EAP and <SemiboldText>US$451 million (29%)</SemiboldText> to LAC.
            </BulletPoint>
            <BulletPoint>
              While IBRD countries account for larger undisbursed commitments{' '}
              <SemiboldText>(76% against 24% for IDA countries)</SemiboldText>,
              there has been a notable increase in the use of DPF Cat DDOs to
              support IDA countries since 2018.
            </BulletPoint>
            <BulletPoint>
              <SemiboldText>10 DPF Cat DDOs</SemiboldText> totaling US are under
              preparation in IDA countries, compared to{' '}
              <SemiboldText>5</SemiboldText>{' '}
              <SemiboldText>operations amounting</SemiboldText> to US for IBRD
              countries.
            </BulletPoint>
          </BulletPointsContainer>
        </ContentWrapper>
      </OverViewContainer>
    </OverViewWrapper>
  );
};

export default OverViewCatDDO;
