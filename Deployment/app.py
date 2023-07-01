from flask import Flask, render_template, request, url_for
from prediction import predict

app = Flask(__name__, template_folder = "templates")


# Controllers
@app.route("/")
def mainPage():
    return render_template("index.html", page = "Home")

@app.route("/predict", methods = ["GET", "POST"])
def home():
    output = "hold"
    if request.method == "POST":
        f = request.files['file']
        f.save("static/inputImage.jpg")
        output = "show"
        predict()
    return render_template("index.html", output = output, page = "Predict")


@app.route("/team")
def team():
    return render_template("index.html", page = "Team")

if __name__ == "__main__":
    app.run(debug = True)
