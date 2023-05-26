import numpy as np
from PIL import Image
from sklearn.preprocessing import LabelEncoder
from tensorflow import keras
from keras.layers import Dense
from keras.models import Sequential, load_model


def getPrediction(filename):

    classes = ['Actinic keratoses', 'Basal cell carcinoma',
               'Benign keratosis-like lesions', 'Dermatofibroma', 'Melanoma',
               'Melanocytic nevi', 'Vascular lesions']
    le = LabelEncoder()
    le.fit(classes)
    le.inverse_transform([2])

    # Load model
    my_model = load_model("model/skin_cancer_model.h5")

    SIZE = 32  # Resize to same size as training images
    img_path = 'static/images/'+filename
    img = np.asarray(Image.open(img_path).resize((SIZE, SIZE)))

    img = img/255.  # Scale pixel values

    img = np.expand_dims(img, axis=0)  # Get it ready as input to the network

    pred = my_model.predict(img)  # Predict

    # Convert prediction to class name
    pred_class = le.inverse_transform([np.argmax(pred)])[0]
    print("Diagnosis is:", pred_class)
    return pred_class
