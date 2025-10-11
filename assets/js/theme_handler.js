// Theme handling JavaScript for plotly graphs and other components

window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        // Function to update plotly graph themes
        update_graph_theme: function(theme_data) {
            const isDark = theme_data.theme === 'dark';
            
            // Default plotly layout for dark theme
            const darkLayout = {
                paper_bgcolor: '#2d3748',
                plot_bgcolor: '#374151',
                font: {
                    color: '#f8f9fa'
                },
                xaxis: {
                    gridcolor: '#4a5568',
                    zerolinecolor: '#4a5568',
                    color: '#f8f9fa'
                },
                yaxis: {
                    gridcolor: '#4a5568',
                    zerolinecolor: '#4a5568',
                    color: '#f8f9fa'
                },
                colorway: [
                    '#63b3ed', '#4fd1c7', '#f093fb', '#f6e05e', 
                    '#fc8181', '#a78bfa', '#68d391', '#fbb6ce'
                ]
            };
            
            // Default plotly layout for light theme
            const lightLayout = {
                paper_bgcolor: 'white',
                plot_bgcolor: 'white',
                font: {
                    color: '#2c3e50'
                },
                xaxis: {
                    gridcolor: '#e2e8f0',
                    zerolinecolor: '#e2e8f0',
                    color: '#2c3e50'
                },
                yaxis: {
                    gridcolor: '#e2e8f0',
                    zerolinecolor: '#e2e8f0',
                    color: '#2c3e50'
                },
                colorway: [
                    '#3498db', '#2ecc71', '#e74c3c', '#f39c12',
                    '#9b59b6', '#1abc9c', '#34495e', '#e67e22'
                ]
            };
            
            return isDark ? darkLayout : lightLayout;
        },
        
        // Function to handle dropdown theme
        update_dropdown_theme: function(theme_data) {
            const isDark = theme_data.theme === 'dark';
            
            if (isDark) {
                return {
                    backgroundColor: '#374151',
                    color: '#f8f9fa',
                    borderColor: '#4a5568'
                };
            } else {
                return {
                    backgroundColor: 'white',
                    color: '#2c3e50',
                    borderColor: '#bdc3c7'
                };
            }
        },
        
        // Function to handle range slider theme
        update_range_slider_theme: function(theme_data) {
            const isDark = theme_data.theme === 'dark';
            
            if (isDark) {
                return {
                    '.rc-slider-track': {
                        backgroundColor: '#63b3ed'
                    },
                    '.rc-slider-handle': {
                        borderColor: '#63b3ed',
                        backgroundColor: '#63b3ed'
                    },
                    '.rc-slider-rail': {
                        backgroundColor: '#4a5568'
                    }
                };
            } else {
                return {
                    '.rc-slider-track': {
                        backgroundColor: '#3498db'
                    },
                    '.rc-slider-handle': {
                        borderColor: '#3498db',
                        backgroundColor: '#3498db'
                    },
                    '.rc-slider-rail': {
                        backgroundColor: '#bdc3c7'
                    }
                };
            }
        }
    }
});

// Function to apply theme to all plotly graphs on the page
function applyThemeToAllGraphs(isDark) {
    // Get all plotly graphs
    const graphs = document.querySelectorAll('.js-plotly-plot');
    
    graphs.forEach(graph => {
        if (graph && graph.layout) {
            const update = isDark ? {
                'paper_bgcolor': '#2d3748',
                'plot_bgcolor': '#374151',
                'font.color': '#f8f9fa',
                'xaxis.gridcolor': '#4a5568',
                'xaxis.zerolinecolor': '#4a5568',
                'xaxis.color': '#f8f9fa',
                'yaxis.gridcolor': '#4a5568',
                'yaxis.zerolinecolor': '#4a5568',
                'yaxis.color': '#f8f9fa'
            } : {
                'paper_bgcolor': 'white',
                'plot_bgcolor': 'white',
                'font.color': '#2c3e50',
                'xaxis.gridcolor': '#e2e8f0',
                'xaxis.zerolinecolor': '#e2e8f0',
                'xaxis.color': '#2c3e50',
                'yaxis.gridcolor': '#e2e8f0',
                'yaxis.zerolinecolor': '#e2e8f0',
                'yaxis.color': '#2c3e50'
            };
            
            try {
                Plotly.relayout(graph, update);
            } catch (error) {
                console.log('Could not update graph theme:', error);
            }
        }
    });
}

// Listen for theme changes
document.addEventListener('DOMContentLoaded', function() {
    // Observer for theme changes
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
                const isDark = document.querySelector('#main-container')?.classList.contains('dark-theme');
                if (isDark !== undefined) {
                    applyThemeToAllGraphs(isDark);
                }
            }
        });
    });
    
    // Start observing
    const mainContainer = document.querySelector('#main-container');
    if (mainContainer) {
        observer.observe(mainContainer, { attributes: true });
    }
});