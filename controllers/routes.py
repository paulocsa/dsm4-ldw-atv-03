from flask import render_template, request, redirect, url_for, flash
import urllib
import json
from models.database import db, Imagem
import os
import uuid


def init_app(app):

    @app.route('/')
    def home():
        return render_template('index.html')

    FILE_TYPES = set(['png', 'jpg', 'jpeg', 'gif'])

    def arquivos_permitidos(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in FILE_TYPES

    @app.route('/galeria', methods=['GET', 'POST'])
    def galeria():
        imagens = Imagem.query.all()
        if request.method == 'POST':
            file = request.files['file']
            if not arquivos_permitidos(file.filename):
                flash("Utilize os tipos de arquivos referente a imagem.", 'danger')
                return redirect(request.url)
            filename = str(uuid.uuid4())
            img = Imagem(filename=filename)
            db.session.add(img)
            db.session.commit()
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash("Imagem enviada com sucesso!", 'success')
        return render_template('galeria.html', imagens=imagens)
