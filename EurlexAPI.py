import requests
import xml.etree.ElementTree as ET
import re


def clean_text(text):
    # Define the patterns to remove
    patterns = [
        r'\(UE\)',  # Matches (UE)
        r'\(CE\)',  # Matches (CE)
        r'\bUE\b',  # Matches UE as a whole word
        r'\bCE\b',  # Matches CE as a whole word
        r'\bno\b'  # Matches the word no
    ]

    # Combine the patterns into a single regular expression
    combined_pattern = '|'.join(patterns)

    # Use re.sub to replace the patterns with an empty string
    cleaned_text = re.sub(combined_pattern, '', text, flags=re.IGNORECASE)

    # Return the cleaned text, stripping any extra spaces
    return cleaned_text.strip()

def eurlexAPI(query):

    # SOAP request URL for EUR-Lex SOAP API
    url = "https://eur-lex.europa.eu/EURLexWebService"  # Update with the correct URL if needed

    # structured XML with WS-Security
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

    # headers
    options = {
        'Content-Type': 'text/xml; charset=utf-8'
    }
    # POST request
    response = requests.post(url, data=payload)
    root = ET.fromstring(response.text)


    for child in root.iter("{http://eur-lex.europa.eu/search}VALUE"):
        if 'eli' and 'data' in child.text:
            return child.text