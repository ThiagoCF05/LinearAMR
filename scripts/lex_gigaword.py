import os
import gzip
import re


dirs = ['/roaming/tcastrof/gigaword/LDC2007T07/gigaword_eng_3a/data/afp_eng',
        '/roaming/tcastrof/gigaword/LDC2007T07/gigaword_eng_3a/data/apw_eng',
        '/roaming/tcastrof/gigaword/LDC2007T07/gigaword_eng_3a/data/cna_eng',
        '/roaming/tcastrof/gigaword/LDC2007T07/gigaword_eng_3b/data/ltw_eng',
        '/roaming/tcastrof/gigaword/LDC2007T07/gigaword_eng_3b/data/nyt_eng',
        '/roaming/tcastrof/gigaword/LDC2007T07/gigaword_eng_3b/data/xin_eng']

if __name__ == '__main__':
    g = open('gigaword_p.txt', 'w')
    regex_text = "<P>(.+?)</P>"
    for directory in dirs[:1]:
        for f in os.listdir(directory)[:1]:
            print f, '\r',
            f = gzip.open(os.path.join(directory, f))
            doc = f.read()
            f.close()
            doc = doc.replace('\n', ' ')#.lower()

            texts = re.findall(regex_text, doc)
            for text in texts:
                g.write(text.strip())
                g.write('\n ')

    g.close()