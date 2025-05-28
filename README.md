# 故障注入工具集

这个项目包含一系列用于Kubernetes环境中进行故障注入测试的工具。

## 环境安装

### 安装uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 安装依赖

```bash
uv sync
```

## 网络故障注入脚本

`scripts/network_fault_injector.py` 是一个用于注入网络故障的Python脚本，基于Datadog的chaos工具。

### 功能

- 修改YAML配置文件中的应用名称和故障注入数量
- 自动应用配置并执行故障注入
- 提供详细的执行状态和错误信息
- 支持停止故障注入

### 使用方法

```bash
# 启动故障注入，更新配置并应用
./scripts/network_fault_injector.py --service <应用名称> --pod_count <数量>

# 使用短参数
./scripts/network_fault_injector.py -s <应用名称> -p <数量>

# 直接应用现有配置，不更新参数
./scripts/network_fault_injector.py

# 停止故障注入
./scripts/network_fault_injector.py --stop
```

### 参数说明

- `-s, --service`: 要注入故障的应用名称（可选，提供时会更新YAML文件）
- `-p, --pod_count`: 故障注入的Pod数量（可选，提供时会更新YAML文件）
- `--stop`: 停止故障注入（与--service参数互斥）

### 示例

```bash
# 示例1：对ts-order-service应用注入网络故障，影响3个Pod
./scripts/network_fault_injector.py --service ts-order-service --pod_count 3

# 使用短参数形式
./scripts/network_fault_injector.py -s ts-order-service -p 3

# 输出示例
YAML file updated successfully: /data/datadog/chaos/usage/network_drop.yaml
YAML file applied successfully: disruption.chaos.datadoghq.com/network-drop configured
Fault injection task submitted successfully

# 示例2：仅更新应用名称，保留其他配置
./scripts/network_fault_injector.py -s ts-payment-service

# 示例3：仅更新Pod数量，保留其他配置
./scripts/network_fault_injector.py -p 5

# 示例4：直接应用现有配置，不更新任何参数
./scripts/network_fault_injector.py

# 示例5：停止故障注入
./scripts/network_fault_injector.py --stop

# 输出示例
Fault injection stopped successfully: disruption.chaos.datadoghq.com "network-drop" deleted
Fault injection stopped successfully
```

### 依赖项

- Python 3
- PyYAML
- kubectl 命令行工具

### 安装依赖

```bash
pip install pyyaml
```
