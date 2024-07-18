from bs4 import BeautifulSoup
from urllib.parse import urljoin
from API import APIgoogle, EurlexAPI


def HTML_RefDic(file_path):
    base_url = 'https://eur-lex.europa.eu'

    # Lire le fichier HTML
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Analyser le contenu HTML
    soup = BeautifulSoup(html_content, 'lxml')
    oj_notes = soup.find_all(class_=['oj-note', 'note'])  # Chercher les deux classes

    result = {}
    for note in oj_notes:
        a_tags = note.find_all('a')
        for a in a_tags:
            if a.get('id'):
                note_id = a['id']
                note_number = a.get_text(strip=True).replace('\xa0', ' ')

                # Trouver le texte suivant immédiatement la balise <a>
                note_text = a.find_next_sibling(text=True).strip().replace('\xa0', ' ')

                # Si le texte est vide, chercher un autre lien <a> dans la même balise <p>
                if not note_text:
                    sibling_a = a.find_next('a', href=True)
                    if sibling_a:
                        note_text = urljoin(base_url, sibling_a['href'])
                    else:
                        note_text = urljoin(base_url, a['href'])
                else:
                    # Si le texte commence par "Directive", "Règlement" ou "Recommandation", prendre seulement les trois premiers termes
                    if note_text.startswith(("Directive", "Règlement", "Recommandation")):
                        temp = note_text
                        note_text = EurlexAPI.clean_text(' '.join(note_text.split()[:4]))
                        note_text = EurlexAPI.eurlexAPI(' '.join(note_text.split()[:2]))
                        if note_text is None:
                            note_text = APIgoogle.requetsGoogleSearch(temp)
                    else:
                        note_text = APIgoogle.requetsGoogleSearch(note_text)

                print(note_text)
                result[note_id] = (note_number, note_text)

    return result


def BetterHTML(file_path, replacements_dict):
    # Lire le contenu du fichier HTML
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Analyser le contenu HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Parcourir toutes les balises <a>
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        # Vérifier si le href commence par '#'
        if href.startswith('#'):
            # Extraire l'id
            id_key = href[1:]
            # Vérifier si l'id est dans le dictionnaire
            if id_key in replacements_dict:
                # Remplacer le href par la valeur correspondante dans le dictionnaire
                a_tag['href'] = replacements_dict[id_key][1]
                # Ajouter l'attribut target="_blank" pour ouvrir dans un nouvel onglet
                a_tag['target'] = '_blank'

    # Sauvegarder le HTML modifié dans le fichier d'origine
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(str(soup))

    print(f'Fichier modifié sauvegardé sous {file_path}')


def insert_tocbot(file_path):
    base_url = 'https://eur-lex.europa.eu'

    # Lire le fichier HTML
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Analyser le contenu HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Ajouter le conteneur de la table des matières
    toc_div = soup.new_tag('div', id='toc')
    soup.body.insert(0, toc_div)

    # Ajouter les liens Tocbot CSS et JS
    tocbot_css = soup.new_tag('link', rel='stylesheet', href='https://cdnjs.cloudflare.com/ajax/libs/tocbot/4.11.1/tocbot.css')
    soup.head.append(tocbot_css)

    tocbot_js = soup.new_tag('script', src='https://cdnjs.cloudflare.com/ajax/libs/tocbot/4.11.1/tocbot.min.js')
    soup.body.append(tocbot_js)

    # Ajouter le script d'initialisation de Tocbot
    init_script = soup.new_tag('script')
    init_script.string = """
    document.addEventListener('DOMContentLoaded', function() {
        tocbot.init({
            tocSelector: '#toc',
            contentSelector: 'body',
            headingSelector: 'h1, h2, h3, h4, h5, h6',
        });
    });
    """
    soup.body.append(init_script)


    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(str(soup))


# Exemple d'utilisation
file_path = '../FichiersDeTest/RIAA.html'  # Remplacez par le chemin de votre fichier HTML

replacements_dict = HTML_RefDic(file_path)

# Modifier le contenu HTML
BetterHTML(file_path, replacements_dict)
