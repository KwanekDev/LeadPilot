# LeadPilot

A production-ready SaaS platform for HVAC companies to manage leads, jobs, reminders, and customer relationships.

## Features

- **Lead Management**: Track and convert installation leads
- **Job Scheduling**: Assign technicians and manage installations
- **Reminder Engine**: Automated maintenance and follow-up reminders via SMS/email
- **Customer Database**: Comprehensive customer and equipment tracking
- **Analytics Dashboard**: Revenue estimates, conversion rates, and activity feeds
- **Multi-Tenant**: Support for multiple companies with tenant isolation
- **Admin Panel**: User management, roles, and system settings

## Tech Stack

- **Backend**: Python 3.12, FastAPI, SQLAlchemy, PostgreSQL, Redis, Celery
- **Frontend**: React, Vite, TypeScript, TailwindCSS, Shadcn UI
- **Infrastructure**: Docker, Docker Compose, Nginx, GitHub Actions

## Quick Start

1. Clone the repository
2. Copy `.env.example` to `.env` and configure
3. Run `docker compose up`
4. Access the application at `http://localhost`

## Documentation

- [Installation Guide](docs/installation.md)
- [Architecture Overview](docs/architecture.md)
- [API Documentation](docs/api.md)
- [Deployment Guide](docs/deployment.md)

## Contributing

This is a monorepo with the following structure:

- `apps/backend/` - FastAPI backend
- `apps/frontend/` - React frontend
- `packages/shared-types/` - Shared TypeScript types
- `packages/ui/` - Reusable UI components
- `infrastructure/` - Docker, Nginx, and deployment scripts
- `docs/` - Documentation

## License

Commercial license. Contact for details.