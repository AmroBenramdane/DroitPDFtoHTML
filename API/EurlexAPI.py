import requests
import xml.etree.ElementTree as ET
import re

def clean_text(text):
    patterns = [
        r'\(UE\)',  # Matches (UE)
        r'\(CE\)',  # Matches (CE)
        r'\bUE\b',  # Matches UE as a whole word
        r'\bCE\b',  # Matches CE as a whole word
        r'\bno\b',   # Matches the word no
        r'\bn° \b'
    ]
    combined_pattern = '|'.join(patterns)
    cleaned_text = re.sub(combined_pattern, '', text, flags=re.IGNORECASE)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    return cleaned_text.strip()

def eurlexAPI(query):
    url = "https://eur-lex.europa.eu/EURLexWebService"

    payload = f"""
    <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:sear="http://eur-lex.europa.eu/search" xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
      <soap:Header>
        <wsse:Security soap:mustUnderstand="1">
          <wsse:UsernameToken wsu:Id="UsernameToken-1">
            <wsse:Username>n00gb64b</wsse:Username>
            <wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">DqrEWtiXOO2</wsse:Password>
          </wsse:UsernameToken>
        </wsse:Security>
      </soap:Header>
      <soap:Body>
        <sear:searchRequest>
          <sear:expertQuery>QUICK_SEARCH = "{clean_text(query)}"</sear:expertQuery>
          <sear:page>1</sear:page>
          <sear:pageSize>10</sear:pageSize>
          <sear:searchLanguage>fr</sear:searchLanguage>
        </sear:searchRequest>
      </soap:Body>
    </soap:Envelope>"""

    encoded_payload = payload.encode('utf-8')

    headers = {
        'Content-Type': 'application/soap+xml; charset=utf-8'
    }

    try:
        response = requests.post(url, data=encoded_payload, headers=headers)

        if response.status_code != 200:
            print("Échec de la requête. Statut:", response.status_code)
            print("Texte de la réponse:", response.text)
            return None


        root = ET.fromstring(response.text)

        for child in root.iter("{http://eur-lex.europa.eu/search}VALUE"):
            if 'eli' in child.text and 'data' in child.text:
                return child.text

        print("Aucun élément correspondant trouvé.")
        return None

    except Exception as e:
        print("Une exception s'est produite:", str(e))
        return None
