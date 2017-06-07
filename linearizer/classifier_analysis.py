import cPickle as p

if __name__ == '__main__':
    clf_one = p.load(open('steps/clf_one_step.cPickle'))

    dev = p.load(open('steps/dev_one_step.cPickle'))

    for row in dev:
        X, y = row
        y_pred = clf_one.classify(X)

        if y_pred != y:
            print X, y, y_pred