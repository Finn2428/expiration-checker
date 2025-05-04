from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    expired_skus = []
    if request.method == "POST":
        month = int(request.form["month"])
        day = int(request.form["day"])
        year = int(request.form["year"])

        uploaded_file = request.files["file"]
        if uploaded_file:
            lines = uploaded_file.read().decode("utf-8").splitlines()
            current_date = datetime(year=2000+year, month=month, day=day)

            for line in lines:
                parts = line.strip().split()
                if len(parts) != 4:
                    continue
                sku, mm, dd, yy = parts
                try:
                    exp_date = datetime(year=2000+int(yy), month=int(mm), day=int(dd))
                    if current_date > exp_date:
                        expired_skus.append((sku, exp_date.strftime("%m/%d/%y")))
                except ValueError:
                    continue

    return render_template("index.html", expired_skus=expired_skus)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

