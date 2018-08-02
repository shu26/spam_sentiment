
# coding: utf-8

# # 単語の出現回数を求め ok-spam.pickle に保存

# In[1]:

# すべてのテキストを巡回して単語データベースを作成する
import os, glob
import MeCab
import numpy as np
import pickle

savefile = "./ok-spam.pickle"
# Mecabの辞書はmecab-ipadic-neologd
tagger = MeCab.Tagger("-d /var/lib/mecab/dic/mecab-ipadic-neologd")
word_dic = {"__id": 0} # 単語辞書
files = [] # 読み込んだ単語データを追加する

# 指定したディレクトリ内のファイル一覧を読み込む
def read_files(dir, label):
    # テキストファイルの一覧を正規表現で指定して取得
    files = glob.glob(dir + '/*.txt')
    for f in files:
        read_file(f, label)
        
# ファイルを読む
def read_file(filename, label):
    with open(filename,"rt", encoding="utf-8") as f:
        text = f.read()
    files.append({
        "label": label,
        "words": text_to_word_id_list(text)
    })
    
# テキストを単語IDのリストに変換
def text_to_word_id_list(text):
    word_s = tagger.parse(text)
    words = []
    for line in word_s.split("\n"):
        if line == 'EOS' or line == '': 
            continue
        word = line.split("\t")[0]
        params = line.split("\t")[1].split(",") 
        hinshi = params[0] 
        original = params[6] 
        if not (hinshi in ['名詞', '動詞', '形容詞']):
            continue
        id = word_to_id(original)
        words.append(id)
    return words

# 単語をidに変換
def word_to_id(word):
    # 単語が既出でなければIDを割り振る
    if not (word in word_dic):
        id = word_dic["__id"]
        word_dic["__id"] += 1
        word_dic[word] = id
    else:
        id = word_dic[word]
    return id

# 単語の出現頻度のデータを作る
def make_freq_data_allfiles():
    y = []
    x = []
    for f in files:
        y.append(f['label'])
        x.append(make_freq_data(f['words']))
    return y, x

# 単語の出現回数を調べる
def make_freq_data(words):
    count = 0
    dat = np.zeros(word_dic["__id"], 'float')
    for word in words:
        dat[word] += 1
        count += 1
    # 回数を出現頻度に直す
    dat = dat / count
    return dat

# ファイルの一覧から学習用のデータベースを作る
if __name__ == "__main__":
    read_files("ok", 0)
    read_files("spam", 1)
    y, x = make_freq_data_allfiles()
    # ファイルにデータを保存
    pickle.dump([y, x, word_dic], open(savefile, 'wb'))
    print("ok")


# In[ ]:



