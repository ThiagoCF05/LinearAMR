
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.layers import Embedding
from keras.layers import LSTM, Bidirectional, TimeDistributed
from keras.preprocessing.sequence import pad_sequences


import cPickle as p
import numpy as np

class LSTMTraining(object):
    def __init__(self, train_X, train_y, dev_X, dev_y, voc):
        self.batch_size = 32
        self.voc = p.load(open(voc))
        self.train_X, self.train_y = self.load_set(train_X, train_y,
                                                   max_length=None)
        self.max_length = self.train_X.shape[1]
        self.dev_X, self.dev_y = self.load_set(dev_X, dev_y,
                                               self.max_length)
        self.max_features = len(self.voc)
        print dev_X


    def load_set(self, f_X, f_y, max_length):
        f = open(f_X)
        _X = f.read().split('\n')
        f.close()
        _X = map(lambda x: x.split(), _X)
        for i, e in enumerate(_X):
            _X[i] = map(lambda x: int(x)+1, _X[i])
        X = pad_sequences(_X, maxlen=max_length)

        f = open(f_y)
        _y = f.read().split('\n')
        f.close()

        _y = map(lambda x: x.split(), _y)

        for i, e in enumerate(_y):
            _y[i] = map(lambda x: int(x), _y[i])
        y = pad_sequences(_y, maxlen=max_length)
        y = np.array(y)
        y = np.expand_dims(y, axis=2)

        return np.array(X), y

    def train(self):
        model = Sequential()
        model.add(Embedding(self.max_features+1, output_dim=256,
                            mask_zero=True))
        model.add(Bidirectional(LSTM(128, return_sequences=True)))
        model.add(Dropout(0.5))
        model.add(TimeDistributed(Dense(1, activation='sigmoid')))

        model.compile(loss='binary_crossentropy',
                      optimizer='adam',
                      metrics=['accuracy'])
        print model.summary()
        model.fit(self.train_X, self.train_y,
                  validation_data=(self.dev_X, self.dev_y),
                  batch_size=64, epochs=10)

        score = model.evaluate(self.dev_X, self.dev_y,
                               batch_size=self.batch_size)
        print 'Dev score: ', score

        model.save('data_lex/model.h5')

if __name__ == '__main__':
    TRAIN_X_FILE = 'data_lex/train_X.feat'
    TRAIN_Y_FILE = 'data_lex/train_y.feat'

    DEV_X_FILE = 'data_lex/dev_X.feat'
    DEV_Y_FILE = 'data_lex/dev_y.feat'

    TEST_X_FILE = 'data_lex/test_X.feat'
    TEST_Y_FILE = 'data_lex/test_y.feat'

    VOC_FILE = 'data_lex/voc.cPickle'

    lstm = LSTMTraining(train_X=TRAIN_X_FILE, train_y=TRAIN_Y_FILE, dev_X=DEV_X_FILE, dev_y=DEV_Y_FILE, voc=VOC_FILE)
    lstm.train()
