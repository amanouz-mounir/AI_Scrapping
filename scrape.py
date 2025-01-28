from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# Définir les informations d'authentification pour se connecter au proxy
AUTH = 'brd-customer-hl_ecc1bceb-zone-ai_scraper:1kwl4owhf2g2'
SBR_WEBDRIVER = f'https://{AUTH}@brd.superproxy.io:9515'

def scrape_website(website):
    """
    Scrape le contenu d'un site web à l'aide d'un navigateur distant.
    Prend en entrée l'URL du site web et retourne le code HTML de la page.
    """
    print("Launching Chromium browser...")

    # Initialisation de la connexion avec le proxy
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    
    # Lancer le navigateur à distance avec les options spécifiées
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        print('Connected! Navigating...')
        
        # Ouvrir le site web dans le navigateur
        driver.get(website)
        
        # Prendre une capture d'écran de la page et l'enregistrer
        print('Taking page screenshot to file page.png')
        driver.get_screenshot_as_file('./page.png')
        
        # Attendre la page soit complètement chargée avant de scraper
        print('Navigated! Scraping page content...')
        
        # Récupérer le code HTML de la page
        html = driver.page_source
        return html

def extract_body_content(html_content):
    """
    Extrait le contenu du corps de la page à partir du HTML.
    Retire toutes les balises non essentielles et retourne seulement le contenu principal du body.
    """
    # Utilisation de BeautifulSoup pour parser le contenu HTML
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Extraire le contenu de la balise <body>
    body_content = soup.body
    
    # Vérifier si le contenu du body existe et le retourner
    if body_content:
        return str(body_content)
    return ""  # Retourner une chaîne vide si le body est vide

def clean_body_content(body_content):
    """
    Nettoie le contenu du body en retirant les balises <script> et <style>,
    puis retourne le texte brut de la page.
    """
    # Parse le contenu HTML du body
    soup = BeautifulSoup(body_content, "html.parser")

    # Supprimer toutes les balises <script> et <style> qui ne sont pas nécessaires
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()
    
    # Extraire le texte brut du contenu HTML, avec un séparateur de lignes
    cleaned_content = soup.get_text(separator="\n")
    
    # Enlever les lignes vides ou seulement composées d'espaces
    cleaned_content = "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())
    
    return cleaned_content

def split_dom_content(dom_content, max_length=3000):
    """
    Divise le contenu DOM en plusieurs parties pour éviter de dépasser la longueur maximale.
    Retourne une liste de chaînes contenant des parties du contenu.
    """
    return [
        dom_content[i: i + max_length] for i in range(0, len(dom_content), max_length)
    ]
