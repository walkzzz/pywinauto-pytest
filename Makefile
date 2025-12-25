# pywinauto-pytest 构建脚本

# 默认目标
.DEFAULT_GOAL := help

# 虚拟环境目录
VENV_DIR := venv

# 依赖文件
REQUIREMENTS := requirements.txt

# 测试目录
TEST_DIR := tests

# 源代码目录
SRC_DIR := src

# 构建输出目录
BUILD_DIR := dist

# 本地仓库目录
LOCAL_REPO := ../local-repo

# 版本文件
VERSION_FILE := VERSION

# Python 解释器
PYTHON := python

# pip 命令
PIP := $(VENV_DIR)/Scripts/pip

# pytest 命令
PYTEST := $(VENV_DIR)/Scripts/pytest

# 帮助信息
help:
	@echo "pywinauto-pytest 构建脚本"
	@echo ""
	@echo "可用目标："
	@echo "  help        - 显示此帮助信息"
	@echo "  venv        - 创建虚拟环境"
	@echo "  install     - 安装项目依赖"
	@echo "  install-dev - 安装开发依赖"
	@echo "  test        - 运行单元测试"
	@echo "  lint        - 运行代码检查"
	@echo "  build       - 构建项目包"
	@echo "  clean       - 清理构建文件"
	@echo "  distribute  - 构建并分发到本地仓库"
	@echo ""

# 创建虚拟环境
venv:
	$(PYTHON) -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip

# 安装项目依赖
install:
	$(PIP) install -r $(REQUIREMENTS)

# 安装开发依赖
install-dev:
	$(PIP) install -r $(REQUIREMENTS)
	$(PIP) install pytest pytest-cov flake8 black

# 运行单元测试
test:
	$(PYTEST) $(TEST_DIR) -v --cov=$(SRC_DIR) --cov-report=term --cov-report=html

# 运行代码检查
lint:
	$(PIP) install flake8 black
	flake8 $(SRC_DIR) $(TEST_DIR)
	black --check $(SRC_DIR) $(TEST_DIR)

# 构建项目包
build:
	$(PYTHON) setup.py sdist bdist_wheel

# 清理构建文件
clean:
	rm -rf $(BUILD_DIR) *.egg-info .pytest_cache htmlcov

distribute: build
	@mkdir -p $(LOCAL_REPO)
	cp $(BUILD_DIR)/* $(LOCAL_REPO)/
	@echo "打包时间: $$(date)" > $(LOCAL_REPO)/PACKAGE_INFO.txt
	@echo "包版本: $$(grep -A 1 'version=' setup.py | grep -o "'[^']*'" | tr -d "'")" >> $(LOCAL_REPO)/PACKAGE_INFO.txt
	@echo "已将包文件分发到本地仓库: $(LOCAL_REPO)"

# 完整构建流程
all: venv install test build distribute
