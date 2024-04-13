from transformers import pipeline
from dotenv import load_dotenv
import streamlit as st

load_dotenv()


model_input = pipeline(
    task='text-generation',
    model='Gonetz/song_creator',
    token=st.secrets["HF_TOKEN"]
)


async def generate_song(first_line: str, genre: str) -> str:
    task = f"[{genre}] \n {first_line}"
    encoded_input = model_input(task, max_new_tokens=200, do_sample=True)

    return (encoded_input[0]).get('generated_text')
