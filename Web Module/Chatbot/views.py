from django.shortcuts import render
from django.http import JsonResponse
import tensorflow as tf
from keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy as np
import re
import ast
import random

model = tf.keras.models.load_model(r'D:\Project\Website-Phoenix13\LearnersEd\chatbot\model\chatbot_model.h5')

df = pd.read_csv(r'D:\Project\Website-Phoenix13\LearnersEd\chatbot\model\dataset\dataframe_chatbot.csv')
df['patterns'] = df['patterns'].astype(str)

tokenizer = Tokenizer(lower=True, split=' ')
tokenizer.fit_on_texts(df['patterns'])

ptrn2seq = tokenizer.texts_to_sequences(df['patterns'])
X = pad_sequences(ptrn2seq, padding='post')

lbl_enc = LabelEncoder()
y = lbl_enc.fit_transform(df['tag'])

exception_list = ["Sorry, can't quite catch that", "Are you abusing? very bad...", "I don't recognize these words yet", "Error 404: Word not found in my dictionary"]

def generate_response(query, model):
        text = []
        txt = re.sub('[^a-zA-Z\']', ' ', query)
        txt = txt.lower()
        txt = txt.split()
        txt = " ".join(txt)
        text.append(txt)
        x_test = tokenizer.texts_to_sequences(text)
        if (len(query.split(' ')) > 1):
                x_test = np.array(x_test).squeeze()
        else:
                x_test = np.reshape(x_test, -1)
        x_test = pad_sequences([x_test], padding='post', maxlen=X.shape[1])
        y_pred = model.predict(x_test)
        y_pred = y_pred.argmax()
        tag = lbl_enc.inverse_transform([y_pred])[0]
        responses = df[df['tag'] == tag]['responses'].values[0]
        response_list = ast.literal_eval(responses)
        return random.choice(response_list)

def chatbot(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        # Retrieve the chat history from the session or initialize it if not present
        chat_history = request.session.get('chat_history', [])

        # Add the user input to the chat history
        chat_history.append(('user', user_input))

        # Generate the chatbot response using the chat history
        try:
                chatbot_response = generate_response(user_input, model)
        except Exception as e:
               chatbot_response = random.choice(exception_list)

        # Add the chatbot response to the chat history
        chat_history.append(('chatbot', chatbot_response))

        # Update the chat history in the session
        request.session['chat_history'] = chat_history

        return JsonResponse({'response': chatbot_response})

    # Retrieve the chat history from the session
    chat_history = request.session.get('chat_history', [])

    return render(request, 'chatbot_interface.html', {'chat_history': chat_history})

