from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
from flask_cors import CORS, cross_origin


### testing 


app = Flask(__name__)
cors = CORS(app)
## set up mongo connection

app.config["MONGO_URI"]= "mongodb://localhost:27017/app"
mongo =PyMongo(app)

@app.route("/", methods=['GET'])
def index():
    # find one record of the data from the mongo db
    mars_details = mongo.db.mars_details.find_one()

    # return template and data
    return render_template("index.html", mars=mars_details)

@app.route("/scrape", methods=['GET'])
def scrape():
    # run the scrape funcion
    mars_info = scrape_mars.scrape()
    
    #update mongo databse using update and insert
    mongo.db.mars_details.update({},mars_info, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)






