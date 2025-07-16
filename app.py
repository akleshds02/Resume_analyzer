import streamlit as st
from resume_parser import parse_resume
import spacy
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from io import BytesIO
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


nlp = spacy.load("en_core_web_sm")

# Load job description from file
def load_jd():
    with open("job_description.txt", "r", encoding="utf-8") as f:
        return f.read()

# Extract keywords using spaCy
def extract_keywords(text):
    doc = nlp(text.lower())
    return [token.text for token in doc if token.is_alpha and not token.is_stop]

# Calculate similarity
def calculate_match(resume_text, jd_text):
    documents = [resume_text, jd_text]
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(documents)
    score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return round(float(score[0][0]) * 100, 2)


st.title("Resume Analyzer")
st.write("Upload your resume and check how well it matches the job description.")

uploaded_file = st.file_uploader("Choose a PDF resume", type="pdf")

if uploaded_file is not None:
    with open("uploaded_resume.pdf", "wb") as f:
        f.write(uploaded_file.read())

    st.success("Resume uploaded successfully!")

    # Parse resume
    resume_data = parse_resume("uploaded_resume.pdf")
    resume_text = resume_data["raw_text"]
    resume_keywords = resume_data["keywords"]


    # Load and process JD
    jd_text = load_jd()
    jd_keywords = extract_keywords(jd_text)


    # Calculate match score
    match_score = calculate_match(resume_text, jd_text)
    st.subheader("Match Score:")
    st.progress(int(match_score))
    st.write(f"🔍 Your resume matches the job description by **{match_score}%**")

    # Find matching keywords
    matching_keywords = [word for word in resume_keywords if word in jd_keywords]

# Show matched keywords
    with st.expander(" Show Matching Keywords"):
        st.markdown("### ✅ Matching Keywords:")
        st.write(matching_keywords)


    # Optional: show extracted keywords
    with st.expander("Show extracted resume keywords"):
        st.write(resume_data["keywords"])

if st.checkbox("Show Word Cloud of Resume Keywords"):
    wc_text = " ".join(resume_keywords)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(wc_text)

    st.markdown("### 🌀 Word Cloud of Resume Keywords")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)

    # Save wordcloud image to buffer
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    
    st.markdown(
    """
    <div style="font-size:13px; color:white; padding-left:25px;">
    📝 <b>Note: • </b> The <b>bigger</b> the word, the more frequently it appears in your resume.<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Word colors are randomly assigned and <b>do not</b> indicate meaning.
    </div>
    """,
    unsafe_allow_html=True
)



    # Download button
    st.download_button(
        label="📥 Download Word Cloud as PNG",
        data=buf,
        file_name="resume_wordcloud.png",
        mime="image/png"
    )

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center;'>
        <p style='font-size: 14px;'>Made with ❤️ by <b>Aklesh Shetty</b></p>
        <p style='font-size: 13px;'>Powered by <b>Streamlit</b></p>
    </div>
    """,
    unsafe_allow_html=True
)


