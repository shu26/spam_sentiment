
# coding: utf-8

# # 頻出単語を機械学習し、 ok-spam-model.pickle に保存

# In[1]:

import pickle
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# データファイルの読み込み
data_file = "./ok-spam.pickle"
save_file = "./ok-spam-model.pickle"
data = pickle.load(open(data_file, "rb"))
y = data[0] # ラベル
x = data[1] # 単語の出現頻度

# 100回、学習とテストを繰り返す
count =100
rate = 0
for i in range(count):
    # データを学習用とテスト用に分割
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2)
    # 学習する
    model = GaussianNB()
    model.fit(x_train, y_train)
    # 評価する
    y_pred = model.predict(x_test)
    acc = accuracy_score(y_test, y_pred)
    # 評価結果が良ければモデルを保存
    if acc > 0.94: pickle.dump(model, open(save_file, "wb"))
    print(acc)
    rate += acc
    
# 平均値を表示
print("----")
print("average=", rate / count)


# In[ ]:



