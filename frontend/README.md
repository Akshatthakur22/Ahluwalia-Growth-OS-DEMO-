# Ahluwalia Growth OS - Frontend

Next.js frontend for Ahluwalia Growth OS.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Configure environment variables:
```bash
cp .env.local.example .env.local
# Edit .env.local with your configuration
```

3. Start the development server:
```bash
npm run dev
```

4. Build for production:
```bash
npm run build
npm start
```

## Project Structure

```
frontend/
├── src/
│   ├── app/           # Next.js app directory
│   ├── components/    # Reusable components
│   ├── lib/           # Utilities and API client
│   └── styles/        # Global styles
├── public/            # Static assets
└── package.json       # Dependencies
```

## Tech Stack

- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- Axios (API client)
- Zustand (state management)

## Design Principles

Following the UI Specification document:
- Apple-inspired simplicity
- Mobile-first design
- Progressive disclosure
- Consistent visual language
- 12px corner radius
- Neutral backgrounds with dark typography
