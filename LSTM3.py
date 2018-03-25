from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Embedding
from keras.layers import LSTM
from keras.datasets import imdb
import numpy as np

#sequences must all be 100 frames long
x = [
    [[0, 0, 50.5],[1, 8, 50.5],[1, 3, 50.5],[0, 3, 50.5],[0, 8, 50.5],[0, 2, 50.5]],
    [[0, 3, 50.5],[0, 2, 50.5],[1, 4, 50.5],[2, 9, 50.5],[2, 11, 50.5],[0, 2, 50.5]],
    [[0, 13, 50.5],[0, 2, 50.5],[0, 2, 50.5],[0, 11, 50.5],[3, 8, 50.5],[3, 2, 50.5]],
    [[0, 7, 50.5],[2, 13, 50.5],[2, 4, 50.5],[0, 0, 50.5],[0, 0, 50.5],[0, 1, 50.5]]
]
x = np.array(x,dtype=np.float32)

y_new = [
    [[1],[1],[1],[1],[1],[1]],
    [[0],[0],[0],[0],[0],[0]],
    [[0],[0],[0],[0],[0],[0]],
    [[1],[1],[1],[1],[1],[1]]
]
y_new = np.array(y_new, dtype=np.int32)


print('Build model...')
model = Sequential()
#input shape cooresponds to x (input)
model.add(LSTM(128, dropout=0.1, recurrent_dropout=0.2, input_shape=(None, 3), return_sequences=True))
#first number cooresponds to y (labels)
model.add(Dense(1, activation='sigmoid'))

# try using different optimizers and different optimizer configs
model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

print('Train...')
model.fit(x,y_new,epochs=800)
pred = model.predict(x)
print("Predicted classes:\n{}".format(pred > 0.5))
print("True classes:\n{}".format(y_new > 0.5))
