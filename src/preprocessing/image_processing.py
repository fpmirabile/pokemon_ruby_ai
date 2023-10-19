from PIL import Image

import imagehash
import numpy as np

def preprocess_image(image):
    image = Image.fromarray(image)
    image = image.resize((84, 84), Image.ANTIALIAS)
    image = np.array(image)
    return np.expand_dims(image, axis=0)  # Añadir dimensión adicional para hacerlo compatible con el modelo.

def image_array_to_hash(image_array):
    return compute_image_hash(Image.fromarray(image_array))

def compute_image_hash(image):
    return str(imagehash.average_hash(image))