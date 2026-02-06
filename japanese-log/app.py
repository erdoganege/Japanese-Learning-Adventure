import random

import streamlit as st
from datetime import date

from helpers import load_all_entries, save_entry, load_all_words

# ---------- UI ----------
st.set_page_config(
    page_title="Japanese Learning Log",
    page_icon="📘",
    layout="centered"
)

st.title("📘 Japanese Learning Log")

tab_entry, tab_history, tab_practice = st.tabs(["➕ New Entry", "📜 History", "🧠 Practice"])


# ---------- New Entry Tab ----------
with tab_entry:
    st.subheader("Daily Entry")

    entry_date = st.date_input("Date", value=date.today())

    st.markdown("### 🈶 Words learned")
    if "words" not in st.session_state:
        st.session_state.words = []

    col_add = st.columns([3, 3, 3, 1])
    with col_add[0]:
        word = st.text_input("Word")
    with col_add[1]:
        reading = st.text_input("Reading")
    with col_add[2]:
        meaning = st.text_input("Meaning")
    with col_add[3]:
        st.write("")
        add_word = st.button("＋")

    if add_word and word and reading and meaning:
        st.session_state.words.append(
            {"word": word, "reading": reading, "meaning": meaning}
        )

    for w in st.session_state.words:
        st.write(f"• {w['word']} ({w['reading']}) – {w['meaning']}")

    st.markdown("### 📘 Grammar learned")
    grammar_input = st.text_input("Add grammar point")
    if "grammar" not in st.session_state:
        st.session_state.grammar = []

    if st.button("Add grammar") and grammar_input:
        st.session_state.grammar.append(grammar_input)

    for g in st.session_state.grammar:
        st.write(f"• {g}")

    st.markdown("### ✍️ Summary")
    summary = st.text_area("What did you do today?")

    if st.button("💾 Save entry"):
        entry = {
            "date": entry_date.isoformat(),
            "words": st.session_state.words,
            "grammar": st.session_state.grammar,
            "summary": summary
        }
        save_entry(entry)
        st.success("Entry saved!")
        st.session_state.words = []
        st.session_state.grammar = []


# ---------- History Tab ----------
with tab_history:
    st.subheader("History")

    entries = load_all_entries()

    if not entries:
        st.info("No entries yet.")
    else:
        for entry in entries:
            with st.expander(entry["date"]):
                if entry["words"]:
                    st.markdown("**Words**")
                    for w in entry["words"]:
                        st.write(f"- {w['word']} ({w['reading']}) – {w['meaning']}")

                if entry["grammar"]:
                    st.markdown("**Grammar**")
                    for g in entry["grammar"]:
                        st.write(f"- {g}")

                if entry["summary"]:
                    st.markdown("**Summary**")
                    st.write(entry["summary"])

# ---------- Practice Tab ----------
def next_word(all_words):
    """Pick a random word"""
    st.session_state.current_word = random.choice(all_words)
    st.session_state.answer_checked = False
    st.session_state.practice_input = ""


with tab_practice:
    st.subheader("🧠 Word Practice")

    all_words = load_all_words()

    if not all_words:
        st.info("No words available yet. Add some entries first 🙂")
    else:
        if "current_word" not in st.session_state:
            st.session_state.current_word = random.choice(all_words)
            st.session_state.answer_checked = False
            st.session_state.practice_input = ""

        word = st.session_state.current_word

        st.markdown(f"### 🈶 {word['word']}")

        user_reading = st.text_input("Enter the reading", key="practice_input")

        if st.button("Check"):
            st.session_state.answer_checked = True
            if user_reading.strip().lower() == word["reading"].lower():
                st.success("✅ Correct!")
                st.success(f"Meaning: {word["meaning"]}")
            else:
                st.error(f"❌ Wrong. Correct reading: **{word['reading']}**")

        if st.session_state.answer_checked:
            st.button("Next word", on_click=next_word, args=(all_words,))
