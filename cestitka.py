import time
import streamlit as st
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Streamlit Config
st.set_page_config(page_title="Čestitka", layout="wide")

# Get expected full name from .env or fallback
EXPECTED_FULL_NAME = os.getenv("EXPECTED_FULL_NAME")


def validate_full_name(user_text: str, expected_name: str) -> tuple[bool, str]:
    cleaned = " ".join(part for part in user_text.strip().split() if part)
    if len(cleaned.split()) < 2:
        return False, cleaned
    if cleaned.lower() != expected_name.strip().lower():
        return False, cleaned
    return True, cleaned


def main():
    ss = st.session_state

    # Initialize session state
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
        st.markdown("\n\n\n")
        st.markdown("## Čestitka za sretan rođendan")
        st.markdown("---")
        st.image("img/image-from-rawpixel.png")

    st.subheader("Autorizacija čestitke")

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
                st.toast(f"Čestitka autorizirana za: {normalized}", icon="🎉")
            else:
                st.error(
                    "Ime i prezime nisu točni. Molimo unesite točno ime i prezime."
                )
    else:
        st.success(
            f"Čestitka je autorizirana za: **{ss.authorized_name}**. Sretan rođendan! 🥳"
        )

        # Show balloons once after authorization
        if ss.celebration_pending and not ss.celebration_done:
            st.balloons()
            ss.celebration_pending = False
            ss.celebration_done = True


if __name__ == "__main__":
    main()
