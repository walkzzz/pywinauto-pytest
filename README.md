# pywinauto-pytest

一个基于 pytest 的 pywinauto UI 自动化测试插件，支持多种测试用例格式和 Allure 报告。

## 功能特性

* **多格式支持**：支持 YAML、JSON、Excel 和 Markdown 格式编写测试用例
* **易用性**：提供简洁的测试用例语法，降低编写 UI 自动化测试的门槛
* **强大的报告**：集成 Allure 报告，支持截图、步骤记录、失败重试等
* **灵活的扩展**：基于抽象基类设计，方便扩展新的解析器或执行器
* **完善的日志**：支持不同级别日志输出，便于调试和问题定位

## 安装

### 从PyPI安装

```bash
pip install pywinauto-pytest
```

### 从源码安装

```bash
git clone https://github.com/yourusername/pywinauto-pytest.git
cd pywinauto-pytest
pip install -e .
```

### 安装开发依赖

```bash
pip install -e .[dev]
```

## 命令行参数

```bash
pytest [options] [file_or_dir]
```

### 主要选项

- `--pywinauto-file`: 指定单个测试文件路径
- `--pywinauto-path`: 指定测试文件目录
- `--pywinauto-log-level`: 设置日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `--pywinauto-log-file`: 指定日志文件路径
- `--alluredir`: 指定Allure报告输出目录

## 使用示例

### 运行单个测试文件

```bash
pytest --pywinauto-file examples/sample_tests/sample.yaml
```

### 运行目录下所有测试文件

```bash
pytest --pywinauto-path examples/sample_tests/
```

### 设置日志级别

```bash
pytest --pywinauto-file examples/sample_tests/sample.yaml --pywinauto-log-level DEBUG
```

### 生成 Allure 报告

```bash
pytest --pywinauto-file examples/sample_tests/sample.yaml --alluredir=allure-results
allure serve allure-results
```

## 测试用例格式

### YAML 格式示例

```yaml
test_suite: Calculator Tests
tests:
  - name: 加法测试
    description: 测试计算器的加法功能
    priority: high
    steps:
      - action: start_application
        target: calc.exe
        timeout: 5
      - action: click
        target: Button
        locator: "1"
        description: 点击数字键1
      - action: click
        target: Button
        locator: "+"
        description: 点击加号键
      - action: click
        target: Button
        locator: "2"
        description: 点击数字键2
      - action: click
        target: Button
        locator: "="
        description: 点击等号键
      - action: assert_text
        target: Edit
        expected: "3"
        description: 验证结果为3
    teardown:
      - action: close_application
        description: 关闭计算器应用
```

### JSON 格式示例

```json
{
  "test_suite": "Calculator Tests",
  "tests": [
    {
      "name": "加法测试",
      "steps": [
        {
          "action": "start_application",
          "target": "calc.exe"
        },
        {
          "action": "click",
          "target": "Button",
          "locator": "1"
        },
        {
          "action": "click",
          "target": "Button",
          "locator": "+"
        },
        {
          "action": "click",
          "target": "Button",
          "locator": "2"
        },
        {
          "action": "click",
          "target": "Button",
          "locator": "="
        },
        {
          "action": "assert_text",
          "target": "Edit",
          "expected": "3"
        }
      ],
      "teardown": [
        {
          "action": "close_application"
        }
      ]
    }
  ]
}
```

### Excel 格式示例

Excel测试用例包含两个工作表：

1. **TestSuite**: 包含测试套件信息
2. **TestCases**: 包含测试用例和步骤

| 列名         | 说明                     | 示例值               |
|--------------|--------------------------|----------------------|
| TestName     | 测试用例名称             | 加法测试             |
| StepIndex    | 步骤索引                 | 1                    |
| Action       | 操作类型                 | start_application    |
| Target       | 目标控件类型             | -                    |
| Locator      | 控件定位器               | calc.exe             |
| Expected     | 预期结果（断言时使用）   | -                    |
| Description  | 步骤描述                 | 启动计算器应用       |

### Markdown 格式示例

```markdown
# Calculator Tests

## 加法测试
1. **start_application**: calc.exe
2. **click**: Button("1")
3. **click**: Button("+")
4. **click**: Button("2")
5. **click**: Button("=")
6. **assert_text**: Edit() == "3"

**Teardown**:
- **close_application**
```

## 支持的操作类型

| 操作类型               | 描述                     | 参数说明                                                                 |
|------------------------|--------------------------|--------------------------------------------------------------------------|
| `start_application`    | 启动应用程序             | `target`: 应用程序路径<br>`timeout`: 超时时间（可选，默认5秒）           |
| `close_application`    | 关闭应用程序             | 无                                                                       |
| `click`                | 点击操作                 | `target`: 控件类型<br>`locator`: 控件定位器<br>`timeout`: 超时时间        |
| `double_click`         | 双击操作                 | `target`: 控件类型<br>`locator`: 控件定位器<br>`timeout`: 超时时间        |
| `right_click`          | 右键点击操作             | `target`: 控件类型<br>`locator`: 控件定位器<br>`timeout`: 超时时间        |
| `type`                 | 输入文本                 | `target`: 控件类型<br>`locator`: 控件定位器<br>`text`: 输入文本           |
| `set_text`             | 设置文本                 | `target`: 控件类型<br>`locator`: 控件定位器<br>`text`: 设置文本           |
| `assert_text`          | 断言文本                 | `target`: 控件类型<br>`locator`: 控件定位器<br>`expected`: 预期文本       |
| `assert_exists`        | 断言元素存在             | `target`: 控件类型<br>`locator`: 控件定位器<br>`timeout`: 超时时间        |
| `assert_not_exists`    | 断言元素不存在           | `target`: 控件类型<br>`locator`: 控件定位器<br>`timeout`: 超时时间        |
| `wait`                 | 等待操作                 | `time`: 等待时间（秒）<br>`condition`: 等待条件（可选）                  |
| `switch_window`        | 切换窗口                 | `title`: 窗口标题<br>`timeout`: 超时时间                                  |
| `get_text`             | 获取文本                 | `target`: 控件类型<br>`locator`: 控件定位器<br>`timeout`: 超时时间        |
| `select_item`          | 选择列表项               | `target`: 控件类型<br>`locator`: 控件定位器<br>`item`: 选择项            |
| `check_box`            | 勾选/取消勾选复选框       | `target`: 控件类型<br>`locator`: 控件定位器<br>`checked`: 是否勾选        |
| `radio_button`         | 选择单选按钮             | `target`: 控件类型<br>`locator`: 控件定位器                               |

## 配置

### 日志配置

可以通过以下方式配置日志：

1. **默认配置**: 无需任何配置，使用内置默认日志设置
2. **自定义配置文件**: 在项目根目录下创建 `logging.conf` 文件
3. **命令行参数**: 
   - `--pywinauto-log-level`: 设置日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
   - `--pywinauto-log-file`: 指定日志文件路径

#### logging.conf 示例

```ini
[loggers]
keys=root

[handlers]
keys=consoleHandler,fileHandler

[formatters]
keys=simpleFormatter

[logger_root]
level=INFO
handlers=consoleHandler,fileHandler

[handler_consoleHandler]
class=StreamHandler
level=INFO
formatter=simpleFormatter
args=(sys.stdout,)

[handler_fileHandler]
class=FileHandler
level=DEBUG
formatter=simpleFormatter
args=('pywinauto-pytest.log', 'w')

[formatter_simpleFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
datefmt=%Y-%m-%d %H:%M:%S
```

### Allure 报告配置

Allure 报告已集成到插件中，无需额外安装。使用以下步骤生成报告：

1. 运行测试时添加 `--alluredir` 参数：
   ```bash
   pytest --pywinauto-file examples/sample_tests/sample.yaml --alluredir=allure-results
   ```

2. 查看报告：
   ```bash
   allure serve allure-results
   ```

### 项目配置文件

可以在项目根目录下创建 `pywinauto-pytest.ini` 文件进行全局配置：

```ini
[pywinauto-pytest]
log_level = INFO
log_file = pywinauto-pytest.log
report_dir = allure-results
```

## 项目结构

```
pywinauto-pytest/ 
 ├── src/ 
 │   └── pywinauto_pytest/ 
 │       ├── __init__.py 
 │       ├── plugin.py              # pytest 插件入口 
 │       ├── parser/                # 多格式解析器 
 │       │   ├── __init__.py 
 │       │   ├── base_parser.py     # 抽象基类 
 │       │   ├── yaml_parser.py     # YAML 解析器 
 │       │   ├── json_parser.py     # JSON 解析器 
 │       │   ├── excel_parser.py    # Excel 解析器 
 │       │   └── markdown_parser.py # Markdown 解析器 
 │       ├── executor/              # 执行引擎 
 │       │   ├── __init__.py 
 │       │   ├── base_executor.py   # 基础执行器 
 │       │   └── pywinauto_executor.py # pywinauto 专用执行器 
 │       ├── fixtures.py            # 自定义 fixtures 
 │       ├── allure_integration.py  # Allure 报告集成 
 │       ├── logger.py              # 日志配置 
 │       └── models.py              # 数据模型 
 ├── tests/                         # 单元测试 
 ├── examples/                      # 示例测试用例 
 ├── setup.py 
 ├── README.md 
 ├── requirements.txt 
 └── logging.conf
```

## 开发

### 安装开发依赖

```bash
pip install -e .[dev]
```

### 运行单元测试

```bash
pytest tests/
```

### 构建包

```bash
python -m build
```

## 许可证

MIT
