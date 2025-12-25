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

## 减法测试
1. **start_application**: calc.exe
2. **click**: Button("5")
3. **click**: Button("-")
4. **click**: Button("3")
5. **click**: Button("=")
6. **assert_text**: Edit() == "2"

**Teardown**:
- **close_application**
