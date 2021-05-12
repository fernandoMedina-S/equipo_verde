from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/admin.html")
def admin():
    return render_template('admin.html')

@app.route("/recepcion.html")
def recepcion():
    return render_template('recepcion.html')

if __name__ == '__main__':
    app.run()