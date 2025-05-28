#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import yaml
import subprocess
import sys
import os


def update_yaml_file(app, count):
    """修改YAML文件中的app和count值"""
    yaml_file_path = "/data/datadog/chaos/usage/network_drop.yaml"
    
    try:
        # 读取YAML文件
        with open(yaml_file_path, 'r') as file:
            data = yaml.safe_load(file)
        
        # 更新值
        data['spec']['selector']['app'] = app
        data['spec']['count'] = count
        
        # 写回YAML文件
        with open(yaml_file_path, 'w') as file:
            yaml.dump(data, file, default_flow_style=False, sort_keys=False)
        
        print(f"成功更新YAML文件: {yaml_file_path}")
        return True
    
    except Exception as e:
        print(f"更新YAML文件时出错: {str(e)}")
        return False


def apply_yaml():
    """使用kubectl应用YAML文件"""
    yaml_file_path = "/data/datadog/chaos/usage/network_drop.yaml"
    
    try:
        # 检查文件是否存在
        if not os.path.exists(yaml_file_path):
            print(f"错误: 找不到YAML文件: {yaml_file_path}")
            return False
        
        # 执行kubectl命令
        command = ["kubectl", "apply", "-f", yaml_file_path]
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"成功应用YAML文件: {result.stdout}")
            return True
        else:
            print(f"应用YAML文件失败: {result.stderr}")
            return False
    
    except Exception as e:
        print(f"执行kubectl命令时出错: {str(e)}")
        return False


def main():
    """主函数"""
    # 创建参数解析器
    parser = argparse.ArgumentParser(description='修改网络故障注入YAML并应用')
    parser.add_argument('--app', type=str, required=True, help='要注入故障的应用名称')
    parser.add_argument('--count', type=int, required=True, help='故障注入的Pod数量')
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 修改YAML文件
    if update_yaml_file(args.app, args.count):
        # 应用YAML文件
        if apply_yaml():
            print("故障注入任务成功提交")
            return 0
    
    print("故障注入任务提交失败")
    return 1


if __name__ == "__main__":
    sys.exit(main()) 