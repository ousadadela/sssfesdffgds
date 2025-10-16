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

# Redimensiona a marca d’água para ocupar toda a largura da imagem
watermark_ratio = watermark.width / watermark.height
new_width = image.width
new_height = int(new_width / watermark_ratio)

# Redimensiona proporcionalmente
watermark = watermark.resize((new_width, new_height))

# Calcula a posição: centralizada horizontalmente, colada na parte de baixo
x = 0
y = image.height - new_height  # parte inferior
position = (x, y)

# Aplica a marca d'água
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

