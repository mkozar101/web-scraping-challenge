# import necessary libraries
from flask import Flask, render_template, redirect
import scrape_mars
from flask_pymongo import PyMongo

# create instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/MarsDB"
mongo = PyMongo(app)

@app.route('/')
def index():
    scrape_dict = mongo.db.WebScrape.find_one()
    return render_template("index.html", dict=scrape_dict)

@app.route("/scrape")
def scrape_function():
    web_scrape_result = scrape_mars.scrape()
    WebScrape = mongo.db.WebScrape
    WebScrape.update({}, web_scrape_result, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
