import os
import csv
import json
import logging
import requests
import pandas as pd
import duckdb
import pandera as pa
from pathlib import Path

logging.basicConfig(level=logging.INFO)

os.makedirs("data/raw", exist_ok=True)
os.makedirs("data/processed", exist_ok=True)
os.makedirs("reports", exist_ok=True)

# .env oxumaq
if os.path.exists(".env"):
    f = open(".env")
    for line in f:
        if "=" in line:
            k, v = line.strip().split("=")
            os.environ[k] = v
    f.close()

url = os.getenv("API_URL", "https://jsonplaceholder.typicode.com/posts")


# csv yazmaq
f = open("data/raw/students.csv", "w", newline="")
w = csv.writer(f)
w.writerow(["id", "name", "score"])
w.writerow([1, "Aysel", 85])
w.writerow([2, "Elvin", "xeta"])
w.writerow([3, "Leyla", 92])
f.close()

# csv oxumaq
def read_csv(p):
    for row in csv.DictReader(open(p)):
        try:
            row["score"] = int(row["score"])
            yield row
        except:
            logging.error("xeta var: " + str(row))

for r in read_csv("data/raw/students.csv"):
    print(r)

# json
data = [{"course": "Python", "hours": 40}, {"course": "SQL", "hours": 30}]
json.dump(data, open("data/raw/courses.json", "w"))
x = json.load(open("data/raw/courses.json"))
print(x)


# API
try:
    res = requests.get(url, timeout=10)
    posts = res.json()
except:
    print("api islemedi")
    posts = []
    for i in range(1, 51):
        posts.append({"userId": i % 5 + 1, "id": i, "title": "basliq " + str(i), "body": "metn"})

json.dump(posts, open("data/raw/posts.json", "w"))

# jsonl
f = open("data/raw/posts.jsonl", "w")
for p in posts:
    f.write(json.dumps(p) + "\n")
f.close()

df = pd.DataFrame(posts)
df.to_csv("data/processed/posts.csv", index=False)
df.to_parquet("data/processed/posts.parquet")

print("csv olcusu", os.path.getsize("data/processed/posts.csv"))
print("parquet olcusu", os.path.getsize("data/processed/posts.parquet"))

# duckdb
q = duckdb.sql("SELECT userId, COUNT(*) as say FROM 'data/processed/posts.parquet' GROUP BY userId")
print(q.df())


# kirli data
orders = pd.DataFrame({
    "order_id": [1, 2, 3, 3, 4, 5, 6, 7],
    "customer_id": [101, 102, 101, 101, 103, 999, 102, 104],
    "product": [" laptop", "PHONE ", "Mouse", "Mouse", "keyboard", "phone", None, "laptop"],
    "quantity": ["1", "2", "3", "3", "-1", "2", "1", "x"],
    "price": ["1200.5", "800", "25.99", "25.99", "45", "800", "abc", "1100"],
    "order_date": ["2026-01-05", "2026-01-06", "2026-01-07", "2026-01-07", "2026-02-10", "bad", "2026-02-11", "2026-03-01"]
})
customers = pd.DataFrame({
    "customer_id": [101, 102, 103, 104],
    "name": ["Aysel", "Elvin", "Leyla", "Murad"],
    "city": ["Baku", "Ganja", "Baku", "Sumqayit"]
})

# temizleme
df2 = orders.copy()
df2["product"] = df2["product"].str.strip().str.title()
df2 = df2.drop_duplicates()
df2["quantity"] = pd.to_numeric(df2["quantity"], errors="coerce")
df2["price"] = pd.to_numeric(df2["price"], errors="coerce")
df2["order_date"] = pd.to_datetime(df2["order_date"], errors="coerce")

# pandera
schema = pa.DataFrameSchema({
    "order_id": pa.Column(int, unique=True),
    "customer_id": pa.Column(int, pa.Check.isin([101, 102, 103, 104])),
    "product": pa.Column(str),
    "quantity": pa.Column(float, pa.Check.gt(0)),
    "price": pa.Column(float, pa.Check.gt(0)),
    "order_date": pa.Column(pa.DateTime)
})

try:
    schema.validate(df2, lazy=True)
except pa.errors.SchemaErrors as e:
    err = e.failure_cases
    print(err)
    err.to_csv("reports/report.csv")
    bad = err["index"].dropna().astype(int).unique()
    df2 = df2.drop(index=bad)

print(df2)

# merge
df3 = df2.merge(customers, on="customer_id")
df3["total"] = df3["quantity"] * df3["price"]

# groupby
print(df3.groupby("city")["total"].sum())

# pivot
p = df3.pivot_table(index="city", columns="product", values="total", aggfunc="sum")
print(p)

df3.to_parquet("data/processed/orders_clean.parquet")
print(duckdb.sql("SELECT product, SUM(total) FROM 'data/processed/orders_clean.parquet' GROUP BY product").df())

# git
print("git init")
print("git add .")
print("git commit -m 'first'")
print("git switch -c feature")
print("git merge feature")
