<style>
div[data-testid="column"]:nth-of-type({i+1}) button {
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
}
</style>
""",
unsafe_allow_html=True,
)

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
