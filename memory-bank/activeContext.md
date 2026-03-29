# Active Context: Gekko Vessel Analytics Dashboard

## Current Work Focus
Vessel image display feature: Added vessel image panels that appear alongside Power BI reports when available. Images display on the right side of the page with vessel name caption.

## Recent Changes
1. Added vessel image display panel to the dashboard layout
2. Configured image paths in REPORTS config for vessels with available images
3. Implemented conditional display - image panel shows only when image exists
4. Murphy Vietnam vessels (Hai Duong 136, Sea Meadow 12/22/39) have vessel images
5. Trident Energy vessels configured without images (none available in folder)
6. Murphy GOM vessels use iframe-based reports without images

## Session Changes Summary
- **Vessel Image Feature**: 
  - Added CSS for `.vessel-image-panel` with styling for vessel card display
  - Modified HTML layout with `report-main-content` wrapper
  - Added `vessel-image-panel`, `vessel-image`, and `vessel-image-name` elements
  - Updated `loadReport()` function to conditionally show/hide vessel images
  - Image paths configured: `Vessels Images/Hai_Duong_136.jpg`, `Sea_Meadow_12.png`, `Sea_Meadow_22.png`, `Sea_Meadow_39.png`

## Next Steps
- Add vessel images for Trident Energy vessels when available
- Add vessel images for Murphy GOM vessels when available
- Optional: Add loading states for images
- Optional: Add image fallback/placeholder for vessels without images

## Active Decisions and Considerations

### Current State Assessment
- Functional dashboard with vessel image display feature
- Images show conditionally based on configuration
- Sidebar navigation includes multiple clients: Murphy GOM, Murphy Vietnam, Trident Energy
- Power BI integration continues to use direct embed URLs with autoAuth

### Important Patterns and Preferences
- Single-file SPA pattern maintained (HTML/CSS/JS in one file)
- Vessel images stored in "Vessels Images/" folder
- Image property optional in REPORTS config - panel hidden when not set
- Consistent styling with blue theme and rounded corners

## Learnings and Project Insights
- Vessel images enhance visual identification of vessels
- Conditional display allows graceful handling of missing images
- Image panel positioned on right side of report area

## Current Project Status
- ✅ Core functionality intact
- ✅ Vessel image display feature working
- ✅ Murphy Vietnam vessels have images configured
- ✅ Image panel hidden gracefully for vessels without images
- ✅ Navigation and active-state styling preserved
- 🔄 Pending: Add images for Trident Energy and Murphy GOM vessels when available
