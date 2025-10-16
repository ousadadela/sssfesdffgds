import telebot
from PIL import Image, ImageDraw, ImageFont

import os
from io import BytesIO

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

WATERMARK_PATH = "watermark.png"

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    image = Image.open(BytesIO(downloaded_file)).convert("RGBA")
    watermark = Image.open(WATERMARK_PATH).convert("RGBA")

    # Redimensiona marca d’água pra 20% do tamanho da imagem
    scale = image.width // 5
    ratio = watermark.width / watermark.height
    watermark = watermark.resize((scale, int(scale / ratio)))

    # Posiciona no canto inferior direito
    position = (image.width - watermark.width - 20, image.height - watermark.height - 20)
    image.alpha_composite(watermark, position)

    output = BytesIO()
    output.name = "watermarked.png"
    image.save(output, format="PNG")
    output.seek(0)

    bot.send_photo(message.chat.id, output)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Envie uma imagem que eu aplico a marca d’água pra você 💧")

bot.infinity_polling()
