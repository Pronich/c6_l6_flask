from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from settings import DB_HOST

# Создаем приложение
app = Flask(__name__)

# Иницилизируем БД

app.config.from_mapping(SQLALCHEMY_DATABASE_URI=DB_HOST)

db = SQLAlchemy(app)


# Создаем модель
class Advertisement(db.Model):

    advert_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, default=datetime.now())
    author = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<advert_id %r>' % self.advert_id


# Добавляем модель в базу данных
db.create_all()


# Создаем routes
@app.route('/')
def home():
    return ('<h1>«Flask»</h1> <h3>[GET, DEL]: api/v1/id</h3> <h3>POST: api/v1</h3>')



@app.route('/api/v1', methods=['POST'])
def post_advert():
    body = request.json
    advert = Advertisement(title=body.get("title"),
                           description=body.get("description"),
                           author=body.get("author"))
    db.session.add(advert)
    db.session.commit()
    return {'id': Advertisement.advert_id}, {'status': 201}


@app.route('/api/v1/<int:get_id>', methods=['GET'])
def get_advert(get_id):
    advert = Advertisement.query.filter_by(advert_id=get_id).first_or_404()
    return {"id": advert.advert_id,
            "title": advert.title,
            "description": advert.description,
            "created": advert.created,
            "author": advert.author
            }, {'status': 200}


@app.route('//api/v1/<int:del_id>', methods=['DELETE'])
def delete_advert(del_id):
    advert = Advertisement.query.filter_by(advert_id=del_id).first_or_404()
    db.session.delete(advert)
    db.session.commit()
    return {'status': 200}


if __name__ == '__main__':
    app.run(port=8000)