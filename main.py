import os
import subprocess

import logging
from aiogram import Bot, Dispatcher, executor

import config
import convert_ogg


logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TG_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(content_types=["voice"])
async def handle_docs(message):
    user_id = message.chat.id

    if user_id == config.ADMIN_ID:
        msg = await message.answer("⬇️ Скачиваю ГС...")

        voice = await message.voice.get_file()
        await bot.download_file(voice.file_path, "origin.ogg")
        await msg.edit_text("⏳ Понижаю тон голоса...")

        convert_ogg.decrease_pitch("origin.ogg", "modified.ogg", semitones=-4)
        await msg.edit_text("⏳ Редактирую кодеки...")

        subprocess.run(["ffmpeg", '-i', 'modified.ogg', '-acodec', 'libopus', 'modified_codec.ogg', '-y'])
        await msg.edit_text("⬆️ Отправляю...")

        v = open("modified_codec.ogg", "rb")
        await bot.send_voice(user_id, v, reply_to_message_id=message.message_id)
        v.close()

        await msg.delete()

        for a in ("origin.ogg", "modified.ogg", "modified_codec.ogg"):
            try:
                os.remove(a)
            except:
                pass


if __name__ == "__main__":
    executor.start_polling(dp, timeout=600)
