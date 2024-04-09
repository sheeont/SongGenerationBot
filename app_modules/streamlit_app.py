import streamlit as st
from models import yandex_llm as gen
import asyncio
import re
# from execute_app import tts_instance
from app_modules.const_for_website import genre, title, range_for_us_picking


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


# def cr_and_upload_song(song):
#     lines = song.split("\n")
#     song = ''
#     for line in lines:
#         if len(line) >= 15 or line == '\n':
#             song = "\n".join([song, line])
#     song = song.strip()
#     path = tts_instance.generate_audio_by_text(song)
#     audio_file = open(path, 'rb')
#     audio_bytes = audio_file.read()
#     st.audio(audio_bytes)
#
#     st.balloons() # шарики


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

    song_first_sentence = st.text_input('Введите первое предложение', '-')

    temperature = st.select_slider(
        'Выберите креативность от 1 до 10',
        options=range_for_us_picking)
    temperature = float(temperature / 10)

    button_clicked = st.button('Сгенерировать!')

    if button_clicked:
        if len(str(song_first_sentence)) > 5 and us_genre in genre: # Заполнил ли пользователь форму

            song = cr_music_text(genre, song_first_sentence, temperature) # Генерация текста песни
            st.write(re.sub("\\n", "  \n", f"Сгенерировано из {song_first_sentence}\n\n{song}\n\nсупер-песня!"))

            if song:
                with st.spinner("Аудиофийл генерируется..."):
                    pass
                    # cr_and_upload_song(song)
                st.error('Аудио временно не имплементировано 🥳')

        else:
            st.write('ЗАПОЛНИТЕ ПРОПУСКИ!')

        # write_to_file(song, 'song.txt')
