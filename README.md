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
- 📦 **自动打包发布** - 每次 push 自动执行 HACS 规范打包；推送 `v*` tag 时自动上传发布包

## 📦 安装

### 方式一：使用 HACS（推荐）

> 当前仓库属于 **自定义仓库安装模式**，可在 HACS 里“自定义仓库”添加后直接搜索安装。

1. 确保已安装 [HACS](https://hacs.xyz/)
2. HACS → 右上角菜单 → **自定义仓库**
3. 填入仓库地址：`https://github.com/KleinPan/qhgas-ha`，类型选择 **Integration**
4. 添加后，进入 HACS 集成页搜索 **QH Gas** 并安装
5. 重启 Home Assistant

### 方式二：手动安装

1. 克隆或下载本仓库
2. 将 `qhgas-ha/custom_components/qhgas` 目录复制到 Home Assistant 的 `custom_components` 目录：

   ```bash
   cp -r qhgas-ha/custom_components/qhgas ~/.homeassistant/custom_components/
   ```

3. 重启 Home Assistant

## 🔧 自动化打包（GitHub Actions）

仓库已包含自动化脚本与工作流：

- `scripts/package_hacs.sh`：生成 `dist/qhgas.zip`，压缩结构符合 HACS 发布包规范（`custom_components/qhgas/**`）
- `.github/workflows/hacs-package.yml`：
  - 任意 `push`：执行 `hassfest` 校验 + 自动打包 + 上传 Actions artifact
  - `v*` tag push：额外把 `qhgas.zip` 自动上传为 GitHub Release 资产

## ⚙️ 配置

### 通过 UI 配置

1. 进入 Home Assistant → **配置** → **集成**
2. 点击右下角 **添加集成**
3. 搜索 "QH Gas" 并选择
4. 输入您的 **Card ID**（燃气卡号）
5. 点击 **提交** 完成配置

## 📄 许可证

本项目基于 MIT 许可证开源 - 详见 [LICENSE](qhgas-ha/LICENSE) 文件。
