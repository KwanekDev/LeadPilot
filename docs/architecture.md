# Architecture Overview

## System Architecture

LeadPilot is built as a modern SaaS platform using a monorepo structure with microservices architecture deployed via Docker.

```
/apps
├── backend/          # FastAPI backend service
└── frontend/         # React frontend application

/packages
├── shared-types/     # Shared TypeScript types
└── ui/              # Reusable UI components

/infrastructure
├── docker/          # Docker configurations
├── nginx/           # Reverse proxy configuration
└── scripts/         # Deployment and utility scripts

/docs                # Documentation
```

## Backend Architecture

### Technology Stack
- **Framework**: FastAPI (Python 3.12)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Cache**: Redis
- **Task Queue**: Celery
- **Migrations**: Alembic

### Core Components

#### Authentication & Authorization
- JWT-based authentication with refresh tokens
- Role-based access control (RBAC)
- Multi-tenant architecture with tenant isolation

#### API Structure
```
app/
├── api/             # API routes and endpoints
├── core/            # Core functionality (auth, config)
├── crud/            # Database CRUD operations
├── db/              # Database models and session
├── models/          # SQLAlchemy models
├── schemas/         # Pydantic schemas
├── scripts/         # Utility scripts
└── tasks/           # Celery tasks
```

#### Key Features
- **CRM**: Lead and customer management
- **Jobs**: Installation and service job tracking
- **Reminders**: Automated maintenance reminders via email/SMS
- **Analytics**: Dashboard analytics and reporting
- **Admin Panel**: User and system management

## Frontend Architecture

### Technology Stack
- **Framework**: React 18 with TypeScript
- **Routing**: React Router
- **State Management**: React Query for server state
- **Styling**: TailwindCSS with Shadcn UI components
- **Build Tool**: Vite

### Key Components
- **Authentication**: Context-based auth with token management
- **Dashboard**: Analytics and quick actions
- **Data Tables**: Sortable, filterable data displays
- **Forms**: Validated forms with error handling

## Infrastructure

### Docker Services
- **backend**: FastAPI application
- **frontend**: React application
- **postgres**: Database
- **redis**: Cache and task queue
- **celery**: Background task worker
- **celery-beat**: Scheduled task manager
- **nginx**: Reverse proxy and static file serving

### Deployment
- **Development**: Docker Compose with hot reload
- **Production**: Docker Compose with optimized builds
- **CI/CD**: GitHub Actions for testing and building

## Security

### Authentication
- JWT tokens with expiration
- Refresh token rotation
- Password hashing with bcrypt

### Authorization
- Tenant-based data isolation
- Role-based permissions
- API endpoint protection

### Data Protection
- Input validation with Pydantic
- SQL injection prevention
- CORS configuration

## Scalability

### Multi-Tenant Design
- Database-level tenant isolation
- Shared infrastructure with data separation
- Scalable architecture for SaaS growth

### Performance
- Redis caching for frequently accessed data
- Asynchronous task processing with Celery
- Optimized database queries with indexes

### Monitoring
- Health check endpoints
- Structured logging
- Error tracking and reporting