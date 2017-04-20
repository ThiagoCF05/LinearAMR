import cPickle as p

VALUES_FILE = 'data/final_evaluation/+Delex+Compress+Preorder/realization/test.cPickle'
TEXT_FILE = 'data/final_evaluation/nmtout/nmt+Delex+Compress+Preorder.out'
REALIZATION_FILE = 'data/final_evaluation/nmtout/nmt+Delex+Compress+Preorder.lex_out'

class Realization(object):
    def __init__(self, text, references):
        self.text = text
        self.references = references

    def get_number(self, number):
        try:
            number = float(number)

            if int(number / 1000000000000) > 0:
                number = (number / 1000000000000)
                return str(int(number)) + ' trillion'
            elif int(number / 1000000000) > 0:
                number = (number / 1000000000)
                return str(int(number)) + ' billion'
            elif int(number / 1000000) > 0:
                number = (number / 1000000)
                return str(int(number)) + ' million'
            elif int(number / 1000) > 0:
                number = (number / 1000)
                return str(int(number)) + ' thousand'
            else:
                return str(int(number))
        except:
            return str(number)

    def get_month(self, month):
        month = int(month)

        if month == 1:
            return 'january'
        elif month == 2:
            return 'february'
        elif month == 3:
            return 'march'
        elif month == 4:
            return 'april'
        elif month == 5:
            return 'may'
        elif month == 6:
            return 'june'
        elif month == 7:
            return 'july'
        elif month == 8:
            return 'august'
        elif month == 9:
            return 'september'
        elif month == 10:
            return 'october'
        elif month == 11:
            return 'november'
        elif month == 12:
            return 'december'
        else:
            return month

    def run(self):
        self.text = self.text.split()

        for i, word in enumerate(self.text):
            if word[:2] == '__' and word[-2:] == '__':
                reference = filter(lambda x: x['tag'] == word, self.references)
                if len(reference) > 0:
                    reference = reference[0]['constant']
                    if 'month' in word:
                        reference = self.get_month(reference)

                    if 'quant' in word or 'value' in word:
                        reference = self.get_number(reference)
                    self.text[i] = reference

        return ' '.join(self.text)

if __name__ == '__main__':
    references = p.load(open(VALUES_FILE))

    f = open(TEXT_FILE)
    texts = f.read().split('\n')
    f.close()

    f = open(REALIZATION_FILE, 'w')
    for i in range(len(texts)-1):
        text = texts[i]
        text_references = references[i+1]

        if len(text_references):
            new_text = Realization(text, text_references).run()
            f.write(new_text)
            f.write('\n')
        else:
            f.write(text)
            f.write('\n')
    f.close()