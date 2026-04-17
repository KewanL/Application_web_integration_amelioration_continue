import pytest
import os
import sqlite3
from logic import services
from data import repository

# Fixture pour préparer une base de données de test propre avant chaque test
@pytest.fixture(autouse=True)
def setup_test_db():
    # On s'assure que le dossier database existe
    if not os.path.exists("database"):
        os.makedirs("database")
    
    # On utilise une base de test spécifique pour ne pas écraser vos vraies données
    test_db = os.path.join("database", "cine_test.db")
    repository.DB_PATH = test_db # On force le repository à utiliser la base de test
    
    # Création des tables (similaire à votre script init_db.py)
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS transactions")
    cursor.execute("DROP TABLE IF EXISTS films")
    cursor.execute("DROP TABLE IF EXISTS members")
    
    cursor.execute("CREATE TABLE members (id INTEGER PRIMARY KEY, name TEXT, balance REAL)")
    cursor.execute("CREATE TABLE films (id INTEGER PRIMARY KEY, title TEXT, price REAL)")
    cursor.execute("CREATE TABLE transactions (id INTEGER PRIMARY KEY, member_id INTEGER, film_id INTEGER)")
    conn.commit()
    conn.close()
    
    yield # Le test s'exécute ici
    
    # Nettoyage après le test
    if os.path.exists(test_db):
        os.remove(test_db)

# --- TEST D'INTÉGRATION 1 : Création de Film ---
def test_integration_create_film():
    services.create_film("Interstellar", 15.0)
    
    films = repository.get_films() # Retourne une liste de tuples
    assert len(films) == 1
    # films est le premier tuple : (1, "Interstellar", 15.0)
    # Le titre "Interstellar" est à l'index 1 du tuple
    assert films[0][1] == "Interstellar"

# --- TEST D'INTÉGRATION 2 : Création de Membre ---
def test_integration_create_member():
    services.create_member("Alice", 100.0)
    
    members = repository.get_members() # Retourne une liste de tuples
    assert len(members) == 1
    # members est le premier tuple : (1, "Alice", 100.0)
    # Le nom "Alice" est à l'index 1 du tuple
    assert members[0][1] == "Alice"

# --- TEST D'INTÉGRATION 3 : Processus d'achat complet ---
def test_integration_purchase_flow():
    # 1. Préparation
    repository.add_member("Bob", 20.0)
    repository.add_film("Matrix", 10.0)
    
    # 2. Exécution (Bob achète Matrix pour 10$)
    services.purchase_film(1, 1)
    
    # 3. Vérifications
    member = repository.get_member(1) # Retourne un seul tuple (1, "Bob", 10.0)
    # Le solde est le 3ème élément, donc l'index 2
    assert member[2] == 10.0
    
    # Vérifier la présence de la transaction
    conn = repository.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions")
    tx = cursor.fetchall()
    conn.close()
    assert len(tx) == 1