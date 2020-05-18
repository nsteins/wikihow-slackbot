from flask import Flask, request, jsonify
from whapi import search
from whapi import get_images
import random

  
app = Flask(__name__) 

@app.route("/")
def index():
    return "<h1>test</h1>"

@app.route("/search") 
def home_view():
    query = request.args.get('text')
    search_results = search(query, 1)
    article_id = search_results[0]['article_id']

    image_list = get_images(article_id)
    image = random.choice(image_list) 
    return jsonify({
            "response_type": "in_channel",
            "text": {
                "type": "markdown",
                "text": f'![Image]({image})'
            }
        })