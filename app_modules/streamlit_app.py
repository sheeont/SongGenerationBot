import streamlit as st
from models import yandex_llm as gen
import asyncio
import re
from tts.main import TTS
from dotenv import load_dotenv
from tts import suno_songs as suno
from app_modules.const_for_website import genre, genre_en, title, range_for_us_picking

load_dotenv()


def cr_music_text(genre, song_first_sentence, temperature):
    with st.spinner('Текст песни генерируется...'):  # виджет загрузки

        task = f"""
                Первая строка: {song_first_sentence}
                Жанр: {genre}
                """
        try:
            song = asyncio.run(gen.generate_song(task, temperature))
            st.success(f'Успех! 😁')
            return song
        except BaseException:
            st.error('Неудача 😔')
            return


def generate_tts(text: str):
    """
    Этой функцией можно сгенерировать text-to-speech
    Можно добавить checkbox'ы для установки генерации
    песни через tts и suno
    """
    tts = TTS()
    path = tts.generate_audio_by_text(text)
    audio_file = open(path, 'rb')
    audio_bytes = audio_file.read()
    st.write('Озвученная песня:')
    st.audio(audio_bytes)


def generate_audio(song, us_genre):
    try:
        url = asyncio.run(suno.generate_audio(song, genre_en[genre.index(us_genre)]))
        st.write('Сгенерированная песня с музыкой:')
        st.audio(url)
    except suno.AudioLoadException as e:
        st.error(e.args[0])


def main_proj():
    # фон
    # page_bg_img = '''
    # <style>
    # .appview-container {
    #     background: url("https://catherineasquithgallery.com/uploads/posts/2021-02/1614433093_57-p-anime-oboi-temnii-fon-108.jpg");
    #     background-size: cover;
    # }
    # </style>
    # '''
    # st.markdown(page_bg_img, unsafe_allow_html=True)

    # CSS для оформления и градиента на задний фон
    song = ''
    st.markdown(
        """
        <style>
        .reportview-container {
            background: linear-gradient(to right, #33ccff, #ff99cc);
        }
        .stTextInput>div>div>input {
            color: #4f8bf9;
        }
        .stButton>button {
            border: 2px solid #4f8bf9;
            border-radius: 20px;
            color: #4f8bf9;
        }
        </style>
        """, unsafe_allow_html=True
    )

    # title
    st.title(title)

    us_genre = st.selectbox(
        "Стиль",
        genre,
        index=None,
        placeholder='Выберите свой вариант'
    )

    song_first_sentence = st.text_input('Введите первое предложение')

    temperature = st.select_slider(
        'Выберите креативность от 1 до 10',
        options=range_for_us_picking)
    temperature = float(temperature / 10)

    use_suno = st.checkbox('Генерировать песню (с музыкой и пр.)', value=True)
    use_tts = st.checkbox('Генерировать озвучку (tts)')

    button_clicked = st.button('Сгенерировать!')

    if button_clicked:
        if len(str(song_first_sentence)) > 5 and us_genre in genre:  # Заполнил ли пользователь форму

            song = cr_music_text(genre, song_first_sentence, temperature)  # Генерация текста песни
            st.write(re.sub("\\n", "  \n", f"Сгенерировано из {song_first_sentence}\n\n{song}\n\nсупер-песня!"))

            if song:
                with st.spinner("Аудиофайл генерируется (в среднем это длится 1,5 минуты)..."):
                    if use_suno:
                        generate_audio(song, us_genre)
                    if use_tts:
                        generate_tts(song)


        else:
            st.write('ЗАПОЛНИТЕ ПРОПУСКИ!')

        # write_to_file(song, 'song.txt')
