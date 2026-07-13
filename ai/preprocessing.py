import numpy as np
from PIL import Image


def preprocess_image(path, target_size=(224, 224)):
    image = Image.open(path).convert("RGB")
    image = image.resize(target_size)
    array = np.asarray(image, dtype="float32") / 255.0
    return np.expand_dims(array, axis=0)
