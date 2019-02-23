from flask import Flask, request, jsonify, render_template
import io
from flask_cors import CORS
import json


app = Flask(__name__)


@app.route("/", methods = ["GET", "POST"])
def index():
    products = ['TVs', 'Headphones', 'Water Bottles']

    if request.method == 'POST':
        product = request.form['product']

        if product == "TVs":
            results = [
                    {'name': 'samsung', 'price': '100', 'rating' : '4.5'},
                    {'name': 'LG', 'price': '100', 'rating' : '4.5'},
                    {'name': 'philips', 'price': '600', 'rating' : '4.5'},
                    {'name': 'panasonic', 'price': '550', 'rating' : '4.5'},
                    {'name': 'samsung', 'price': '40', 'rating' : '3.5'}
                ]
        elif product == "Headphones":
            results = [{'name': 'bose', 'price': '70', 'rating' : '4.7'}]
        elif product == "Water Bottles":
            results = [{'name': 'sistema', 'price': '5', 'rating' : '4.4'}]


        return render_template('index.html', products = products, results = results)


    return render_template('index.html', products = products)




if __name__ == '__main__':
   app.run()
