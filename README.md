# LeadPilot

A production-ready SaaS platform for HVAC, air conditioning, and heat pump installation companies. Built with modern technologies for scalability, maintainability, and ease of deployment.

## Features

- **Multi-Tenant SaaS**: Complete tenant isolation and management
- **CRM System**: Lead and customer management with full lifecycle tracking
- **Job Management**: Installation and service job scheduling and tracking
- **Reminder Engine**: Automated maintenance reminders via email and SMS
- **Dashboard Analytics**: Real-time insights and reporting
- **Admin Panel**: User management and system administration
- **Authentication**: JWT-based auth with role-based access control
- **Docker Deployment**: Easy self-hosting with Docker Compose

## Tech Stack

### Backend
- **Python 3.12** with **FastAPI**
- **PostgreSQL** database with **SQLAlchemy** ORM
- **Redis** for caching and task queuing
- **Celery** for background tasks
- **Alembic** for database migrations

### Frontend
- **React 18** with **TypeScript**
- **Vite** for fast development and building
- **TailwindCSS** with **Shadcn UI** components
- **React Query** for state management

### Infrastructure
- **Docker** and **Docker Compose** for containerization
- **Nginx** reverse proxy
- **GitHub Actions** for CI/CD

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/KwanekDev/LeadPilot.git
cd LeadPilot
```

2. Copy environment configuration:
```bash
cp .env.example .env
```

3. Start the application:
```bash
docker compose up -d
```

4. Run database migrations:
```bash
docker compose run --rm backend alembic upgrade head
```

5. Access the application:
- **Frontend**: http://localhost:3000
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/v1/docs

### Default Admin Account
- Email: `admin@leadpilot.com`
- Password: `admin123`

## Development

### Backend Setup
```bash
cd apps/backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend Setup
```bash
cd apps/frontend
npm install
npm run dev
```

## Documentation

- [Installation Guide](docs/installation.md)
- [Architecture Overview](docs/architecture.md)
- [API Documentation](http://localhost:8000/api/v1/docs) (when running)

## Deployment

### Production
```bash
docker compose -f docker-compose.yml up -d
```

### Environment Variables
See `.env.example` for all configuration options.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `docker compose run --rm backend pytest`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review the API documentation when running locally