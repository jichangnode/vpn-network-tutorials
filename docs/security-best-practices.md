# 网络安全与隐私保护最佳实践

## 概述

使用代理和 VPN 服务时,安全性和隐私保护至关重要。本指南提供全面的安全建议和最佳实践。

## 基础安全原则

### 1. 选择可信的服务提供商

**评估标准**:
- ✅ 明确的隐私政策
- ✅ 无日志政策承诺
- ✅ 透明的公司信息
- ✅ 良好的用户口碑
- ✅ 定期安全审计

**避免的服务特征**:
- ❌ 免费但来源不明
- ❌ 过度收集个人信息
- ❌ 隐私政策模糊
- ❌ 频繁出现安全事件
- ❌ 注册地在高风险地区

选择服务商时可以参考独立评测: [机场服务评测](https://jichangspeed.com/) 和 [工具安全分析](https://outsideweb.net/)

### 2. 使用强加密

**推荐加密标准**:
```
对称加密: AES-256-GCM, ChaCha20-Poly1305
非对称加密: RSA-4096, ECC (Curve25519)
哈希算法: SHA-256, SHA-512
TLS 版本: TLS 1.3 (最低 TLS 1.2)
```

**避免的加密**:
- ❌ DES, 3DES (已过时)
- ❌ RC4 (存在漏洞)
- ❌ MD5, SHA-1 (不安全的哈希)
- ❌ SSL 2.0/3.0, TLS 1.0/1.1 (已弃用)

### 3. 定期更新软件

**更新策略**:
- 🔄 客户端软件: 每周检查更新
- 🔄 操作系统: 开启自动更新
- 🔄 证书: 定期更新 SSL/TLS 证书
- 🔄 配置文件: 订阅自动更新

## 账号安全

### 密码管理

**密码要求**:
- 最少 16 字符
- 包含大小写字母、数字、特殊符号
- 不使用字典单词
- 每个服务使用唯一密码

**推荐工具**:
- 1Password
- Bitwarden
- KeePassXC

**密码示例生成**:
```bash
# Linux/macOS 生成强密码
openssl rand -base64 32

# 自定义长度
openssl rand -base64 48 | cut -c1-32
```

### 多因素认证 (MFA)

**启用 2FA**:
1. 使用认证器应用 (Google Authenticator, Authy)
2. 备份恢复代码
3. 避免使用 SMS 作为唯一方式

**硬件密钥** (更安全):
- YubiKey
- Google Titan
- 支持 FIDO2/U2F 标准

### API 密钥保护

**安全存储**:
```bash
# 使用环境变量
export VPN_API_KEY="your-key-here"

# 使用密钥管理工具
# macOS Keychain
security add-generic-password -a "$USER" -s "vpn-api" -w "key-value"

# 读取
security find-generic-password -a "$USER" -s "vpn-api" -w
```

**避免**:
- ❌ 硬编码在代码中
- ❌ 提交到 Git 仓库
- ❌ 明文存储在配置文件
- ❌ 通过不安全的渠道传输

## 连接安全

### DNS 安全

**DNS 泄露防护**:
```yaml
# Clash 配置
dns:
  enable: true
  enhanced-mode: fake-ip
  nameserver:
    - 223.5.5.5
    - 119.29.29.29
  fallback:
    - tls://1.1.1.1:853
    - https://dns.google/dns-query
  fallback-filter:
    geoip: true
    ipcidr:
      - 240.0.0.0/4
```

**DNS 加密**:
- DoH (DNS over HTTPS)
- DoT (DNS over TLS)
- DNSCrypt

**测试 DNS 泄露**:
```bash
# 检查 DNS 服务器
nslookup google.com

# 测试泄露
curl https://dnsleaktest.com
```

### Kill Switch

**作用**:
- VPN 断开时自动断网
- 防止真实 IP 泄露
- 保护敏感操作

**配置示例** (Linux):
```bash
#!/bin/bash
# VPN Kill Switch 脚本

# 允许的网络接口
VPN_INTERFACE="tun0"

# 清空现有规则
iptables -F
iptables -X

# 默认拒绝所有流量
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT DROP

# 允许本地回环
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

# 允许 VPN 流量
iptables -A INPUT -i $VPN_INTERFACE -j ACCEPT
iptables -A OUTPUT -o $VPN_INTERFACE -j ACCEPT

# 允许连接到 VPN 服务器
iptables -A OUTPUT -d VPN_SERVER_IP -j ACCEPT
iptables -A INPUT -s VPN_SERVER_IP -j ACCEPT
```

**客户端设置**:
- Clash: General → "System Proxy on Exit"
- V2Ray: 连接断开时的处理策略
- Shadowrocket: 断开时自动停止

### IPv6 泄露防护

**问题**:
- 部分 VPN 不支持 IPv6
- IPv6 流量可能绕过 VPN

**解决方案**:

1. **禁用 IPv6** (临时):
```bash
# Linux
sudo sysctl -w net.ipv6.conf.all.disable_ipv6=1

# macOS
networksetup -setv6off Wi-Fi
```

2. **客户端配置**:
```yaml
# Clash
ipv6: false

# V2Ray
"routing": {
  "rules": [{
    "type": "field",
    "outboundTag": "block",
    "protocol": ["ipv6"]
  }]
}
```

3. **测试泄露**:
```bash
curl https://ipv6leak.com
```

### WebRTC 泄露

**风险**:
- 浏览器 WebRTC 可能泄露真实 IP
- 即使使用 VPN 也会泄露

**防护措施**:

**Firefox**:
```
about:config
media.peerconnection.enabled = false
```

**Chrome/Edge**:
- 安装扩展: WebRTC Leak Prevent
- 或使用 uBlock Origin (高级设置)

**测试**:
```
访问 https://browserleaks.com/webrtc
```

## 流量特征隐藏

### 协议混淆

**V2Ray WebSocket + TLS**:
```json
{
  "streamSettings": {
    "network": "ws",
    "security": "tls",
    "tlsSettings": {
      "serverName": "example.com",
      "allowInsecure": false
    },
    "wsSettings": {
      "path": "/random-path",
      "headers": {
        "Host": "example.com"
      }
    }
  }
}
```

**Trojan 伪装**:
```json
{
  "ssl": {
    "sni": "example.com",
    "alpn": ["h2", "http/1.1"],
    "cert": "/path/to/fullchain.pem",
    "key": "/path/to/privkey.pem"
  }
}
```

### CDN 中转

**优势**:
- 隐藏真实服务器 IP
- 利用 CDN 高可用性
- 流量看起来更自然

**支持的 CDN**:
- Cloudflare
- Fastly
- AWS CloudFront

**配置要点**:
- 使用 WebSocket
- 启用 TLS
- 自定义域名

了解更多中转优化方案: [网络加速工具](https://outsideweb.net/)

## 隐私保护

### 浏览器安全

**推荐浏览器**:
- Firefox (隐私友好)
- Brave (内置隐私保护)
- Tor Browser (最高隐私)

**必要扩展**:
- uBlock Origin (广告拦截)
- HTTPS Everywhere (强制 HTTPS)
- Privacy Badger (追踪拦截)
- NoScript (脚本控制)

**浏览器设置**:
```
Firefox:
- 增强跟踪保护: 严格
- 禁用遥测
- 启用 DNS over HTTPS
- Cookie: 仅来自访问的网站

Chrome:
- 安全浏览: 增强保护
- 不跟踪: 启用
- 清除第三方 Cookie
```

### 防指纹追踪

**浏览器指纹**:
- User Agent
- 屏幕分辨率
- 字体列表
- Canvas 指纹
- WebGL 信息
- 时区/语言

**对抗措施**:
- 使用 Tor Browser (最佳)
- Firefox + Canvas Blocker
- 定期清除 Cookie
- 禁用 JavaScript (极端情况)

**测试工具**:
- https://amiunique.org
- https://coveryourtracks.eff.org

### Cookie 和存储管理

**自动清理**:
```
Firefox:
设置 → 隐私与安全 → Cookie 和网站数据
→ 管理数据 → 清除
→ 关闭 Firefox 时清除数据
```

**定期清理**:
- Cookie
- LocalStorage
- IndexedDB
- Cache
- Service Workers

## 服务器端安全

### 服务器加固

**基础安全**:
```bash
# 更新系统
apt update && apt upgrade -y

# 配置防火墙
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp
ufw allow 443/tcp
ufw enable

# 禁用 root 登录
sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
systemctl restart sshd

# 安装 fail2ban
apt install fail2ban -y
```

**SSH 安全**:
```bash
# 生成强 SSH 密钥
ssh-keygen -t ed25519 -C "your_email@example.com"

# 上传公钥
ssh-copy-id user@server

# 禁用密码登录
echo "PasswordAuthentication no" >> /etc/ssh/sshd_config
systemctl restart sshd
```

### 日志管理

**重要日志**:
```bash
# 连接日志
tail -f /var/log/v2ray/access.log

# 错误日志
tail -f /var/log/v2ray/error.log

# 系统日志
journalctl -u v2ray -f
```

**日志轮转**:
```bash
# /etc/logrotate.d/v2ray
/var/log/v2ray/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
}
```

**敏感信息过滤**:
```json
{
  "log": {
    "loglevel": "warning",
    "access": "/var/log/v2ray/access.log",
    "error": "/var/log/v2ray/error.log"
  }
}
```

### 证书安全

**Let's Encrypt 自动续期**:
```bash
# 安装 certbot
apt install certbot -y

# 获取证书
certbot certonly --standalone -d example.com

# 自动续期
echo "0 3 * * * certbot renew --quiet" | crontab -
```

**证书权限**:
```bash
chmod 600 /etc/letsencrypt/live/example.com/privkey.pem
chown v2ray:v2ray /etc/letsencrypt/live/example.com/privkey.pem
```

## 审计与监控

### 定期安全检查

**每日**:
- [ ] 检查异常流量
- [ ] 查看错误日志
- [ ] 验证服务运行状态

**每周**:
- [ ] 更新软件包
- [ ] 审查连接日志
- [ ] 测试备份恢复

**每月**:
- [ ] 更换密码
- [ ] 审计用户权限
- [ ] 安全扫描
- [ ] 证书有效期检查

### 监控工具

**服务器监控**:
```bash
# 安装 netdata
bash <(curl -Ss https://my-netdata.io/kickstart.sh)

# 访问监控面板
http://server-ip:19999
```

**流量监控**:
```bash
# vnstat
apt install vnstat -y
vnstat -l  # 实时流量

# iftop
apt install iftop -y
iftop -i eth0  # 实时连接
```

### 入侵检测

**AIDE (文件完整性检查)**:
```bash
# 安装
apt install aide -y

# 初始化
aideinit

# 检查
aide --check
```

**Fail2Ban 规则**:
```ini
# /etc/fail2ban/jail.local
[sshd]
enabled = true
port = 22
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600
```

## 应急响应

### 发现入侵迹象

**立即行动**:
1. 断开网络连接
2. 保存当前状态
3. 查看活动连接
4. 检查用户登录

**取证命令**:
```bash
# 查看活动连接
netstat -antp

# 登录历史
last -a
lastlog

# 运行进程
ps aux | grep -v root

# 文件修改
find / -mtime -1 -type f

# 计划任务
crontab -l
cat /etc/crontab
```

### 恢复流程

1. **隔离系统**
2. **修改所有密码**
3. **重新部署服务**
4. **恢复备份数据**
5. **加强安全措施**
6. **持续监控**

## 合规性考虑

### 数据保护

**GDPR 要求** (如适用):
- 明确的数据收集目的
- 用户同意机制
- 数据访问和删除权
- 数据泄露通知

**最小化收集**:
- 仅收集必要信息
- 定期清理旧数据
- 加密敏感数据
- 安全存储和传输

### 使用限制

**禁止行为**:
- ❌ 非法内容传播
- ❌ 网络攻击
- ❌ 垃圾邮件发送
- ❌ 侵犯版权
- ❌ 滥用服务

**负责任使用**:
- 遵守当地法律
- 尊重服务条款
- 保护他人隐私
- 合理使用资源

## 安全检查清单

### 客户端安全

- [ ] 使用最新版客户端
- [ ] 启用强加密
- [ ] 配置 DNS 防泄露
- [ ] 启用 Kill Switch
- [ ] 禁用 IPv6 或配置正确
- [ ] 浏览器隐私设置
- [ ] 定期清理缓存和 Cookie
- [ ] 使用强密码和 2FA

### 服务器安全

- [ ] 系统及时更新
- [ ] SSH 密钥认证
- [ ] 防火墙正确配置
- [ ] 证书有效且自动续期
- [ ] 日志正常记录
- [ ] 监控工具运行
- [ ] 定期备份
- [ ] 入侵检测系统

### 网络安全

- [ ] 使用 TLS 1.3
- [ ] 协议混淆配置
- [ ] 流量特征隐藏
- [ ] 多层代理 (如需要)
- [ ] CDN 中转 (如需要)
- [ ] 定期更换端口
- [ ] 域名伪装

## 常见问题

### Q1: VPN 服务会记录我的活动吗?

取决于服务商的政策:
- 优质服务: 无日志或最小日志
- 可疑服务: 可能记录一切

**验证方法**:
- 阅读隐私政策
- 查看独立审计报告
- 参考用户评价

### Q2: 使用 VPN 是否完全匿名?

不完全,VPN 只是增强隐私的一部分:
- ✅ 隐藏 IP 地址
- ✅ 加密流量
- ❌ 无法防止浏览器指纹
- ❌ 已登录账号仍可识别
- ❌ 无法对抗国家级攻击

### Q3: 免费 VPN 安全吗?

大多数免费 VPN 存在风险:
- 可能出售用户数据
- 注入广告
- 带宽限制严重
- 安全性无保障

建议使用信誉良好的付费服务。

### Q4: 如何测试我的连接是否安全?

**测试清单**:
```
1. IP 泄露: https://ipleak.net
2. DNS 泄露: https://dnsleaktest.com
3. WebRTC 泄露: https://browserleaks.com/webrtc
4. 浏览器指纹: https://amiunique.org
```

### Q5: 多重代理更安全吗?

可能更安全,但有代价:
- ✅ 增加追踪难度
- ✅ 分散信任风险
- ❌ 显著降低速度
- ❌ 增加配置复杂度
- ❌ 更多故障点

## 相关资源

- [VPN 基础知识](./vpn-basics.md)
- [协议对比分析](./protocol-comparison.md)
- [客户端配置指南](./client-setup.md)

### 安全工具推荐

- [服务商安全评测](https://jichangspeed.com/)
- [隐私保护指南](https://outsideweb.net/)

---

更新时间: 2026-10-12
