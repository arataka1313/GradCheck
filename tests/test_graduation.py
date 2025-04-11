import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.check_graduation import check_graduation

def test_user_passes():
    result = check_graduation(
        "required_courses.json",
        "elective_courses.json",
        "general_courses.json",
        "fusion_courses.json",
        "clasify.json",
        "tests/data/pass_user.json"  # 合格するユーザーのデータ
    )
    assert result == True

def test_user_fails():
    result = check_graduation(
        "required_courses.json",
        "elective_courses.json",
        "general_courses.json",
        "fusion_courses.json",
        "clasify.json",
        "tests/data/fail_user.json"  # 不合格ユーザーのデータ
    )
    assert result == False
