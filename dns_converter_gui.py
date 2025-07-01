#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
华为云DNS转DNSPOD工具 - 图形界面版本

这是华为云DNS转DNSPOD工具的图形界面版本，提供友好的用户界面，
让非技术用户也能轻松完成DNS记录格式转换。

功能特点：
- 简洁直观的图形界面
- 文件拖拽支持
- 实时转换进度显示
- 详细的转换日志
- 自动打开输出目录

使用方法：
1. 运行程序：python dns_converter_gui.py
2. 选择华为云或阿里云DNS Excel文件
3. 点击"开始转换"按钮
4. 等待转换完成

作者: DNS转换工具开发团队
许可证: MIT License
版本: 1.0.0
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import os
from dns_converter import DNSConverter


class DNSConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("华为云/阿里云DNS转DNSPOD工具")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # 设置样式
        style = ttk.Style()
        style.theme_use('clam')
        
        self.converter = DNSConverter()
        self.input_file = ""
        self.output_file = ""
        
        self.create_widgets()
    
    def create_widgets(self):
        """创建GUI组件"""
        
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 标题
        title_label = ttk.Label(main_frame, text="华为云/阿里云DNS转DNSPOD工具",
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # 输入文件选择
        ttk.Label(main_frame, text="DNS文件:").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.input_file_var = tk.StringVar()
        input_entry = ttk.Entry(main_frame, textvariable=self.input_file_var, width=50)
        input_entry.grid(row=1, column=1, padx=(10, 5), pady=5, sticky=(tk.W, tk.E))
        
        input_button = ttk.Button(main_frame, text="浏览", command=self.select_input_file)
        input_button.grid(row=1, column=2, padx=(5, 0), pady=5)
        
        # 输出文件选择
        ttk.Label(main_frame, text="DNSPOD模板文件:").grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.output_file_var = tk.StringVar()
        output_entry = ttk.Entry(main_frame, textvariable=self.output_file_var, width=50)
        output_entry.grid(row=2, column=1, padx=(10, 5), pady=5, sticky=(tk.W, tk.E))
        
        output_button = ttk.Button(main_frame, text="浏览", command=self.select_output_file)
        output_button.grid(row=2, column=2, padx=(5, 0), pady=5)
        
        # 转换按钮
        convert_frame = ttk.Frame(main_frame)
        convert_frame.grid(row=3, column=0, columnspan=3, pady=20)
        
        self.convert_button = ttk.Button(convert_frame, text="开始转换", 
                                        command=self.start_conversion, style="Accent.TButton")
        self.convert_button.pack(side=tk.LEFT, padx=5)
        
        self.clear_button = ttk.Button(convert_frame, text="清空", command=self.clear_fields)
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, 
                                           mode='indeterminate')
        self.progress_bar.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # 状态标签
        self.status_var = tk.StringVar(value="请选择DNS文件（支持华为云和阿里云格式）")
        status_label = ttk.Label(main_frame, textvariable=self.status_var)
        status_label.grid(row=5, column=0, columnspan=3, pady=5)
        
        # 日志文本框
        log_frame = ttk.LabelFrame(main_frame, text="转换日志", padding="5")
        log_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # 创建文本框和滚动条
        self.log_text = tk.Text(log_frame, height=15, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(6, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
    
    def select_input_file(self):
        """选择输入文件"""
        file_path = filedialog.askopenfilename(
            title="选择DNS文件（华为云或阿里云格式）",
            filetypes=[
                ("Excel文件", "*.xlsx *.xls"),
                ("CSV文件", "*.csv"),
                ("所有文件", "*.*")
            ]
        )
        
        if file_path:
            self.input_file_var.set(file_path)
            self.input_file = file_path
            
            # 自动生成输出文件名
            if not self.output_file_var.get():
                base_name = os.path.splitext(file_path)[0]
                output_path = f"{base_name}_dnspod.xlsx"
                self.output_file_var.set(output_path)
                self.output_file = output_path
            
            self.status_var.set("已选择输入文件，点击开始转换")
    
    def select_output_file(self):
        """选择输出文件"""
        file_path = filedialog.asksaveasfilename(
            title="保存DNSPOD模板文件",
            defaultextension=".xlsx",
            filetypes=[
                ("Excel文件", "*.xlsx"),
                ("所有文件", "*.*")
            ]
        )
        
        if file_path:
            self.output_file_var.set(file_path)
            self.output_file = file_path
    
    def clear_fields(self):
        """清空所有字段"""
        self.input_file_var.set("")
        self.output_file_var.set("")
        self.input_file = ""
        self.output_file = ""
        self.log_text.delete(1.0, tk.END)
        self.status_var.set("请选择DNS文件（支持华为云和阿里云格式）")
    
    def log_message(self, message):
        """添加日志消息"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def start_conversion(self):
        """开始转换（在新线程中执行）"""
        if not self.input_file:
            messagebox.showerror("错误", "请先选择DNS文件")
            return
        
        if not self.output_file:
            messagebox.showerror("错误", "请先选择输出文件路径")
            return
        
        # 禁用转换按钮
        self.convert_button.config(state='disabled')
        self.progress_bar.start()
        self.status_var.set("正在转换...")
        
        # 清空日志
        self.log_text.delete(1.0, tk.END)
        
        # 在新线程中执行转换
        thread = threading.Thread(target=self.perform_conversion)
        thread.daemon = True
        thread.start()
    
    def perform_conversion(self):
        """执行实际的转换工作"""
        try:
            self.log_message("开始转换DNS记录...")
            
            # 读取DNS文件（自动检测华为云或阿里云格式）
            self.log_message(f"读取文件: {self.input_file}")
            dns_df = self.converter.read_dns_file(self.input_file)
            self.log_message(f"成功读取 {len(dns_df)} 条记录")
            
            # 转换为DNSPOD格式
            self.log_message("转换为DNSPOD格式...")
            dnspod_df = self.converter.convert_dns_records(dns_df)
            self.log_message(f"转换完成，共 {len(dnspod_df)} 条DNSPOD记录")
            
            # 保存DNSPOD模板
            self.log_message(f"保存到: {self.output_file}")
            self.converter.save_dnspod_template(dnspod_df, self.output_file)
            
            # 显示转换摘要
            self.log_message("\n=== 转换摘要 ===")
            record_counts = dnspod_df['Type'].value_counts()
            for record_type, count in record_counts.items():
                self.log_message(f"{record_type} 记录: {count} 条")
            
            self.log_message(f"\n总计: {len(dnspod_df)} 条DNS记录")
            self.log_message("\n转换成功完成！")
            
            # 更新UI
            self.root.after(0, self.conversion_completed, True)
            
        except Exception as e:
            error_msg = f"转换失败: {str(e)}"
            self.log_message(error_msg)
            self.root.after(0, self.conversion_completed, False, error_msg)
    
    def conversion_completed(self, success, error_msg=None):
        """转换完成后的UI更新"""
        self.progress_bar.stop()
        self.convert_button.config(state='normal')
        
        if success:
            self.status_var.set("转换成功完成！")
            messagebox.showinfo("成功", f"DNS记录转换成功！\n输出文件: {self.output_file}")
        else:
            self.status_var.set("转换失败")
            messagebox.showerror("错误", error_msg or "转换过程中发生未知错误")


def main():
    """主函数"""
    try:
        # 检查依赖
        import pandas
        import openpyxl
    except ImportError as e:
        messagebox.showerror("依赖错误", 
                           f"缺少必要的依赖包: {e}\n\n请运行以下命令安装:\npip install pandas openpyxl")
        return
    
    root = tk.Tk()
    app = DNSConverterGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
