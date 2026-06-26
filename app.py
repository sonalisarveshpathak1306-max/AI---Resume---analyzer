import streamlit as st
import PyPDF2
import google.generativeai as genai

GOOGLE_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
genai.configure(api_key=GOOGLE_API_KEY)

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")
st.title("AI Resume Analyzer 🤖")
st.subheader("Analyze your resume and get the best career insights!")
st.markdown("---")

uploaded_file = st.file_uploader("Upload your Resume here (PDF format recommended)", type=["pdf"])

if uploaded_file is not None:
    st.success(f"'{uploaded_file.name}' has been successfully uploaded.")
    
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    resume_text = ""
    for page in pdf_reader.pages:
        text = page.extract_text()
        if text:
            resume_text += text

    if st.button("Analyze Resume"):
        with st.spinner("AI is analyzing your resume... Please wait..."):
            try:
                prompt = f"""
                You are an expert HR Manager and Technical Recruiter. Analyze the following resume text carefully.
                Provide a detailed feedback in clear English covering:
                1. Professional Summary Evaluation
                2. Key Skills Identified
                3. Missing Critical Skills (based on modern data/tech roles)
                4. Overall Resume Score (out of 100)
                5. Actionable tips for improvement.
                
                Resume Text:
                {resume_text}
                """
                
                model = genai.GenerativeModel('gemini-2.5-flash')
                response = model.generate_content(prompt)
                
                st.markdown("---")
                st.header("📋 AI Analysis Results")
                st.write(response.text)
                st.balloons()
                
            except Exception as e:
                st.error(f"An error occurred: {e}. Please check your API Key.")
