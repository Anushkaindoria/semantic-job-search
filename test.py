from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

a = model.encode("frontend internship")
b = model.encode("React developer intern")
c = model.encode("chef in a restaurant")

print("frontend vs React:", util.cos_sim(a, b).item())
print("frontend vs chef:", util.cos_sim(a, c).item())