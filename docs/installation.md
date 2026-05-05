# Installation Guide

## Prerequisites

- Docker and Docker Compose
- Git

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/KwanekDev/LeadPilot.git
cd LeadPilot
```

2. Copy environment file:
```bash
cp .env.example .env
```

3. Edit `.env` with your configuration (database, email, etc.)

4. Start the application:
```bash
docker compose up -d
```

5. Run database migrations:
```bash
docker compose run --rm backend alembic upgrade head
```

6. Seed the database with initial data:
```bash
docker compose run --rm backend python -m app.scripts.seed
```

7. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/v1/docs

## Default Admin Account

- Email: admin@leadpilot.com
- Password: admin123

## Development Setup

### Backend

```bash
cd apps/backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend

```bash
cd apps/frontend
npm install
npm run dev
```

## Production Deployment

### Using Docker Compose

1. Update `.env` with production settings
2. Run:
```bash
docker compose -f docker-compose.yml up -d
```

### Environment Variables

See `.env.example` for all required environment variables.

### Database

The application uses PostgreSQL. Make sure to:
- Set `DATABASE_URL` in your environment
- Run migrations: `alembic upgrade head`
- Seed initial data if needed

### Email Configuration

Configure SMTP settings for email functionality:
- `SMTP_SERVER`
- `SMTP_PORT`
- `SMTP_USERNAME`
- `SMTP_PASSWORD`

### SMS Configuration (Optional)

For SMS reminders, configure Twilio:
- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_PHONE_NUMBER`