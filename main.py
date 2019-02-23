from flask import Flask, request, jsonify, render_template
import io
from flask_cors import CORS
import json
import scraper


app = Flask(__name__)


@app.route("/", methods = ["GET", "POST"])
def index():
    products = ['TVs', 'Headphones', 'Water Bottles']

    if request.method == 'POST':
        product = request.form['product']

        results = scraper.getAllItems(scraper.categories[product])

        return render_template('index.html', products = products, results = results)


    return render_template('index.html', products = products)




if __name__ == '__main__':
   app.run()
