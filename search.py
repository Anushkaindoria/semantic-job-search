from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

jobs = [
    "React developer intern at a startup in Bengaluru",
    "Backend engineer working with Node.js and MongoDB",
    "Python developer intern building FastAPI services",
    "Data analyst intern using Pandas and SQL",
    "Machine learning intern working with LLMs",
    "UI/UX designer for mobile apps",
    "Chef needed for a restaurant in Delhi",
    "Sales executive for a software company",
]

job_embeddings = model.encode(jobs)

query = "frontend internship"
query_embedding = model.encode(query)

scores = util.cos_sim(query_embedding, job_embeddings)[0]

top = scores.argsort(descending=True)[:3]
for i in top:
    print(round(scores[i].item(), 2), jobs[i])