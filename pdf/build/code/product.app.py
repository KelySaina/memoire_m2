from flask import Flask, request, jsonify
from flask_cors import CORS
from ariadne import graphql_sync, load_schema_from_path, make_executable_schema
from ariadne.constants import PLAYGROUND_HTML
from schema import schema  # your existing schema
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Enable CORS for all origins (or restrict with origins=["http://localhost:8080"])
CORS(app)

# GraphQL Playground (GET)
@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200

# GraphQL API (POST)
@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,  # you can add {"user": ...} if needed
        debug=True
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code

if __name__ == "__main__":
    port = int(os.getenv("PORT", 4003))  # default for product service
    app.run(host="0.0.0.0", port=port)
