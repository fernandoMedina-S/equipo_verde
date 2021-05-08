from flask import Flask

app = Flask(__name__)

@app.route("/")
def Index():
    return "<h1>Que chingue su madre el cumpleañero</h1>"

@app.route("/pito")
def Pito():
    x="12xd" + "zS"
    return x

if __name__ == "__main__":
    app.run(port = 3000, debug = True)