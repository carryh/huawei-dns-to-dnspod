# 华为云/阿里云DNS转DNSPOD工具

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

这个工具可以将华为云和阿里云的DNS记录Excel文件转换为DNSPOD格式的模板文件，解决不同云服务商DNS记录格式不兼容的问题。

## 🌟 为什么需要这个工具？

当您需要从华为云或阿里云DNS迁移到DNSPOD时，会遇到以下格式不兼容问题：

### 华为云格式问题
- **Host记录格式不同**：华为云包含完整域名，DNSPOD只需要子域名
- **TXT记录引号问题**：华为云TXT记录包含引号，DNSPOD不需要
- **多IP处理**：华为云支持一个A记录多个IP，DNSPOD需要拆分

### 阿里云格式问题
- **解析线路列**：阿里云有解析线路设置，DNSPOD不需要
- **状态列**：阿里云有启用/暂停状态，DNSPOD不需要
- **MX优先级格式**：阿里云MX优先级列名不同

### 通用问题
- **MX字段格式**：DNSPOD要求非MX记录的MX字段显示为 `-`
- **NS记录处理**：DNSPOD的NS记录由服务商管理，无需导入

本工具完美解决所有这些问题，让您一键完成DNS记录迁移！

## ✨ 功能特点

### 🔧 核心转换功能
- **智能Host记录清理**：自动从Host字段中移除域名部分
  ```
  www.example.com.  →  www
  example.com.      →  @
  mail.example.com. →  mail
  ```

- **TXT记录值清理**：自动移除TXT记录值的引号
  ```
  "v=spf1 include:_spf.example.com ~all"  →  v=spf1 include:_spf.example.com ~all
  "295f9c7a-c772-4def-878f-a607a80095b5"  →  295f9c7a-c772-4def-878f-a607a80095b5
  ```

- **MX字段格式修正**：符合DNSPOD标准格式
  ```
  A、TXT、CNAME等记录：MX字段显示为 "-"
  MX记录：MX字段显示优先级数值
  ```

- **多IP地址智能拆分**：华为云一个A记录的多个IP自动拆分为多个DNSPOD记录

### 🛠️ 技术特性
- ✅ **支持多云平台**：华为云和阿里云DNS格式自动识别
- ✅ 支持常见DNS记录类型（A、AAAA、CNAME、MX、TXT、SRV、PTR）
- ⚠️ **自动跳过NS记录**：DNSPOD的NS记录由服务商管理，无需导入
- ✅ 智能识别中英文列名，兼容不同的导出格式
- ✅ 生成标准的DNSPOD导入模板
- ✅ 支持Excel (.xlsx, .xls) 和CSV格式
- ✅ 详细的转换日志和错误处理

### 🎯 用户体验
- ✅ **图形界面**：简单易用，适合所有用户
- ✅ **命令行工具**：适合批处理和自动化
- ✅ **Windows批处理**：拖拽文件即可转换

## 🚀 快速开始

### 📋 环境要求
- Python 3.7 或更高版本
- Windows、macOS 或 Linux

### 📦 安装方法

#### 方法1: 下载发布版本（推荐）
1. 前往 [Releases](../../releases) 页面下载最新版本
2. 解压到任意目录
3. 双击 `install.bat` 自动安装依赖（Windows）

#### 方法2: 克隆源码
```bash
git clone https://github.com/carryh/huawei-dns-to-dnspod.git
cd huawei-dns-to-dnspod
pip install -r requirements.txt
```

### 🎮 使用方法

#### 方法1: 图形界面（推荐新手）
```bash
python dns_converter_gui.py
```
1. 点击"选择文件"选择华为云或阿里云DNS Excel文件
2. 点击"开始转换"
3. 转换完成后会自动打开输出目录

#### 方法2: Windows批处理（最简单）
1. 双击 `convert_dns.bat` 文件
2. 将华为云或阿里云DNS Excel文件拖拽到窗口中
3. 按回车键开始转换

#### 方法3: 命令行（适合批处理）
```bash
# 基本用法
python dns_converter.py input.xlsx

# 指定输出文件
python dns_converter.py input.xlsx -o output.xlsx

# 查看帮助
python dns_converter.py --help
```

## 📖 使用示例

### 转换效果对比

**华为云原始格式：**
```csv
类型,主机记录,记录值,TTL,备注,MX
A,www.example.com.,8.8.8.8\n1.1.1.1,600,Web服务器,
NS,example.com.,ns1.huaweicloud-dns.com,600,华为云NS,
TXT,example.com.,"v=spf1 include:_spf.example.com ~all",600,SPF记录,
MX,example.com.,mail.example.com,600,邮件交换,10
```

**阿里云原始格式：**
```csv
记录类型,主机记录,解析线路,记录值,MX优先级,TTL值,状态(启用/暂停)
A,www,默认,1.1.1.1,,600,启用
CNAME,@,默认,www.aliyun.com,,600,启用
MX,@,默认,mx1.qiye.aliyun.com,5,600,启用
TXT,@,默认,v=spf1 include=spf1.staff.mail.aliyun.com ~all,,600,启用
```

**转换后的DNSPOD格式：**
```csv
Type,Host,Split Zone,Value,MX,TTL,Remarks
A,www,Default,8.8.8.8,-,600,Web服务器
A,www,Default,1.1.1.1,-,600,Web服务器
A,www,Default,1.1.1.1,-,600,
CNAME,@,Default,www.aliyun.com,-,600,
TXT,@,Default,v=spf1 include:_spf.example.com ~all,-,600,SPF记录
TXT,@,Default,v=spf1 include=spf1.staff.mail.aliyun.com ~all,-,600,
MX,@,Default,mail.example.com,10,600,邮件交换
MX,@,Default,mx1.qiye.aliyun.com,5,600,
```

> 📝 **注意**：NS记录已自动跳过，解析线路和状态列被忽略，因为DNSPOD不需要这些信息。

### 命令行用法

```bash
# 基本用法
python dns_converter.py 华为云DNS文件.xlsx

# 指定输出文件
python dns_converter.py 华为云DNS文件.xlsx -o 我的DNSPOD模板.xlsx
```

## 📋 支持的文件格式

### 华为云DNS导出格式
| 华为云列名 | 标准列名 | 说明 |
|-----------|---------|------|
| 类型/Type/type | Type | DNS记录类型（A、CNAME、MX等） |
| 主机记录/Host/host/域名 | Host | 主机记录名称 |
| 记录值/Value/value/值/IP | Value | 记录值（支持多IP） |
| TTL/ttl/TTL值 | TTL | 生存时间（秒） |
| MX/mx/优先级/Priority | MX | MX记录优先级 |
| 备注/Remarks/remarks/说明 | Remarks | 备注信息 |

### 阿里云DNS导出格式
| 阿里云列名 | 标准列名 | 说明 |
|-----------|---------|------|
| 记录类型 | Type | DNS记录类型（A、CNAME、MX等） |
| 主机记录 | Host | 主机记录名称 |
| 记录值 | Value | 记录值 |
| TTL值 | TTL | 生存时间（秒） |
| MX优先级 | MX | MX记录优先级 |
| 解析线路 | Line | 解析线路（忽略） |
| 状态(启用/暂停) | Status | 记录状态（忽略） |

### 输出格式
生成标准的DNSPOD导入模板，包含以下列：

| 列名 | 位置 | 说明 |
|------|------|------|
| Type | A列 | 记录类型 |
| Host | B列 | 主机记录（已清理域名） |
| Split Zone | C列 | 分区（默认Default） |
| Value | D列 | 记录值（已清理引号） |
| MX | E列 | MX优先级（非MX记录显示"-"） |
| TTL | F列 | 生存时间 |
| Remarks | G列 | 备注信息 |

## ❓ 常见问题

### Q: 支持哪些云服务商的DNS格式？
A: 目前支持华为云和阿里云DNS格式，工具会自动识别并转换。**NS记录会被自动跳过**，因为DNSPOD的NS记录由服务商管理。

### Q: 支持哪些DNS记录类型？
A: 支持常见类型：A、AAAA、CNAME、MX、TXT、SRV、PTR等。

### Q: 如何区分华为云和阿里云格式？
A: 工具会自动检测：
- 阿里云：检测到"解析线路"列时识别为阿里云格式
- 华为云：检测到"备注"列时识别为华为云格式
- 默认：未明确识别时按华为云格式处理

### Q: 文件格式不识别怎么办？
A: 工具支持中英文列名，如果仍有问题，请检查：
- 文件是否为Excel格式（.xlsx, .xls）
- 第一行是否为列标题
- 列名是否包含"类型"、"主机记录"、"记录值"等关键字

### Q: 转换后的文件可以直接导入DNSPOD吗？
A: 是的！转换后的文件完全符合DNSPOD导入格式，可以直接使用。

### Q: 为什么NS记录没有被转换？
A: 这是正常的！DNSPOD的NS记录由服务商自动管理，不需要手动导入。工具会自动跳过所有NS记录并在日志中提示。

### Q: 阿里云的解析线路和状态信息会转换吗？
A: 不会。DNSPOD不需要解析线路和状态信息，工具会自动忽略这些列，只转换DNS记录的核心信息。

### Q: 如何处理转换错误？
A: 工具会显示详细的错误信息和日志，请根据提示检查源文件格式。

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

### 开发环境设置
```bash
git clone https://github.com/carryh/huawei-dns-to-dnspod.git
cd huawei-dns-to-dnspod
pip install -r requirements.txt
```

### 提交规范
- 提交前请确保代码通过测试
- 遵循PEP 8代码规范
- 提交信息使用中文或英文均可

## 📄 许可证

本项目采用 [MIT 许可证](LICENSE)。

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者！

## 📞 支持

如果您遇到问题或有建议，请：
1. 查看 [常见问题](#-常见问题)
2. 搜索现有的 [Issues](../../issues)
3. 创建新的 [Issue](../../issues/new)

---

⭐ 如果这个工具对您有帮助，请给个Star支持一下！
