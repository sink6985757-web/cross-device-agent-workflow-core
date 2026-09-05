# <PROJECT_NAME>

當本次對話或已確認工作單已明列更新、commit／push 與驗收範圍，沿用該授權完成，不為相同動作重複提問；未涵蓋的動作仍停在確認點。Startup 維持唯讀，完成讀取報告後可轉入已授權的獨立工作階段。

## Project lifecycle manifest

- Portable manifest：`.agents/project-lifecycle.json`
- Part：只做分類／路由，不是 Git repository。
- Project root：每次以 `git rev-parse --show-toplevel` 驗證，必須等於 manifest 所在 repository root。
- Canonical path：只用專案相對路徑；裝置絕對路徑與 credential 留在 ignored `policy.local.yaml`。
- Checkpoint mode：`manual`（預設）或經工作單核准的 `standing_scoped`。
- Startup：fetch／對照遠端 SHA 後停止，不建立空 commit。
- Shutdown：更新 changelog／handoff；`manual` 等確認，`standing_scoped` 只 commit／push allowlist 內變更並回讀 SHA。
- Denylist：建立 repository、force push、auto merge／rebase、tag／release、PR merge、刪除／封存、權限變更。

## 目標

<一句話說明接收者能用本專案完成什麼；未知就寫「待確認」。>

## Workflow profile

- Profile：`lite`
- Full Core：`NOT_CONFIGURED`
- ReadyGate：`ON_DEMAND`

## 生命週期路由

- `initial`：只用於第一次建立治理結構、修復缺件或明確部署技能；完成後停止。
- `startup`：每次開工唯讀回報，完成後停止並等待工作選擇。
- `shutdown`：每次收工更新 `CHANGELOG.md` 與 `handoff.md`；不自動 commit 或 push。
- `ReadyGate`：只有重大返工、高風險、不可逆或外部交付工作按需插入；`READY` 不等於自動取得外部授權。

## 專案結構

- `README.md`：人類與 Agent／Tool 安裝、使用及公開版本文案。
- `CHANGELOG.md`：每次收工的近期修改、驗證與 delivery 狀態。
- `handoff.md`：目前狀態、下一步與唯一續跑點。
- `<relative/path>`：<其他用途>

## 權威

- 程式與專案規則：本 repository。
- 穩定規則：`AGENTS.md`。
- 對外說明：`README.md`。
- 版本紀錄：`CHANGELOG.md`。
- 目前交接：`handoff.md`。
- 個人全域設定：repository 外的 private dotfiles。

## 共用規則

1. 每個 Agent 開工先讀本檔、`handoff.md` 與 Git 狀態。
2. Canonical 路徑只使用專案相對路徑。
3. 保留既有修改；不覆寫或 stage 未知檔案。
4. 不提交 Secret、credential、認證快取、裝置絕對路徑或私人識別資訊。
5. 一般工作使用 Lite；只有觸發特定能力時才讀 Full SOP。
6. 每次收工更新 `CHANGELOG.md` 與 `handoff.md`。
7. GitHub delivery 前更新 `README.md`；發布、刪除、搬移、封存、批次遷移與權限變更使用 ReadyGate。
8. 外部知識庫一律 `ON_DEMAND_ONLY`，不屬於 initial／startup／shutdown。

## 整合

- GitHub：`<remote-reference>` 或 `NOT_CONFIGURED`
- 外部知識庫：`ON_DEMAND_ONLY`
- 其他：`<integration>` 或 `NONE`

## 專案 policy

個人或團隊差異寫入 ignored 的 `policy.local.yaml`；不要把私人值填回本模板。
