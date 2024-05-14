from flask import Flask, request, render_template, jsonify
import os
from datetime import datetime
import wave
import assemblyai as aai
import openai

app = Flask(__name__)

aai.settings.api_key = "e6c9df8c62d44b2b863a655ab8d3a777"
openai.api_key = "sk-proj-lWylDZuPXxFyGC6U5KydT3BlbkFJVo5fnOSJkMunQ3xOUWvR"
transcriber = aai.Transcriber()

import openai

# Route to serve the recording interface
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_bhaiya():
    data = request.get_json()  # Get JSON data sent from the frontend
    question = data['question']
    print("Question Received:", question)  # Print the question to the console

    # Load transcript from the file
    with open('transcript.txt', 'r') as f:
        transcript = f.read()

    # Call the OpenAI API to get the answer, sending the file transcript as context with the question to get the answer
    answer = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. ALWAYS GIVE VERY SHORT RESPONSES"},
            {"role": "user", "content": transcript},
            {"role": "user", "content": question}
        ],
        max_tokens=100
    )

    # Access the response content correctly
    # response_text = answer.choices[0].message['content']
    response_text = answer.choices[0].message.content
    print("Answer:", response_text)  # Print the answer to the console
    return jsonify(message=response_text)  # Send the answer back to the frontend

# Route to handle audio uploads
@app.route('/upload', methods=['POST'])
def upload():
    audio_file = request.files['audio_data']
    if audio_file:
        filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.wav'
        save_path = os.path.join('recordings', filename)
        with open(save_path, 'wb') as f:
            f.write(audio_file.read())


        transcript = transcriber.transcribe(save_path)
        if transcript.status == aai.TranscriptStatus.error:
            print(transcript.error)
        else:
            print(transcript.text)
            # save the transcript to a text file appending the same filename
            with open('transcript.txt', 'a') as f:
                f.write(transcript.text)

        return {'message': 'File saved successfully'}, 200
    return {'message': 'No file received'}, 400


if __name__ == '__main__':
    os.makedirs('recordings', exist_ok=True)
    # app.run(debug=True, ssl_context=('localhost.crt', 'localhost.key'), host= '192.168.0.5')
    app.run(host="0.0.0.0", port=5000)



# number of queery
# types of queries 
# amoount of words transribed
# battery life test


#todolist functionalisty
#output full transcript


