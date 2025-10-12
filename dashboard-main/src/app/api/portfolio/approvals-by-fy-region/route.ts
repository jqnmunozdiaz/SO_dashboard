import { NextResponse } from 'next/server';
import {
  crosstabFiscalYearRegion,
  loadPortfolioFiltered,
} from '@/lib/portfolio';
import { parseFiltersFromRequest } from '@/lib/api-utils';

export const dynamic = 'force-dynamic';

export async function GET(request: Request) {
  try {
    const filters = parseFiltersFromRequest(request);

    const portfolio = loadPortfolioFiltered(filters);
    const { regions, years, matrix } = crosstabFiscalYearRegion(portfolio);
    return NextResponse.json({ regions, years, matrix });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : 'Unknown error';
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
