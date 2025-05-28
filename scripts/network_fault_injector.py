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


def delete_yaml():
    """删除应用的YAML配置"""
    yaml_file_path = "/data/datadog/chaos/usage/network_drop.yaml"
    
    try:
        # 检查文件是否存在
        if not os.path.exists(yaml_file_path):
            print(f"Error: YAML file not found: {yaml_file_path}")
            return False
        
        # 执行kubectl delete命令
        command = ["kubectl", "delete", "-f", yaml_file_path]
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"Fault injection stopped successfully: {result.stdout}")
            return True
        else:
            print(f"Failed to stop fault injection: {result.stderr}")
            return False
    
    except Exception as e:
        print(f"Error executing kubectl command: {str(e)}")
        return False


def main():
    """主函数"""
    # 创建参数解析器
    parser = argparse.ArgumentParser(
        description='Network fault injection tool'
    )
    
    # 添加互斥参数组
    group = parser.add_mutually_exclusive_group(required=True)
    
    # 启动故障注入的参数
    group.add_argument('--service', type=str, 
                      help='Target application name')
    parser.add_argument('--pod_count', type=int,
                      help='Number of pods to inject fault')
    
    # 停止故障注入的参数
    group.add_argument('--stop', action='store_true',
                      help='Stop the fault injection')
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 如果是停止故障注入
    if args.stop:
        if delete_yaml():
            print("Fault injection stopped successfully")
            return 0
        print("Failed to stop fault injection")
        return 1
    
    # 否则执行故障注入
    if not args.pod_count:
        parser.error("--pod_count is required when --service is specified")
    
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