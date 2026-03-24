import requests

from app.core.config import settings


def build_review_link(place_id: str) -> str:
    return f'https://search.google.com/local/writereview?placeid={place_id}'


def fetch_place_details(place_id: str) -> dict:
    if not settings.google_api_key:
        raise RuntimeError('GOOGLE_API_KEY não configurada')

    url = 'https://maps.googleapis.com/maps/api/place/details/json'
    params = {
        'place_id': place_id,
        'key': settings.google_api_key,
        'fields': 'place_id,name,url,rating,user_ratings_total',
    }

    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()
    return response.json()
