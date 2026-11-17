import sqlite3, random

random.seed(42)

roles = {
    "React Developer": "Build user interfaces with React, TypeScript and Tailwind CSS",
    "Backend Engineer": "Build REST APIs with Node.js, Express and MongoDB",
    "Python Developer": "Build backend services with FastAPI and SQL queries",
    "Data Analyst": "Analyse data using Pandas, SQL and dashboards",
    "Machine Learning Engineer": "Train and evaluate machine learning models in Python",
    "LLM Engineer": "Build LLM agents, prompts, embeddings and RAG pipelines",
    "Full Stack Developer": "Build web apps with React, Node.js and PostgreSQL",
    "DevOps Engineer": "Manage Docker, CI/CD pipelines and cloud deployments",
    "Android Developer": "Build Android apps with Kotlin and REST APIs",
    "UI/UX Designer": "Design mobile and web app screens in Figma",
    "Data Engineer": "Build data pipelines with Python, SQL and Airflow",
    "QA Engineer": "Write automated tests with Jest and Selenium",
    "Product Manager": "Plan product features and work with engineers",
    "Sales Executive": "Sell software products to business customers",
    "Chef": "Cook dishes in a busy restaurant kitchen",
}
companies = ["PixelWorks", "CloudNest", "DataLoop", "InsightHub", "NeuralBay",
             "StackLabs", "ShipFast", "CodeCraft", "BrightApps", "TechNova",
             "ByteForge", "AlphaSoft", "Zenith Labs", "OrbitAI", "Nimbus Tech"]
locations = ["Bengaluru", "Gurugram", "Remote", "Hyderabad", "Pune", "Delhi"]
types = ["Internship", "Full-time"]

conn = sqlite3.connect("jobs.db")
conn.execute("DROP TABLE IF EXISTS jobs")
conn.execute("""
CREATE TABLE jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    company TEXT,
    location TEXT,
    job_type TEXT,
    description TEXT
)
""")

rows = []
for _ in range(200):
    role = random.choice(list(roles))
    job_type = random.choice(types)
    title = role + (" Intern" if job_type == "Internship" else "")
    rows.append((title, random.choice(companies), random.choice(locations), job_type, roles[role]))

conn.executemany(
    "INSERT INTO jobs (title, company, location, job_type, description) VALUES (?, ?, ?, ?, ?)", rows)
conn.commit()
conn.close()
print("200 jobs saved")