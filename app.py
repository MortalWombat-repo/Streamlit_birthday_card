import time
import streamlit as st
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

st.set_page_config(page_title="Čestitka", layout="wide")

EXPECTED_FULL_NAME = os.getenv("EXPECTED_FULL_NAME")


def validate_full_name(user_text: str, expected_name: str) -> tuple[bool, str]:
    cleaned = " ".join(part for part in user_text.strip().split() if part)
    if len(cleaned.split()) < 2:
        return False, cleaned
    if expected_name is None:
        return True, cleaned
    if cleaned.lower() != expected_name.strip().lower():
        return False, cleaned
    return True, cleaned


# Inject Pacifico font and CSS for the birthday card header
def inject_pacifico_css():
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Pacifico&display=swap" rel="stylesheet">
        <style>
        .birthday-card-title {
            font-family: 'Pacifico', cursive !important;
            font-size: 3rem;
            color: #ff7f7f; /* Pastel red */
            margin: 20px 0;
        }
        </style>
    """, unsafe_allow_html=True)


def show_birthday_card(name: str):
    inject_pacifico_css()
    st.markdown(f"""
        <div style="text-align:center; padding: 20px;">
            <h1 class="birthday-card-title">Sretan rođendan, {name}!</h1>
            <p style="font-size:1.5rem;">Želimo ti puno zdravlja, sreće i uspjeha! 🥳</p>
        </div>
    """, unsafe_allow_html=True)


def main():
    ss = st.session_state
    if "authorized" not in ss:
        ss.authorized = False
    if "authorized_name" not in ss:
        ss.authorized_name = ""
    if "celebration_pending" not in ss:
        ss.celebration_pending = False
    if "celebration_done" not in ss:
        ss.celebration_done = False

    col1, col2 = st.columns([1, 15])
    with col1:
        st.title("🎉")
    with col2:
        st.title("Čestitka za sretan rođendan")

    with st.sidebar:
        st.markdown("\n\n")
        st.markdown("## Čestitka za sretan rođendan")
        st.markdown("---")
        st.image("img/image-from-rawpixel.png")

    if not ss.authorized:
        name_input = st.text_input(
            "Molimo autorizirajte čestitku točnim imenom i prezimenom:",
            value="",
            max_chars=100,
            key="name_input_box",
        )

        if st.button("Potvrdi"):
            ok, normalized = validate_full_name(name_input, EXPECTED_FULL_NAME)
            if ok:
                ss.authorized = True
                ss.authorized_name = normalized
                ss.celebration_pending = True
                st.experimental_rerun()
            else:
                st.error(
                    "Ime i prezime nisu točni. Molimo unesite točno ime i prezime kako je navedeno u ugovoru."
                )
    else:
        if ss.celebration_pending and not ss.celebration_done:
            st.toast(
                f"Čestitka autorizirana za: {ss.authorized_name}! Sretan rođendan! 🥳",
                icon="🎉",
            )
            st.balloons()
            time.sleep(3)  # Pause to let balloons finish animation
            show_birthday_card(ss.authorized_name)
            ss.celebration_pending = False
            ss.celebration_done = True
        elif ss.celebration_done:
            show_birthday_card(ss.authorized_name)


if __name__ == "__main__":
    main()
