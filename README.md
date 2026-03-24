# AvaliaZap Pro - MVP Funcional

Projeto de demonstração para coleta de avaliações via WhatsApp com roteamento para Google Meu Negócio.

## O que já funciona

- Cadastro de empresa com WhatsApp e link de avaliação no Google.
- Registro de solicitações de avaliação por cliente.
- Simulação de resposta com nota de 1 a 5.
- Triagem automática:
  - 1-2 estrelas: fluxo interno (feedback crítico).
  - 3-5 estrelas: direcionamento para Google Meu Negócio.
- Dashboard com métricas em tempo real.
- Histórico de comunicação e avaliações.
- Persistência local via `localStorage`.

## Como executar

```bash
cd /workspace/TESTE
python3 -m http.server 8000
```

Acesse: `http://localhost:8000`.

## Próxima etapa sugerida

- Backend com autenticação multiempresa.
- Banco de dados (PostgreSQL).
- Integração real com WhatsApp Business API e Google Business Profile API.
