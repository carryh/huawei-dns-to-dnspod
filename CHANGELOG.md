# 更新日志

## [1.0.0] - 2024-07-01

### 新增功能
- ✨ 华为云DNS记录转DNSPOD格式的核心功能
- ✨ 智能Host记录清理（移除域名部分）
- ✨ TXT记录值引号自动清理
- ✨ MX字段格式修正（非MX记录显示"-"）
- ✨ 多IP地址自动拆分功能
- ✨ 图形界面版本（dns_converter_gui.py）
- ✨ 命令行版本（dns_converter.py）
- ✨ Windows批处理脚本（convert_dns.bat）
- ✨ 一键安装脚本（install.bat）

### 支持的功能
- 📋 支持所有常见DNS记录类型（A、AAAA、CNAME、MX、TXT、NS、SRV、PTR）
- 🌐 智能识别中英文列名
- 📊 支持Excel (.xlsx, .xls) 和CSV格式
- 🛡️ 详细的错误处理和日志
- 📝 完整的转换摘要报告

### 转换功能详情
- **Host记录清理**: `www.example.com.` → `www`, `example.com.` → `@`
- **TXT记录清理**: `"v=spf1 include:_spf.example.com ~all"` → `v=spf1 include:_spf.example.com ~all`
- **MX字段修正**: 非MX记录的MX字段自动设置为 `-`
- **多IP拆分**: 华为云一个A记录的多个IP自动拆分为多个DNSPOD记录
- **格式标准化**: 完全符合DNSPOD导入格式要求

### 文档
- 📖 完整的README.md使用指南
- 📄 MIT开源许可证
- 🔧 详细的安装和使用说明
