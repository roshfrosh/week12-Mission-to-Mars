from flask import Flask, render_template
from flask_pymongo import PyMongo
import mars_scrape
import os

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/visipedia_annotation_toolkit"
mongo = PyMongo(app)

@app.route("/")
def home(): 

    # Find data
    mars = mongo.db.mars.find_one()

    # Return template and data
    return render_template("index.html", mars=mars)

# Route that will trigger scrape function
@app.route("/scrape")
def scrapeee(): 

    # Run scrapped functions
    mars = mongo.db.mars
    data = mars_scrape.scrape()
    mars.update({}, data, upsert = True)

    return "Scraping Successful"

if __name__ == "__main__": 
    app.run(debug= True)
