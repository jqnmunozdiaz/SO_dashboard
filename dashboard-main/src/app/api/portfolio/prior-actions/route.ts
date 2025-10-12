import { NextResponse } from 'next/server';
import { loadPriorActions, loadPortfolioFiltered } from '@/lib/portfolio';
import { parseFiltersFromRequest } from '@/lib/api-utils';
import {
  makeDrmPillarComparator,
  DRM_PILLAR_COLORS,
} from '@/constants/drmPillars';

export const dynamic = 'force-dynamic';

export async function GET(request: Request) {
  try {
    const filters = parseFiltersFromRequest(request);

    const filteredPortfolio = loadPortfolioFiltered(filters);
    const filteredProjectIds = new Set(
      filteredPortfolio
        .map((row) => (row['P#'] ?? '').toString().trim())
        .filter(Boolean)
    );

    // Load all prior actions and filter by Project IDs
    const allPriorActions = loadPriorActions();
    const priorActions = allPriorActions
      .filter((row) =>
        filteredProjectIds.has((row['P#'] ?? '').toString().trim())
      )
      .filter((row) => {
        const drmPillar = (row['DRM Pillar'] ?? '').toString().trim();
        return drmPillar !== '' && !drmPillar.toLowerCase().includes('not drm');
      })
      .filter((row) => {
        if (!filters.pillars.length) return true;
        const rowPillar = (row['DRM Pillar'] ?? '').toString().trim();
        return filters.pillars.includes(rowPillar);
      });

    const pillarColorMap: Record<string, string> = DRM_PILLAR_COLORS;

    const pillarCounts = new Map<string, number>();

    for (const row of priorActions) {
      const pillar = row['DRM Pillar'] ?? 'Unknown';
      pillarCounts.set(pillar, (pillarCounts.get(pillar) ?? 0) + 1);
    }

    const comparator = makeDrmPillarComparator();
    const sortedPillars = Array.from(pillarCounts.keys()).sort(comparator);

    const chartData = sortedPillars.map((pillar) => ({
      id: pillar,
      label: pillar,
      values: {
        [pillar]: pillarCounts.get(pillar) || 0,
      },
    }));

    const series = sortedPillars.map((pillar) => ({
      key: pillar,
      label: pillar,
      color: pillarColorMap[pillar] || '#cccccc',
    }));

    return NextResponse.json({
      chartData,
      series,
      tableData: priorActions,
    });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : 'Unknown error';
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
