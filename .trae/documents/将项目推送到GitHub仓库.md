# 将项目推送到GitHub仓库

## 1. 创建.gitignore文件
创建一个标准的.gitignore文件，排除不需要提交的文件和目录，包括：
- 虚拟环境目录（venv）
- 构建输出目录（build, dist）
- 本地仓库目录（local-repo）
- 测试缓存（.pytest_cache）
- 日志文件（*.log, log.html, report.html）
- IDE配置文件（.vscode, .idea）
- 临时文件和缓存

## 2. 初始化git仓库
使用`git init`命令初始化本地git仓库

## 3. 配置远程仓库
添加GitHub远程仓库：`git remote add origin https://github.com/walkzzz/pywinauto-pytest.git`

## 4. 提交代码
1. 添加所有文件到暂存区：`git add .`
2. 提交代码：`git commit -m "Initial commit: pywinauto-pytest library with multi-format test support"`

## 5. 推送代码到GitHub
推送代码到远程仓库：`git push -u origin master`

## 6. 验证推送结果
检查推送是否成功，并验证GitHub仓库中是否有所有文件

## 7. 后续步骤
- 配置GitHub Actions进行CI/CD（可选）
- 添加项目标签和版本号（可选）
- 配置分支保护规则（可选）