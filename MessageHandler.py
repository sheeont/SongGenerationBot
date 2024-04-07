async def start_command(message: types.Message):
    await message.answer("Привет! Напиши мне первые строки песни, и я помогу тебе создать остальное.")

async def text_message_handler(message: types.Message):
    generator = ContentGenerator()
    result = await generator.generate_text(message.text)
    await message.answer(result)
