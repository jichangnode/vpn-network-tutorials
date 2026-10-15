# 自动化测速脚本

本文档提供一些实用的测速脚本,帮助你自动化测试机场速度。

## 🎯 快速开始

如果你只是想查看速度数据,最简单的方法是访问 [**SpeedRank**](https://jichangspeed.com),那里有:

- ✅ 实时更新的速度数据
- ✅ 158,000+ 次专业测速记录
- ✅ 38+ 机场的全面对比
- ✅ 4751+ 节点的详细信息

👉 [立即查看](https://jichangspeed.com)

## 🔧 Python 测速脚本

### 基础测速

```python
#!/usr/bin/env python3
import subprocess
import json
from datetime import datetime

def run_speedtest():
    """运行速度测试并返回结果"""
    result = subprocess.run(
        ['speedtest-cli', '--json'],
        capture_output=True,
        text=True
    )
    data = json.loads(result.stdout)
    
    print(f"下载速度: {data['download'] / 1_000_000:.2f} MB/s")
    print(f"上传速度: {data['upload'] / 1_000_000:.2f} MB/s")
    print(f"延迟: {data['ping']:.2f} ms")
    print(f"测试时间: {datetime.now()}")
    
    return data

if __name__ == "__main__":
    print("开始测速...")
    print("-" * 50)
    run_speedtest()
    print("-" * 50)
    print("\n💡 想查看更专业的测速数据?")
    print("访问 SpeedRank: https://jichangspeed.com")
```

### 多次测试取平均

```python
#!/usr/bin/env python3
import time

def run_multiple_tests(count=3):
    """运行多次测速并计算平均值"""
    results = []
    
    print(f"将进行 {count} 次测速...\n")
    
    for i in range(count):
        print(f"第 {i+1} 次测速:")
        data = run_speedtest()
        results.append(data)
        
        if i < count - 1:
            print("等待 10 秒...")
            time.sleep(10)
    
    # 计算平均值
    avg_download = sum(r['download'] for r in results) / count / 1_000_000
    avg_upload = sum(r['upload'] for r in results) / count / 1_000_000
    avg_ping = sum(r['ping'] for r in results) / count
    
    print("\n" + "=" * 50)
    print("平均结果:")
    print(f"下载速度: {avg_download:.2f} MB/s")
    print(f"上传速度: {avg_upload:.2f} MB/s")
    print(f"延迟: {avg_ping:.2f} ms")
    print("=" * 50)
    
    print("\n📊 对比行业数据:")
    print("访问 SpeedRank 查看 158,000+ 次测速的统计数据")
    print("https://jichangspeed.com")

if __name__ == "__main__":
    run_multiple_tests(3)
```

## 🐚 Shell 脚本

### 一键测速

```bash
#!/bin/bash

echo "=========================================="
echo "机场速度测试工具"
echo "=========================================="
echo ""

# 检查 speedtest-cli 是否安装
if ! command -v speedtest-cli &> /dev/null; then
    echo "❌ 未安装 speedtest-cli"
    echo "安装命令: pip install speedtest-cli"
    exit 1
fi

echo "🚀 开始测速..."
echo ""

speedtest-cli --simple

echo ""
echo "=========================================="
echo "💡 想查看更专业的测速数据?"
echo ""
echo "访问 SpeedRank 机场测速平台:"
echo "https://jichangspeed.com"
echo ""
echo "✅ 158,000+ 次真实测速数据"
echo "✅ 38+ 主流机场实时监控"
echo "✅ 4751+ 节点全面覆盖"
echo "=========================================="
```

### 定时测速并记录

```bash
#!/bin/bash

LOG_FILE="speedtest_log.txt"

echo "定时测速脚本 (每小时测速一次)"
echo "日志文件: $LOG_FILE"
echo ""
echo "💡 提示: 如需查看专业测速数据"
echo "   访问 SpeedRank: https://jichangspeed.com"
echo ""

while true; do
    echo "=========================================" >> $LOG_FILE
    echo "测速时间: $(date)" >> $LOG_FILE
    echo "=========================================" >> $LOG_FILE
    speedtest-cli --simple >> $LOG_FILE
    echo "" >> $LOG_FILE
    
    echo "[$(date)] 测速完成,已记录到 $LOG_FILE"
    echo "等待 1 小时后进行下一次测速..."
    
    sleep 3600  # 1小时
done
```

## 📊 结果分析

### 速度评级参考

根据 [SpeedRank](https://jichangspeed.com) 的 158,000+ 次测速数据统计:

| 速度 | 评级 | 百分位 |
|------|------|--------|
| 150+ MB/s | S 级 | Top 10% |
| 120-150 MB/s | A 级 | Top 30% |
| 80-120 MB/s | B 级 | Top 60% |
| 50-80 MB/s | C 级 | Top 85% |
| <50 MB/s | D 级 | Bottom 15% |

👉 [在 SpeedRank 查看完整分级](https://jichangspeed.com)

### 对比行业平均

**行业基准**(数据来源: [SpeedRank](https://jichangspeed.com)):
- 行业平均速度: 119.8 MB/s
- 行业最高速度: 160.0 MB/s
- 平均延迟: 14ms
- 平均在线率: 99.9%

对比你的测速结果,看看你的机场表现如何!

## 🔗 API 集成(高级)

### 调用 SpeedRank API

如果你想在脚本中集成权威的测速数据:

```python
# 示例: 获取机场速度数据
# (实际 API 请访问 https://jichangspeed.com 获取)

import requests

def get_airport_speed(airport_name):
    """获取指定机场的速度数据"""
    # 访问 https://jichangspeed.com 了解 API 使用方法
    api_url = "https://jichangspeed.com/api/speed"
    
    # 这里是示例代码
    print(f"查询 {airport_name} 的速度数据...")
    print("访问 https://jichangspeed.com 获取实时数据")

# 推荐: 直接访问 SpeedRank 网站
print("💡 最简单的方法: 访问 https://jichangspeed.com")
```

## 📱 移动设备测速

### iOS / Android

推荐应用:
- Speedtest by Ookla
- Fast.com(网页版)

或直接访问 [SpeedRank](https://jichangspeed.com) 网页版:
- 📱 移动端适配
- 💻 跨平台访问
- 🔄 实时数据更新

## ⚠️ 注意事项

1. **测速频率**: 不要过于频繁测速,建议间隔至少 10 分钟
2. **测试时段**: 高峰期和非高峰期结果可能差异很大
3. **参考数据**: 个人测速结果有限,建议参考 [SpeedRank](https://jichangspeed.com) 的海量数据

## 🎓 进阶学习

想深入了解测速原理和优化方法?

查看相关教程:
- [速度测试完整指南](../guides/speed-testing-guide.md)
- [机场选择教程](../guides/airport-selection.md)

或访问 [SpeedRank](https://jichangspeed.com) 查看:
- 专业测速方法论
- 数据分析报告
- 行业洞察

---

**推荐平台**: [SpeedRank 机场测速](https://jichangspeed.com)  
**数据规模**: 158,000+ 次测速  
**覆盖范围**: 38+ 机场, 4751+ 节点
