# AI Assistant Guidance: Project Structure

## Quick Reference for AI Assistant

### Directory Layout (AI Focus)
```
fish_project/
├── index.html                 # Single-page application
├── css/styles.css            # All styling (one file)
├── data/fish.json            # Fish catalog (JSON array)
└── img/                      # Organized images
    ├── homepage/             # Site-wide assets
    └── <species-folder>/     # Kebab-case species names
        ├── image1.jpg        # Primary thumbnail
        ├── image2.jpg        # Carousel image
        ├── image3.jpg        # Carousel image
        └── image4.jpg        # Carousel image
```

## AI Assistant Workflow

### When Adding New Content
1. **New fish species**: Create folder in `img/` with kebab-case name
2. **Add images**: Use sequential naming (image1.jpg, image2.jpg, etc.)
3. **Update JSON**: Add entry to `data/fish.json` following schema
4. **Test**: Gallery auto-updates, no code changes needed

### When Modifying Code
1. **HTML**: Edit `index.html` directly
2. **CSS**: Modify `css/styles.css` (single file)
3. **Data**: Update `data/fish.json`
4. **Images**: Replace files in appropriate folders

## File Naming Rules for AI Assistant

### Must Follow
- Species folders: `kebab-case-name` (e.g., `blue-knight-rams`)
- Images: `image1.jpg`, `image2.jpg`, etc. (sequential)
- Homepage assets: descriptive names (`banner.webm`, `about_us.jpg`)

### Must Avoid
- Spaces in folder or file names
- Inconsistent image naming
- Breaking relative paths in JSON

## Architecture Patterns for AI Assistant

### Single-Page Application
- All content in `index.html`
- Smooth scrolling navigation
- Modal-based detail views
- Dynamic gallery from JSON

### Static-First Design
- No build process
- CDN dependencies only
- Optional Flask backend
- File-based data storage

### Responsive Components
- Hero section with video background
- Gallery grid with hover effects
- About section with image + text
- Footer with contact info
- Detail modal with carousel

## AI Assistant Maintenance Checklist

### Before Committing Changes
- [ ] Verify image paths in JSON are correct
- [ ] Test responsive behavior on mobile
- [ ] Check dark theme consistency
- [ ] Ensure no broken animations
- [ ] Validate JSON structure

### When Adding Features
- [ ] Maintain static site compatibility
- [ ] Follow existing naming conventions
- [ ] Keep CSS in single file
- [ ] Use jQuery/Bootstrap patterns
- [ ] Test in both static and backend modes

## Common AI Assistant Tasks

### 1. Adding New Fish
- Create species folder in `img/`
- Add 2-4 images with sequential naming
- Add JSON entry with correct image paths
- Test gallery display

### 2. Updating Styles
- Edit `css/styles.css`
- Maintain glass morphism effects
- Preserve dark theme
- Test responsive breakpoints

### 3. Enhancing Features
- Use existing jQuery/Bootstrap patterns
- Keep inline JavaScript approach
- Maintain single-page architecture
- Test modal and carousel functionality

## Troubleshooting for AI Assistant

### Common Issues
- **Images not loading**: Check JSON image paths
- **Modal not working**: Verify Bootstrap/jQuery loading
- **Responsive issues**: Test CSS media queries
- **JSON errors**: Validate JSON structure

### Quick Fixes
- Use browser developer tools
- Check console for JavaScript errors
- Verify CDN links are working
- Test with Python HTTP server first