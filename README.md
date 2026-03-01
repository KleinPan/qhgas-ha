# QH Gas Home Assistant Integration

[![GitHub Release](https://img.shields.io/github/release/KleinPan/qhgas-ha)](https://github.com/KleinPan/qhgas-ha/releases)
[![Home Assistant Version](https://img.shields.io/badge/Home-Assistant-%23041B4D?logo=home-assistant)](https://www.home-assistant.io)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## 📋 简介

QH Gas 是一个 Home Assistant 自定义集成，用于获取**秦华燃气**智能表数据。通过调用秦华燃气云平台 API，您可以实时监控燃气余额、气价、电池电量、阀门状态和信号强度等关键信息。

## ✨ 功能特性

- 🔄 **自动数据同步** - 每小时自动获取最新燃气数据
- 📊 **多维度监控** - 提供 5 种传感器类型：
  | 传感器 | 单位 | 说明 |
  |-------|------|------|
  | Balance | 元 | 燃气账户余额 |
  | Price | 元/m³ | 当前燃气价格 |
  | Battery | V | 电池电量 |
  | Valve | - | 阀门状态 |
  | Signal | - | 信号强度 |
- 🔧 **易于配置** - 通过 UI 界面即可完成设置
- 🛡️ **数据安全** - 使用 MD5 令牌认证，保障 API 通信安全

## 📦 安装

### 方式一：使用 HACS（推荐）

1. 确保已安装 [HACS](https://hacs.xyz/)
2. 进入 HACS → 集成 → 浏览并添加仓库
3. 搜索 "QH Gas" 并安装
4. 重启 Home Assistant

### 方式二：手动安装

1. 克隆或下载本仓库
2. 将 `qhgas-ha` 目录复制到 Home Assistant 的 `custom_components` 目录：

   ```bash
   # 假设 HA 配置目录为 ~/.homeassistant
   cp -r qhgas-ha ~/.homeassistant/custom_components/
   ```

3. 重启 Home Assistant

## ⚙️ 配置

### 通过 UI 配置

1. 进入 Home Assistant → **配置** → **集成**
2. 点击右下角 **添加集成**
3. 搜索 "QH Gas" 并选择
4. 输入您的 **Card ID**（燃气卡号）
5. 点击 **提交** 完成配置

### 配置文件示例

如需手动配置，可在 `configuration.yaml` 中添加：

```yaml
# configuration.yaml (可选，高级配置)
sensor:
  - platform: qhgas
    card_id: "your_card_id"
```

> **注意**：推荐使用 UI 配置方式。

## 🔧 技术细节

### 实体列表

配置完成后，将创建以下实体（以 Card ID `12345` 为例）：

| 实体 ID | 名称 | 单位 |
|---------|------|------|
| `sensor.qh_gas_12345_balance` | QH Gas 12345 Balance | 元 |
| `sensor.qh_gas_12345_price` | QH Gas 12345 Price | 元/m³ |
| `sensor.qh_gas_12345_battery` | QH Gas 12345 Battery | V |
| `sensor.qh_gas_12345_valve` | QH Gas 12345 Valve | - |
| `sensor.qh_gas_12345_signal` | QH Gas 12345 Signal | - |

## 🎨 自动化示例

### 余额不足告警

```yaml
automation:
  - alias: "燃气余额不足提醒"
    trigger:
      - platform: numeric_state
        entity_id: sensor.qh_gas_your_card_id_balance
        below: 10
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "燃气提醒"
          message: "燃气余额不足，请及时充值！当前余额：{{ states('sensor.qh_gas_your_card_id_balance') }}元"
```

### 电池电量低提醒

```yaml
automation:
  - alias: "燃气表电池低电量提醒"
    trigger:
      - platform: numeric_state
        entity_id: sensor.qh_gas_your_card_id_battery
        below: 3.0
    action:
      - service: persistent_notification.create
        data:
          title: "燃气表提醒"
          message: "燃气表电池电量低，请及时更换电池！当前电压：{{ states('sensor.qh_gas_your_card_id_battery') }}V"
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

## 📄 许可证

本项目基于 MIT 许可证开源 - 详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

感谢所有为这个项目做出贡献的人！

---

**注意**：本项目仅供学习和个人使用。使用前请确保您有权限访问秦华燃气 API 服务。