from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/invocations", methods=["POST"])
def invoke_agent():
    data = request.json
    prompt = data.get("prompt", "")
    # your agentic RAG logic: retrieve from Bedrock KB, reason, respond
    # result = agent(prompt)
    return jsonify({"output": prompt})

@app.route("/ping")
def ping():
    return jsonify({"status": "healthy"})

if __name__== "__main__":
    app.run(port=8080, debug=False)