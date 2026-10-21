from pathlib import Path

URL = (Path(__file__).parent.parent / "demo.html").as_uri()
username = "陈宁悦"
password = "123456"
expected = "登录成功"
expected_empty = "用户名和密码不能为空"