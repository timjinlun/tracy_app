from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from datetime import datetime
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('stopwords')


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tracy.db'
app.config['SECRET_KEY'] = '123456'
db = SQLAlchemy(app)



class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_message = db.Column(db.String(500), nullable=False)
    bot_response = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()


admin = Admin(app, name='Tracy Admin', template_mode='bootstrap3')

admin.add_view(ModelView(Conversation, db.session))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    bot_response = process_message(user_message)
    
    # Save conversation to database
    conversation = Conversation(user_message=user_message, bot_response=bot_response)
    db.session.add(conversation)
    db.session.commit()
    
    return jsonify({'response': bot_response})

def process_message(message):
    # Simple keyword-based responses
    if 'hello' in message.lower():
        return "Hello! How are you feeling today?"
    elif 'bye' in message.lower():
        return "Goodbye! Take care of yourself."
    else:
        # Extract keywords
        tokens = word_tokenize(message.lower())
        stop_words = set(stopwords.words('english'))
        keywords = [word for word in tokens if word.isalnum() and word not in stop_words]
        
        return f"I see you mentioned {', '.join(keywords)}. Can you tell me more about that?"

if __name__ == '__main__':
    app.run(debug=True)