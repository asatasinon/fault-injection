#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import yaml
import subprocess
import sys
import os


def update_yaml_file(service, pod_count):
    """修改YAML文件中的app和count值"""
    yaml_file_path = "/data/datadog/chaos/usage/network_drop.yaml"
    
    try:
        # 读取YAML文件
        with open(yaml_file_path, 'r') as file:
            data = yaml.safe_load(file)
        
        # 更新值
        data['spec']['selector']['app'] = service
        data['spec']['count'] = pod_count
        
        # 写回YAML文件
        with open(yaml_file_path, 'w') as file:
            yaml.dump(data, file, default_flow_style=False, sort_keys=False)
        
        print(f"YAML file updated successfully: {yaml_file_path}")
        return True
    
    except Exception as e:
        print(f"Error updating YAML file: {str(e)}")
        return False


def apply_yaml():
    """使用kubectl应用YAML文件"""
    yaml_file_path = "/data/datadog/chaos/usage/network_drop.yaml"
    
    try:
        # 检查文件是否存在
        if not os.path.exists(yaml_file_path):
            print(f"Error: YAML file not found: {yaml_file_path}")
            return False
        
        # 执行kubectl命令
        command = ["kubectl", "apply", "-f", yaml_file_path]
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"YAML file applied successfully: {result.stdout}")
            return True
        else:
            print(f"Failed to apply YAML file: {result.stderr}")
            return False
    
    except Exception as e:
        print(f"Error executing kubectl command: {str(e)}")
        return False


def main():
    """主函数"""
    # 创建参数解析器
    parser = argparse.ArgumentParser(description='Network fault injection tool')
    parser.add_argument('--service', type=str, required=True, 
                        help='Target application name')
    parser.add_argument('--pod_count', type=int, required=True, 
                        help='Number of pods to inject fault')
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 修改YAML文件
    if update_yaml_file(args.service, args.pod_count):
        # 应用YAML文件
        if apply_yaml():
            print("Fault injection task submitted successfully")
            return 0
    
    print("Fault injection task submission failed")
    return 1


if __name__ == "__main__":
    sys.exit(main()) 