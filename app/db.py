import psycopg2

# Função que realiza a conexão com o BD a partir das especificações dele
def conectar():
    print("Conectando ao banco de dados...")
    return psycopg2.connect(
        host="db",
        database="notas_db",
        user="admin",
        password="admin123"
    )
