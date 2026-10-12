# 客户端配置完全指南 2026

## 概述

本指南涵盖主流平台的代理客户端配置,包括 Windows、macOS、iOS、Android 和 Linux。

## Windows 客户端

### Clash for Windows (推荐)

**下载和安装**:
1. 从 GitHub 下载最新版本
2. 解压到任意目录
3. 运行 `Clash for Windows.exe`

**配置步骤**:

1. **导入订阅链接**:
   ```
   Profiles → 输入订阅链接 → Download
   ```

2. **启用系统代理**:
   ```
   General → System Proxy → 开启
   ```

3. **选择代理模式**:
   - **全局模式**: 所有流量走代理
   - **规则模式**: 根据规则自动分流(推荐)
   - **直连模式**: 不使用代理

4. **配置规则**:
   ```yaml
   rules:
     - DOMAIN-SUFFIX,google.com,PROXY
     - DOMAIN-SUFFIX,youtube.com,PROXY
     - GEOIP,CN,DIRECT
     - MATCH,PROXY
   ```

**常见问题**:
- ❌ 无法启动: 检查是否被杀毒软件拦截
- ❌ 连接失败: 验证订阅链接是否有效
- ❌ 速度慢: 切换不同节点测试

### V2RayN

**特点**:
- 轻量级,资源占用少
- 支持多种协议
- 适合高级用户

**配置示例**:
```json
{
  "inbounds": [{
    "port": 10808,
    "protocol": "socks",
    "settings": {
      "udp": true
    }
  }],
  "outbounds": [{
    "protocol": "vmess",
    "settings": {
      "vnext": [{
        "address": "example.com",
        "port": 443,
        "users": [{
          "id": "uuid-here",
          "alterId": 0
        }]
      }]
    }
  }]
}
```

## macOS 客户端

### ClashX Pro (推荐)

**安装步骤**:
1. 下载 ClashX Pro.dmg
2. 拖拽到应用程序文件夹
3. 首次启动需授权系统扩展

**配置方法**:

1. **导入配置**:
   ```
   配置 → 托管配置 → 管理 → 添加
   ```

2. **设置为系统代理**:
   ```
   设置为系统代理 → 开启
   ```

3. **选择代理模式**:
   - 规则模式(推荐)
   - 全局模式
   - 直连模式

**高级功能**:
- TUN 模式: 接管所有流量
- 增强模式: DNS 解析优化
- 脚本模式: 自定义分流规则

### Surge

**特点**:
- 功能最强大的 macOS 客户端
- 支持模块化配置
- 付费软件但体验极佳

**基础配置**:
```ini
[General]
loglevel = notify
dns-server = system, 223.5.5.5, 119.29.29.29

[Proxy]
Proxy1 = ss, server.com, 8388, encrypt-method=aes-256-gcm, password=pwd

[Proxy Group]
Proxy = select, Proxy1, DIRECT

[Rule]
DOMAIN-SUFFIX,google.com,Proxy
GEOIP,CN,DIRECT
FINAL,Proxy
```

想了解哪些服务提供优质的 macOS 节点?访问 [机场评测平台](https://jichangspeed.com/) 查看详细对比。

## iOS 客户端

### Shadowrocket (推荐)

**购买和安装**:
1. 需要非中国区 App Store 账号
2. 价格: $2.99 (美区)
3. 支持所有主流协议

**配置步骤**:

1. **添加订阅**:
   ```
   首页 → + → 类型: Subscribe
   URL: 订阅链接
   ```

2. **启用代理**:
   ```
   全局路由 → 选择"配置"
   顶部开关 → 打开
   ```

3. **配置规则**:
   ```
   配置 → 编辑配置
   添加自定义规则
   ```

**推荐规则**:
```
[Rule]
DOMAIN-SUFFIX,apple.com,DIRECT
DOMAIN-SUFFIX,icloud.com,DIRECT
DOMAIN-KEYWORD,google,PROXY
GEOIP,CN,DIRECT
FINAL,PROXY
```

### Quantumult X

**特点**:
- 功能强大,可玩性高
- 支持重写和脚本
- 学习曲线较陡

**基础配置**:
```ini
[server_local]
vmess=example.com:443, method=aes-128-gcm, password=uuid, obfs=wss, obfs-uri=/path

[policy]
static=Proxy, server-tag-regex=.*, img-url=https://example.com/icon.png

[filter_local]
host-suffix, google.com, Proxy
geoip, cn, direct
final, Proxy
```

### Surge iOS

**特点**:
- iOS 上最专业的网络工具
- 价格较高但功能全面
- 适合追求极致体验的用户

## Android 客户端

### Clash for Android (推荐)

**安装方法**:
1. 从 GitHub 或第三方商店下载
2. 安装 APK 文件
3. 授予 VPN 权限

**配置流程**:

1. **导入配置**:
   ```
   配置 → 新配置 → URL
   输入订阅链接 → 保存
   ```

2. **启动服务**:
   ```
   点击主界面 ⚡ 图标
   允许 VPN 权限
   ```

3. **选择节点**:
   ```
   代理 → 选择合适的节点
   测速 → 选择延迟低的
   ```

**优化设置**:
- 允许局域网连接
- IPv6 支持
- 开机自启动
- 后台运行白名单

### V2RayNG

**特点**:
- 开源免费
- 支持多种协议
- 资源占用低

**快速配置**:
1. 复制 vmess:// 链接
2. 打开 V2RayNG
3. 点击 + → 从剪贴板导入
4. 点击右下角启动

### SagerNet

**特点**:
- 新一代代理工具
- 基于 sing-box 内核
- 性能优秀

需要找支持 Android 的优质服务?查看 [外网工具指南](https://outsideweb.net/) 的详细推荐。

## Linux 客户端

### Clash 命令行版

**安装步骤**:
```bash
# 下载
wget https://github.com/Dreamacro/clash/releases/download/v1.18.0/clash-linux-amd64-v1.18.0.gz

# 解压
gunzip clash-linux-amd64-v1.18.0.gz
mv clash-linux-amd64-v1.18.0 /usr/local/bin/clash
chmod +x /usr/local/bin/clash

# 创建配置目录
mkdir -p ~/.config/clash
```

**配置文件**:
```yaml
# ~/.config/clash/config.yaml
port: 7890
socks-port: 7891
allow-lan: false
mode: rule
log-level: info

proxies:
  - name: "Proxy1"
    type: ss
    server: server.com
    port: 8388
    cipher: aes-256-gcm
    password: "password"

proxy-groups:
  - name: "Proxy"
    type: select
    proxies:
      - Proxy1

rules:
  - DOMAIN-SUFFIX,google.com,Proxy
  - GEOIP,CN,DIRECT
  - MATCH,Proxy
```

**启动服务**:
```bash
# 前台运行
clash -f ~/.config/clash/config.yaml

# 后台运行
nohup clash -f ~/.config/clash/config.yaml > /dev/null 2>&1 &
```

**系统代理设置**:
```bash
export http_proxy=http://127.0.0.1:7890
export https_proxy=http://127.0.0.1:7890
export all_proxy=socks5://127.0.0.1:7891
```

### V2Ray 命令行

**安装脚本**:
```bash
bash <(curl -L https://raw.githubusercontent.com/v2fly/fhs-install-v2ray/master/install-release.sh)
```

**配置文件位置**:
```
/usr/local/etc/v2ray/config.json
```

**服务管理**:
```bash
# 启动
systemctl start v2ray

# 开机自启
systemctl enable v2ray

# 查看状态
systemctl status v2ray
```

### Qv2ray (图形界面)

**特点**:
- 跨平台图形客户端
- 支持多种内核
- 功能强大

**安装** (Ubuntu/Debian):
```bash
sudo add-apt-repository ppa:qv2ray/qv2ray
sudo apt update
sudo apt install qv2ray
```

## 路由规则配置

### 基础规则

**直连规则**:
```
# 国内域名
DOMAIN-SUFFIX,cn
DOMAIN-SUFFIX,baidu.com
DOMAIN-SUFFIX,taobao.com

# 国内 IP
GEOIP,CN

# 局域网
IP-CIDR,192.168.0.0/16
IP-CIDR,10.0.0.0/8
```

**代理规则**:
```
# 常用国外服务
DOMAIN-SUFFIX,google.com
DOMAIN-SUFFIX,youtube.com
DOMAIN-SUFFIX,facebook.com
DOMAIN-SUFFIX,twitter.com
DOMAIN-SUFFIX,github.com

# 关键词匹配
DOMAIN-KEYWORD,google
DOMAIN-KEYWORD,youtube
```

### 高级规则

**按应用分流** (Android):
```
# 特定应用走代理
PACKAGE,com.android.chrome,Proxy
PACKAGE,com.google.android.youtube,Proxy

# 其他应用直连
PACKAGE,com.tencent.mm,DIRECT
```

**按进程分流** (Windows):
```
PROCESS-NAME,chrome.exe,Proxy
PROCESS-NAME,firefox.exe,Proxy
PROCESS-NAME,WeChat.exe,DIRECT
```

**时间规则**:
```
# 工作时间使用代理
TIME,09:00-18:00,Proxy
# 其他时间直连
TIME,18:00-09:00,DIRECT
```

## 性能优化

### 1. DNS 优化

**推荐 DNS**:
```
国内: 223.5.5.5 (阿里)
国内: 119.29.29.29 (腾讯)
国外: 1.1.1.1 (Cloudflare)
国外: 8.8.8.8 (Google)
```

**DNS 分流**:
```yaml
dns:
  enable: true
  nameserver:
    - 223.5.5.5
    - 119.29.29.29
  fallback:
    - 1.1.1.1
    - 8.8.8.8
  fallback-filter:
    geoip: true
```

### 2. 连接优化

**TCP 优化**:
- 启用 TCP Fast Open
- 调整 TCP 窗口大小
- 使用 BBR 拥塞控制

**UDP 优化**:
- 启用 UDP 支持
- mKCP 加速(V2Ray)

### 3. 节点选择

**选择标准**:
- ✅ 延迟 < 100ms (优秀)
- ✅ 延迟 100-200ms (良好)
- ⚠️ 延迟 > 200ms (较慢)
- ❌ 延迟 > 500ms (不推荐)

**自动选择**:
```yaml
proxy-groups:
  - name: Auto
    type: url-test
    url: http://www.gstatic.com/generate_204
    interval: 300
    proxies:
      - Proxy1
      - Proxy2
      - Proxy3
```

## 故障排查

### 常见问题

**1. 无法连接**

检查项:
- [ ] 订阅链接是否过期
- [ ] 节点服务器是否正常
- [ ] 本地防火墙设置
- [ ] 时间是否同步

**2. 连接慢**

优化方法:
- 切换不同节点
- 更换协议
- 检查本地网络
- 查看服务器负载

**3. 部分网站无法访问**

解决方案:
- 检查分流规则
- 尝试全局模式
- 清除 DNS 缓存
- 更换 DNS 服务器

**4. 频繁断线**

改善措施:
- 使用 TCP 协议
- 启用自动重连
- 降低 UDP 使用
- 更换稳定节点

### 测试工具

**连接测试**:
```bash
# 测试代理连接
curl -x socks5://127.0.0.1:1080 https://google.com

# 查看公网 IP
curl https://api.ip.sb/ip
```

**速度测试**:
- Speedtest.net
- Fast.com
- 各机场提供的测速工具

想了解哪些服务更稳定?查看 [实时测速数据](https://jichangspeed.com/)。

## 安全建议

### 1. 密码安全

- 使用强密码
- 不同服务用不同密码
- 定期更换密码
- 启用两步验证

### 2. 流量安全

- 使用 HTTPS 访问网站
- 避免在代理下输入敏感信息
- 定期检查连接日志
- 使用可信的服务商

### 3. 设备安全

- 及时更新客户端
- 不使用破解版
- 定期扫描病毒
- 避免安装来源不明的软件

## 推荐配置方案

### 方案一: 新手入门

**平台**: Windows/macOS
**客户端**: Clash
**协议**: Shadowsocks/Trojan
**特点**: 配置简单,稳定可靠

### 方案二: 高级用户

**平台**: 全平台
**客户端**: V2Ray/Surge
**协议**: V2Ray + CDN
**特点**: 功能强大,可定制性强

### 方案三: 移动优先

**平台**: iOS/Android
**客户端**: Shadowrocket/Clash
**协议**: Trojan/VLESS
**特点**: 省电,速度快

## 相关资源

- [协议对比分析](./protocol-comparison.md)
- [服务器搭建教程](./server-setup.md)
- [性能优化指南](./speed-optimization.md)

### 服务推荐

- [机场服务评测](https://jichangspeed.com/) - 各平台客户端配置教程
- [科学上网工具](https://outsideweb.net/) - 客户端下载和使用指南

---

更新时间: 2026-10-12
