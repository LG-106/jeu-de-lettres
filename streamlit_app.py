import streamlit as st
import uuid

# Initialisation des données persistantes
if "index" not in st.session_state:
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.total = 0
    st.session_state.clicked = []
    st.session_state.locked = False

st.set_page_config(page_title="Jeu des Lettres", layout="wide")
st.title("🎯 Jeu des Lettres")

# Choix du mode utilisateur
mode = st.radio("Qui utilise cette application ?", ["Elève", "Enseignant 🔐"], horizontal=True)

if mode == "Enseignant 🔐":
    mdp = st.text_input("Mot de passe enseignant :", type="password")
    if mdp != "modou123":
        st.warning("Mot de passe incorrect.")
        st.stop()
    show_teacher = True
else:
    show_teacher = False

# Saisie enseignant (protégée)
if show_teacher:
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

# Jeu actif
if "phrases" in st.session_state and st.session_state.index < len(st.session_state.phrases):
    phrase = st.session_state.phrases[st.session_state.index]
    lettres_cibles = st.session_state.consignes[st.session_state.index]

    if st.session_state.index == 0 or st.session_state.consignes[st.session_state.index] != st.session_state.consignes[st.session_state.index - 1]:
        st.markdown(f"### 🌐 Appuie sur la lettre{'s' if len(lettres_cibles) > 1 else ''} : **{', '.join(lettres_cibles)}**")

    # Zone d'affichage personnalisée
    phrase_zone = ""
    for i, lettre in enumerate(phrase):
        unique_id = f"letter_{st.session_state.index}_{i}"
        if "_clicks" not in st.session_state:
            st.session_state._clicks = {}
        clicked = st.session_state.clicked[st.session_state.index][i]

        if st.session_state.locked:
            if clicked and lettre.lower() in lettres_cibles:
                bg = "#28a745"
            elif clicked and lettre.lower() not in lettres_cibles:
                bg = "#dc3545"
            elif not clicked and lettre.lower() in lettres_cibles:
                bg = "#fd7e14"
            else:
                bg = "#ffffff"
        else:
            bg = "#00cc44" if clicked else "#ffffff"

        style = f"""
        <style>
        div[role="button"][id="{unique_id}"] {{
            background-color: {bg};
            color: black;
            display: inline-block;
            margin: 0.2em;
            padding: 0.5em 0.7em;
            border-radius: 0.5em;
            cursor: pointer;
            border: 1px solid #ccc;
            font-size: 1.2em;
            text-align: center;
            width: 2.5em;
        }}
        </style>
        """

        st.markdown(style + f'<div id="{unique_id}" role="button">{lettre}</div>', unsafe_allow_html=True)

        if not st.session_state.locked:
            if st.session_state.get("_last_clicked") == unique_id:
                st.session_state.clicked[st.session_state.index][i] = not clicked
                st.session_state._last_clicked = None

    # JS pour gérer le clic en HTML pur
    st.markdown("""
    <script>
    const blocks = window.parent.document.querySelectorAll('[role="button"]');
    blocks.forEach(btn => {
        btn.onclick = () => {
            const input = window.parent.document.createElement("input");
            input.type = "hidden";
            input.name = "click_event";
            input.value = btn.id;
            window.parent.document.body.appendChild(input);
            input.form.dispatchEvent(new Event("submit", {cancelable: true}));
        }
    });
    </script>
    """, unsafe_allow_html=True)

    clicked_id = st.experimental_get_query_params().get("click_event", [None])[0]
    if clicked_id:
        st.session_state._last_clicked = clicked_id

    # Validation
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
