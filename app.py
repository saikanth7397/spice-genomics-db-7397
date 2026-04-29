from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Spice SSR Genomics API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        unix_socket=os.getenv("DB_SOCKET"),
        cursorclass=pymysql.cursors.DictCursor
    )

@app.get("/")
def home():
    return {"message": "Spice SSR Genomics API is running"}

@app.get("/search")
def search_ssr(
    crop: str = Query(...),
    trait: str | None = None,
    gene: str | None = None,
    feature: str | None = None,
    limit: int = 50
):
    sql = """
    SELECT c.crop_name, m.ssr_id, m.chr_name, m.start_pos, m.end_pos,
           m.motif_standard, m.feature_type,
           g.gene_id, g.gene_description,
           t.trait_name, con.constituent_name
    FROM ssr_master m
    JOIN crops c ON c.crop_id = m.crop_id
    LEFT JOIN genes g ON g.gene_pk = m.gene_pk
    LEFT JOIN ssr_traits st ON st.ssr_pk = m.ssr_pk
    LEFT JOIN traits t ON t.trait_id = st.trait_id
    LEFT JOIN ssr_constituents sc ON sc.ssr_pk = m.ssr_pk
    LEFT JOIN constituents con ON con.constituent_id = sc.constituent_id
    WHERE c.crop_name = %s
    """
    params = [crop]

    if trait:
        sql += " AND t.trait_name = %s"
        params.append(trait)
    if gene:
        sql += " AND g.gene_id = %s"
        params.append(gene)
    if feature:
        sql += " AND m.feature_type = %s"
        params.append(feature)

    sql += " LIMIT %s"
    params.append(limit)

    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(sql, params)
        rows = cur.fetchall()
    conn.close()
    return {"count": len(rows), "results": rows}

@app.get("/motif-analysis")
def motif_analysis(crop: str):
    sql = """
    SELECT m.motif_standard, COUNT(*) AS motif_count
    FROM ssr_master m
    JOIN crops c ON c.crop_id = m.crop_id
    WHERE c.crop_name = %s
    GROUP BY m.motif_standard
    ORDER BY motif_count DESC
    LIMIT 50
    """
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(sql, (crop,))
        rows = cur.fetchall()
    conn.close()
    return {"crop": crop, "results": rows}
