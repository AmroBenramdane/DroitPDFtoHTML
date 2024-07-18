import requests
from bs4 import BeautifulSoup

API_KEY = 'AIzaSyAs53fYWlqCTaLrfEL_ZrA36M_GU4nDzB0'

SEARCH_ENGINE_ID = '51d9b1ff1dd284d67'

def requetsGoogleSearchTEST(requetes):

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



def requetsGoogleSearch(query):
    # Préparer l'URL de la recherche Google
    url = "https://www.google.com/search"
    params = {
        'q': query,
        'num': 1  # Obtenir uniquement le premier résultat
    }

    # Effectuer la requête de recherche
    response = requests.get(url, params=params)
    response.raise_for_status()  # Assurer que la requête a réussi

    # Analyser le contenu HTML de la page de résultats de recherche
    soup = BeautifulSoup(response.text, 'html.parser')
    # Trouver le premier lien dans les résultats de recherche
    link = soup.find('a', href=True)
    if link:
        return link['href']
    else:
        return None

