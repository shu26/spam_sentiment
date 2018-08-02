
# coding: utf-8

# # 実際にスパム判定と感情分析をしてみる

# In[1]:

import pickle
import MeCab
import numpy as np
import re
import pandas as pd
from sklearn.naive_bayes import GaussianNB

# テストするテキスト
test_text1 = """
お疲れ様です！
こちら担当分は一旦修正したので、masterと私のブランチをマージしました。
キリの良いところでブランチとmasterをマージ→競合解消・全機能最終チェックしてからipa作成をお願いします
"""
test_text2 = """
コンテンツ利用料金の精算確認が取れません。
本日ご連絡なき場合には法的手続きに移行します。
アマゾンジャパン（株）(0342182663)
"""

# ファイル名
data_file = "./ok-spam.pickle"
model_file = "./ok-spam-model.pickle"
label_names = ['OK', 'SPAM']
# 単語辞書を読み出す
data = pickle.load(open(data_file, "rb"))
word_dic = data[2]
# MeCabの準備
tagger = MeCab.Tagger("-d /var/lib/mecab/dic/mecab-ipadic-neologd")
# 学習済みのモデルを読み出す
model = pickle.load(open(model_file, "rb"))



###########   感情分析   ###############

    
# PN Tableを読み込み (downloaded by http://www.lr.pi.titech.ac.jp/~takamura/pndic_ja.html)
pn_df = pd.read_csv('./pn_ja.dic.txt', sep=':', encoding='shift-jis', names=('Word','Reading','POS', 'PN'))
# PN Tableをデータフレームからdict型に変換しておく
word_list = list(pn_df['Word'])
pn_list = list(pn_df['PN'])  
pn_dict = dict(zip(word_list, pn_list))

# PNの平均値をとる関数
def get_pnmean(diclist):
    pn_list = []
    for pn in diclist:
        if pn != 'notfound':
            pn_list.append(pn)  # notfoundだった場合は追加もしない    
    if len(pn_list) > 0:        # 「全部notfound」じゃなければ
        pnmean = np.mean(pn_list)
    else:
        pnmean = 0              # 全部notfoundならゼロにする
    return(pnmean)

# テキストを判定する
def check_spam(text):
    # テキストを単語IDのリストに変換し単語の頻出頻度を調べる
    zw = np.zeros(word_dic['__id'])
    count = 0
    diclist_new = []
    s = tagger.parse(text)
    # 単語毎の回数を加算
    for line in s.split("\n"):
        if line == 'EOS' or line == '': 
            continue
        params = line.split("\t")[1].split(",")
        original = params[6]
        # 単語の出現回数を計算
        if original in word_dic:
            id = word_dic[original]
            zw[id] += 1
            count += 1
        # PN値を追加
        if original in pn_dict:
            pn = float(pn_dict[original])         # floatに変換
        else:
            pn = 'notfound'   
        diclist_new.append(pn)
    zw = zw / count
          
    # スパムかどうか予測
    pre = model.predict([zw])[0]
    print("- 結果＝", label_names[pre], )
    
    # 感情分析
    pnmean = get_pnmean(diclist_new)
    print("- PN値＝", pnmean)
    
    return label_names[pre], pnmean
    
    
        
if __name__ == '__main__':
    check_spam(test_text1)
    check_spam(test_text2)
    


# In[ ]:



