from app import app


# обработчик домашней страницы
@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")
