# Cross-Device Agent Workflow Core

## 2026-09-05 維護更新

本次 source 更新包含portable lifecycle schema、template、唯讀 Git classifier 與 Full Core 維護流程。版本以 Git commit 識別；既有發行 tag 保持不變。當本次對話或已確認工作單已明列更新、commit／push 與驗收範圍，沿用該授權完成，不為相同動作重複提問；未涵蓋的動作仍停在確認點。Startup 維持唯讀，完成讀取報告後可轉入已授權的獨立工作階段。

目前交接與驗收範圍見 [handoff.md](handoff.md)，歷史變更見 [CHANGELOG.md](CHANGELOG.md)。

## Portable Project Lifecycle v2

Full Core 提供共同契約，不把所有專案合併成 monorepo：

| 層 | 定義 |
|---|---|
| Authority Kernel | 本 Core 的 `.schemas/project-lifecycle.schema.json`、template、validator，以及外部 pinned Lite／ReadyGate revision |
| Part routing | 只回答「這個 Project 屬於哪個 Part」；不是固定 Part 9，也不是 Git root／branch |
| Project instance | 每個實際 repository 自己的 `.agents/project-lifecycle.json`、Git top-level、remote、branch 與歷史 |
| Device binding | 絕對路徑、裝置名稱、登入與 credential；只留 runtime／ignored `policy.local.yaml` |

部署步驟是「複製 template → 填入不可變 authority revision 與 Project identity → 放在專案根 `.agents/project-lifecycle.json` → 驗證」，不是把 Core 文件整份覆蓋到每個專案。專案既有 `AGENTS.md`、README 與規則必須保留，只修改 allowlist 或明確 managed block。

```powershell
python .\scripts\project_lifecycle.py validate-manifest .\templates\project-lifecycle.template.json
python .\scripts\project_lifecycle.py classify-git <project-root>\.agents\project-lifecycle.json --project-root <project-root>
```

`classify-git` 唯讀；不 clone、pull、commit、push、merge、rebase、切 branch 或改 remote。Initial 建立 bootstrap checkpoint，Startup fetch 並對照遠端 SHA（不建空 commit），Shutdown 建立工作 checkpoint。`manual` 每次等確認；`standing_scoped` 只在既有正確 remote、目前 branch、allowlist、安全檢查與非 force push 限制全通過時生效。

資料型專案使用 `content.tracked_roots`、`excluded_roots` 與 `large_file_policy` 說明要進 Git 的內容；private／raw／大型資料可選 `manifest-only`、`git-lfs` 或 `exclude`，不得假設所有資料 bytes 都應 push。

跨裝置 Agent 工作流的公開 Full Core。它負責第一次部署、完整治理、相容性檢查與按需 SOP；日常專案則使用外部 Lite 三技能。

目前 GitHub 發行版：`v0.1.0`
GitHub `main` 候選版本：`v0.2.0`（source 已 push；尚未 tag／Release）

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

## 生命週期路由

| 流程 | 何時使用 | 完成與停止點 |
|---|---|---|
| `initial` | 新專案第一次建立治理結構、既有專案缺件修復或明確技能部署 | 建立／修復並回讀後停止；不自動開始工作或 GitHub delivery |
| `startup` | 每次開始或接續既有專案 | 唯讀開工報告後停止，等待工作選擇 |
| 工作執行 | 範圍已確認後進行修改與驗證 | 高風險、不可逆或外部動作先通過 Requirement Gate |
| `shutdown` | 每次工作階段結束或換電腦 | 更新本機版本紀錄與交接；沒有外部授權就停止在 `LOCAL_ONLY`／`PENDING_GATE` |

```text
新專案／缺件 → initial → 停止
每次開始     → startup → 等待工作選擇
確認工作     → [需要時 Requirement Gate] → 執行與驗證
每次結束     → shutdown：先更新本機紀錄與交接
                 ├─ 無外部授權 → LOCAL_ONLY／PENDING_GATE，停止
                 └─ 已授權 → Delivery Gate → 精確授權的 delivery → 回讀
```

ReadyGate 是橫向雙閘門，不是第四個固定日常階段。一般唯讀開工不啟動；`WORK_ORDER_CONFIRMED` 不是驗證證據，`READY` 也不是自動取得 commit、push、tag 或 release 的許可。

## 目前限制

- `scripts/install.ps1 -Apply` 仍會停止，因為 Apply 是 `PLANNED`。
- Lite `v2.0.0` source 已在 GitHub `main`；正式安裝基準仍需區分 `main` 候選與已發布 tag。
- commit、push、tag、release、批次移動、封存與權限變更必須通過確認工作單與 Delivery Gate。
- 公開文件不得保存 credential、私人 vault、裝置絕對路徑或本機 checkout 名稱。

## 最新變更

`v0.2.0` 開發版已改用四檔契約、明確要求 Core profile 的四技能，並把所有外部知識庫從專案生命週期拆出。完整紀錄見 [`CHANGELOG.md`](CHANGELOG.md)。
