# AI Assistant Guidance: Technical Implementation

## Development Guidelines for AI Assistant

### Core Technical Stack
- **Frontend**: HTML5, CSS3 (Bootstrap 5.3, Custom CSS)
- **Interactivity**: jQuery 3.6, Bootstrap JS
- **Optional Backend**: Python Flask (admin features only)
- **Data**: JSON file-based storage (no database)

### Development Setup for AI Assistant

#### Quick Start Commands
```bash
# Static mode (no backend)
python -m http.server 8000

# With backend (admin features)
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
python server.py
```

### File Structure Conventions for AI Assistant
1. **Images**: `img/<species-folder>/image[1-4].jpg` (kebab-case folders)
2. **Data**: `data/fish.json` - array of fish objects
3. **Styles**: Single CSS file with organized sections
4. **Scripts**: Inline in index.html for simplicity

### JSON Data Structure
```json
{
  "name": "Species Name",
  "price": "$32",
  "rating": 5,
  "description": "Description text",
  "images": ["img/folder/image1.jpg", "..."]
}
```

### CSS Architecture for AI Assistant
- Use CSS variables for theming
- Mobile-first responsive design
- Glass morphism effects via `backdrop-filter`
- Bubble animations with `@keyframes`

### JavaScript Patterns
- jQuery for DOM manipulation
- Bootstrap components via data attributes
- AJAX for JSON loading
- Modal and carousel components

### AI Assistant Development Rules
1. **Don't** add build tools or complex tooling
2. **Do** maintain single-file CSS approach
3. **Don't** add database dependencies
4. **Do** follow existing naming conventions
5. **Don't** break static site generation
6. **Do** maintain dark theme consistency

### Testing Guidelines
- Test in static mode first
- Verify image paths in JSON
- Check mobile responsiveness
- Test modal and carousel functionality

### Deployment Notes for AI
- GitHub Pages ready (static files only)
- No server required for basic features
- Admin features need Flask backend
- All assets should be relative paths