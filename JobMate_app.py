
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
        prompt = f"Act as an experienced HR who is teaching how to build ATS friendly resume to the both Technical cal Non Tecnical for {role}.\nuniversity: {university}\nDegree: {degree}\nExperience: {exp_level}\nSkills: {skills}\nCareer Goals: {goals}"
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
        prompt = f"""Act as an experienced HR professional who teaching how to build ATS friendly resume to the both Technical cal Non Tecnical and tailored in a way that would impress the interviewer for

        Full Name: {name} Email: {email} Phone Number: {phone} Degree: {degree} Experience: {experience} Skills: {skills} Career Objective: {career_goal} Projects: {projects} Certifications: {certifications}
        Structure the resume with proper sections like Header, Summary, Skills, Projects, Education, Certifications, and Contact Info. Use professional formatting and make it ready to paste into a Word document or PDF.""" 
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
        prompt = f"""Act as a experienced oxford university professor who is helping how to write a cover letter for students and fresher who are applying for {role} position.
        Degree: {degree}. Skills: {skills}. Career Goals: {goals}.
        The letter should be professional, enthusiastic, and persuasive."""
        with st.spinner("Creating Cover Letter..."):
            result = generate_text(prompt, max_length=300)
            st.success(result)

with tab4:
    st.header("Mock Interview Q&A")
    topic = st.text_input("Enter Interview Topic (e.g. Python, Data Structures, DBMS)")
    role = st.text_input("Enter Role:")
    if st.button("Generate Mock Q&A"):
        prompt = f"Act as an Experienced Recruiter who is tutoring fresher and experienced candidate for the job they apply give the 15 most importance question that mabe asked as per their role and topic the user give. topic: {topic},role: {role}"
        with st.spinner("Generating Interview Q&A..."):
            result = generate_text(prompt, max_length=700)
            st.success(result)

with tab5:
    st.header("Extract Skills from Job Description")
    jd = st.text_area("Paste Job Description")

    if st.button("Extract Skills"):
        prompt = f"Extract 5 key skills from the following job description:\n{jd}"
        with st.spinner("Extracting Skills..."):
            result = generate_text(prompt, max_length=100)
            st.success(result)
