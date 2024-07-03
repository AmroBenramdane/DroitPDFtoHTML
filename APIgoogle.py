import requests

API_KEY = 'AIzaSyAs53fYWlqCTaLrfEL_ZrA36M_GU4nDzB0'

SEARCH_ENGINE_ID = '51d9b1ff1dd284d67'

def requetsGoogleSearch(requetes):

    url = 'https://www.googleapis.com/customsearch/v1'

    params = {
        'q': requetes,
        'key': API_KEY,
        'cx': SEARCH_ENGINE_ID
    }

    response = requests.get(url, params=params)
    results = response.json()

    if 'items' in results:
        return results['items'][0]['link']
