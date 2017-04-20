
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.layers import Embedding
from keras.layers import LSTM

import cPickle as p

class LSTMTraining(object):
    def __init__(self, train_X, train_y, dev_X, dev_y, voc):
        self.load_files(train_X, train_y, dev_X, dev_y)

        self.voc = p.load(open(voc))
        self.max_features = len(self.voc)

    def load_files(self, ftrain_X, ftrain_y, fdev_X, fdev_y):
        # Training set
        f = open(ftrain_X)
        self.train_X = f.read().split('\n')
        self.train_X = map(lambda x: x.split(), self.train_X)

        for i, X in enumerate(self.train_X):
            self.train_X[i] = map(lambda x: int(x), self.train_X[i])
        f.close()

        f = open(ftrain_y)
        self.train_y = f.read().split('\n')
        self.train_y = map(lambda x: x.split(), self.train_y)

        for i, y in enumerate(self.train_y):
            self.train_y[i] = map(lambda x: int(x), self.train_y[i])
        f.close()

        # Dev set
        f = open(fdev_X)
        self.dev_X = f.read().split('\n')
        self.dev_X = map(lambda x: x.split(), self.dev_X)

        for i, X in enumerate(self.dev_X):
            self.dev_X[i] = map(lambda x: int(x), self.dev_X[i])
        f.close()

        f = open(fdev_y)
        self.dev_y = f.read().split('\n')
        self.dev_y = map(lambda x: x.split(), self.dev_y)

        for i, y in enumerate(self.dev_y):
            self.dev_y[i] = map(lambda x: int(x), self.dev_y[i])
        f.close()

    def save(self):
        pass

    def train(self):
        model = Sequential()
        model.add(Embedding(self.max_features, output_dim=256))
        model.add(LSTM(128))
        model.add(Dropout(0.5))
        model.add(Dense(1, activation='sigmoid'))

        model.compile(loss='binary_crossentropy',
                      optimizer='rmsprop',
                      metrics=['accuracy'])

        model.fit(self.train_X, self.train_y, batch_size=16, epochs=40)

        score = model.evaluate(self.dev_X, self.dev_y, batch_size=16)
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