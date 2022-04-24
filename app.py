from flask import Flask,request,jsonify
from flask_cors import CORS
import recomendacion

app = Flask(__name__)
CORS(app) 
        
@app.route('/peli', methods=['GET'])
def recommend_movies():
        
        res = recomendacion.get_movie_recommendation(request.args.get('title'))
        return '''<h1>The language value is: {}</h1>'''.format(res)
        

if __name__=='__main__':
        app.run(port = 5000, debug = True)