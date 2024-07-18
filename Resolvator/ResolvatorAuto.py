import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Constantes pour le chemin vers ChromeDriver et l'extension
CHROME_DRIVER_PATH = 'ChromeExtension/chromedriver'
EXTENSION_PATH = 'ChromeExtension/ResolvatorExtension'

def modify_html_with_extension(html_file_path):
    # Configurer les options de Chrome
    chrome_options = Options()
    chrome_options.add_argument(f"--load-extension={os.path.abspath(EXTENSION_PATH)}")

    # Démarrer le service de Chrome
    service = Service(os.path.abspath(CHROME_DRIVER_PATH))
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Vérifier que le fichier HTML existe
    if not os.path.exists(html_file_path):
        raise FileNotFoundError(f"Le fichier {html_file_path} n'existe pas.")

    # Convertir le chemin du fichier en URL
    html_file_url = f"file://{os.path.abspath(html_file_path)}"

    # Ouvrir le document HTML
    driver.get(html_file_url)

    # Attendre que l'extension soit appliquée (ajustez le délai si nécessaire)
    input('Press enter to close browser')

    # Récupérer le contenu modifié
    modified_html = driver.page_source

    # Enregistrer le contenu modifié dans le même fichier
    with open(html_file_path, "w") as file:
        file.write(modified_html)

    # Fermer le navigateur
    driver.quit()


