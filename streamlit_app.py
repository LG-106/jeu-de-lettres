import streamlit as st

st.set_page_config(page_title="Jeu des Lettres", layout="wide")
st.title("🎯 Jeu des Lettres")

# Choix du mode utilisateur
mode = st.radio("Qui utilise cette application ?", ["Elève", "Enseignant 🔐"], horizontal=True)

if mode == "Enseignant 🔐":
    mdp = st.text_input("Mot de passe enseignant :", type="password")
    if mdp != "modou123":
        st.warning("Mot de passe incorrect.")
        st.stop()
    with st.expander("🧑‍🏫 Paramètres enseignant", expanded=True):
        phrases_input = st.text_area("Phrases (une par ligne)", height=150)
        lettres_input = st.text_area("Lettres à chercher (une ligne par phrase, ou vide pour répéter)", height=150)
        if st.button("Lancer le jeu"):
            st.session_state.index = 0
            st.session_state.score = 0
            st.session_state.total = 0
            st.session_state.locked = False

            st.session_state.phrases = [p.strip() for p in phrases_input.split("\n") if p.strip()]
            consignes_brutes = lettres_input.split("\n")
            consignes = []
            last = []
            for ligne in consignes_brutes:
                lettres = [l.strip().lower() for l in ligne.strip().split(",") if l.strip()]
                if lettres:
                    last = lettres
                consignes.append(last.copy())
            while len(consignes) < len(st.session_state.phrases):
                consignes.append(last.copy())
            st.session_state.consignes = consignes
            st.session_state.clicked = [[False] * len(p) for p in st.session_state.phrases]

if mode == "Elève":
    if "phrases" not in st.session_state or "consignes" not in st.session_state:
        st.error("Aucune donnée trouvée. Veuillez d'abord lancer le jeu depuis l'interface enseignant.")
        st.stop()

    phrase = st.session_state.phrases[st.session_state.index]
    lettres_cibles = st.session_state.consignes[st.session_state.index]

    if st.session_state.index == 0 or st.session_state.consignes[st.session_state.index] != st.session_state.consignes[st.session_state.index - 1]:
        st.markdown(f"### 🌐 Appuie sur la lettre{'s' if len(lettres_cibles) > 1 else ''} : **{', '.join(lettres_cibles)}**")

    cols = st.columns(len(phrase))
    for i, lettre in enumerate(phrase):
        clicked = st.session_state.clicked[st.session_state.index][i]

        if st.session_state.locked:
            if clicked and lettre.lower() in lettres_cibles:
                color = "#28a745"
            elif clicked and lettre.lower() not in lettres_cibles:
                color = "#dc3545"
            elif not clicked and lettre.lower() in lettres_cibles:
                color = "#fd7e14"
            else:
                color = "#ffffff"
        else:
            color = "#00cc44" if clicked else "#ffffff"

        if cols[i].button(lettre, key=f"btn_{st.session_state.index}_{i}"):
            if not st.session_state.locked:
                st.session_state.clicked[st.session_state.index][i] = not clicked

        st.markdown(f"""
        <style>
        div[data-testid="column"]:nth-of-type({i+1}) button {{
            background-color: {color} !important;
            box-shadow: none !important;
            outline: none !important;
            color: black;
            font-size: 20px;
            height: 3em;
            width: 3em;
            border: none;
            border-radius: 8px;
            margin-bottom: 0.5em;
        }}
        </style>
        """, unsafe_allow_html=True)

    if not st.session_state.locked:
        if st.button("✅ Valider mes réponses"):
            st.session_state.locked = True
            phrase = st.session_state.phrases[st.session_state.index]
            lettres = lettres_cibles
            score = 0
            total = sum(1 for l in phrase if l.lower() in lettres)

            for i, l in enumerate(phrase):
                if st.session_state.clicked[st.session_state.index][i] and l.lower() in lettres:
                    score += 1

            st.session_state.score += score
            st.session_state.total += total

    else:
        st.success(f"✔ Tu as trouvé {st.session_state.score} lettre(s) sur {st.session_state.total}.")
        if st.button("➡ Phrase suivante"):
            st.session_state.index += 1
            if st.session_state.index < len(st.session_state.phrases):
                st.session_state.locked = False
            else:
                st.balloons()
                st.success(f"🎉 Jeu terminé ! Score total : {st.session_state.score}/{st.session_state.total}")
                del st.session_state["phrases"]
                del st.session_state["consignes"]
                del st.session_state["clicked"]
import streamlit as st

st.set_page_config(page_title="Jeu des Lettres", layout="wide")
st.title("🎯 Jeu des Lettres")

# Choix du mode utilisateur
mode = st.radio("Qui utilise cette application ?", ["Elève", "Enseignant 🔐"], horizontal=True)

if mode == "Enseignant 🔐":
    mdp = st.text_input("Mot de passe enseignant :", type="password")
    if mdp != "modou123":
        st.warning("Mot de passe incorrect.")
        st.stop()
    with st.expander("🧑‍🏫 Paramètres enseignant", expanded=True):
        phrases_input = st.text_area("Phrases (une par ligne)", height=150)
        lettres_input = st.text_area("Lettres à chercher (une ligne par phrase, ou vide pour répéter)", height=150)
        if st.button("Lancer le jeu"):
            st.session_state.index = 0
            st.session_state.score = 0
            st.session_state.total = 0
            st.session_state.locked = False

            st.session_state.phrases = [p.strip() for p in phrases_input.split("\n") if p.strip()]
            consignes_brutes = lettres_input.split("\n")
            consignes = []
            last = []
            for ligne in consignes_brutes:
                lettres = [l.strip().lower() for l in ligne.strip().split(",") if l.strip()]
                if lettres:
                    last = lettres
                consignes.append(last.copy())
            while len(consignes) < len(st.session_state.phrases):
                consignes.append(last.copy())
            st.session_state.consignes = consignes
            st.session_state.clicked = [[False] * len(p) for p in st.session_state.phrases]

if mode == "Elève":
    if "phrases" not in st.session_state or "consignes" not in st.session_state:
        st.error("Aucune donnée trouvée. Veuillez d'abord lancer le jeu depuis l'interface enseignant.")
        st.stop()

    phrase = st.session_state.phrases[st.session_state.index]
    lettres_cibles = st.session_state.consignes[st.session_state.index]

    if st.session_state.index == 0 or st.session_state.consignes[st.session_state.index] != st.session_state.consignes[st.session_state.index - 1]:
        st.markdown(f"### 🌐 Appuie sur la lettre{'s' if len(lettres_cibles) > 1 else ''} : **{', '.join(lettres_cibles)}**")

    cols = st.columns(len(phrase))
    for i, lettre in enumerate(phrase):
        clicked = st.session_state.clicked[st.session_state.index][i]

        if st.session_state.locked:
            if clicked and lettre.lower() in lettres_cibles:
                color = "#28a745"
            elif clicked and lettre.lower() not in lettres_cibles:
                color = "#dc3545"
            elif not clicked and lettre.lower() in lettres_cibles:
                color = "#fd7e14"
            else:
                color = "#ffffff"
        else:
            color = "#00cc44" if clicked else "#ffffff"

        with cols[i]:
            if st.button(lettre, key=f"btn_{st.session_state.index}_{i}"):
                if not st.session_state.locked:
                    st.session_state.clicked[st.session_state.index][i] = not clicked

            st.markdown(
                f"""
                <style>
                div[data-testid="column"]:nth-of-type({i+1}) button {{
                    background-color: {color} !important;
                    box-shadow: none !important;
                    outline: none !important;
                    color: black;
                    font-size: 20px;
                    height: 3em;
                    width: 3em;
                    border: none;
                    border-radius: 8px;
                    margin-bottom: 0.5em;
                }}
                </style>
                """,
                unsafe_allow_html=True
            )

    if not st.session_state.locked:
        if st.button("✅ Valider mes réponses"):
            st.session_state.locked = True
            phrase = st.session_state.phrases[st.session_state.index]
            lettres = lettres_cibles
            score = 0
            total = sum(1 for l in phrase if l.lower() in lettres)

            for i, l in enumerate(phrase):
                if st.session_state.clicked[st.session_state.index][i] and l.lower() in lettres:
                    score += 1

            st.session_state.score += score
            st.session_state.total += total

    else:
        st.success(f"✔ Tu as trouvé {st.session_state.score} lettre(s) sur {st.session_state.total}.")
        if st.button("➡ Phrase suivante"):
            st.session_state.index += 1
            if st.session_state.index < len(st.session_state.phrases):
                st.session_state.locked = False
            else:
                st.balloons()
                st.success(f"🎉 Jeu terminé ! Score total : {st.session_state.score}/{st.session_state.total}")
                del st.session_state["phrases"]
                del st.session_state["consignes"]
                del st.session_state["clicked"]
