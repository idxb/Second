from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_debugtoolbar import DebugToolbarExtension
import view

# Создаем экземпляр приложения на основе имени текущего файла
app = Flask(__name__)
# настраиваем экземпляр app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///invent.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "This is not so secret"

db = SQLAlchemy(app)

app.debug = True
toolbar = DebugToolbarExtension(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    info = db.Column(db.String(100), nullable=False)
    invnum = db.Column(db.String(300), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Item %r>' % self.id





# обработчик вывода всех постов
@app.route('/posts')
def posts():
    items = Item.query.order_by(Item.date.desc()).all()
    return render_template("posts.html", items=items)


# обработчик вывода конкретного поста
@app.route('/posts/<int:id>')
def post_detail(id):
    item = Item.query.get(id)
    return render_template("post_detail.html", item=item)


# обработчик удаления конкретного поста
@app.route('/posts/<int:id>/del')
def post_delete(id):
    item = Item.query.get_or_404(id)

    try:
        db.session.delete(item)
        db.session.commit()
        return redirect('/posts')
    except:
        return "Ошибка при удалении"


# обработчик удаления конкретного поста about
@app.route('/about')
def about():
    return render_template("about.html")


# обработчик шаблона редактирования
@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    item = Item.query.get(id)
    if request.method == 'POST':
        item.info = request.form['info']
        item.invnum = request.form['invnum']
        item.comment = request.form['comment']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "Ошибка при редактировании элемента"
    else:
        return render_template("post-update.html", item=item)


# вывод шаблона создания записи
@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        info = request.form['info']
        invnum = request.form['invnum']
        comment = request.form['comment']

        item = Item(info=info, invnum=invnum, comment=comment)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/posts')
        except:
            return "Ошибка"

    else:
        return render_template("create-article.html")


# Точка входа в приложение
if __name__ == '__main__':
    app.run()
