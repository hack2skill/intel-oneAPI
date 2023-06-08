from flask import Flask, render_template, request, url_for

app = Flask(__name__, template_folder = "templates")


# Controllers
@app.route("/", methods = ["GET", "POST"])
def home():
    output = "hold"
    if request.method == "POST":
        print("HERE")
        output = "show"
    return render_template("index.html", output = output)

if __name__ == "__main__":
    app.run(debug = True)