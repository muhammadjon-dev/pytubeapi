from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import os
import pathlib

# Get the current directory
cur_dir = pathlib.Path(__file__).parent.resolve()

# Get the parent directory
parent_dir = cur_dir.parent

def getimage(data, content):
	template_image_path = os.path.join(parent_dir, "ftemplate.png")
	template_image = Image.open(template_image_path)

	# Load the avatar image
	avatar_image_response = requests.get(data["avatar"])
	avatar_image = Image.open(BytesIO(avatar_image_response.content))

	# Resize avatar to fit the template
	avatar_size = (130, 130)  # Example size, adjust as needed
	avatar_image = avatar_image.resize(avatar_size)

	mask = Image.new("L", avatar_size, 0)
	draw = ImageDraw.Draw(mask)
	draw.ellipse((0, 0) + avatar_size, fill=255)

	avatar_image.putalpha(mask)

	# Paste the avatar image onto the template
	avatar_position = (480, 70)
	template_image.paste(avatar_image, avatar_position)

	# Prepare to draw text
	draw = ImageDraw.Draw(template_image)

	# Define text positions
	channel_position = (450, 235)
	followers_position = (600, 830)
	videos_position = (860, 830)
	views_position = (200, 480)
	date_position = (200, 550)
	length_position = (200, 620)

	# Define font and font size
	font = ImageFont.truetype(font=os.path.join(parent_dir, "montserrat_r.ttf"), size=32)
	font_b = ImageFont.truetype(font=os.path.join(parent_dir, "montserrat_r.ttf"), size=32)



	# Draw text onto the template with increased font size
	draw.text(channel_position, data['channel'], fill='black', font=font_b)
	draw.text(followers_position, f" {data['followers']}", fill='black', font=font_b)
	draw.text(videos_position, f"{data['videos']}", fill='black', font=font_b)
	draw.text(views_position, data['views'], fill='black', font=font)
	draw.text(date_position, data['date'], fill='black', font=font)
	draw.text(length_position, data['length'], fill='black', font=font)

	try:
		# Convert the image to RGB mode
		template_image = template_image.convert('RGB')

		# Save the edited image as JPEG
		template_image.save(os.path.join(parent_dir, "result.jpg"))

		print("Image saved successfully.")
	except Exception as e:
		print(f"Error saving image: {e}")

