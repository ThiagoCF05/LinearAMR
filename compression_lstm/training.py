
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.layers import Embedding
from keras.layers import LSTM, Bidirectional

import cPickle as p
import numpy as np

class LSTMTraining(object):
    def __init__(self, train_X, train_y, dev_X, dev_y, voc):
        self.cwin = 25

        self.voc = p.load(open(voc))
        self.train_X, self.train_y = self.load_set(train_X, train_y)
        self.dev_X, self.dev_y = self.load_set(dev_X, dev_y)

        self.max_features = len(self.voc)

    def contextwin(self, l, win):
        '''
        win :: int corresponding to the size of the window
        given a list of indexes composing a sentence

        l :: array containing the word indexes

        it will return a list of list of indexes corresponding
        to context windows surrounding each word in the sentence
        '''
        assert (win % 2) == 1
        assert win >= 1
        l = list(l)

        lpadded = win // 2 * [self.voc['pad']] + l + win // 2 * [self.voc['pad']]
        out = [lpadded[i:(i + win)] for i in range(len(l))]

        assert len(out) == len(l)
        return out

    def load_set(self, f_X, f_y):
        X, y = [], []

        f = open(f_X)
        _X = f.read().split('\n')
        _X = map(lambda x: x.split(), _X)

        for i, e in enumerate(_X):
            _X[i] = map(lambda x: int(x), _X[i])

            X.extend(self.contextwin(_X[i], self.cwin))
        f.close()

        f = open(f_y)
        _y = f.read().split('\n')
        _y = map(lambda x: x.split(), _y)

        for i, e in enumerate(_y):
            _y[i] = map(lambda x: int(x), _y[i])

            y.extend(_y[i])
        f.close()
        return np.array(X), np.array(y)

    def train(self):
        model = Sequential()
        model.add(Embedding(self.max_features, output_dim=256))
        model.add(Bidirectional(LSTM(128)))
        model.add(Dropout(0.5))
        model.add(Dense(1, activation='sigmoid'))

        model.compile(loss='binary_crossentropy',
                      optimizer='rmsprop',
                      metrics=['accuracy'])

        model.fit(self.train_X, self.train_y, batch_size=64, epochs=5)

        score = model.evaluate(self.dev_X, self.dev_y, batch_size=64)
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