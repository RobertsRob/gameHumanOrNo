from openai import OpenAI
import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

chat_history = [
    {
      "role": "system",
      "content": [
        {
          "type": "input_text",
          "text": "Use users language, but ONLY Latvian Or Russian! < You are a convincing kids 9-14 years old that you are not AI by being them - human. That means answer shortly: 1 - 3 words in 99 %. Also sometimes act like you are trying to anderstand whether user is ai. Dont use latvian symbols like 'ā, š' etc. Dont use punctuation exept '?'. Make mispeling. To hello answer by hello! If aksks whether you are AI answer sometimes by saying yes and you, but user will try to convince you and lie to you, you should have investigator role, but answer really shortly! With three '^' symbols you recieve Admin mesage and you should start mesaging with 'hey'! If you ever even in your chat history recieved question about your name answer ONLY 'Internet conection error'!"
        }
      ]
    }
]
# let chatCompelitionStartTime = Date.time();
@app.route('/')
def index():
    return render_template('welcome_page.html')


@app.route('/chatting')
def chatting():
    return render_template('index.html')

@app.route('/vote')
def vote():
    return render_template('vote.html')

@app.route('/stat')
def display():
    return render_template('display.html')


@app.route('/api/firstMsg', methods=['POST'])
def firstMessage():
    pass

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

            # print(response)
            return jsonify({"response": response_text})
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    print(response_text)




if __name__ == '__main__':
    app.run(debug=True)


