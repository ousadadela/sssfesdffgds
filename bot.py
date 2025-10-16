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
