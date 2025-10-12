import { NextResponse } from 'next/server';
import {
  loadPortfolioFiltered,
  sumDisbursementsByRegion,
} from '@/lib/portfolio';
import { parseFiltersFromRequest } from '@/lib/api-utils';

export const dynamic = 'force-dynamic';

export async function GET(request: Request) {
  try {
    const filters = parseFiltersFromRequest(request);

    const portfolio = loadPortfolioFiltered(filters);
    const regions = sumDisbursementsByRegion(portfolio);
    return NextResponse.json({ regions });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : 'Unknown error';
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
