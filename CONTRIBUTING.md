# 贡献指南

感谢您对华为云DNS转DNSPOD工具的关注！我们欢迎任何形式的贡献。

## 🤝 如何贡献

### 报告问题
如果您发现了bug或有功能建议：
1. 搜索现有的 [Issues](../../issues) 确认问题未被报告
2. 创建新的 [Issue](../../issues/new)
3. 详细描述问题或建议，包括：
   - 操作系统和Python版本
   - 错误信息和日志
   - 重现步骤
   - 期望的行为

### 提交代码
1. Fork 本仓库
2. 创建功能分支：`git checkout -b feature/your-feature-name`
3. 提交更改：`git commit -am 'Add some feature'`
4. 推送到分支：`git push origin feature/your-feature-name`
5. 创建 Pull Request

## 🛠️ 开发环境设置

### 环境要求
- Python 3.7+
- pip

### 安装依赖
```bash
git clone https://github.com/your-username/huawei-dns-to-dnspod.git
cd huawei-dns-to-dnspod
pip install -r requirements.txt
```

### 项目结构
```
huawei-dns-to-dnspod/
├── dns_converter.py          # 核心转换逻辑
├── dns_converter_gui.py      # 图形界面
├── convert_dns.bat          # Windows批处理脚本
├── install.bat              # 安装脚本
├── requirements.txt         # Python依赖
├── huawei_dns_sample.xlsx   # 华为云示例文件
├── dnspod_format_sample.csv # DNSPOD格式示例
├── README.md               # 项目说明
├── LICENSE                 # 许可证
├── CHANGELOG.md           # 更新日志
└── CONTRIBUTING.md        # 本文件
```

## 📝 代码规范

### Python代码规范
- 遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 代码风格
- 使用有意义的变量和函数名
- 添加适当的注释和文档字符串
- 保持函数简洁，单一职责

### 提交信息规范
使用清晰的提交信息：
```
类型: 简短描述

详细描述（可选）

- 修复了什么问题
- 添加了什么功能
- 影响范围
```

类型包括：
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

### 示例
```
feat: 添加AAAA记录支持

- 支持IPv6地址转换
- 更新测试用例
- 更新文档说明
```

## 🧪 测试

在提交代码前，请确保：
1. 代码能正常运行
2. 不会破坏现有功能
3. 添加了必要的错误处理

### 手动测试
1. 准备华为云DNS测试文件
2. 运行转换工具
3. 验证输出格式正确
4. 测试各种边界情况

## 📋 Pull Request 检查清单

提交PR前请确认：
- [ ] 代码遵循项目规范
- [ ] 添加了必要的注释
- [ ] 测试通过
- [ ] 更新了相关文档
- [ ] 提交信息清晰明确

## 🎯 优先级功能

我们特别欢迎以下方面的贡献：
- 支持更多DNS记录类型
- 改进错误处理和用户体验
- 添加单元测试
- 性能优化
- 国际化支持
- 支持其他云服务商格式

## 📞 联系方式

如果您有任何问题或建议，可以通过以下方式联系：
- 创建 [Issue](../../issues/new)
- 发起 [Discussion](../../discussions)

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者！

您的贡献将帮助更多用户轻松完成DNS记录迁移。
