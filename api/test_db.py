import psycopg2

try:
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres.wqvtwctdjevzldwpderu",
        password="0123456789Ziad",
        host="aws-1-eu-north-1.pooler.supabase.com",
        port=6543,
        sslmode="require"
    )
    print("✅ Connected successfully!")
    conn.close()
except Exception as e:
    print("❌ Connection error:", e)


