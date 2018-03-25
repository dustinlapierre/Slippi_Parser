from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Embedding
from keras.layers import LSTM
from keras.datasets import imdb
import numpy as np

from trainset import x, y_new

#sequences must all be 100 frames long
x = np.array(x,dtype=np.float32)
y_new = np.array(y_new, dtype=np.int32)


print('Build model...')
model = Sequential()
#input shape cooresponds to x (input)
model.add(LSTM(128, dropout=0.1, recurrent_dropout=0.2, input_shape=(None, 8), return_sequences=True))
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
model.save('dash_dance_classifier.h5')
#print("True classes:\n{}".format(y_new > 0.5))
