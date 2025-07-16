import fitz  # PyMuPDF
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_keywords(text):
    doc = nlp(text)
    keywords = [token.text.lower() for token in doc 
                if token.is_alpha and not token.is_stop and len(token.text) > 2]
    return list(set(keywords))

def parse_resume(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    keywords = extract_keywords(text)
    return {
        "raw_text": text,
        "keywords": keywords
    }


if __name__ == "__main__":
    result = parse_resume("sample_resume.pdf")
    print("Extracted Keywords:\n", result["keywords"])
