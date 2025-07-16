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
    """Return (is_valid, normalized_name)."""
    cleaned = " ".join(part for part in user_text.strip().split() if part)
    if len(cleaned.split()) < 2:
        return False, cleaned
    if expected_name is None:
        # If we don't have an expected name, any two-part name passes.
        return True, cleaned
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
                ss.celebration_pending = True  # trigger on next run
                st.rerun()  # refresh the UI so input disappears
            else:
                st.error(
                    "Ime i prezime nisu točni. Molimo unesite točno ime i prezime kako je navedeno u ugovoru."
                )
    else:
        # Show a simple inline message (no st.success)
        st.markdown(
            f"**Čestitka je autorizirana za:** {ss.authorized_name}. Sretan rođendan! 🥳"
        )

        # Fire toast + balloons exactly once when authorization first succeeds.
        if ss.celebration_pending and not ss.celebration_done:
            st.toast(
                f"Čestitka autorizirana za: {ss.authorized_name}! Sretan rođendan! 🥳",
                icon="🎉",
            )
            st.balloons()
            ss.celebration_pending = False
            ss.celebration_done = True


if __name__ == "__main__":
    main()
