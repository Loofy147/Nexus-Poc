from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/hybrid_search', methods=['POST'])
def hybrid_search():
    data = request.get_json()
    query = data.get('query')
    print(f"Knowledge Graph Mock: Received query: {query}")

    # Mocked response
    mock_response = {
        "document_hits": [
            {"id": "doc1", "score": 0.9, "text": "This is a relevant document about topic A."},
            {"id": "doc2", "score": 0.85, "text": "Another document mentioning topic A and B."},
        ],
        "graph_expansions": [
            {"node": "Topic A", "relationship": "related_to", "target": "Topic C"}
        ]
    }

    return jsonify(mock_response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)