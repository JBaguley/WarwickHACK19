from flask import Flask, request, jsonify, render_template
import io
from flask_cors import CORS
import json
import scraper



app = Flask(__name__)

minPrice = 0
maxPrice = 1000

@app.route("/", methods = ["GET", "POST"])
def index():
    products = ['TVs', 'Headphones', 'Water Bottles']

    if request.method == 'POST':
        product = request.form['product']
        minPrice = request.form['min price']
        maxPrice = request.form['max price']

        results = scraper.getAllItems(scraper.categories[product])
        finalResults =  []
        i = 0
        for result in results:
            if i >= 10:
                break
            if (result.price >= int(minPrice)) & (result.price <= int(maxPrice)):
                finalResults.append(result)
                i += 1

        return render_template('index.html', products = products, product = product, minPrice = minPrice, maxPrice = maxPrice, results = finalResults)


    return render_template('index.html', products = products)




if __name__ == '__main__':
   app.run()
