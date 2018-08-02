
# coding: utf-8

# In[ ]:

import json
import flask
from flask import request
import test_spam_ok

# ポート番号
TM_PORT_NO = 8086
# HTTP サーバーを起動
app = flask.Flask(__name__)
print("http://localhost:" + str(TM_PORT_NO))

# ルートへアクセスした場合
@app.route('/', methods=['GET'])
def index():
    with open("spam_ok.html", "rb") as f:
        return f.read()
    
# /api　へアクセスした場合
@app.route('/api', methods=['GET'])
def api():
    # URL パラメーターを取得
    q = request.args.get('q', '')
    if q ==  '':
        return '{"label": "空です", "per": 0}'
    print("q=", q)
    # テキストのジャンル判定を行う
    label, pnmean = test_spam_ok.check_spam(q)
    # 結果をJSONで出力
    return json.dumps({
        "label": label,
        "pnmean": pnmean
    })

if __name__ == '__main__':
    # サーバーを起動
    app.run(debug=False, port=TM_PORT_NO)

