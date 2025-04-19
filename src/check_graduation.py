import os
import json

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def check_graduation(
    required_path,
    elective_path,
    general_path,
    fusion_path,
    clasify_path,
    user_path
) -> bool:
    base_dir = os.path.dirname(__file__)
    project_root = os.path.abspath(os.path.join(base_dir, ".."))

    required = load_json(os.path.join(project_root, "data", required_path))
    elective = load_json(os.path.join(project_root, "data", elective_path))
    general  = load_json(os.path.join(project_root, "data", general_path))
    fusion   = load_json(os.path.join(project_root, "data", fusion_path))
    clasify  = load_json(os.path.join(project_root, "data", clasify_path))
    user     = load_json(os.path.join(project_root, user_path))

    user_codes = {c["code"]: c for c in user}
    user_credits = {c["code"]: c["credits"] for c in user}
    not_passed = False

    # 専門必修
    missing_required = [c for c in required if c["code"] not in user_codes]
    if missing_required:
        not_passed = True
        print("【不合格】専門必修に未取得科目があります：")
        for c in missing_required:
            print(f" - {c['code']}「{c['name']}」({c['credits']}単位)")

    # 専門選択
    sel_credits = sum(c["credits"] for c in elective if c["code"] in user_codes)
    if sel_credits < 8:
        not_passed = True
        print(f"【不合格】専門選択が不足（{sel_credits}/8単位）")

    # 共通教育
    area = {k: 0 for k in ["健", "人", "社", "自", "総", "琉", "C", "情11", "英語", "外国語_英語以外"]}
    total = 0
    for c in user:
        code = c["code"]
        cr = c["credits"]
        total += cr
        if code.startswith("健"): area["健"] += cr
        elif code.startswith("人"): area["人"] += cr
        elif code.startswith("社"): area["社"] += cr
        elif code.startswith("自"): area["自"] += cr
        elif code.startswith("総"): area["総"] += cr
        elif code.startswith("琉"): area["琉"] += cr
        elif code.startswith("C"): area["C"] += cr
        elif code == "情11": area["情11"] += cr
        elif code.startswith("外"):
            if code[1] == "1": area["英語"] += cr
            else: area["外国語_英語以外"] += cr

    教養 = area["人"] + area["社"] + area["自"] + area["総"] + area["琉"] + area["C"]
    required_eng = {"外101", "外102", "外108"}
    eng_condition = (required_eng.issubset(user_codes) and area["外国語_英語以外"] >= 4) or area["英語"] >= 12

    if area["健"] < 2:
        not_passed = True
        print(f"【不合格】健康運動系が不足（{area['健']}単位）")
    if area["人"] < 2:
        not_passed = True
        print(f"【不合格】人文系が不足（{area['人']}単位）")
    if area["社"] < 2 and area["自"] < 2:
        not_passed = True
        print(f"【不合格】社会系または自然系が不足（社: {area['社']} 自: {area['自']}）")
    if area["総"] + area["琉"] + area["C"] < 2:
        not_passed = True
        print(f"【不合格】総合領域が不足（{area['総'] + area['琉'] + area['C']}単位）")
    if 教養 < 14:
        not_passed = True
        print(f"【不合格】教養領域が不足（{教養}/14単位）")
    if area["情11"] < 2:
        not_passed = True
        print("【不合格】日本語表現法入門（情11）が未取得または不足")
    if not eng_condition:
        not_passed = True
        print(f"【不合格】英語要件未達（英語: {area['英語']} 外国語: {area['外国語_英語以外']}）")
    if total < 30:
        not_passed = True
        print(f"【不合格】共通教育合計が30単位未満（{total}単位）")

    # 専門基礎（先修）
    required_senshu = {"先11", "先12", "先31"}
    user_senshu = [c for c in user if c["code"].startswith("先")]
    user_senshu_codes = {c["code"] for c in user_senshu}
    senshu_total = sum(c["credits"] for c in user_senshu)

    if not required_senshu.issubset(user_senshu_codes):
        not_passed = True
        miss = required_senshu - user_senshu_codes
        print(f"【不合格】先修科目未取得：{', '.join(miss)}")
    if senshu_total < 6:
        not_passed = True
        print(f"【不合格】先修単位数が不足（{senshu_total}/6）")

    # 工学融合
    導入 = sum(user_credits.get(c["code"], 0) for c in fusion["fusion_course_condition"]["options"][0]["courses"])
    選択 = sum(user_credits.get(c["code"], 0) for c in fusion["fusion_course_condition"]["options"][1]["courses"])
    if 導入 < 4 and 選択 < 4:
        not_passed = True
        print("【不合格】工学融合が不足（導入/選択で4単位必要）")
        print(f" - 導入: {導入}/4, 選択: {選択}/4")

    # 専門分類
    basic_math = {"工共111", "工共112", "知能103"}
    extra_math = {"工共213", "工共211", "工共212"}
    adv = [c["code"] for c in clasify["知能情報アドバンスト"]]
    rel = [c["code"] for c in clasify["知能情報関連"]["明示的リスト"]]
    rel_ex = set(clasify["知能情報関連"]["除外コード"])
    rel_add = [c for c in user_credits if c.startswith("工共") and c not in rel_ex]
    fusion_codes = [c["code"] for o in fusion["fusion_course_condition"]["options"] for c in o["courses"]]

    known = set().union(*[
        {c["code"] for v in clasify.values() if isinstance(v, list) for c in v if isinstance(c, dict)},
        set(rel), set(rel_add), set(adv), set(fusion_codes)
    ])
    自由単位 = sum(c["credits"] for c in user if c["code"] not in known)

    # チェック関数
    def check_category(name, required):
        total = sum(user_credits.get(c["code"], 0) for c in clasify.get(name, []))
        if total < required:
            print(f"【不合格】{name} が不足（{total}/{required}単位）")
            miss = [c for c in clasify[name] if c["code"] not in user_codes]
            for m in miss:
                print(f" - {m['code']}「{m['name']}」({m['credits']}単位)")
            return True
        return False

    not_passed |= check_category("情報技術系", 2)
    not_passed |= check_category("総合力演習", 7)
    not_passed |= check_category("研究・基礎演習・実験", 16)
    core_total = sum(user_credits.get(c["code"], 0) for c in clasify["知能情報コア"])
    if core_total < 26:
        not_passed = True
        print(f"【不合格】知能情報コアが不足（{core_total}/26）")
    basic_total = sum(user_credits.get(c, 0) for c in basic_math)
    if basic_total < 6:
        not_passed = True
        print(f"【不合格】数学基礎（基本3科目）が不足（{basic_total}/6）")

    # 合算22/37
    合算22 = sum(user_credits.get(c, 0) for c in extra_math) + sum(user_credits.get(c, 0) for c in adv + rel + rel_add)
    合算37 = 合算22 + 導入 + 選択 + 自由単位

    if 合算22 < 22:
        not_passed = True
        print(f"【不合格】専門合算22単位未満（{合算22}単位）")
    if 合算37 < 37:
        not_passed = True
        print(f"【不合格】専門合算37単位未満（{合算37}単位）")

    if not not_passed:
        print("🎉【合格】すべての条件を満たしています！")

    return not not_passed

if __name__ == "__main__":
    check_graduation(
        "required_courses.json",
        "elective_courses.json",
        "general_courses.json",
        "fusion_courses.json",
        "clasify.json",
        "data/my_courses.json"
    )
