import { NextResponse } from 'next/server';
import { loadPortfolioFiltered } from '@/lib/portfolio';
import { parseFiltersFromRequest } from '@/lib/api-utils';

export const dynamic = 'force-dynamic';

export async function GET(request: Request) {
  try {
    const filters = parseFiltersFromRequest(request);

    const portfolio = loadPortfolioFiltered(filters);

    const activeClosed = portfolio.filter((row) =>
      ['Active', 'Closed'].includes(row.Status || '')
    );

    const groupedData = new Map<string, Map<string, number>>();

    for (const row of activeClosed) {
      const fiscalYear = row['Fiscal Year'] || '';
      const globalPractice = row['Global Practice'] || 'Unknown';

      if (!groupedData.has(fiscalYear)) {
        groupedData.set(fiscalYear, new Map());
      }

      const deptMap = groupedData.get(fiscalYear)!;
      deptMap.set(globalPractice, (deptMap.get(globalPractice) || 0) + 1);
    }

    const chartData = Array.from(groupedData.entries()).map(
      ([fiscalYear, deptMap]) => {
        const values: Record<string, number> = {};

        const allDepartments = [
          'Urban, Resilience and Land',
          'Macroeconomics, Trade and Investment',
          'Environment, Natural Resources & the Blue Economy',
          'Finance, Competitiveness and Innovation',
          'Governance',
        ];

        allDepartments.forEach((dept) => {
          values[dept] = deptMap.get(dept) || 0;
        });

        return {
          id: fiscalYear,
          label: fiscalYear,
          values,
        };
      }
    );

    chartData.sort((a, b) => a.label.localeCompare(b.label));

    const series = [
      {
        key: 'Urban, Resilience and Land',
        label: 'Urban, Resilience and Land',
        color: '#295e84',
      },
      {
        key: 'Macroeconomics, Trade and Investment',
        label: 'Macroeconomics, Trade and Investment',
        color: '#9d4449',
      },
      {
        key: 'Environment, Natural Resources & the Blue Economy',
        label: 'Environment, Natural Resources & the Blue Economy',
        color: '#a3c0e4',
      },
      {
        key: 'Finance, Competitiveness and Innovation',
        label: 'Finance, Competitiveness and Innovation',
        color: '#89a3c5',
      },
      {
        key: 'Governance',
        label: 'Governance',
        color: '#e7cabc',
      },
    ];

    return NextResponse.json({
      data: chartData,
      series,
    });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : 'Unknown error';
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
