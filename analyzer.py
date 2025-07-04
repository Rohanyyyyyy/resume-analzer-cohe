import cohere
import os
from numpy import dot
from numpy.linalg import norm

co = cohere.Client(os.getenv("COHERE_API_KEY", "your-cohere-api-key"))  # Replace or set env variable

def get_match_score(resume_text, jd_text):
    response = co.embed(texts=[resume_text, jd_text], model="embed-english-v3.0")
    res_vec, jd_vec = response.embeddings
    sim = dot(res_vec, jd_vec) / (norm(res_vec) * norm(jd_vec))
    return sim * 100

def get_keyword_suggestions(resume_text, jd_text):
    prompt = f"Job Description:\n{jd_text}\n\nResume:\n{resume_text}\n\nSuggest 5 keywords missing in the resume that match the job description."
    response = co.generate(
        model='command-r-plus',
        prompt=prompt,
        max_tokens=100,
        temperature=0.6
    )
    return response.generations[0].text.strip()
