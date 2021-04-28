"""
Antes de tudo...
- Instalação dos pacotes necessários:
    os
    time
    pandas
    sqlalchemy (pip3 install SQLAlchemy)
    dotenv (pip3 install python-dotenv)

- Instalação MySQLdb para Python 3
    https://github.com/PyMySQL/mysqlclient-python

- arquivo .env (caso esteja rodando localmente)
    MYSQL_USERNAME='username'
    MYSQL_PASSWORD='password'
    MYSQL_HOST='IP address'
    MYSQL_PORT='3306'

- arquivo MySQLpy.py
"""

# Importação de módulos
from utils.MySQLpy import MySQLpy
# from mysql import MySQLpy # conexão com o mysql
from sqlalchemy.sql import select # criação de queries para obtenção dos dados
from sqlalchemy import and_, or_ # complemento das queries


# Não sei de nada do banco de dados, nem nomes de tabelas
db = MySQLpy(None)
db.test_connection()
db.show_databases()

# Conheço um pouquinho
db = MySQLpy('vagao')
db.show_tables()
tb = db.table('EFVM')
for c in tb.columns:
    print(c)

# Obtenção dos dados
# Via sqlalchemy:
stmt = select([tb.c.suspentiontravel_mm_20_segundos])

stmt = select([tb.c.suspentiontravel_mm_20_segundos, tb.c.velocidadekmh]).where(and_(tb.c.km_ini_cc > 100, tb.c.km_ini_cc < 500))

stmt = select([tb.c.suspentiontravel_mm_20_segundos, tb.c['velocidadekmh']]) \
    .where(and_(tb.c.km_ini_cc > 100, tb.c.km_ini_cc < 200))

stmt = select([tb.c['velocidadekmh']]).group_by(tb.c['velocidadekmh'])
stmt = select([tb.c.velocidadekmh])

# Via SQL query
stmt = "SELECT * FROM vagao.EFVM LIMIT 50;"

df = db.read_sql(stmt)
df.head()


# Se rolar dúvida com alguma query específica, 
#   pesquisa no google SQL QUERY + pergunta que certamente encontra a resposta

# Para ver a documentação, help(MySQLpy)
#   digite q para sair
