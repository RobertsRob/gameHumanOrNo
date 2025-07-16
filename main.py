from openai import OpenAI
import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

chat_history = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_prompt = data.get("prompt", "")

    response_text = ""
    if request.method == 'POST':

        # OpenAI request
        try:
            chat_history.append(
                {
                "role": "user",
                "content": [
                    {
                    "type": "input_text",
                    "text": user_prompt
                    }
                ]
                })
            
            response = client.responses.create(
            model="gpt-4.1",
            input=chat_history,
            reasoning={},
            tools=[],
            temperature=1,
            max_output_tokens=2048,
            top_p=1,
            store=True
            )

            response_text = response.output[0].content[0].text
            response_id = response.output[0].id

            chat_history.append({
            "id": response_id,
            "role": "assistant",
            "content": [
                {
                "type": "output_text",
                "text": response_text
                }
            ]
            })


            return jsonify({"response": response_text})
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    print(response_text)




if __name__ == '__main__':
    app.run(debug=True)


