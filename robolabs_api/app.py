from flask import Flask, render_template, request

from robolabs_api.api import RoboLabsApi

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        date_from = request.form["date_from"]
        date_to = request.form["date_to"]
        is_sorting_enabled = request.form.get("sort", None)
        robolabs_api = RoboLabsApi()
        try:
            job_id = robolabs_api.get_invoice_list(date_from=date_from, date_to=date_to)
            data = robolabs_api.get_job_response_data(job_id)
        except Exception as e:
            return render_template("index.html", error=e)
        data = robolabs_api.extract_desired_data(data)
        if is_sorting_enabled:
            data = sorted(data, key=lambda item: item["date"])
        return render_template("index.html", data=data)
    elif request.method == "GET":
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
