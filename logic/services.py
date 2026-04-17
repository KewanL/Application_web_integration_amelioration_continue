from data import repository


def create_film(title, price):
    if not title or price <= 0:
        raise ValueError("Film invalide")

    repository.add_film(title, price)


def create_member(name, balance):
    if not name or balance < 0:
        raise ValueError("Membre invalide")

    repository.add_member(name, balance)


def purchase_film(member_id, film_id):
    member = repository.get_member(member_id)
    film = repository.get_film(film_id)

    if member is None or film is None:
        raise ValueError("Données invalides")

    balance = member[2]
    price = film[2]

    if balance < price:
        raise ValueError("Solde insuffisant")

    new_balance = balance - price

    repository.update_balance(member_id, new_balance)
    repository.add_transaction(member_id, film_id)

    return True