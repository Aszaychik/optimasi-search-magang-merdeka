from flask import Flask, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

magang_opportunities = pd.read_csv('data/magang_opportunities.csv')
cleaned_data = pd.read_csv('data/cleaned_data.csv')

tfidf_vectorizer = TfidfVectorizer()

X = tfidf_vectorizer.fit_transform(cleaned_data['result_stemming'])

def content_based_recommendation(content_id, n=10):
    content_index = magang_opportunities.index[magang_opportunities['id'] == content_id].tolist()[0]

    similarity_score = cosine_similarity(X)
    sorted_similar_content = similarity_score[content_index].argsort()[::-1]

    top_n_content = sorted_similar_content[1:n+1]

    recommendation_result = pd.DataFrame(columns=['id', 'name', 'score'])

    print(f"Content magang: {magang_opportunities.loc[magang_opportunities['id'] == content_id, 'name'].iloc[0]}")

    print(f"Top {n} Recommendation result: ")

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
    print(f"Query: {query}")
    print(f"Top {n} Recommendation result: ")
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

@app.route('/', methods=['GET'])
def home():
    return "Welcome Search Recommendation Magang Merdeka"

@app.route('/content-based-recommend/<content_id>', methods=['GET'])
def content_based_recommend(content_id):
    n = request.args.get('n', 5, type=int)
    result = content_based_recommendation(content_id, n)
    return jsonify(result.to_dict(orient='records'))

@app.route('/query-based-recommend', methods=['GET'])
def query_based_recommend():
    query = request.args.get('query')
    n = request.args.get('n', 5, type=int)
    result = query_based_recommendation(query, n)
    return jsonify(result.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)