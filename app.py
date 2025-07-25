import time
import streamlit as st
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

st.set_page_config(page_title="Čestitka", layout="wide")

EXPECTED_FULL_NAME = os.getenv("EXPECTED_FULL_NAME")
first_name = os.getenv("FIRST_NAME")
baka_name = os.getenv("BAKA_NAME")
teta_name = os.getenv("TETA_NAME")
bratic_name = os.getenv("BRATIC_NAME")


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
            margin: 20px 0;
        }
        </style>
    """, unsafe_allow_html=True)

import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

image_base64 = get_base64_image("img/Pngtree6555382.png")

# Convert to Base64
def get_audio_base64(file_path):
    with open(file_path, "rb") as audio_file:
        return base64.b64encode(audio_file.read()).decode()

audio_base64 = get_audio_base64("music/happy_birthday.mp3")


def show_birthday_card(first_name: str):
    inject_pacifico_css()
    st.markdown(f"""
    <div style="text-align:center; padding: 20px;">
        <h1 class="birthday-card-title">🎉 Sretan rođendan, draga {first_name}! 🎉</h1>
        <p class="birthday-card-title" style="font-size:1.5rem;">Želimo ti puno zdravlja, sreće i uspjeha! 🥳</p>
        <p class="birthday-card-title" style="font-size:1.5rem;">Vole te tvoji Baka {baka_name}, Teta i Bratić</p>
        <img src="data:image/png;base64,{image_base64}" style="width:300px; margin-top:20px;"/>
        <audio autoplay>
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        </audio>
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
                st.rerun()  # immediately rerun so the 'authorized' branch executes
            else:
                st.error(
                    "Ime i prezime nisu točni. Molimo unesite točno ime i prezime kako je navedeno."
                )
    else:
        if ss.celebration_pending and not ss.celebration_done:
            st.toast(
                f"Čestitka autorizirana za: {ss.authorized_name}! Sretan rođendan! 🥳",
                icon="🎉",
            )
            st.balloons()
            time.sleep(3)  # Pause to let balloons finish animation
            show_birthday_card(first_name)
            ss.celebration_pending = False
            ss.celebration_done = True
        elif ss.celebration_done:
            show_birthday_card(first_name)


if __name__ == "__main__":
    main()
