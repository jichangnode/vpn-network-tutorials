# 网络加速与速度优化完全指南

## 概述

本指南提供系统的网络加速优化方案,涵盖协议选择、服务器优化、客户端配置等多个层面,帮助你获得最佳的网络速度体验。

## 影响速度的关键因素

### 1. 物理距离

**延迟与距离的关系**:
```
本地 → 香港: 20-50ms
本地 → 新加坡: 50-80ms
本地 → 日本: 80-120ms
本地 → 美国西海岸: 150-200ms
本地 → 欧洲: 200-300ms
```

**优化建议**:
- ✅ 优先选择地理位置近的节点
- ✅ 不同用途使用不同区域节点
- ✅ 利用 CDN 中转降低延迟

### 2. 协议选择

**速度排名** (相同条件下):
1. **WireGuard** - 最快 (UDP 协议)
2. **VLESS** - 接近 WireGuard
3. **Trojan** - 优秀的速度和隐蔽性平衡
4. **Shadowsocks** - 轻量快速
5. **V2Ray** - 功能丰富但稍慢
6. **OpenVPN** - 较慢但稳定

详细协议对比见: [协议性能分析](./protocol-comparison.md)

### 3. 加密算法

**性能对比** (速度 vs 安全性):
```
AES-128-GCM: ⭐⭐⭐⭐⭐ (最快,安全性足够)
ChaCha20-Poly1305: ⭐⭐⭐⭐⭐ (移动设备首选)
AES-256-GCM: ⭐⭐⭐⭐ (更安全,略慢)
AES-256-CFB: ⭐⭐⭐ (不推荐,已过时)
```

**推荐配置**:
- 桌面设备: AES-128-GCM (CPU 有 AES-NI)
- 移动设备: ChaCha20-Poly1305 (省电)
- 高安全需求: AES-256-GCM

### 4. 服务器性能

**关键指标**:
- CPU 性能 (影响加密速度)
- 带宽 (上行/下行)
- 内存 (影响并发连接)
- 网络质量 (丢包率)

### 5. 网络线路

**线路等级**:
```
CN2 GIA > CN2 GT > 普通直连 > 普通线路
```

**特点对比**:
- **CN2 GIA**: 速度快,稳定,价格高
- **CN2 GT**: 性价比较好,高峰拥堵
- **普通直连**: 便宜,速度不稳定
- **中转/隧道**: 绕路但可能更快

想了解哪些服务提供优质线路? 访问 [机场测速评测](https://jichangspeed.com/) 查看最新线路质量对比。

## 客户端优化

### Windows 优化

**1. 系统网络优化**:
```powershell
# 提升 TCP 接收窗口
netsh int tcp set global autotuninglevel=normal

# 启用 TCP Fast Open
netsh int tcp set global fastopen=enabled

# 禁用网络限制
netsh int tcp set global congestionprovider=bbr2
```

**2. DNS 优化**:
```
优选 DNS:
- 主: 223.5.5.5 (阿里)
- 备: 119.29.29.29 (腾讯DNS)
- 国际: 1.1.1.1 (Cloudflare)
```

**3. 客户端设置**:

Clash for Windows:
```yaml
# 增加并发连接数
experimental:
  ignore-resolve-fail: true
  interface-name: WLAN

# 开启 TUN 模式
tun:
  enable: true
  stack: system
  dns-hijack:
    - any:53
```

### macOS 优化

**1. 网络调优**:
```bash
# 提升 TCP 缓冲区
sudo sysctl -w net.inet.tcp.sendspace=2097152
sudo sysctl -w net.inet.tcp.recvspace=2097152

# 启用 TCP Fast Open
sudo sysctl -w net.inet.tcp.fastopen=3
```

**2. ClashX 优化**:
```yaml
dns:
  enable: true
  enhanced-mode: fake-ip
  nameserver:
    - 223.5.5.5
    - 119.29.29.29
  fallback:
    - 1.1.1.1
    - 8.8.8.8
```

### iOS 优化

**1. Shadowrocket 设置**:
```
全局路由 → 配置
DNS 设置:
- 服务器: 223.5.5.5,119.29.29.29
- 备用: 1.1.1.1

高级设置:
✓ TCP Fast Open
✓ 重连功能
✓ 包含所有代理
```

**2. Quantumult X 优化**:
```ini
[general]
dns_exclusion_list=*.lan, cable.auth.com
network_check_url=http://www.qualcomm.cn/generate_204

[dns]
server=223.5.5.5
server=119.29.29.29
server=1.1.1.1
```

### Android 优化

**1. 系统设置**:
```
设置 → 开发者选项:
✓ 停用 HW 叠加层
✓ 强制进行 GPU 渲染
✓ 4x MSAA(多重采样抗锯齿)
```

**2. Clash for Android**:
```yaml
# 性能模式
mode: rule
allow-lan: false
bind-address: '*'
log-level: warning

# 开启 IPv6
ipv6: true
```

## 服务器端优化

### TCP 加速算法

**1. BBR (推荐)**:
```bash
# 检查内核版本 (需要 4.9+)
uname -r

# 开启 BBR
echo "net.core.default_qdisc=fq" >> /etc/sysctl.conf
echo "net.ipv4.tcp_congestion_control=bbr" >> /etc/sysctl.conf
sysctl -p

# 验证
sysctl net.ipv4.tcp_congestion_control
lsmod | grep bbr
```

**2. BBR Plus (增强版)**:
```bash
# 下载并安装 BBR Plus 内核
wget -O tcp.sh "https://github.com/cx9208/Linux-NetSpeed/raw/master/tcp.sh"
chmod +x tcp.sh
./tcp.sh
```

**3. 锐速 (商业方案)**:
- 适用于低内核版本
- 效果显著但不开源
- 需要购买授权

### 系统参数优化

**完整优化脚本**:
```bash
#!/bin/bash
# 网络性能优化脚本

cat >> /etc/sysctl.conf << EOF
# TCP 优化
net.ipv4.tcp_fastopen = 3
net.ipv4.tcp_slow_start_after_idle = 0
net.ipv4.tcp_no_metrics_save = 1

# 增加 TCP 缓冲区
net.core.rmem_max = 134217728
net.core.wmem_max = 134217728
net.ipv4.tcp_rmem = 4096 87380 67108864
net.ipv4.tcp_wmem = 4096 65536 67108864

# 连接队列
net.core.netdev_max_backlog = 250000
net.core.somaxconn = 4096

# TIME_WAIT 优化
net.ipv4.tcp_max_tw_buckets = 5000
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_fin_timeout = 30

# MTU 探测
net.ipv4.tcp_mtu_probing = 1

# 拥塞控制
net.core.default_qdisc = fq
net.ipv4.tcp_congestion_control = bbr
EOF

# 应用配置
sysctl -p
```

### 协议优化配置

**V2Ray 优化**:
```json
{
  "inbounds": [{
    "streamSettings": {
      "tcpSettings": {
        "header": {
          "type": "http"
        }
      },
      "sockopt": {
        "tcpFastOpen": true,
        "tproxy": "off"
      }
    }
  }],
  "outbounds": [{
    "streamSettings": {
      "sockopt": {
        "tcpFastOpen": true
      }
    }
  }]
}
```

**Trojan 优化**:
```json
{
  "tcp": {
    "no_delay": true,
    "keep_alive": true,
    "fast_open": true
  }
}
```

## 路由优化策略

### 智能分流

**基础规则**:
```yaml
rules:
  # 直连中国大陆
  - GEOIP,CN,DIRECT
  - DOMAIN-SUFFIX,cn,DIRECT
  
  # 流媒体专线
  - DOMAIN-KEYWORD,youtube,Media
  - DOMAIN-KEYWORD,netflix,Media
  
  # 高速节点访问
  - DOMAIN-SUFFIX,google.com,Fast
  - DOMAIN-SUFFIX,github.com,Fast
  
  # 默认代理
  - MATCH,Proxy
```

**高级分流**:
```yaml
proxy-groups:
  # 自动选择最快节点
  - name: Auto
    type: url-test
    url: http://www.gstatic.com/generate_204
    interval: 300
    tolerance: 50
    
  # 负载均衡
  - name: Balance
    type: load-balance
    strategy: consistent-hashing
    
  # 故障转移
  - name: Fallback
    type: fallback
    url: http://www.gstatic.com/generate_204
    interval: 300
```

### UDP 加速

**适用场景**:
- 游戏加速
- 视频通话
- 实时流媒体

**配置方法**:

V2Ray mKCP:
```json
{
  "streamSettings": {
    "network": "mkcp",
    "kcpSettings": {
      "mtu": 1350,
      "tti": 50,
      "uplinkCapacity": 100,
      "downlinkCapacity": 100,
      "congestion": true,
      "readBufferSize": 2,
      "writeBufferSize": 2
    }
  }
}
```

## 特定场景优化

### 视频流媒体

**优化重点**:
- 选择带宽充足的节点
- 启用 TCP Fast Open
- 使用专用流媒体线路
- 关闭不必要的加密

**推荐配置**:
```yaml
# 流媒体专用节点组
proxy-groups:
  - name: Media
    type: select
    proxies:
      - HK-IPLC  # 香港专线
      - US-Netflix  # 美国 Netflix 专用
      - JP-Media  # 日本流媒体
```

**优质流媒体节点推荐**: 查看 [外网工具评测](https://outsideweb.net/) 的流媒体专项测试。

### 游戏加速

**关键指标**:
- 延迟 < 50ms (理想)
- 丢包率 < 0.5%
- 抖动 < 10ms

**优化方案**:
```yaml
# 游戏专用配置
proxy-groups:
  - name: Game
    type: url-test
    url: http://www.gstatic.com/generate_204
    interval: 60  # 频繁测试
    tolerance: 10  # 低容差
    proxies:
      - JP-Game-01
      - HK-Game-01
      - SG-Game-01

rules:
  # 游戏服务器直连或专线
  - DOMAIN-SUFFIX,steam.com,Game
  - IP-CIDR,1.1.1.1/24,Game
```

**UDP 加速必备**:
- 启用 UDP 转发
- 使用 mKCP 或 QUIC
- 关闭 QoS 限制

### 下载加速

**多线程下载**:
```bash
# aria2 配置
max-connection-per-server=16
min-split-size=10M
split=16
```

**BT/PT 优化**:
```yaml
# 全局模式 or 白名单
rules:
  - DOMAIN-KEYWORD,tracker,DIRECT
  - DOMAIN-SUFFIX,torrent,DIRECT
```

### 办公协作

**Microsoft 365 优化**:
```yaml
rules:
  # Office 服务直连
  - DOMAIN-SUFFIX,office.com,DIRECT
  - DOMAIN-SUFFIX,office365.com,DIRECT
  - DOMAIN-SUFFIX,sharepoint.com,DIRECT
  
  # OneDrive 加速
  - DOMAIN-KEYWORD,onedrive,Proxy
```

**Google Workspace**:
```yaml
rules:
  - DOMAIN-SUFFIX,google.com,Fast
  - DOMAIN-SUFFIX,googleapis.com,Fast
  - DOMAIN-SUFFIX,gstatic.com,Fast
```

## 测速与监控

### 测速工具

**在线测速**:
- Speedtest.net
- Fast.com (Netflix)
- CloudFlare Speed Test

**命令行测速**:
```bash
# speedtest-cli
pip install speedtest-cli
speedtest-cli --proxy socks5://127.0.0.1:1080

# curl 测速
curl -x socks5://127.0.0.1:1080 -o /dev/null https://speed.cloudflare.com/__down?bytes=100000000
```

### 节点监控

**自动化测速脚本**:
```bash
#!/bin/bash
# 批量测试节点延迟

NODES=(
  "https://node1.example.com"
  "https://node2.example.com"
  "https://node3.example.com"
)

for node in "${NODES[@]}"; do
  echo "Testing $node"
  time=$(curl -o /dev/null -s -w '%{time_total}\n' "$node")
  echo "Response time: ${time}s"
done
```

**Clash 内置测速**:
```yaml
# 自动测速并选择最快节点
proxy-groups:
  - name: Auto
    type: url-test
    url: http://www.gstatic.com/generate_204
    interval: 300
```

## 故障排查

### 速度慢的常见原因

**1. 服务器问题**:
- ❌ 服务器负载过高
- ❌ 带宽不足
- ❌ 线路拥堵

**解决方案**: 更换节点

**2. 本地网络问题**:
- ❌ WiFi 信号差
- ❌ ISP 限速
- ❌ 本地带宽不足

**解决方案**: 
- 使用有线连接
- 联系 ISP
- 升级带宽

**3. 配置问题**:
- ❌ 协议选择不当
- ❌ 加密算法过重
- ❌ 分流规则错误

**解决方案**: 优化配置

### 诊断命令

**检查延迟**:
```bash
# Ping 测试
ping -c 10 server.com

# TCP Ping
tcping server.com 443

# HTTP 响应时间
curl -o /dev/null -s -w 'Total: %{time_total}s\n' https://google.com
```

**检查路由**:
```bash
# 路由追踪
traceroute server.com

# MTR 综合测试
mtr -r -c 100 server.com
```

**检查带宽**:
```bash
# iperf3 测试
# 服务端
iperf3 -s

# 客户端
iperf3 -c server.com
```

## 终极优化方案

### 方案一: 家庭用户

**配置**:
- 协议: Trojan/VLESS
- 加密: AES-128-GCM
- 节点: 本地 CN2 GIA
- 分流: 智能规则

**预期效果**:
- 延迟: < 50ms
- 下载: 接近本地带宽
- 稳定性: 99%+

### 方案二: 重度用户

**配置**:
- 主力: IPLC 专线
- 备用: CN2 GIA
- 加速: BBR + TCP Fast Open
- 监控: 自动故障转移

**预期效果**:
- 延迟: < 30ms
- 零丢包
- 24/7 稳定

### 方案三: 企业用户

**配置**:
- VPN: WireGuard
- 专线: SD-WAN
- 冗余: 多线路备份
- 管理: 集中监控

**预期效果**:
- 企业级 SLA
- 完全可控
- 安全合规

## 速度对比基准

### 协议速度 (100Mbps 带宽)

| 场景 | WireGuard | Trojan | V2Ray | SS |
|------|-----------|--------|-------|-----|
| 网页浏览 | 98 Mbps | 95 Mbps | 90 Mbps | 92 Mbps |
| 视频流媒体 | 97 Mbps | 94 Mbps | 88 Mbps | 90 Mbps |
| 大文件下载 | 99 Mbps | 96 Mbps | 92 Mbps | 94 Mbps |
| 游戏 (延迟) | 12ms | 15ms | 18ms | 16ms |

### 优化前后对比

| 指标 | 优化前 | 优化后 | 提升 |
|------|--------|--------|------|
| 下载速度 | 50 Mbps | 95 Mbps | +90% |
| 上传速度 | 20 Mbps | 40 Mbps | +100% |
| 延迟 | 80ms | 25ms | -69% |
| 稳定性 | 85% | 99% | +16% |

## 相关资源

- [协议选择指南](./protocol-comparison.md)
- [客户端配置教程](./client-setup.md)
- [服务器搭建指南](./server-setup.md)

### 推荐服务

- [实时速度测试](https://jichangspeed.com/) - 各节点最新测速数据
- [加速工具评测](https://outsideweb.net/) - 优化方案和工具推荐

---

更新时间: 2026-10-12
