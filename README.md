# GradCheck
![Python CI](https://github.com/arataka1313/GradCheck/actions/workflows/python-ci.yml/badge.svg)

> 知能情報コースの学生向け、卒業要件チェックツールです。  
> 履修科目（JSON）をもとに卒業要件の達成状況を自動判定するCLIツールです。

---

## 概要

**GradCheck** は、大学の卒業要件に基づいて、  
「自分があと何の単位を取れば卒業できるか」を自動で判定してくれます。

-  履修ミスや取りこぼしを防げる

---

## ターゲット

- 琉球大学工学部工学科知能情報コース4年生(2022年度入学学生)
- 毎年履修ミスで卒業できない先輩を見て不安な人

---
## セットアップ手順

### 1. このリポジトリをダウンロード

#### 方法①（Gitが使える人向け）:
```bash
git clone https://github.com/your-username/GradCheck.git
cd GradCheck
```

#### 方法②（Gitが使えない人向け）:
1. このページの右上の「**Code > Download ZIP**」をクリック  
2. ZIPを解凍し、`GradCheck` フォルダに移動

### 3. 自分の履修科目データを編集
```bash
# data/my_courses.json を自分の履修科目に書き換える or 他のjsonファイルから自分が取った科目をコピペすればOK
# サンプルが入っているので、それをベースに修正すればOK
```

---

### 4. 卒業判定の実行
```bash
python3 src/check_graduation.py
```

---

### 5. 結果を確認！
```~/GradCheck/src$
【不合格】専門必修に未取得科目があります：
 - 工共401「卒業研究Ⅰ」(3単位)
 - 工共402「卒業研究Ⅱ」(3単位)
 - 工共406「セミナーⅡ」(1単位)
【不合格】研究・基礎演習・実験 が不足（9/16単位）
 - 工共401「卒業研究Ⅰ」(3単位)
 - 工共402「卒業研究Ⅱ」(3単位)
 - 工共406「セミナーⅡ」(1単位)
```

---

## ファイル構成
```bash
GradCheck/
├── src/
│   └── check_graduation.py         # 判定ロジック
├── data/
│   ├── my_courses.json             # 自分の履修科目（手動で編集）
│   ├── required_courses.json       # 専門必修科目一覧
│   ├── elective_courses.json       # 専門選択科目一覧
│   ├── general_courses.json        # 共通教育科目一覧
│   ├── fusion_courses.json         # 融合科目一覧
│   └── clasify.json                # 専門科目分類ルール
```

---

## 注意点
- `data/my_courses.json` を編集することで、自分の履修履歴に基づいた判定が可能です。
- あくまで卒業できるかどうかの判定だけなので、教職科目は考慮していません。
- "専門科目（自由）"の扱いがよくわからなかったので、判定ロジックにいれてないです(だから、とった専門科目(自由)に相当する適当な科目をmy_courses.jsonに追加してね)
- JSONフォーマットが壊れていると読み込みに失敗しますので、カンマ抜け等に注意してください。

---

## コントリビューション歓迎！

「UI作るの手伝いたい！」などなど大歓迎です

---

## 免責事項

- このプログラムの利用によって発生したいかなる損害・損失に対しても、作成者は一切の責任を負いません。
- 利用は自己責任でお願いします。

---

## ライセンス

MIT License

---

## 作者

GradCheck開発者  Taka(B4)
[@arataka1313](https://github.com/arataka1313)  
琉球大学 知能情報コースB4（卒業予定 2026/3）