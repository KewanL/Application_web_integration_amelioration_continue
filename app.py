import streamlit as st
from logic import services
from data import repository

st.title("Cinéma App")

menu = st.sidebar.selectbox("Menu", ["Ajouter Film", "Ajouter Membre", "Acheter Film"])

# ---- Ajouter Film ----
if menu == "Ajouter Film":
    st.header("Ajouter un film")

    title = st.text_input("Titre")
    price = st.number_input("Prix", min_value=0.0)

    if st.button("Ajouter"):
        try:
            services.create_film(title, price)
            st.success("Film ajouté")
        except Exception as e:
            st.error(str(e))


# ---- Ajouter Membre ----
elif menu == "Ajouter Membre":
    st.header("Ajouter un membre")

    name = st.text_input("Nom")
    balance = st.number_input("Solde", min_value=0.0)

    if st.button("Ajouter"):
        try:
            services.create_member(name, balance)
            st.success("Membre ajouté")
        except Exception as e:
            st.error(str(e))


# ---- Acheter Film ----
elif menu == "Acheter Film":
    st.header("Acheter un film")

    members = repository.get_members()
    films = repository.get_films()

    member_dict = {f"{m[1]} (solde: {m[2]})": m[0] for m in members}
    film_dict = {f"{f[1]} (prix: {f[2]})": f[0] for f in films}

    selected_member = st.selectbox("Membre", list(member_dict.keys()))
    selected_film = st.selectbox("Film", list(film_dict.keys()))

    if st.button("Acheter"):
        try:
            services.purchase_film(member_dict[selected_member], film_dict[selected_film])
            st.success("Achat réussi")
        except Exception as e:
            st.error(str(e))