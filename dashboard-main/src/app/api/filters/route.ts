import { NextResponse } from 'next/server';
import { makeDrmPillarComparator } from '@/constants/drmPillars';
export const dynamic = 'force-dynamic';
import { loadPortfolio, loadPriorActions } from '@/lib/portfolio';

type FilterData = {
  regions: string[];
  countries: string[];
  statuses: string[];
  pillars: string[];
};

export async function GET() {
  try {
    const portfolioRows = loadPortfolio();
    const priorActionsRows = loadPriorActions();

    const regions = Array.from(
      new Set(
        portfolioRows
          .map((r) => (r['Region'] ?? '').toString().trim())
          .filter(Boolean)
      )
    ).sort();

    const countries = Array.from(
      new Set(
        portfolioRows
          .map((r) => (r['Country'] ?? '').toString().trim())
          .filter(Boolean)
      )
    ).sort();

    const statuses = Array.from(
      new Set(
        portfolioRows
          .map((r) => (r['Status'] ?? '').toString().trim())
          .filter(Boolean)
      )
    ).sort();

    const rawPillars = Array.from(
      new Set(
        priorActionsRows
          .map((r) => (r['DRM Pillar'] ?? '').toString().trim())
          .filter(Boolean)
          .filter((pillar) => pillar !== 'Not DRM')
      )
    );

    const comparator = makeDrmPillarComparator();
    const pillars = rawPillars.sort(comparator);

    const filterData: FilterData = {
      regions,
      countries,
      statuses,
      pillars,
    };

    return NextResponse.json({ data: filterData });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : 'Unknown error';
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
