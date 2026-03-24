import requests

from app.core.config import settings


def send_review_template(to: str, customer_name: str, company_name: str, review_link: str) -> dict:
    if not settings.whatsapp_access_token or not settings.whatsapp_phone_number_id:
        raise RuntimeError('Credenciais do WhatsApp não configuradas')

    url = (
        f"https://graph.facebook.com/{settings.whatsapp_api_version}/"
        f"{settings.whatsapp_phone_number_id}/messages"
    )

    payload = {
        'messaging_product': 'whatsapp',
        'to': to,
        'type': 'template',
        'template': {
            'name': 'review_request',
            'language': {'code': 'pt_BR'},
            'components': [
                {
                    'type': 'body',
                    'parameters': [
                        {'type': 'text', 'text': customer_name},
                        {'type': 'text', 'text': company_name},
                        {'type': 'text', 'text': review_link},
                    ],
                }
            ],
        },
    }

    response = requests.post(
        url,
        json=payload,
        headers={'Authorization': f'Bearer {settings.whatsapp_access_token}'},
        timeout=15,
    )
    response.raise_for_status()
    return response.json()
