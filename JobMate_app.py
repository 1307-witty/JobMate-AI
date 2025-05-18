import streamlit as st
import openai
from PIL import Image

# ------------------------ Page Config & Logo ------------------------
st.set_page_config(page_title="JobMate: Your AI Career Assistant", layout="centered")
logo = Image.open("JobMate_logo.jpeg")  # Ensure this file is present
st.image(logo, width=120)
st.title("JobMate: Your AI Career Assistant")
st.caption("Use OpenAI to generate resume summaries, cover letters, mock interviews, and extract skills.")

# ------------------------ OpenAI API Setup ------------------------
openai.api_key = st.secrets["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"]

# ------------------------ Generate Text Function ------------------------
def generate_text(prompt, system_msg="You are an expert HR helping job seekers.", max_tokens=700):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=max_tokens
    )
    return response['choices'][0]['message']['content'].strip()

# ------------------------ Tabs ------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📝 Resume Summary", 
    "📄 Full Resume", 
    "📩 Cover Letter", 
    "❓ Mock Interview Q&A", 
    "🧠 Extract Skills"
])

# ------------------------ Resume Summary Tab ------------------------
with tab1:
    st.header("Generate Resume Summary")
    role = st.text_input("Job Role")
    university = st.text_input("University")
    degree = st.text_input("Degree")
    exp_level = st.selectbox("Experience Level", ["Fresher", "1-2 years", "3-5 years", "5-10 years", "Other"])
    if exp_level == "Other":
        exp_level = st.text_input("Enter custom experience")
    skills = st.text_area("Skills (comma-separated)")
    goals = st.text_area("Career Goals")

    if st.button("Generate Summary"):
        prompt = f"""Create a professional resume summary for a candidate applying for a {role} position.
University: {university}
Degree: {degree}
Experience: {exp_level}
Skills: {skills}
Career Goals: {goals}"""
        with st.spinner("Generating Summary..."):
            result = generate_text(prompt, max_tokens=500)
            st.success(result)

# ------------------------ Full Resume Tab ------------------------
with tab2:
    st.header("Generate Full Resume")
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    degree = st.text_input("Degree")
    experience = st.text_input("Experience")
    skills = st.text_input("Skills")
    career_goal = st.text_area("Career Objective")
    projects = st.text_area("Mention Your Projects")
    certifications = st.text_area("Certifications")

    if st.button("Generate Full Resume"):
        prompt = f"""Generate a professional resume for:
Name: {name}
Email: {email}
Phone: {phone}
Degree: {degree}
Experience: {experience}
Skills: {skills}
Career Objective: {career_goal}
Projects: {projects}
Certifications: {certifications}

Include sections: Header, Summary, Skills, Projects, Education, Certifications, and Contact Info. Use clear, ATS-friendly formatting."""
        with st.spinner("Generating Resume..."):
            result = generate_text(prompt, max_tokens=800)
            st.success(result)

# ------------------------ Cover Letter Tab ------------------------
with tab3:
    st.header("Generate Cover Letter")
    role = st.text_input("Target Role", key="role2")
    university = st.text_input("University", key="university2")
    degree = st.text_input("Degree", key="degree2")
    skills = st.text_area("Skills", key="skills2")
    goals = st.text_area("Career Goals", key="goals2")

    if st.button("Generate Cover Letter"):
        prompt = f"""Write a compelling cover letter for a fresher applying to a {role} role.
University: {university}
Degree: {degree}
Skills: {skills}
Career Goals: {goals}

Make it sound confident, enthusiastic, and tailored to the job role."""
        with st.spinner("Creating Cover Letter..."):
            result = generate_text(prompt, max_tokens=400)
            st.success(result)

# ------------------------ Mock Interview Q&A Tab ------------------------
with tab4:
    st.header("Mock Interview Q&A")
    topic = st.text_input("Interview Topic (e.g. Python)")
    role = st.text_input("Target Role")

    if st.button("Generate Q&A"):
        prompt = f"""Generate 15 common interview questions and answers for the role of {role} focusing on the topic: {topic}."""
        with st.spinner("Generating Interview Q&A..."):
            result = generate_text(prompt, max_tokens=700)
            st.success(result)

# ------------------------ Skill Extractor Tab ------------------------
with tab5:
    st.header("Extract Skills from Job Description")
    jd = st.text_area("Paste Job Description")

    if st.button("Extract Skills"):
        prompt = f"""Extract 5 key skills from this job description:\n{jd}"""
        with st.spinner("Extracting Skills..."):
            result = generate_text(prompt, max_tokens=100)
            st.success(result)