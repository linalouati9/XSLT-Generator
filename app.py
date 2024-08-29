import json
from flask import Flask, jsonify, request
from langchain_community.llms import Ollama
from flask_cors import CORS
from langchain_core.prompts import PromptTemplate

app = Flask(__name__)
CORS(app)

@app.route("/", methods=['POST'])
def home():
    try:
        llm = Ollama(model="phi3", stop=["<|end|>"])

        data = json.loads(request.data)

        template = """
        <|system|>
            As an XSLT developer in xmlns:xsl='xmlns:xsl="http://www.w3.org/1999/XSL/Transform'
            and without xsl:output in the response, write only the code.
        <|end|>\n
        <|user|>\n 
            {question}
            {xml}
        <|end|>\n
        <|assistant|>
        <|end|>\n
        """

        # Check if XML is provided and create the xml_part of the prompt accordingly
        xml = f"Here is the XML:\n{data['xml']}" if 'xml' in data and data['xml'] else ""

        prompt = PromptTemplate.from_template(template)

        response = llm.invoke(prompt.format(question=data["prompt"], xml = xml))

        return jsonify({"response": response})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
