from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.layers import Embedding
from keras.layers import LSTM
import numpy as np

#define melee data set
#using a fake for now
#what do I do here????
x = [[
[20, -31, 9, -1],
[20, -33, 9, -1],
[20, -35, 9, -1],
[20, -37, 9, -1],
[20, -39, 9, -1],
[20, -41, 9, -1],
[20, -42, 9, -1],
[18, -43, 9, -1],
[20, -43, 9, 1],
[20, -41, 9, 1]
[20, -39, 9, 1],
[20, -37, 9, 1],
[20, -35, 9, 1],
[20, -33, 9, 1],
[20, -32, 9, 1],
]]

#define model
#16 melee input numbers so the input dim is 16xnumber of sequences?
model = Sequential()
#input shape number = number of inputs per time step
#dense number = number of possible output actions
model.add(LSTM(128, dropout=0.2, recurrent_dropout=0.2, input_shape=(None, 4)))
model.add(Dense(1, activation='sigmoid'))

# Compile model
model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

# Fit the model
print('Train...')
model.fit(x,y2,epochs=10)
pred = model.predict(x)
predict_classes = np.argmax(pred,axis=1)
print("Predicted classes: {}",predict_classes)
print("Expected classes: {}",predict_classes)
