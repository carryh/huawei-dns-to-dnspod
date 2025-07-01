#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
华为云DNS记录转换为DNSPOD格式的工具

这个工具可以将华为云的DNS记录Excel文件转换为DNSPOD格式的模板文件，
解决两个平台DNS记录格式不兼容的问题。

主要功能：
- 智能Host记录清理（移除域名部分）
- TXT记录值引号自动清理
- MX字段格式修正（非MX记录显示"-"）
- 多IP地址自动拆分
- 支持所有常见DNS记录类型

作者: DNS转换工具开发团队
许可证: MIT License
版本: 1.0.0
"""

import pandas as pd
import argparse
import sys
import os
from typing import List, Dict, Any
import re


class DNSConverter:
    """DNS记录转换器"""
    
    def __init__(self):
        # 华为云到DNSPOD的记录类型映射
        self.type_mapping = {
            'A': 'A',
            'AAAA': 'AAAA', 
            'CNAME': 'CNAME',
            'MX': 'MX',
            'TXT': 'TXT',
            'NS': 'NS',
            'SRV': 'SRV',
            'PTR': 'PTR'
        }
        
        # DNSPOD模板列名（按照正确的DNSPOD格式）
        self.dnspod_columns = [
            'Type',        # A列：记录类型
            'Host',        # B列：主机记录
            'Split Zone',  # C列：分区
            'Value',       # D列：记录值
            'MX',          # E列：MX优先级
            'TTL',         # F列：TTL值
            'Remarks'      # G列：备注
        ]
    
    def read_dns_file(self, file_path: str) -> pd.DataFrame:
        """读取DNS记录文件（支持华为云和阿里云格式）"""
        try:
            # 尝试读取Excel文件，支持多种格式
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path, encoding='utf-8-sig')
            else:
                df = pd.read_excel(file_path)

            print(f"成功读取DNS文件: {file_path}")
            print(f"共读取到 {len(df)} 条记录")

            # 显示列名以便调试
            print(f"检测到的列名: {list(df.columns)}")

            # 检测云服务商类型
            cloud_provider = self.detect_cloud_provider(df)
            print(f"检测到云服务商: {cloud_provider}")

            # 标准化列名
            df = self.normalize_column_names(df)

            return df
        except Exception as e:
            print(f"读取DNS文件失败: {e}")
            sys.exit(1)

    def detect_cloud_provider(self, df: pd.DataFrame) -> str:
        """检测云服务商类型"""
        columns = [col.lower() for col in df.columns]

        # 阿里云特征：解析线路列
        if any('解析线路' in col or '线路' in col for col in df.columns):
            return "阿里云"

        # 华为云特征：备注列
        if any('备注' in col or 'remarks' in col.lower() for col in df.columns):
            return "华为云"

        # 默认按华为云处理
        return "华为云"

    def normalize_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """标准化列名，支持中英文混合"""
        column_mapping = {
            # 记录类型 (华为云 + 阿里云)
            '类型': 'Type', 'type': 'Type', 'Type': 'Type', '记录类型': 'Type',
            # 主机记录 (华为云 + 阿里云)
            '主机记录': 'Host', 'host': 'Host', 'Host': 'Host', '名称': 'Host',
            'name': 'Host', 'Name': 'Host', '域名': 'Host',
            # 记录值 (华为云 + 阿里云)
            '记录值': 'Value', 'value': 'Value', 'Value': 'Value', '值': 'Value',
            'ip': 'Value', 'IP': 'Value', 'target': 'Value', 'Target': 'Value',
            # TTL (华为云 + 阿里云)
            'TTL': 'TTL', 'ttl': 'TTL', 'TTL值': 'TTL', 'TTL(秒)': 'TTL',
            # MX优先级 (华为云 + 阿里云)
            'MX': 'MX', 'mx': 'MX', '优先级': 'MX', 'priority': 'MX', 'Priority': 'MX',
            'MX优先级': 'MX',
            # 备注 (华为云)
            '备注': 'Remarks', 'remarks': 'Remarks', 'Remarks': 'Remarks',
            'comment': 'Remarks', 'Comment': 'Remarks', '说明': 'Remarks',
            # 阿里云特有列（忽略这些列）
            '解析线路': 'Line', '线路': 'Line',
            '状态(启用/暂停)': 'Status', '状态': 'Status'
        }

        # 重命名列
        df = df.rename(columns=column_mapping)

        print(f"标准化后的列名: {list(df.columns)}")
        return df
    
    def parse_multiple_ips(self, value: str) -> List[str]:
        """解析华为云A记录中的多个IP地址"""
        if pd.isna(value) or not value:
            return []
        
        # 华为云可能用换行符、分号、逗号等分隔多个IP
        # 根据图片显示，看起来是用换行符分隔
        ips = []
        for line in str(value).split('\n'):
            line = line.strip()
            if line and self.is_valid_ip(line):
                ips.append(line)
        
        return ips if ips else [str(value).strip()]
    
    def is_valid_ip(self, ip: str) -> bool:
        """简单的IP地址验证"""
        pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        if re.match(pattern, ip):
            parts = ip.split('.')
            return all(0 <= int(part) <= 255 for part in parts)
        return False
    
    def clean_host_record(self, host: str) -> str:
        """清理主机记录，移除域名部分"""
        if not host or pd.isna(host) or host == 'nan':
            return '@'

        host = str(host).strip()

        # 如果是根域名标识
        if host == '@' or host == '':
            return '@'

        # 移除末尾的点号
        if host.endswith('.'):
            host = host[:-1]

        # 检查是否包含域名，需要提取子域名部分
        # 常见的域名模式：www.example.com, mail.example.com, example.com
        if '.' in host:
            parts = host.split('.')

            # 如果只有两个部分，可能是 example.com 格式，应该转为 @
            if len(parts) == 2:
                # 检查是否是常见的顶级域名格式
                tld_patterns = ['.com', '.cn', '.net', '.org', '.cc', '.co']
                if any(host.endswith(pattern) for pattern in tld_patterns):
                    return '@'

            # 如果有三个或更多部分，取第一个作为子域名
            elif len(parts) >= 3:
                return parts[0]

        # 如果没有点号，直接返回（可能已经是正确的子域名）
        return host

    def clean_record_value(self, value: str, record_type: str) -> str:
        """清理记录值，移除不必要的引号和格式化"""
        if not value:
            return value

        value = str(value).strip()

        # 对于TXT记录，移除首尾的引号
        if record_type.upper() == 'TXT':
            # 移除首尾的双引号
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            # 移除首尾的单引号
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]

        return value

    def convert_record(self, record: Dict[str, Any]) -> List[Dict[str, Any]]:
        """转换单条DNS记录"""
        converted_records = []

        # 获取基本信息，使用标准化后的列名
        record_type = str(record.get('Type', '')).upper().strip()
        host = str(record.get('Host', '')).strip()
        value = record.get('Value', '')
        ttl = record.get('TTL', 600)
        mx_priority = record.get('MX', '')
        remarks = record.get('Remarks', '')

        # 跳过空记录
        if not record_type or pd.isna(record_type) or record_type == 'NAN':
            return converted_records

        # 跳过NS记录（DNSPOD不需要导入NS记录，由服务商自动管理）
        if record_type == 'NS':
            print(f"跳过NS记录: {host} -> {value} (DNSPOD不需要导入NS记录)")
            return converted_records

        # 清理主机记录，移除域名部分
        host = self.clean_host_record(host)

        # 处理TTL
        try:
            ttl = int(float(ttl)) if ttl and not pd.isna(ttl) else 600
        except (ValueError, TypeError):
            ttl = 600

        # 处理记录值
        if pd.isna(value) or value == '':
            print(f"警告: {record_type} 记录 {host} 的值为空，跳过")
            return converted_records

        # 清理记录值（移除不必要的引号）
        value = self.clean_record_value(str(value), record_type)

        # 处理备注
        remarks = str(remarks) if remarks and not pd.isna(remarks) else ''
        
        # 根据记录类型处理
        if record_type == 'A':
            # A记录可能包含多个IP地址
            ips = self.parse_multiple_ips(value)
            for ip in ips:
                converted_record = {
                    'Type': 'A',
                    'Host': host,
                    'Split Zone': 'Default',
                    'Value': ip,
                    'MX': '-',
                    'TTL': ttl,
                    'Remarks': remarks
                }
                converted_records.append(converted_record)

        elif record_type == 'MX':
            # MX记录需要处理优先级
            converted_record = {
                'Type': 'MX',
                'Host': host,
                'Split Zone': 'Default',
                'Value': str(value) if value and not pd.isna(value) else '',
                'MX': str(mx_priority) if mx_priority and not pd.isna(mx_priority) else '',
                'TTL': ttl,
                'Remarks': remarks
            }
            converted_records.append(converted_record)

        else:
            # 其他记录类型直接转换
            if record_type in self.type_mapping:
                converted_record = {
                    'Type': self.type_mapping[record_type],
                    'Host': host,
                    'Split Zone': 'Default',
                    'Value': str(value) if value and not pd.isna(value) else '',
                    'MX': '-',
                    'TTL': ttl,
                    'Remarks': remarks
                }
                converted_records.append(converted_record)
        
        return converted_records
    
    def convert_dns_records(self, huawei_df: pd.DataFrame) -> pd.DataFrame:
        """转换所有DNS记录"""
        all_converted_records = []
        
        print("开始转换DNS记录...")
        
        for index, record in huawei_df.iterrows():
            try:
                converted_records = self.convert_record(record.to_dict())
                all_converted_records.extend(converted_records)
                
                # 显示转换进度
                if (index + 1) % 10 == 0:
                    print(f"已处理 {index + 1}/{len(huawei_df)} 条记录")
                    
            except Exception as e:
                print(f"转换第 {index + 1} 条记录时出错: {e}")
                continue
        
        # 创建DNSPOD格式的DataFrame
        dnspod_df = pd.DataFrame(all_converted_records, columns=self.dnspod_columns)
        
        print(f"转换完成！华为云 {len(huawei_df)} 条记录转换为DNSPOD {len(dnspod_df)} 条记录")
        
        return dnspod_df
    
    def save_dnspod_template(self, dnspod_df: pd.DataFrame, output_path: str):
        """保存DNSPOD模板文件"""
        try:
            dnspod_df.to_excel(output_path, index=False)
            print(f"DNSPOD模板已保存到: {output_path}")
        except Exception as e:
            print(f"保存DNSPOD模板失败: {e}")
            sys.exit(1)
    
    def print_conversion_summary(self, dnspod_df: pd.DataFrame):
        """打印转换摘要"""
        print("\n=== 转换摘要 ===")
        record_counts = dnspod_df['Type'].value_counts()
        for record_type, count in record_counts.items():
            print(f"{record_type} 记录: {count} 条")

        print(f"\n总计: {len(dnspod_df)} 条DNS记录")


def main():
    parser = argparse.ArgumentParser(description='华为云/阿里云DNS记录转换为DNSPOD格式')
    parser.add_argument('input_file', help='DNS Excel文件路径（支持华为云和阿里云格式）')
    parser.add_argument('-o', '--output', help='输出的DNSPOD模板文件路径',
                       default='dnspod_template.xlsx')

    args = parser.parse_args()

    # 检查输入文件是否存在
    if not os.path.exists(args.input_file):
        print(f"错误: 输入文件不存在: {args.input_file}")
        sys.exit(1)

    # 创建转换器并执行转换
    converter = DNSConverter()

    # 读取DNS文件（自动检测华为云或阿里云格式）
    dns_df = converter.read_dns_file(args.input_file)

    # 转换为DNSPOD格式
    dnspod_df = converter.convert_dns_records(dns_df)

    # 保存DNSPOD模板
    converter.save_dnspod_template(dnspod_df, args.output)

    # 打印转换摘要
    converter.print_conversion_summary(dnspod_df)


if __name__ == '__main__':
    main()
