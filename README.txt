

# 2.1 Lancer l'appli web 
streamlit run app.py


# 2.2 Lancer les tests unitaires 
python -m pytest tests/test_services.py

# 2.3 Lancer les tests d'integration 
python -m pytest tests/test_integration.py

# 2.4 Lancer les tests fonctionnels 
python -m pytest tests/test_functional.py

# 2.5 
# Lancer la couverture de test : 
coverage run -m pytest
coverage report

# Pylint pour mesurer la qualité, complexité, duplication indirecte, conventions du code : 
pylint logic data app.py

# Pour la vulnérabilité :
bandit -r .  # Tout le code, même les libraires
bandit -r app.py logic data   # S'arrête au code du site web

# Pour la qualité Gate
coverage report --fail-under=70


# 2.7 Intégration de la surveillance 
# Tester New Relic : 
newrelic-admin validate-config newrelic.ini stdout

# Tester monitor_dashboard :
streamlit run monitor_dashboard.py