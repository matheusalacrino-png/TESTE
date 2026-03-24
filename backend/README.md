# AvaliaZap API (FastAPI + PostgreSQL)

Backend multiempresa com autenticação JWT e integração com WhatsApp Business API / Google Business Profile.

## Requisitos

- Python 3.11+
- PostgreSQL 14+

## Setup

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Configure as variáveis no `.env`.

## Subir API

```bash
uvicorn app.main:app --reload --port 9000
```

Base URL: `http://localhost:9000`

## Endpoints principais

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/business/me`
- `PATCH /api/v1/business/me`
- `POST /api/v1/reviews/requests`
- `POST /api/v1/reviews/requests/{id}/respond`
- `GET /api/v1/reviews/dashboard`
- `POST /api/v1/integrations/whatsapp/send-template`
- `GET /api/v1/integrations/google/review-link`
- `GET /api/v1/integrations/google/place-details`

## Observação

As integrações externas exigem credenciais reais (Meta/Google) para funcionar em produção.
