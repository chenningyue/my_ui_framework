# my_ui_framework — UI 自动化测试框架

基于 **Python + pytest + Playwright** 的 UI 自动化框架，用 **Page Object** 分层。

> 这个仓库是「从 0 搭一套 UI 自动化框架」的产出物，目标是：**别人 clone 下来，装依赖，就能跑；push 到 GitHub 后 CI 自动跑**。

## 技术栈

- Python 3.11
- pytest 9.x（用例 + fixture + 断言）
- Playwright 1.64（sync API，Chromium）

## 目录结构

```
my_ui_framework/
├── pages/                 # 页面对象层（Page Object）
│   └── login_page.py        # 登录页：定位器 + 操作封装成一个类
├── testcase/              # 用例层：只写业务步骤 + 断言
│   └── test_login.py        # 2 条用例：正常登录 / 空密码
├── data/                  # 数据层：URL / 账号 / 期望值，与代码分离
│   └── test_data.py
├── conftest.py            # fixture：browser(session级) / page(function级) + 失败自动截图
├── demo.html              # 登录页（框架自带，跟仓库走）
├── .github/workflows/     # CI 配置
│   └── ci.yml
├── requirements.txt       # 依赖清单
└── .gitignore
```

## 环境准备

```bash
pip install -r requirements.txt
playwright install chromium     # 装 Chromium 内核（首次需要）
```

## 怎么跑

```bash
cd my_ui_framework
pytest -v                # 有头模式：能看到浏览器一步步操作（学习时用）
HEADLESS=1 pytest -v     # 无头模式：后台跑，不弹窗口（CI 用）
```

## 分层思路（一句话）

**Page Object 模式：定位器收进 pages、操作收进方法、数据收进 data、用例只写业务 + 断言**——页面变了改 pages、数据变了改 data、断言变了改 testcase，互不影响。

以登录为例：`test_login.py` 里用例只写「打开登录页 → 填账号密码 → 点登录 → 断言结果」，至于「用户名框的定位器是什么、怎么填」全封装在 `LoginPage` 类里，用例层看不到。

## 关键设计点

1. **headless 交给环境变量**：`conftest.py` 里 `headless = os.getenv("HEADLESS") == "1"` —— 本地不设走有头（能看到浏览器），CI 设 `HEADLESS=1` 走无头（CI 机器没显示器）。
2. **demo.html 跨平台定位**：`data/test_data.py` 里 `URL = (Path(__file__).parent.parent / "demo.html").as_uri()` —— 用 `__file__` 定位到框架根目录、`as_uri()` 转成 `file://` 地址，Windows / Linux 都能用，**不写死绝对路径**。
3. **失败自动截图**：用例失败时，`conftest.py` 的 fixture 自动把页面截图存到 `report/`（该目录已 gitignore）。

## CI（GitHub Actions）

push 到 `main` 会自动触发 `.github/workflows/ci.yml`：**拉代码 → 装依赖 → 装 Chromium → 无头跑测试**。比接口框架多「装浏览器」一步（CI 的 Linux 机器默认没有 Chromium）。

## 练手页面 demo.html

一个本地登录页：填用户名 + 密码点「登录」，两个都填了显示「登录成功，欢迎 XXX」，密码留空显示「用户名和密码不能为空」。对应的两条用例就是 `test_login_success` 和 `test_login_null`。
