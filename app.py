from flask import Flask, render_template, flash
from controllers import routes
from models.database import db
import os
import pymysql

app = Flask(__name__, template_folder='views')
routes.init_app(app)

app.secret_key = os.urandom(24)

dir = os.path.abspath(os.path.dirname(__file__))
DB_NAME = 'bigcatsnap'
app.config['DATABASE_NAME'] = DB_NAME

# ✅ Alternar entre SQLite e MySQL
USE_SQLITE = True

if USE_SQLITE:
    # Caminho para criar o banco dentro da pasta models/
    sqlite_path = os.path.join(dir, 'models', 'dogs.sqlite3')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{sqlite_path}'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:@localhost/{DB_NAME}'

app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

if __name__ == '__main__':
    if not USE_SQLITE:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        try:
            with connection.cursor() as cursor:
                cursor.execute(f'CREATE DATABASE IF NOT EXISTS {DB_NAME}')
                print(f'O banco de dados {DB_NAME} foi criado com sucesso!')
        except Exception as e:
            print(f'Erro ao criar o banco de dados: {e}')
        finally:
            connection.close()
    
    # Inicializa e cria as tabelas
    db.init_app(app)
    with app.app_context():
        db.create_all()
    
    app.run(host='0.0.0.0', port=4000, debug=True)
