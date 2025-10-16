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
    
    # Redimensiona a marca d'água para ter a MESMA LARGURA da imagem
    new_width = image.width
    ratio = watermark.width / watermark.height
    new_height = int(new_width / ratio)
    watermark = watermark.resize((new_width, new_height), Image.LANCZOS)
    
    # Cria uma nova imagem maior (imagem original + altura da marca d'água)
    total_height = image.height + new_height
    final_image = Image.new("RGBA", (image.width, total_height), (255, 255, 255, 0))
    
    # Cola a imagem original no topo
    final_image.paste(image, (0, 0))
    
    # Cola a marca d'água na parte inferior
    final_image.alpha_composite(watermark, (0, image.height))
    
    # Converte para RGB e salva
    final_image = final_image.convert("RGB")
    
    output = BytesIO()
    output.name = "watermarked.jpg"
    final_image.save(output, format="JPEG", quality=95)
    output.seek(0)
    
    bot.send_photo(message.chat.id, output)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Envie uma imagem que eu aplico a marca d'água pra você 💧")

bot.infinity_polling()
