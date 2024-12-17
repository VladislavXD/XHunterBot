# from gradio_client import Client 
# from PIL import Image
# client = Client("black-forest-labs/FLUX.1-schnell")

# result = client.predict(
#   prompt='cute cat',
#   seed=0,
#   randomize_seed=True,
#   width=1024,
#   height=1024,
#   num_inference_steps=4,
#   api_name="/infer",
# )
 


# Image.open(result)



import os

# The text that you want to convert to audio
mytext = 'Welcome to geeksforgeeks Joe!'

# Language in which you want to convert

# Passing the text and language to the engine, 
# here we have marked slow=False. Which tells 
# the module that the converted audio should 
# have a high speed

# Saving the converted audio in a mp3 file named
# welcome 

# Playing the converted file
os.system("play welcome.mp3")