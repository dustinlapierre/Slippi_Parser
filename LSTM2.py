from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Embedding
from keras.layers import LSTM
from keras.datasets import imdb
import numpy as np

x = [
    [[0],[1],[1],[0],[0],[0]],
    [[0],[0],[1],[2],[2],[0]],
    [[0],[0],[0],[0],[3],[3]],
    [[0],[2],[2],[0],[0],[0]]
]
x = np.array(x,dtype=np.float32)

y_new = [
    [[0],[1],[1],[1],[1],[1]],
    [[0],[0],[1],[1],[0],[0]],
    [[0],[0],[0],[0],[0],[0]],
    [[0],[0],[0],[0],[0],[0]]
]
y_new = np.array(y_new, dtype=np.int32)


print('Build model...')
model = Sequential()
model.add(LSTM(128, dropout=0.2, recurrent_dropout=0.2, input_shape=(None, 1), return_sequences=True))
model.add(Dense(1, activation='sigmoid'))

# try using different optimizers and different optimizer configs
model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

print('Train...')
model.fit(x,y_new,epochs=300)
pred = model.predict(x)
#predict_classes = np.argmax(pred,axis=2)
print("Predicted classes:\n{}".format(pred > 0.5))
#true_classes = np.argmax(y_new,axis=2)
print("True classes:\n{}".format(y_new > 0.5))
