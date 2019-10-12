from keras.models import load_model
import numpy as np
model = load_model('model/model.h5')
array = np.array([[1, -1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
t = model.predict(array, batch_size=10)
print(t)