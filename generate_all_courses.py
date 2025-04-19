# 共通教育、融合科目、専門必修、専門選択科目の4つの科目のjsonファイルを一つにしてくれるプログラム
# ui(gradcheck-ui)を作ろうとした時の残骸。

import json
from pathlib import Path

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

base = Path(__file__).parent
required = load_json(base / "data" / "required_courses.json")
elective = load_json(base / "data" / "elective_courses.json")
general_raw = load_json(base / "data" / "general_courses.json")
fusion_raw = load_json(base / "data" / "fusion_courses.json")

# general_courses.json の中からすべてのコースを抽出（4階層ネスト解除）
general = []
for domain in general_raw["共通教育科目"].values():  # 教養領域・総合領域など
    for category in domain.values():  # 人文系科目・総合科目など
        for course in category:  # 各授業
            general.append(course)

# fusion もネストされてるので展開
fusion = []
for option in fusion_raw["fusion_course_condition"]["options"]:
    fusion.extend(option["courses"])

# 全部結合
all_courses = required + elective + general + fusion

# 出力パス
output_path = base / "gradcheck-ui" / "src" / "data" / "all_courses.json"

# 改行あり・1行1教科の形式で保存
with open(output_path, "w", encoding="utf-8") as f:
    f.write("[\n")
    for i, course in enumerate(all_courses):
        line = json.dumps(course, ensure_ascii=False)
        if i != len(all_courses) - 1:
            line += ","
        f.write(f"  {line}\n")
    f.write("]\n")

print("✅ all_courses.json を生成しました！")
