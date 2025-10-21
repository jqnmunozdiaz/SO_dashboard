/**
 * Cities Distribution d3.js Treemap Visualization
 * Renders an interactive treemap showing distribution of urban population across city size categories
 */

(function() {
    'use strict';

    // Load d3.js from CDN if not already loaded
    function loadD3(callback) {
        if (window.d3 && window.d3.version >= '7') {
            callback();
        } else {
            const script = document.createElement('script');
            script.src = 'https://d3js.org/d3.v7.min.js';
            script.onload = callback;
            script.onerror = function() {
                console.error('Failed to load d3.js');
            };
            document.head.appendChild(script);
        }
    }

    // Main rendering function
    window.renderCitiesDistribution = function(storeData) {
        loadD3(function() {
            try {
                const container = document.getElementById('cities-distribution-d3');
                if (!container) {
                    console.error('Container #cities-distribution-d3 not found');
                    return;
                }

                // Check for errors first
                if (!storeData || storeData.error || !storeData.data || storeData.data.length === 0) {
                    const errorMsg = storeData?.error || 'No data available';
                    container.innerHTML = `
                        <div style="display: flex; align-items: center; justify-content: center; height: 100%; color: #666;">
                            <div style="text-align: center;">
                                <i class="fas fa-exclamation-circle" style="font-size: 48px; margin-bottom: 16px;"></i>
                                <p style="font-size: 16px; margin: 0;">${errorMsg}</p>
                            </div>
                        </div>
                    `;
                    return;
                }

                const data = storeData.data;
                const countryName = storeData.country_name;
                const year = storeData.year;
                const colors = storeData.colors;
                const sizeCategories = storeData.size_categories || [];

                // Calculate dimensions
                const width = container.clientWidth;
                const height = container.clientHeight;
                const margin = {top: 80, right: 200, bottom: 20, left: 20};

                // Calculate total population
                const totalPop = d3.sum(data, d => d.population);

                // Create hierarchy data structure for d3.treemap
                const root = d3.hierarchy({children: data})
                    .sum(d => d.population)
                    .sort((a, b) => b.value - a.value);

                // Create treemap layout
                const treemap = d3.treemap()
                    .size([width - margin.left - margin.right, height - margin.top - margin.bottom])
                    .padding(2)
                    .round(true);

                treemap(root);

                // Check if SVG already exists (for updates)
                let svg = d3.select(container).select('svg');
                const isUpdate = !svg.empty();

                if (!isUpdate) {
                    // Create new SVG
                    svg = d3.select(container)
                        .append('svg')
                        .attr('width', width)
                        .attr('height', height);
                } else {
                    // Update SVG dimensions
                    svg.attr('width', width)
                        .attr('height', height);
                }

                // Update title with transition
                let title = svg.select('.treemap-title');
                if (title.empty()) {
                    title = svg.append('text')
                        .attr('class', 'treemap-title');
                }
                title.transition()
                    .duration(300)
                    .attr('x', width / 2)
                    .attr('y', 30)
                    .attr('text-anchor', 'middle')
                    .style('font-size', '18px')
                    .style('font-weight', 'bold')
                    .style('fill', '#374151')
                    .tween('text', function() {
                        const node = this;
                        const newText = `${countryName} | Cities Distribution by Size (${year})`;
                        return function(t) {
                            node.textContent = newText;
                        };
                    });

                // Create or select main group for treemap
                let g = svg.select('.treemap-group');
                if (g.empty()) {
                    g = svg.append('g')
                        .attr('class', 'treemap-group')
                        .attr('transform', `translate(${margin.left},${margin.top})`);
                }

                // Create tooltip if it doesn't exist
                let tooltip = d3.select('body').select('.cities-treemap-tooltip');
                if (tooltip.empty()) {
                    tooltip = d3.select('body').append('div')
                        .attr('class', 'cities-treemap-tooltip')
                        .style('position', 'absolute')
                        .style('visibility', 'hidden')
                        .style('background-color', 'white')
                        .style('border', '1px solid #ccc')
                        .style('border-radius', '4px')
                        .style('padding', '10px')
                        .style('box-shadow', '0 2px 8px rgba(0,0,0,0.15)')
                        .style('font-size', '14px')
                        .style('pointer-events', 'none')
                        .style('z-index', '1000');
                }

                // Update cells with smooth transitions
                const cell = g.selectAll('.treemap-cell')
                    .data(root.leaves(), d => d.data.name);

                // Exit: fade out removed cells
                cell.exit()
                    .transition()
                    .duration(500)
                    .attr('opacity', 0)
                    .remove();

                // Enter: create new cells
                const cellEnter = cell.enter()
                    .append('g')
                    .attr('class', 'treemap-cell')
                    .attr('transform', d => `translate(${d.x0},${d.y0})`)
                    .attr('opacity', 0);

                // Add rectangles to new cells
                cellEnter.append('rect')
                    .attr('class', 'treemap-rect')
                    .attr('width', d => d.x1 - d.x0)
                    .attr('height', d => d.y1 - d.y0)
                    .attr('fill', d => d.data.color)
                    .attr('stroke', 'white')
                    .attr('stroke-width', 2)
                    .style('cursor', 'pointer')
                    .on('mouseover', function(event, d) {
                        d3.select(this)
                            .transition()
                            .duration(200)
                            .attr('opacity', 0.8)
                            .attr('stroke', '#333')
                            .attr('stroke-width', 3);
                        
                        const percentage = (d.value / totalPop * 100).toFixed(1);
                        tooltip.html(`
                            <strong>${d.data.name}</strong><br/>
                            Population: ${d.value.toLocaleString()}<br/>
                            Percentage: ${percentage}%<br/>
                            Category: ${d.data.size_category}
                        `)
                        .style('visibility', 'visible');
                    })
                    .on('mousemove', function(event) {
                        tooltip
                            .style('top', (event.pageY - 10) + 'px')
                            .style('left', (event.pageX + 10) + 'px');
                    })
                    .on('mouseout', function() {
                        d3.select(this)
                            .transition()
                            .duration(200)
                            .attr('opacity', 1)
                            .attr('stroke', 'white')
                            .attr('stroke-width', 2);
                        tooltip.style('visibility', 'hidden');
                    });

                // Add text container to new cells
                cellEnter.append('text')
                    .attr('class', 'treemap-text')
                    .attr('x', d => (d.x1 - d.x0) / 2)
                    .attr('y', d => (d.y1 - d.y0) / 2)
                    .attr('text-anchor', 'middle')
                    .attr('dominant-baseline', 'middle');

                // Merge enter and update selections
                const cellMerge = cellEnter.merge(cell);

                // Animate cell position and opacity
                cellMerge
                    .transition()
                    .duration(800)
                    .ease(d3.easeCubicInOut)
                    .attr('transform', d => `translate(${d.x0},${d.y0})`)
                    .attr('opacity', 1);

                // Update rectangles with transitions
                cellMerge.select('.treemap-rect')
                    .transition()
                    .duration(800)
                    .ease(d3.easeCubicInOut)
                    .attr('width', d => d.x1 - d.x0)
                    .attr('height', d => d.y1 - d.y0)
                    .attr('fill', d => d.data.color);

                // Update text labels
                cellMerge.select('.treemap-text')
                    .transition()
                    .duration(800)
                    .ease(d3.easeCubicInOut)
                    .attr('x', d => (d.x1 - d.x0) / 2)
                    .attr('y', d => (d.y1 - d.y0) / 2)
                    .attr('text-anchor', 'middle')
                    .attr('dominant-baseline', 'middle');

                cellMerge.select('.treemap-text')
                    .selectAll('tspan')
                    .data(d => {
                        const percentage = (d.value / totalPop * 100).toFixed(1);
                        const name = d.data.name;
                        const width = d.x1 - d.x0;
                        const height = d.y1 - d.y0;
                        
                        // Only show text if cell is large enough
                        if (width < 60 || height < 40) return [];
                        
                        // Truncate name if too long
                        let displayName = name;
                        if (width < 100 && name.length > 15) {
                            displayName = name.substring(0, 12) + '...';
                        }
                        
                        return [displayName, `${percentage}%`];
                    })
                    .join('tspan')
                    .text(d => d)
                    .transition()
                    .duration(800)
                    .ease(d3.easeCubicInOut)
                    .attr('dy', (d, i, nodes) => {
                        const lineHeight = 14;
                        const totalLines = nodes.length;
                        return i === 0 ? -(totalLines - 1) * lineHeight / 2 : lineHeight;
                    })
                    .style('font-size', '12px')
                    .style('font-weight', (d, i) => i === 1 ? 'bold' : 'normal')
                    .style('fill', '#000')
                    .style('pointer-events', 'none');

                // Create or update legend
                let legend = svg.select('.treemap-legend');
                if (legend.empty()) {
                    legend = svg.append('g')
                        .attr('class', 'treemap-legend');
                    
                    legend.append('text')
                        .attr('class', 'legend-title')
                        .attr('x', 0)
                        .attr('y', 0)
                        .style('font-size', '14px')
                        .style('font-weight', 'bold')
                        .style('fill', '#374151')
                        .text('Size Categories');
                }

                legend.transition()
                    .duration(300)
                    .attr('transform', `translate(${width - margin.right + 20}, ${margin.top})`);

                // Update legend items
                const legendItems = legend.selectAll('.legend-item')
                    .data(sizeCategories);

                const legendEnter = legendItems.enter()
                    .append('g')
                    .attr('class', 'legend-item')
                    .attr('opacity', 0);

                legendEnter.append('rect')
                    .attr('class', 'legend-rect')
                    .attr('width', 18)
                    .attr('height', 18)
                    .attr('stroke', '#e2e8f0')
                    .attr('stroke-width', 1);

                legendEnter.append('text')
                    .attr('class', 'legend-text')
                    .attr('x', 24)
                    .attr('y', 9)
                    .attr('dominant-baseline', 'middle')
                    .style('font-size', '12px')
                    .style('fill', '#374151');

                const legendMerge = legendEnter.merge(legendItems);

                legendMerge
                    .transition()
                    .duration(500)
                    .attr('transform', (d, i) => `translate(0, ${i * 25 + 20})`)
                    .attr('opacity', 1);

                legendMerge.select('.legend-rect')
                    .transition()
                    .duration(500)
                    .attr('fill', d => colors[d] || '#95a5a6');

                legendMerge.select('.legend-text')
                    .text(d => d);

                legendItems.exit()
                    .transition()
                    .duration(300)
                    .attr('opacity', 0)
                    .remove();

            } catch (error) {
                console.error('Error rendering d3 treemap:', error);
                const container = document.getElementById('cities-distribution-d3');
                if (container) {
                    container.innerHTML = `
                        <div style="display: flex; align-items: center; justify-content: center; height: 100%; color: #666;">
                            <div style="text-align: center;">
                                <i class="fas fa-exclamation-circle" style="font-size: 48px; margin-bottom: 16px;"></i>
                                <p style="font-size: 16px; margin: 0;">Error rendering visualization</p>
                            </div>
                        </div>
                    `;
                }
            }
        });
    };

    // Listen for data store changes
    if (window.dash_clientside) {
        window.dash_clientside = window.dash_clientside || {};
        window.dash_clientside.citiesDistribution = {
            render: function(storeData) {
                if (storeData) {
                    window.renderCitiesDistribution(storeData);
                }
                return window.dash_clientside.no_update;
            }
        };
    }

})();
