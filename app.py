import streamlit as st
import fitz  # PyMuPDF
from groq_api import summarize_text, generate_mcq, parse_mcq_text

st.set_page_config(page_title="AI PDF Summarizer & MCQ Quizzer", layout="wide")
st.title("📄 AI PDF Summarizer & Interactive MCQ Test (Groq + LLaMA 3.3)")

# File Upload
uploaded_file = st.file_uploader("📤 Upload a PDF file", type=["pdf"])

if uploaded_file:
    with st.spinner("📚 Extracting text from PDF..."):
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        full_text = ""
        for page in doc:
            full_text += page.get_text()

 

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🧾 Generate Summary"):
            with st.spinner("Generating summary using LLaMA 3.3..."):
                summary = summarize_text(full_text)
            st.subheader("📌 Summary")
            st.write(summary)

    with col2:
        if st.button("🧠 Generate MCQ Quiz"):
            with st.spinner("Creating quiz..."):
                raw_quiz = generate_mcq(full_text[:4000])  # Limit to safe size
                st.session_state.mcq_data = parse_mcq_text(raw_quiz)

# If quiz exists in session state
if "mcq_data" in st.session_state:
    st.subheader("📝 MCQ Test")
    score = 0
    total = len(st.session_state.mcq_data)
    user_answers = {}

    for idx, q in enumerate(st.session_state.mcq_data):
        st.markdown(f"**Q{idx+1}. {q['question']}**")
        selected = st.radio(
            f"Choose an answer for Q{idx+1}",
            options=list(q["options"].keys()),
            format_func=lambda x: f"{x}) {q['options'][x]}",
            key=f"q_{idx}"
        )
        user_answers[idx] = selected

    if st.button("✅ Submit Test"):
        with st.spinner("Checking answers..."):
            for idx, q in enumerate(st.session_state.mcq_data):
                if user_answers.get(idx) == q["answer"]:
                    score += 1

        st.success(f"🎉 You scored {score} out of {total}")
        st.subheader("✅ Correct Answers")
        for idx, q in enumerate(st.session_state.mcq_data):
            correct_option = q["answer"]
            correct_text = q["options"].get(correct_option, "[Invalid Answer]")
            st.markdown(f"**Q{idx+1}:** {q['question']}")
            st.markdown(f"✔️ Correct Answer: `{correct_option}) {correct_text}`")
