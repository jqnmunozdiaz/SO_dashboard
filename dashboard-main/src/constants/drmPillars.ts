export const DRM_PILLAR_ORDER: string[] = [
  'DRM policies and institutions',
  'Mainstreaming DRM into national development plans',
  'Risk Identification',
  'Territorial and urban planning',
  'Public investment at the central level',
  'Sector-specific risk reduction measures',
  'Early Warning Systems',
  'Emergency Preparedness and Response',
  'Adaptive Social Protection',
  'Fiscal Risk',
  'Disaster Risk Financing strategies and instruments',
  'Resilient Reconstruction',
];

export const makeDrmPillarComparator = () => {
  const index = new Map<string, number>(
    DRM_PILLAR_ORDER.map((p, i) => [p.toLowerCase(), i])
  );
  return (a: string, b: string) => {
    const ai = index.get(a.toLowerCase());
    const bi = index.get(b.toLowerCase());
    const aIn = ai !== undefined;
    const bIn = bi !== undefined;
    if (aIn && bIn) return (ai as number) - (bi as number);
    if (aIn) return -1;
    if (bIn) return 1;
    return a.toLowerCase().localeCompare(b.toLowerCase());
  };
};

export const DRM_PILLAR_COLORS: Record<string, string> = {
  'Legal and Institutional DRM Framework': '#e4a3a3',
  'DRM policies and institutions': '#e4a3a3',
  'Mainstreaming DRM into national development plans': '#e4a3a3',
  'Risk Identification': '#e4e4a3',
  'Risk Reduction': '#a3e4a3',
  'Territorial and urban planning': '#a3e4a3',
  'Public investment at the central level': '#a3e4a3',
  'Sector-specific risk reduction measures': '#a3e4a3',
  Preparedness: '#a3e4e4',
  'Early Warning Systems': '#a3e4e4',
  'Emergency Preparedness and Response': '#a3e4e4',
  'Adaptive Social Protection': '#a3e4e4',
  'Financial Protection': '#a3a3e4',
  'Fiscal Risk': '#a3a3e4',
  'Disaster Risk Financing strategies and instruments': '#a3a3e4',
  'Resilient Reconstruction': '#e4a3e4',
};
