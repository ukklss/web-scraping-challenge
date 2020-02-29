from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_x"
mongo = PyMongo(app)

@app.route("/")
def index():

    mars_dict_data = mongo.db.collection.find_one()
    return render_template("index.html", mars_index=mars_dict_data)


@app.route("/scrape")
def scrape():

    mars_dict = scrape_mars.scrape()

    mongo.db.collection.update({}, mars_dict, upsert=True)


    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
