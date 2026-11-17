import sqlite3

conn = sqlite3.connect("jobs.db")
conn.execute("""
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    company TEXT,
    location TEXT,
    description TEXT
)
""")

rows = [
    ("React Developer Intern", "PixelWorks", "Bengaluru", "Build UI with React and Tailwind"),
    ("Backend Engineer", "CloudNest", "Gurugram", "Node.js, MongoDB and REST APIs"),
    ("Python Developer Intern", "DataLoop", "Remote", "Build FastAPI services and SQL queries"),
    ("Data Analyst Intern", "InsightHub", "Bengaluru", "Pandas, SQL and dashboards"),
    ("ML Intern", "NeuralBay", "Gurugram", "Work with LLMs, prompts and embeddings"),
    ("UI/UX Designer", "DesignCo", "Remote", "Design mobile app screens in Figma"),
    ("Full Stack Intern", "StackLabs", "Bengaluru", "React, Node.js and PostgreSQL"),
    ("Chef", "Spice Hub", "Delhi", "Cook North Indian dishes in a restaurant"),
    ("Sales Executive", "SoftSell", "Gurugram", "Sell software products to businesses"),
    ("DevOps Intern", "ShipFast", "Remote", "Docker, CI/CD and cloud deployments"),
]
conn.executemany("INSERT INTO jobs (title, company, location, description) VALUES (?, ?, ?, ?)", rows)
conn.commit()
conn.close()
print("Done, jobs saved")