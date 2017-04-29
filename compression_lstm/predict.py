
from keras.models import load_model

import cPickle as p

class LSTMPredicting(object):
    def __init__(self, model, voc):
        self.model = load_model(model)

        self.voc = p.load(open(voc))
        self.cwin = 25

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

    def predict(self, X):
        X = self.contextwin(X, self.cwin)

        y = self.model.predict(X, batch_size=32)
        return y

    def run(self, fX, wX):
        f = open(fX)
        amrs = f.read().split('\n')
        f.close()

        predictions = []
        for amr in amrs:
            X = map(lambda x: int(x), amr.split())
            y = self.predict(X)

            predictions.append(y)

        f = open(wX, 'w')
        for y in predictions:
            for label in y:
                if label == 1:
                    f.write('+')
                else:
                    f.write('-')
                f.write('\n')
            f.write('\n')
        f.close()

if __name__ == '__main__':
    VOC_FILE = ''
    MODEL_FILE = ''

    TRAIN_READ_FILE = ''
    TRAIN_WRITE_FILE = ''
    DEV_READ_FILE = ''
    DEV_WRITE_FILE = ''
    TEST_READ_FILE = ''
    TEST_WRITE_FILE = ''

    lstm = LSTMPredicting(model=MODEL_FILE, voc=VOC_FILE)