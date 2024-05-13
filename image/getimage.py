from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import os
import pathlib
import numpy as np
import matplotlib.pyplot as plt 

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
	avatar_size = (150, 150)  # Example size, adjust as needed
	avatar_image = avatar_image.resize(avatar_size)
	
	npImage=np.array(avatar_image)
	h,w=avatar_image.size

	# Create same size alpha layer with circle
	alpha = Image.new('L', avatar_image.size,0)
	draw = ImageDraw.Draw(alpha)
	draw.pieslice(((0, 0), (h, w)), 0, 360, fill=255)

	# Convert alpha Image to numpy array
	npAlpha=np.array(alpha)

	# Add alpha layer to RGB
	npImage=np.dstack((npImage,npAlpha))

	# Paste the avatar image onto the template
	img = Image.fromarray(npImage)

	avatar_position = (466, 60)
	template_image.paste(img, avatar_position, img)

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
	font_b = ImageFont.truetype(font=os.path.join(parent_dir, "montserrat_b.ttf"), size=32)



	# Draw text onto the template with increased font size
	draw.text(channel_position, data['channel'], fill='black', font=font_b)
	draw.text(followers_position, f" {data['followers']}", fill='black', font=font_b)
	draw.text(videos_position, f"{data['videos']}", fill='black', font=font_b)
	draw.text(views_position, data['views'], fill='black', font=font)
	draw.text(date_position, data['date'], fill='black', font=font)
	draw.text(length_position, data['length'], fill='black', font=font)
	
 
	graph_position = (565, 450)

	if content == "playlist":
		objects = [i for i in range(1, len(data["all_views"]) + 1)]
		y_pos = np.arange(len(objects))
		performance = data["all_views"]

		plt.subplots(figsize=(4.3, 2.5))
		plt.bar(y_pos, performance, align='center', alpha=0.5)
		if len(objects)>10:
			# Specify the xticks to be shown
			xticks = [i-1 for i in range(1, len(objects)+1) if i%5==0] 
			xticks.append(0)
			if len(objects) % 5:
				xticks.append(objects[-1]-1)
			
			plt.xticks(xticks, [objects[i] for i in xticks]) # Adjust labels according to xticks
		else:
			plt.xticks(y_pos, objects)
		plt.ylabel('Views')
  
		# Save the plot to a BytesIO object
		graph_buffer = BytesIO()
		plt.savefig(graph_buffer, format='png')
		plt.close()

		# Open the saved plot as an image
		graph_image = Image.open(graph_buffer)

		# Paste the graph image onto the template
		template_image.paste(graph_image, graph_position)

		content_type = "Statistics"
	else:
		response = requests.get(data["cover"])
		cover_image = Image.open(BytesIO(response.content)).resize((410, 230))
		left = 578
		top = 445
		right = left + cover_image.width
		bottom = top + cover_image.height
		region = (left, top, right, bottom)
		template_image.paste(cover_image, region)
  
		content_type = "Thumbnail"
  
	draw.text((581, 397), content_type, fill='black', font=ImageFont.truetype(font=os.path.join(parent_dir, "montserrat_sb.ttf"), size=32))
		
	try:
		# Convert the image to RGB mode
		template_image = template_image.convert('RGB')

		# Save the edited image as JPEG
		template_image.save(os.path.join(parent_dir, "result.jpg"))

		print("Image saved successfully.")
	except Exception as e:
		print(f"Error saving image: {e}")

