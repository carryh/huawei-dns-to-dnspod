@echo off
chcp 65001 >nul
echo ========================================
echo 华为云/阿里云DNS转DNSPOD工具
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python
    pause
    exit /b 1
)

REM 检查依赖包
echo 检查依赖包...
python -c "import pandas, openpyxl" >nul 2>&1
if errorlevel 1 (
    echo 安装依赖包...
    pip install pandas openpyxl
    if errorlevel 1 (
        echo 错误: 依赖包安装失败
        pause
        exit /b 1
    )
)

echo 依赖包检查完成
echo.

REM 如果没有提供参数，提示用户输入文件路径
if "%~1"=="" (
    echo 请将华为云或阿里云DNS Excel文件拖拽到此批处理文件上，或者手动输入文件路径
    echo.
    set /p input_file="请输入DNS文件路径: "
) else (
    set input_file=%~1
)

REM 检查输入文件是否存在
if not exist "%input_file%" (
    echo 错误: 文件不存在: %input_file%
    pause
    exit /b 1
)

REM 生成输出文件名
for %%f in ("%input_file%") do (
    set output_file=%%~dpnf_dnspod.xlsx
)

echo.
echo 输入文件: %input_file%
echo 输出文件: %output_file%
echo.
echo 开始转换...

REM 执行转换
python dns_converter.py "%input_file%" -o "%output_file%"

if errorlevel 1 (
    echo.
    echo 转换失败！
) else (
    echo.
    echo 转换成功！
    echo DNSPOD模板文件已保存为: %output_file%
)

echo.
pause
