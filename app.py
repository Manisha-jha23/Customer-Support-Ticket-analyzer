
# from flask import Flask, render_template, request
# import pickle

# app = Flask(__name__)

# # Load saved models
# with open("models/category_model.pkl", "rb") as f:
#     category_model = pickle.load(f)

# with open("models/priority_model.pkl", "rb") as f:
#     priority_model = pickle.load(f)

# with open("models/vectorizer.pkl", "rb") as f:
#     vectorizer = pickle.load(f)

# @app.route("/", methods=["GET", "POST"])
# def index():
#     category = None
#     priority = None

#     if request.method == "POST":
#         text = request.form["ticket"]

#         text_vector = vectorizer.transform([text])

#         category = category_model.predict(text_vector)[0]
#         priority = priority_model.predict(text_vector)[0]

#     return render_template("index.html",
#                             category=category,
#                             priority=priority)

# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# Load models
category_model = pickle.load(open("models/category_model.pkl", "rb"))
priority_model = pickle.load(open("models/priority_model.pkl", "rb"))
vectorizer = pickle.load(open("models/vectorizer.pkl", "rb"))

# Resolution suggestions
def get_resolution(category):
    category = category.strip().lower()
    resolutions = {
        "Billing Issue": "Verify transaction details and initiate refund if necessary.",
        "Technical Issue": "Guide customer through troubleshooting steps or escalate to tech team.",
        "Account Access": "Reset password or verify account credentials.",
        "Shipping Issue": "Check courier status and provide tracking update.",
        "Refund Request": "Validate eligibility and process refund within 3–5 business days."
    }

    return resolutions.get(category, "Forward to customer support executive for manual review.")

@app.route("/", methods=["GET", "POST"])
def home():
    category = None
    priority = None
    resolution = None

    if request.method == "POST":
        ticket = request.form["ticket"]

        ticket_vec = vectorizer.transform([ticket])

        category = category_model.predict(ticket_vec)[0]
        priority = priority_model.predict(ticket_vec)[0]

        resolution = get_resolution(category)

    return render_template("index.html",
                            category=category,
                            priority=priority,
                            resolution=resolution)

if __name__ == "__main__":
    app.run(debug=True)

