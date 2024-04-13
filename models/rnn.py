from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import pickle


def generate_text(model, tokenizer, start_text, num_words):
    for _ in range(num_words):
        sequence = tokenizer.texts_to_sequences([start_text])[0]
        sequence = pad_sequences([sequence], maxlen=429, padding='pre')
        predicted = model.predict(sequence, verbose=0)
        predicted_index = np.argmax(predicted, axis=-1)[0]
        new_word = ''

        for word, index in tokenizer.word_index.items():
            if index == predicted_index:
                new_word = word
                break

        start_text += ' ' + new_word
    return start_text


async def generate_song(first_line: str, genre: str) -> str:
    # Загрузка модели
    model = load_model('models/rnn_cache/model_64.h5')

    # Загрузка токенизатора
    with open('models/rnn_cache/tokenizer.pkl', 'rb') as handle:
        tokenizer = pickle.load(handle)

    text = f"Жанр: {genre}\n{first_line}"
    return generate_text(model, tokenizer, text, 30)
