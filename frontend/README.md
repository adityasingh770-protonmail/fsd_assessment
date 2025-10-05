# Frontend - Movie Explorer Platform

React + TypeScript application for the Movie Explorer Platform.

## Structure

```
frontend/
├── public/              # Static assets
├── src/
│   ├── components/      # Reusable React components
│   ├── pages/          # Page components
│   ├── services/       # API service layer
│   ├── types/          # TypeScript type definitions
│   ├── utils/          # Utility functions
│   ├── App.tsx         # Root application component
│   └── main.tsx        # Application entry point
├── package.json
├── tsconfig.json       # TypeScript configuration
└── vite.config.ts      # Vite configuration
```

## Setup Instructions

### Local Development

1. Install dependencies:
```bash
npm install
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API URL
```

3. Run the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run test` - Run tests
- `npm run lint` - Run ESLint
- `npm run format` - Format code with Prettier

## Testing

Run tests with:
```bash
npm run test
```

With coverage:
```bash
npm run test:coverage
```

## Building for Production

```bash
npm run build
```

The build output will be in the `dist/` directory.