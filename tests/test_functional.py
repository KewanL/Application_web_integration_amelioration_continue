import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="module")
def driver():
    chrome_options = Options()
    # chrome_options.add_argument("--headless") # Décommentez pour Jenkins
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    yield driver
    driver.quit()

def navigate_to_menu(driver, wait, menu_name):
    """Fonction utilitaire pour manipuler le selectbox Streamlit"""
    # 1. On cherche et on clique sur le selectbox pour l'ouvrir
    selectbox = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-baseweb='select']")))
    selectbox.click()
    time.sleep(1) # Petit délai pour laisser la liste s'afficher
    
    # 2. On clique sur l'option souhaitée dans la liste qui vient de s'ouvrir
    option = wait.until(EC.element_to_be_clickable((By.XPATH, f"//li[contains(., '{menu_name}')]")))
    option.click()
    time.sleep(1) # Attendre la mise à jour de la page

# --- TEST 1 : Vérifier le titre ---
def test_home_page_title(driver):
    driver.get("http://localhost:8501")
    wait = WebDriverWait(driver, 15)
    title_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
    assert "Cinéma App" in title_element.text

# --- TEST 2 : Navigation vers "Acheter Film" ---
def test_navigation_to_buy_movie(driver):
    driver.get("http://localhost:8501")
    wait = WebDriverWait(driver, 15)
    
    navigate_to_menu(driver, wait, "Acheter Film")
    
    header = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h2")))
    assert "Acheter un film" in header.text

# --- TEST 3 : Ajouter un membre (Scénario complet) ---
def test_add_member_flow(driver):
    driver.get("http://localhost:8501")
    wait = WebDriverWait(driver, 15)

    navigate_to_menu(driver, wait, "Ajouter Membre")

    # On récupère la liste de TOUS les champs de saisie
    inputs = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "input")))

    # On cible spécifiquement le premier champ  pour le nom
    inputs[1].send_keys("User Test Selenium")
    time.sleep(1.5) # Petit délai pour éviter les problèmes de synchronisation

    # On cible spécifiquement le deuxième champ [2] pour le solde
    inputs[2].click()
    time.sleep(1.5)
    # On simule CTRL+A (sélectionner tout) puis BACKSPACE (effacer) 
    # pour forcer la suppression du "0.00" par défaut
    inputs[2].send_keys(Keys.CONTROL + "a")
    time.sleep(1.5)
    inputs[2].send_keys(Keys.BACKSPACE)
    time.sleep(0.5)
    # On tape la valeur souhaitée
    inputs[2].send_keys("200,00")
    time.sleep(1.5)

    # Cliquer sur le bouton de validation
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Ajouter')]")))
    button.click()

    # Vérification du message de succès
    success_msg = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".stAlert")))
    assert "succès" in success_msg.text.lower() or "ajouté" in success_msg.text.lower()