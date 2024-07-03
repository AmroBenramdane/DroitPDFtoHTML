
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time


#runscript
profile_path = '/Users/amrobenramdane/Library/Application Support/Google/Chrome/Default'

# Chemin vers ChromeDriver (assurez-vous que ChromeDriver est dans /usr/local/bin)
chrome_driver_path = '/usr/local/bin/chromedriver'

# Chemin vers l'extension Resolvator
# extension_path = 'ChromeExtension/ResolvatorExtension.crx'
extension_path = '/Users/amrobenramdane/Downloads/ResolvatorExtension'
# Configurer les options de Chrome
chrome_options = Options()
#chrome_options.add_argument(f"user-data-dir={profile_path}")
chrome_options.add_argument(f"--load-extension={extension_path}")

# Démarrer le service de Chrome

service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Chemin vers votre fichier HTML
html_file_path = "file:///Users/amrobenramdane/Desktop/StageLAMSADE/test2.html"

# Ouvrir le document HTML
driver.get(html_file_path)


# Attendre que l'extension soit appliquée (ajustez le délai si nécessaire)

input('press enter to close browser')
# Récupérer le contenu modifié
modified_html = driver.page_source

# Enregistrer le contenu modifié dans un nouveau fichier
with open("modified_document.html", "w") as file:
    file.write(modified_html)

# Fermer le navigateur
driver.quit()
