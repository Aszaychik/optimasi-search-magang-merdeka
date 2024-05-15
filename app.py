from flask import Flask, request, jsonify, render_template
from flask_assets import Bundle, Environment
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random

app = Flask(__name__)

assets = Environment(app)
css = Bundle("src/main.css", output="dist/main.css")

assets.register("css", css)
css.build()

magang_opportunities = pd.read_csv('data/magang_opportunities.csv')
cleaned_data = pd.read_csv('data/cleaned_data.csv')

tfidf_vectorizer = TfidfVectorizer()

X = tfidf_vectorizer.fit_transform(cleaned_data['result_stemming'])

def random_magang(n=10):
    filter_magang = magang_opportunities.dropna(subset=['mitra_name', 'external_platform_logo_url'])
    items = filter_magang.sample(n)
    return items.to_dict('records')

def content_based_recommendation(content_id, n=10):
    content_index = magang_opportunities.index[magang_opportunities['id'] == content_id].tolist()[0]

    similarity_score = cosine_similarity(X)
    sorted_similar_content = similarity_score[content_index].argsort()[::-1]

    top_n_content = sorted_similar_content[1:n+1]

    recommendation_result = pd.DataFrame(columns=['id', 'name', 'score'])

    for i in top_n_content:
        score = similarity_score[content_index][i]
        if score != 0: # Check if similarity score is not equal to 0
            recommendation_result = pd.concat([
                recommendation_result,
                pd.DataFrame({
                    'id': [magang_opportunities.iloc[i]['id']],
                    'name': [magang_opportunities.iloc[i]['name']],
                    'score': [score],
                    'mitra': [magang_opportunities.iloc[i]['mitra_name']]
                })
            ], ignore_index=True)

    return recommendation_result


def query_based_recommendation(query, n=10):
    query = query.casefold()  # Make sure the query is in lowercase
    query_vector = tfidf_vectorizer.transform([query])
    
    similarity_score = cosine_similarity(query_vector, X)
    sorted_similar_content = similarity_score.argsort()[0][::-1]
    top_n_content = sorted_similar_content[1:n+1]

    recommendation_result = pd.DataFrame(columns=['id', 'name', 'score'])

    for i in top_n_content:
        score = similarity_score[0][i]
        if score != 0:  # Check if similarity score is not equal to 0
            recommendation_result = pd.concat([
                recommendation_result,
                pd.DataFrame({
                    'id': [magang_opportunities.iloc[i]['id']],
                    'name': [magang_opportunities.iloc[i]['name']],
                    'score': [score],
                    'mitra': [magang_opportunities.iloc[i]['mitra_name']]
                })
            ], ignore_index=True)

    return recommendation_result

@app.route('/')
def home():
    items = random_magang(3)
    return render_template('index.html', items=items)

@app.route('/content-based-recommend/<content_id>', methods=['GET'])
def content_based_recommend(content_id):
    n = request.args.get('n', 5, type=int)
    result = content_based_recommendation(content_id, n)
    print(result)
    return jsonify(result.to_dict(orient='records'))

@app.route('/query-based-recommend', methods=['GET'])
def query_based_recommend():
    query = request.args.get('query')
    n = request.args.get('n', 5, type=int)
    result = query_based_recommendation(query, n)
    return jsonify(result.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)