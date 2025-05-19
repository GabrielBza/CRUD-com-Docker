import psycopg2

def conectar():
    print("Conectando ao banco de dados...")
    return psycopg2.connect(
        host="db",
        database="notas_db",
        user="admin",
        password="admin123"
    )
