import streamlit as st
import json
from pathlib import Path
from datetime import date

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)


# ---------- Helpers ----------
def save_entry(entry):
    file_path = DATA_DIR / f"{entry['date']}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(entry, f, ensure_ascii=False, indent=2)


def load_all_entries():
    entries = []
    for file in DATA_DIR.glob("*.json"):
        with open(file, "r", encoding="utf-8") as f:
            entries.append(json.load(f))
    return sorted(entries, key=lambda x: x["date"], reverse=True)


# ---------- UI ----------
st.set_page_config(
    page_title="Japanese Learning Log",
    page_icon="📘",
    layout="centered"
)

st.title("📘 Japanese Learning Log")

tab_entry, tab_history = st.tabs(["➕ New Entry", "📜 History"])


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
