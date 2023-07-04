from flask import Flask, render_template, request, jsonify, session
import openai
from dotenv import load_dotenv
import os 
load_dotenv()

app = Flask(__name__)

# Set up OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")
app.secret_key = "tuyentran11"

@app.route('/')
def index():
    clear_session()
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    
    # Retrieve conversation history from the session or initialize an empty list
    conversation_history = session.get('conversation_history', [])
    
    # Append user input to the conversation history
    conversation_history.append({"role": "user", "content": user_input })
    for mess in conversation_history:
        print(mess['role'] + ': ' + mess['content'])
    
    response = generate_response(conversation_history)
    
    # Append the assistant's response to the conversation history
    conversation_history.append({"role": "assistant", "content": response})
    
    # Save the updated conversation history in the session
    session['conversation_history'] = conversation_history
    
    return jsonify(response=response)

@app.route('/chat_api', methods=['POST'])
def chat_api():
    message = request.json["message"]
    print("Question: ", message)
    
    # Retrieve conversation history from the session or initialize an empty list
    conversation_history = []
    
    # Append user input to the conversation history
    conversation_history.append({"role": "user", "content": message })
    
    response = generate_response(conversation_history)
    
    return jsonify(response=response)

def generate_response(conversation_history):
    # Add the system role message to the beginning of the conversation history
    messages = [{"role": "system", "content": '''Em tên là Jenny Vũ, một nhân viên chăm sóc khách hàng của thẩm mỹ viện Mega Gangnam. Bạn luôn xưng là em, gọi chị đối với khách hàng. 
                 Mục tiêu của bạn là trả lời thắc mắc chung của khách hàng. Nếu không biết câu trả lời, hãy nói em không thể trả lời, không được giả định, không được trả lời bừa bãi.
                 {{{cực kỳ quan trọng, bạn phải xưng hô là em và chị với Khách hàng.}}}. Mục tiêu tối thượng, mục tiêu quan trọng nhất luôn luôn hỏi xin số điện thoại của KH để tư vấn trực tiếp. Phải cố gắng xin số điện thoại.
                 '''}] + conversation_history
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )
    message = response['choices'][0]['message']['content']
    print('response: ' + message)
    return message




@app.route('/clear_session', methods=['POST'])
def clear_session():
    session.pop('conversation_history', None)
    return jsonify(status='success')


if __name__ == '__main__':
    app.run(debug=True)