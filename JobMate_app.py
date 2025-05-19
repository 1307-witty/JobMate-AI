import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from PIL import Image
import torch

# ------------------------ Page Config & Logo ------------------------
st.set_page_config(page_title="JobMate: Your AI Career Assistant", layout="centered")
logo = Image.open("JobMate_logo.jpeg")  # Make sure this logo is in the same directory
st.image(logo, width=120)
st.title("JobMate: Your AI Career Assistant")
st.caption("Use open-source AI to generate resume summaries, cover letters, mock interviews, and extract skills.")

# ------------------------ Load Model ------------------------
@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
    model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")
    return tokenizer, model

tokenizer, model = load_model()

def generate_text(prompt, max_length=256):
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
    outputs = model.generate(**inputs, max_length=max_length, temperature=0.7)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# ------------------------ Tabs ------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📝 Resume Summary", 
    "📄 Full Resume", 
    "📩 Cover Letter", 
    "❓ Mock Interview Q&A", 
    "🧠 Extract Skills"
    ])

with tab1:
    st.header("Generate Resume Summary")
    role = st.text_input("Job Role (e.g. Software Developer)")
    university = st.text_input("University (e.g.Indian Institute of Technology)")
    degree = st.text_input("Degree (e.g. B.Sc Computer Science)")
    exp_level = st.selectbox("Experience Level", ["Fresher", "1-2 years", "3-5 years", "5-10 years", "Other"])
    if exp_level == "Other":
        custom_exp = st.text_input("Enter your experience (years)")
        exp_display = custom_exp
    else:
        exp_display = exp_level
    skills = st.text_area("Skills (comma-separated)")
    goals = st.text_area("Career Goals")
    if st.button("Generate Summary"):
        prompt = f"""
You are an experienced HR consultant. Write a concise, professional resume summary for a candidate applying for the role of {role}.
Include:
- University: {university}
- Degree: {degree}
- Experience: {exp_display}
- Skills: {skills}
- Career Goals: {goals}

Use strong action verbs and make it suitable for ATS systems. Avoid repetition and buzzwords."""

        with st.spinner("Generating Summary..."):
            result = generate_text(prompt, max_length=1000)
            st.success(result)

with tab2:
    st.header("Generate Full Resume") 
    name = st.text_input("Full Name") 
    email = st.text_input("Email") 
    phone = st.text_input("Phone Number") 
    degree = st.text_input("Degree") 
    experience = st.text_input("Experience") 
    skills = st.text_input("Skills (comma-separated)") 
    career_goal = st.text_area("Career Objective") 
    projects = st.text_area("Mention Your Projects") 
    certifications = st.text_area("Certifications (Optional)")

    if st.button("Generate Full Resume"):
        prompt = f"""
You are an expert in creating ATS-optimized resumes. Create a complete resume based on this data:

Name: {name}
Email: {email}
Phone: {phone}
Degree: {degree}
Experience: {experience}
Skills: {skills}
Career Objective: {career_goal}
Projects: {projects}
Certifications: {certifications}
Divide it into sections: Header, Summary, Skills, Projects, Education, Certifications, and Contact Info. Use professional formatting and make it suitable for a Word or PDF resume."""

        with st.spinner("Generating Resume..."):
            result = generate_text(prompt, max_length=600) 
            st.success(result)

with tab3:
    st.header("Generate Cover Letter")
    role = st.text_input("Target Role", key="role2")
    university = st.text_input("Your Degree", key="university2")
    degree = st.text_input("Your Degree", key="degree2")
    skills = st.text_area("Your Skills", key="skills2")
    goals = st.text_area("Your Career Goals", key="goals2")

    if st.button("Generate Cover Letter"):
        prompt = f"""
You are an Oxford professor mentoring students on job applications. Write a compelling, structured cover letter for a fresher applying for the position of {role}.

Details:
- University: {university}
- Degree: {degree}
- Skills: {skills}
- Career Goals: {goals}
Make the tone confident and enthusiastic. Highlight the candidate's strengths and eagerness to contribute."""

        with st.spinner("Creating Cover Letter..."):
            result = generate_text(prompt, max_length=300)
            st.success(result)

with tab4:
    st.header("Mock Interview Q&A")
    topic = st.text_input("Enter Interview Topic (e.g. Python, Data Structures, DBMS)")
    role = st.text_input("Enter Role:")
    if st.button("Generate Mock Q&A"):
        prompt = f"""
You are an experienced recruiter preparing candidates for interviews. List 15 relevant and important interview questions and sample answers.

Role: {role}
Topic: {topic}

Include a mix of basic and advanced questions with clear and short model answers. Focus on practical and technical relevance."""

        with st.spinner("Generating Interview Q&A..."):
            result = generate_text(prompt, max_length=700)
            st.success(result)

with tab5:
    st.header("Extract Skills from Job Description")
    jd = st.text_area("Paste Job Description")

    if st.button("Extract Skills"):
        prompt = f"""
You are an expert in parsing job descriptions. Extract 5 important and relevant technical or soft skills from the job description below.

Job Description: {jd}
Return the skills as a comma-separated list.
"""
        with st.spinner("Extracting Skills..."):
            result = generate_text(prompt, max_length=100)
            st.success(result)
