from keras.preprocessing import sequence
from keras.models import Sequential, load_model
from keras.layers import Dense, Embedding
from keras.layers import LSTM
from keras.datasets import imdb
import numpy as np

model = load_model("dash_dance_classifier.h5")

#single timestep version
def make_prediction(data):
    batch_size = len(data)
    data = np.array(data, dtype=np.float32)
    data = data.reshape((1, batch_size, 4))
    pred = model.predict(data)
    #print("Predicted classes:\n{}".format(pred > 0.5))
    #count amount of True in batch
    count = 0
    for i in range(batch_size):
        if(pred[0][i][0] > 0.5):
            count += 1
    #return the percentage of true
    return (count/batch_size)

#normalize data into range -1 to 1
def normalize(data):
    #action range 0 to 400
    action = 2 * (data[0]/400) - 1
    #x range -250 to 250
    x = 2 * ((data[1] + 250)/500) - 1
    #y range -150 to 150
    y = 2 * ((data[2] + 150)/300) - 1
    #direction is alreqady normalized
    return [action, x, y, data[3]]
