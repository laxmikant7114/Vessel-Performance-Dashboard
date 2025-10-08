# System Patterns: Gekko Vessel Analytics Dashboard

## Architecture Overview
The system follows a client-side web application pattern with embedded analytics, designed for simplicity and direct deployment.

## Key Technical Decisions
1. **Single-Page Application**: All functionality contained in one HTML file for easy deployment
2. **Embedded Analytics**: Power BI reports embedded via iframe for full functionality
3. **Client-Side Navigation**: JavaScript handles report switching without server requests
4. **Static Asset Management**: Logo and styling embedded/referenced locally

## Design Patterns in Use

### Frontend Architecture
- **Component-Based Layout**: Sidebar navigation + main content area
- **State Management**: Simple JavaScript object for report configurations
- **Event-Driven Navigation**: Button clicks trigger report loading
- **Responsive Design**: CSS flexbox for layout management

### Code Organization
```
report.html
├── HTML Structure
│   ├── Sidebar (navigation)
│   ├── Header (dynamic titles)
│   ├── Main Content (iframe container)
│   └── Footer (branding)
├── CSS Styling
│   ├── Layout (flexbox)
│   ├── Component styles
│   ├── Interactive states
│   └── Responsive design
└── JavaScript Logic
    ├── Report configuration object
    ├── loadReport() function
    └── DOM manipulation
```

## Component Relationships

### Navigation Flow
```
User Click → Button Event → loadReport() → Update iframe src + UI state
```

### Data Flow
```
Power BI Service → iframe embed → User interaction → Power BI Service
```

## Critical Implementation Paths

### Report Loading Mechanism
1. **Configuration Object**: Maps report names to Power BI URLs and metadata
2. **Dynamic Loading**: iframe src updated based on user selection
3. **UI Synchronization**: Title and button states updated simultaneously
4. **Initial State**: Default to 'Java' report on page load

### Styling Architecture
- **CSS Variables**: Could be implemented for theme consistency
- **Component Isolation**: Each UI section has dedicated CSS classes
- **Interactive States**: Hover and active states for navigation
- **Professional Theme**: Corporate blue (#0078D4) as primary color

## Security Considerations
- **API Key Management**: Gemini API key stored in .env file (not currently used)
- **Power BI Embedding**: Uses public embed URLs with autoAuth
- **Client-Side Only**: No server-side processing reduces attack surface

## Scalability Patterns
- **Report Addition**: New reports easily added to configuration object
- **Styling Updates**: Centralized CSS for consistent changes
- **Feature Extension**: Modular JavaScript structure supports additions

## Development Patterns
- **Single File Deployment**: Entire application in one HTML file
- **Asset Management**: Local logo reference, external Power BI content
- **Environment Configuration**: .env file for sensitive data (future use)
- **Empty Python File**: Placeholder for potential backend development
