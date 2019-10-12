from keras.models import Sequential
from keras.layers import Dense
import pickle
import numpy as np
with open('data/data.pckl', 'rb') as f:
    train_x, train_y, test_x, test_y = pickle.load(f)

model = Sequential()
model.add(Dense(units=25, activation='relu', input_shape=(42,)))
model.add(Dense(units=7, activation='relu'))
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])


model.fit(np.array(train_x), np.array(train_y), epochs=10, batch_size=10)

loss_and_metrics = model.evaluate(np.array(test_x), np.array(test_y))

print(loss_and_metrics)
array = np.array([[1, -1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
print(model.predict(array, batch_size=10))
model.save('model/model.h5')