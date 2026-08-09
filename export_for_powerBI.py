import oracledb
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

connection = oracledb.connect(
    user=os.getenv("ORACLE_USER"),
    password=os.getenv("ORACLE_PASSWORD"),
    dsn=os.getenv("ORACLE_DSN"),
    config_dir="oracle_wallet",
    wallet_location="oracle_wallet",
    wallet_password=os.getenv("ORACLE_WALLET_PASSWORD")
)

# --- Export postings ---
postings_query = """
    SELECT job_id, title, company, country, source, url,
           salary_min, salary_max, posted_date, collected_date
    FROM job_postings
"""
postings_df = pd.read_sql(postings_query, con=connection)
postings_df.to_csv("job_postings.csv", index=False)
print(f"Exported {len(postings_df)} postings to job_postings.csv")

# --- Export postings + skills, joined (this is the main table Power BI will use) ---
skills_query = """
    SELECT jp.job_id, jp.title, jp.company, jp.country, jp.source,
           jp.salary_min, jp.salary_max, jp.posted_date, jp.collected_date,
           s.skill_name
    FROM job_postings jp
    JOIN posting_skills ps ON jp.job_id = ps.job_id
    JOIN skills s ON ps.skill_id = s.skill_id
"""
skills_df = pd.read_sql(skills_query, con=connection)
skills_df.to_csv("job_postings_with_skills.csv", index=False)
print(f"Exported {len(skills_df)} posting-skill rows to job_postings_with_skills.csv")

connection.close()