# Cross-Device Agent Workflow Core

跨裝置 Agent 工作流的公開 Full Core。它負責第一次部署、完整治理、相容性檢查與按需 SOP；日常專案則使用外部 Lite 三技能。

目前 GitHub 發行版：`v0.1.0`
開發中版本：`v0.2.0`（本機未 commit／push）

## 先選 profile

| 情境 | Profile | 必要技能 |
|---|---|---|
| 一般專案日常生命週期 | Lite | `initial`、`startup`、`shutdown` |
| 新裝置、首次完整部署、批次治理或高風險工作 | Core | Lite 三技能加 `readygate` |

Lite 三技能與 ReadyGate 都維持外部單一權威；本 repository 只登記相容版本與整合契約，不複製第二份 canonical Skill。

## 權威與相依關係

| 角色 | Canonical | 責任 |
|---|---|---|
| Full Core | 本 repository | `BOOTSTRAP.md`、完整 SOP、profile 與相容性驗證 |
| Lite 三技能 | [`cross-device-agent-skills`](https://github.com/sink6985757-web/cross-device-agent-skills) | 公開 `initial`／`startup`／`shutdown` 發行權威 |
| ReadyGate | [`readygate-skill-chatgpt-app`](https://github.com/sink6985757-web/readygate-skill-chatgpt-app) | 需求確認、Delivery Gate 與高風險工作單 |
| 個人全域核心 | private `dotfiles` | `~/.agents` 的 chezmoi source、runtime 同步與薄轉接 |
| 專案狀態 | 各專案 repository | 專案四檔、程式與 Git 歷史 |

Google Drive checkout 是工作副本或鏡像，不取代 GitHub remote；runtime `~/.agents/skills` 是執行副本，也不取代各 Skill 發行來源。Notion、Obsidian、Knowledge Master 或其他外部知識庫均為獨立 `ON_DEMAND_ONLY` 工作，不屬於 initial／startup／shutdown。

## 專案四檔契約

| 檔案 | 責任 | 主要更新者 |
|---|---|---|
| `AGENTS.md` | 穩定規則、權威、邊界與相依 | 規則／架構變更 |
| `README.md` | GitHub 人類安裝、Agent／Tool 安裝、使用、公開版本與最新變更 | 授權 GitHub delivery 前 |
| `CHANGELOG.md` | 每次收工的近期修改、驗證、版本與 delivery 狀態 | `shutdown` |
| `handoff.md` | 現況、風險、下一步與唯一續跑點 | `shutdown` |

## 人類安裝

```powershell
git clone https://github.com/sink6985757-web/cross-device-agent-workflow-core.git
Set-Location .\cross-device-agent-workflow-core
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1
```

`install.ps1` 目前只做 doctor 與建議，不會安裝、登入、覆寫或修改 dotfiles；`-Apply` 仍未開放。

## Agent／Tool 安裝

把 repository 連結交給 Agent，並指定：

```text
先讀 BOOTSTRAP.md，回報 NONE／LITE／FULL／DRIFT／BLOCKED。
只做唯讀偵測與來源比較，不登入、不安裝、不覆寫。
需要修改、commit、push、搬移、封存或發布時，先以 ReadyGate 建立工作單。
```

Agent 必須以 Git remote 與 revision 辨識 Core checkout，不以資料夾名稱猜權威。

## 入口

- [`BOOTSTRAP.md`](BOOTSTRAP.md)：首次部署契約。
- [`WORKFLOW.md`](WORKFLOW.md)：十項按需 SOP 與 ReadyGate 接點。
- [`MAINTAINERS.md`](MAINTAINERS.md)：版本、repository 關係、驗證與發布。
- [`FEATURES.json`](FEATURES.json)：機器可讀 profile、依賴與功能狀態。
- [`CHANGELOG.md`](CHANGELOG.md)：近期版本與 delivery 狀態。

## 最短流程

```text
初始化專案 → initial
開始工作   → startup
結束工作   → shutdown
高風險任務 → ReadyGate
```

## 目前限制

- `scripts/install.ps1 -Apply` 仍會停止，因為 Apply 是 `PLANNED`。
- Lite `v2.0.0` 目前是本機候選版；GitHub 發行前仍以已發布版本為外部可安裝基準。
- commit、push、tag、release、批次移動、封存與權限變更必須通過確認工作單與 Delivery Gate。
- 公開文件不得保存 credential、私人 vault、裝置絕對路徑或本機 checkout 名稱。

## 最新變更

`v0.2.0` 開發版已改用四檔契約、明確要求 Core profile 的四技能，並把所有外部知識庫從專案生命週期拆出。完整紀錄見 [`CHANGELOG.md`](CHANGELOG.md)。
