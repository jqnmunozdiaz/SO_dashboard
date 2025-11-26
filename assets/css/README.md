# CSS Organization

Modular CSS structure with component-specific files imported via `custom.css`.

## Files

- **base.css** - Typography, resets, scrollbar
- **layout.css** - Page structure, containers
- **hero.css** - Hero section, map
- **navigation.css** - Main tabs
- **tabs-theme.css** - Tab color themes (blue/green/orange)
- **filters.css** - Country selector, filters
- **dropdowns.css** - Dropdown components
- **benchmarks.css** - Benchmark selectors
- **slider.css** - Year slider
- **buttons.css** - Action buttons
- **notes.css** - Indicator notes
- **responsive.css** - Mobile breakpoints
- **custom.css** - Imports all above

## Tab Color Themes

Apply to `dbc.Tab` components:

```python
class_name="tab-blue"    # Urban indicators, national data
class_name="tab-green"   # Services & infrastructure
class_name="tab-orange"  # City-level analysis
```

Edit `tabs-theme.css` to add new colors.
