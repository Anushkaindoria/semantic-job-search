import os
import sqlite3

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse
from google import genai
from google.genai import types
from sentence_transformers import SentenceTransformer, util

app = FastAPI()

load_dotenv()
# Short timeout and no retries, so the page never waits for a long time
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options=types.HttpOptions(
        timeout=15000,
        retry_options=types.HttpRetryOptions(attempts=1),
    ),
)

model = SentenceTransformer("all-MiniLM-L6-v2")

conn = sqlite3.connect("jobs.db")
rows = conn.execute(
    "SELECT id, title, company, location, job_type, description FROM jobs"
).fetchall()
conn.close()

texts = [f"{r[1]} at {r[2]} in {r[3]}. {r[5]}" for r in rows]
job_embeddings = model.encode(texts)


@app.get("/")
def home():
    return FileResponse("index.html")


@app.get("/search")
def search(q: str, location: str = None, job_type: str = None, top_k: int = 3):
    # Step 1: SQL filter
    conn = sqlite3.connect("jobs.db")
    ids = conn.execute(
        """SELECT id FROM jobs
           WHERE (? IS NULL OR LOWER(location) = LOWER(?))
             AND (? IS NULL OR LOWER(job_type) = LOWER(?))""",
        (location, location, job_type, job_type),
    ).fetchall()
    conn.close()
    allowed = {i[0] for i in ids}
    indices = [i for i, r in enumerate(rows) if r[0] in allowed]
    if not indices:
        return []

    # Step 2: semantic ranking on filtered jobs
    query_embedding = model.encode(q)
    scores = util.cos_sim(query_embedding, job_embeddings[indices])[0]
    top = scores.argsort(descending=True)[:top_k]

    return [
        {
            "title": rows[indices[j]][1],
            "company": rows[indices[j]][2],
            "location": rows[indices[j]][3],
            "job_type": rows[indices[j]][4],
            "score": round(scores[j].item(), 2),
        }
        for j in top
    ]


@app.get("/ask")
def ask(q: str, location: str = None, job_type: str = None):
    # Retrieval: find the best jobs
    jobs = search(q, location or None, job_type or None, top_k=3)
    if not jobs:
        return {"answer": "No matching jobs found.", "jobs": [], "ai_busy": False}

    context = "\n".join(
        f"- {j['title']} at {j['company']} ({j['location']}, {j['job_type']})"
        for j in jobs
    )
    prompt = f"""You are a helpful job assistant.
Answer using ONLY the jobs listed below. If none fit, say so.

Jobs:
{context}

Question: {q}
Answer in 3-4 short lines. Use plain text, no markdown."""

    # Generation: Gemini reads the jobs and answers
    answer = None
    for name in ["gemini-3.5-flash", "gemini-3.5-flash-lite"]:
        try:
            response = client.models.generate_content(model=name, contents=prompt)
            answer = response.text
            break
        except Exception as e:
            print("Model failed:", name, e)

    if answer is None:
        return {
            "answer": "Gemini is busy, try again later.",
            "jobs": jobs,
            "ai_busy": True,
        }
    return {"answer": answer, "jobs": jobs, "ai_busy": False}