from openpyxl import Workbook

# 创建一个新的工作簿
workbook = Workbook()
sheet = workbook.active

# 设置测试套件名称（A1 单元格）
sheet['A1'] = 'Calculator Tests'

# 设置列标题（第 2 行）
sheet['A2'] = 'Test Case'
sheet['B2'] = 'Action'
sheet['C2'] = 'Target'
sheet['D2'] = 'Locator'
sheet['E2'] = 'Expected'

# 加法测试用例
sheet['A3'] = '## 加法测试'
sheet['B4'] = 'start_application'
sheet['C4'] = 'calc.exe'
sheet['B5'] = 'click'
sheet['C5'] = 'Button'
sheet['D5'] = '1'
sheet['B6'] = 'click'
sheet['C6'] = 'Button'
sheet['D6'] = '+'
sheet['B7'] = 'click'
sheet['C7'] = 'Button'
sheet['D7'] = '2'
sheet['B8'] = 'click'
sheet['C8'] = 'Button'
sheet['D8'] = '='
sheet['B9'] = 'assert_text'
sheet['C9'] = 'Edit'
sheet['E9'] = '3'
sheet['A10'] = 'Teardown'
sheet['B10'] = 'close_application'

# 减法测试用例
sheet['A12'] = '## 减法测试'
sheet['B13'] = 'start_application'
sheet['C13'] = 'calc.exe'
sheet['B14'] = 'click'
sheet['C14'] = 'Button'
sheet['D14'] = '5'
sheet['B15'] = 'click'
sheet['C15'] = 'Button'
sheet['D15'] = '-'
sheet['B16'] = 'click'
sheet['C16'] = 'Button'
sheet['D16'] = '3'
sheet['B17'] = 'click'
sheet['C17'] = 'Button'
sheet['D17'] = '='
sheet['B18'] = 'assert_text'
sheet['C18'] = 'Edit'
sheet['E18'] = '2'
sheet['A19'] = 'Teardown'
sheet['B19'] = 'close_application'

# 保存工作簿
workbook.save('sample.xlsx')
print('Excel sample file generated successfully!')
