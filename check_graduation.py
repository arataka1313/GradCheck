import json

def load_courses(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

general = load_courses("general_courses.json")      # 共通教育科目
required = load_courses("required_courses.json")    # 専門必修科目
elective = load_courses("elective_courses.json")    # 門選択科目
fusion   = load_courses("fusion_courses.json")      # 専門工学融合科目


# 共通教育科目判定
def total_credits(courses):
    return sum(c["credits"] for c in courses)

def is_common_education_ok(my_courses, general_courses):
    # 情報科学演習（情01）は除外
    valid_courses = [
        c for c in my_courses 
        if c["code"] != "情01" and any(c["code"] == g["code"] for g in general_courses)
    ]
    return total_credits(valid_courses) >= 30
