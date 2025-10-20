# CSS File Organization

The dashboard CSS has been split into modular files for better maintainability and easier understanding. All styles are imported through the main `custom.css` file.

## File Structure

### Main Import File
- **custom.css** - Main file that imports all other CSS modules

### CSS Modules

#### Base Styles
- **base.css** - Global resets, typography, fonts, and scrollbar styles

#### Layout & Structure
- **layout.css** - Dashboard container, header, content areas, and chart containers
- **hero.css** - Hero section with title, description, and map image

#### Navigation
- **navigation.css** - Main navigation tabs and sub-navigation tabs
- **tabs-theme.css** - Color-coded themes for urbanization and disaster subtabs

#### Form Components
- **filters.css** - Country selector, year filter, and radio button styles
- **dropdowns.css** - Generic dropdown (Select) component styles
- **benchmarks.css** - Regional and country benchmark selector components
- **slider.css** - Year selector slider component (rc-slider)

#### UI Elements
- **buttons.css** - Download buttons and action button styles
- **notes.css** - Indicator notes and data source annotations

#### Responsive
- **responsive.css** - Mobile and tablet breakpoints (768px, 576px)

## How to Edit

### To modify a specific component:
1. Locate the relevant CSS file from the list above
2. Edit the file directly
3. Changes will be automatically reflected (no rebuild needed)

### To add new styles:
1. Add styles to the appropriate existing file, OR
2. Create a new CSS file and import it in `custom.css`

### Example: Adding new button styles
Edit `buttons.css`:
```css
.my-new-button {
    /* your styles here */
}
```

### Example: Creating a new module
1. Create `assets/css/my-module.css`
2. Add to `custom.css`:
```css
@import url('my-module.css');
```

## Benefits of This Structure

✅ **Easier to navigate** - Find styles quickly by component type  
✅ **Better maintainability** - Changes are isolated to specific files  
✅ **Clearer organization** - Each file has a single, clear purpose  
✅ **Smaller file sizes** - Each module is ~50-150 lines instead of 800+  
✅ **Team-friendly** - Multiple developers can work on different files without conflicts
