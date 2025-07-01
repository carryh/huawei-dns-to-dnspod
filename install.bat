@echo off
chcp 65001 >nul
echo ========================================
echo 华为云DNS转DNSPOD工具 - 安装脚本
echo ========================================
echo.

REM 检查Python是否安装
echo 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python
    echo 请先安装Python 3.7或更高版本
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

python --version
echo Python环境检查通过
echo.

REM 升级pip
echo 升级pip...
python -m pip install --upgrade pip

REM 安装依赖包
echo 安装依赖包...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo 依赖包安装失败，尝试使用国内镜像源...
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
    
    if errorlevel 1 (
        echo 依赖包安装失败！
        echo 请检查网络连接或手动安装：
        echo pip install pandas openpyxl
        pause
        exit /b 1
    )
)

echo.
echo ========================================
echo 安装完成！
echo ========================================
echo.
echo 使用方法：
echo 1. 图形界面：双击运行 dns_converter_gui.py
echo 2. 命令行：python dns_converter.py 输入文件.xlsx
echo 3. 批处理：双击 convert_dns.bat 然后拖拽文件
echo.
echo 测试安装：
echo python test_converter.py
echo.
pause
