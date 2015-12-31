#!/usr/bin/env python
# coding=utf-8
import nltk
import sys
from os import listdir
from os.path import isfile, join
import re
import threading
import Queue

reload(sys)
sys.setdefaultencoding('utf-8')


class UyghurHandler(object):
    def __init__(self, path):
        self.path = path
        self.data_path = path + '/data/'
        # read file in data path

    def handlerContent(self):
        onlyfiles = [f for f in listdir(self.data_path) if isfile(join(self.data_path, f))]
        for file in onlyfiles:
            # read only txt file
            if '.txt' in file:
                with open(self.data_path + file) as content:
                    data = content.read().replace('\n', ' ').decode('utf-8')
                    # handle invalid character
                    data = self.letters(data)
                    # write all content to file
                    # self.writeContent(file, data)
                    # write single word split content
                    self.writeDic(file, data)

    def uniqueWordList(self):
        list = []
        dic_path = self.path + '/dic/'
        onlyfiles = [f for f in listdir(dic_path) if isfile(join(dic_path, f))]
        for file in onlyfiles:
            if '.txt' in file:
                with open(dic_path + file) as content:
                    data = content.read().decode('utf-8')
                    words = data.split("\n")
                    for w in words:
                        list.append(w)
        seen = set()
        seen_add = seen.add
        unique_list = [x for x in list if not (x in seen or seen_add(x))]

        f = []
        for u in unique_list:
            f.append(u + "\n")
        f_content = ''.join(f)

        self.writeFile('unique.dic', f_content, self.path + '/')

    def writeContent(self, filename, content):
        try:
            # write all content to file
            self.writeFile(filename, content, self.path + "/content/")
        except:
            print('Write Content Exception')

    def writeDic(self, filename, content):
        try:
            dic = []
            # split to words
            tokens = nltk.word_tokenize(content)
            for n in tokens:
                dic.append(n + '\n')
            values = ''.join(dic)
            self.writeFile(filename, values, self.path + "/dic/")
        except:
            print('Write Content Exception')


    def letters(self, input):
        valids = []
        for character in input:
            # letters only alpha
            if character.isalpha() or character.isspace():
                # not english letters
                character = re.sub(r"[A-Za-z]+", ' ', character)
                # not chinese letters
                for n in re.findall(ur'[^\u4e00-\u9fff]+', character):
                    valids.append(n)
        values = ''.join(valids)
        values = re.sub(' +', ' ', values)
        # values = re.sub('. +', '.', values)
        return values

    def writeFile(self, filename, content, path):
        try:
            print(path)
            fout = file(path + filename, 'w')
            fout.write(content)
            fout.close()
        except Exception, e:
            print('Write File Exception', e)


class WriteFile(threading.Thread):
    def __init__(self, filename, content, path):
        threading.Thread.__init__(self)
        self.path = path
        self.filename = filename
        self.content = content

    def run(self):
        try:
            print(self.content)
            # fout = file(self.path + self.filename)
            # fout.write(self.content)
            # fout.close()
        except Exception, e:
            print('Write File Exception', e)


if __name__ == "__main__":
    handler = UyghurHandler("chinabroadcast")
    handler.uniqueWordList()
