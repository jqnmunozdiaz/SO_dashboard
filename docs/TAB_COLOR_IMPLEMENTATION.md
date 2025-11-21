# Tab Color Implementation Summary

## Overview
The dashboard uses a **class-based styling system** for tab colors, replacing the previous `nth-child` selector approach. This ensures that tab colors remain consistent regardless of their position in the layout and makes the code more maintainable.

## Implementation

### CSS Classes (assets/css/tabs-theme.css)

Three main color themes are defined:

1.  **Blue Theme (`.tab-blue`)**
    *   **Use for:** Urban indicators, national-level data.
    *   **Colors:** Light blue background, darker blue text/border.
    *   **Active State:** Sky blue background.

2.  **Green Theme (`.tab-green`)**
    *   **Use for:** Services & infrastructure (water, sanitation, electricity).
    *   **Colors:** Light green background, darker green text/border.
    *   **Active State:** Lime green background.

3.  **Orange Theme (`.tab-orange`)**
    *   **Use for:** City-level data and analysis.
    *   **Colors:** Light orange background, darker orange text/border.
    *   **Active State:** Bright orange background.

### Python Implementation (src/layouts/world_bank_layout.py)

Tabs are assigned their color theme using the `class_name` argument in `dbc.Tab`:

```python
# Example: Urban Population (Blue)
dbc.Tab(
    label="Urban Population",
    tab_id="urban-population-projections",
    class_name="tab-blue"
)

# Example: Access to Electricity (Green)
dbc.Tab(
    label="Access to Electricity",
    tab_id="access-to-electricity-urban",
    class_name="tab-green"
)

# Example: Cities Distribution (Orange)
dbc.Tab(
    label="Cities Distribution",
    tab_id="cities-distribution",
    class_name="tab-orange"
)
```

## Benefits
*   **Position Independence:** Tabs can be reordered without breaking the color scheme.
*   **Explicit Intent:** The class name clearly indicates the intended color theme.
*   **Maintainability:** Colors are defined in a single CSS file (`tabs-theme.css`) and applied explicitly in Python.

## How to Add New Colors
1.  Define a new class in `assets/css/tabs-theme.css` (e.g., `.tab-purple`).
2.  Apply the class to the `dbc.Tab` component in `src/layouts/world_bank_layout.py` using `class_name="tab-purple"`.

