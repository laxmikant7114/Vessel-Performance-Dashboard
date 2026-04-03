# Tech Context: Gekko Vessel Analytics Dashboard

## Technologies Used

### Frontend Stack
- **HTML5**: Semantic markup with modern standards
- **CSS3**: Advanced styling with flexbox, gradients, and transitions
- **Vanilla JavaScript**: No frameworks, pure DOM manipulation
- **Power BI Embedded**: Microsoft's business intelligence platform

### Development Environment
- **File Structure**: Simple flat structure for easy deployment
- **Asset Management**: Local logo file (gekko-logo-white.png)
- **Configuration**: Environment variables in .env file

### External Dependencies
- **Power BI Service**: Cloud-hosted analytics platform
- **Gemini API**: Google's AI service (configured but not implemented)

## Development Setup

### File Organization
```
testgem/
├── report.html          # Main application file
├── gekko-logo-white.png # Brand logo asset
├── .env                 # Environment configuration
├── test.py             # Empty Python file (future development)
└── memory-bank/        # Documentation system
```

### Environment Configuration
- **Gemini API Key**: 
- **Power BI URLs**: Embedded directly in JavaScript configuration

### Deployment Requirements
- **Web Server**: Any HTTP server (can run locally or deployed)
- **Browser Support**: Modern browsers with iframe support
- **Network Access**: Internet connection for Power BI reports

## Technical Constraints

### Current Limitations
1. **Static Content**: No server-side processing
2. **Power BI Dependency**: Requires external service availability
3. **Single File**: All functionality in one HTML file
4. **No Authentication**: Public Power BI embed URLs

### Browser Requirements
- **JavaScript Enabled**: Required for navigation functionality
- **iframe Support**: Essential for Power BI embedding
- **CSS3 Support**: For modern styling and layout
- **Responsive Design**: Optimized for desktop/tablet viewing

## Dependencies

### External Services
- **Power BI Service**: Microsoft cloud analytics platform
- **Gemini API**: Google AI service (future integration)

### Asset Dependencies
- **Logo File**: gekko-logo-white.png (local asset)
- **Fonts**: System fonts (Segoe UI, fallbacks)

## Tool Usage Patterns

### Development Workflow
1. **Direct File Editing**: HTML/CSS/JS in single file
2. **Browser Testing**: Open report.html directly in browser
3. **Asset Management**: Local file references
4. **Configuration**: Environment variables for sensitive data

### Power BI Integration
- **Embed URLs**: Direct iframe embedding
- **Report IDs**: Specific to each vessel/supplier
- **Auto Authentication**: Simplified access pattern
- **Full Screen Support**: Native Power BI functionality

## Performance Considerations
- **Single File Load**: Minimal HTTP requests
- **External Content**: Power BI reports load separately
- **CSS Optimization**: Inline styles for performance
- **JavaScript Efficiency**: Minimal DOM manipulation

## Security Patterns
- **API Key Storage**: Environment file (not in source code)
- **Public Embeds**: Power BI reports use public URLs
- **Client-Side Only**: No server-side vulnerabilities
- **Asset Security**: Local logo file, no external dependencies

## Future Technical Possibilities
- **Python Backend**: test.py suggests potential server development
- **API Integration**: Gemini API key ready for implementation
- **Database Integration**: Could add data persistence
- **Authentication**: Could implement user management
- **Mobile Optimization**: Responsive design foundation exists
