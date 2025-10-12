import { NextResponse } from 'next/server';
import { cobenefitsBars } from '@/lib/climate';
import { loadPortfolioFiltered } from '@/lib/portfolio';
import { parseFiltersFromRequest } from '@/lib/api-utils';

export const dynamic = 'force-dynamic';

export async function GET(request: Request) {
  try {
    const filters = parseFiltersFromRequest(request);

    // Filter the portfolio first to get the relevant Project IDs
    const filteredPortfolio = loadPortfolioFiltered(filters);
    const filteredProjectIds = new Set(
      filteredPortfolio
        .map((row) => (row['P#'] ?? '').toString().trim())
        .filter(Boolean)
    );

    // Pass the filtered Project IDs to the cobenefits function
    const result = cobenefitsBars(filteredProjectIds);
    return NextResponse.json(result);
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : 'Unknown error';
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
