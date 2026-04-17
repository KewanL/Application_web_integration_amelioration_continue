import pytest
from unittest.mock import patch
from logic import services

# --- FONCTIONNALITÉ 1 : Création de Film ---
def test_create_film_nominal():
    # Cas nominal : données valides
    # On simule l'accès aux données pour que le test reste "unitaire"
    with patch("data.repository.add_film") as mock_add:
        services.create_film("Inception", 12.5)
        mock_add.assert_called_once() # Vérifie que la logique a bien tenté d'enregistrer

def test_create_film_invalid_price():
    # Cas limite : prix négatif (doit lever une erreur) [6, 7]
    with pytest.raises(ValueError, match="Film invalide"):
        services.create_film("Test", -5)

# --- FONCTIONNALITÉ 2 : Création de Membre ---
def test_create_member_nominal():
    # Cas nominal : membre valide
    with patch("data.repository.add_member") as mock_add:
        services.create_member("Alice", 100)
        mock_add.assert_called_once()

def test_create_member_invalid_name():
    # Cas erreur : nom vide [6, 7]
    with pytest.raises(ValueError, match="Membre invalide"):
        services.create_member("", 50)

# --- FONCTIONNALITÉ 3 : Achat de Film ---
def test_purchase_insufficient_balance():
    # Cas d'erreur : solde insuffisant [6, 8]
    # On simule un membre avec 5$ et un film à 10$
    with patch("data.repository.get_member", return_value=(1, "Bob", 5)):
        with patch("data.repository.get_film", return_value=(2, "Avatar", 10)):
            with pytest.raises(ValueError, match="Solde insuffisant"):
                services.purchase_film(1, 2)

def test_purchase_nominal():
    # Cas nominal : solde suffisant
    with patch("data.repository.get_member", return_value=(1, "Bob", 50)):
        with patch("data.repository.get_film", return_value=(2, "Avatar", 10)):
            with patch("data.repository.update_balance") as mock_update:
                with patch("data.repository.add_transaction") as mock_tx:
                    services.purchase_film(1, 2)
                    mock_update.assert_called_once() # Le solde doit être mis à jour
                    mock_tx.assert_called_once() # La transaction doit être enregistrée