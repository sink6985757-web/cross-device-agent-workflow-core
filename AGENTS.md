# Cross-Device Agent Workflow Core

當本次對話或已確認工作單已明列更新、commit／push 與驗收範圍，沿用該授權完成，不為相同動作重複提問；未涵蓋的動作仍停在確認點。Startup 維持唯讀，完成讀取報告後可轉入已授權的獨立工作階段。

## 目標

提供公開安全、可跨裝置重建的 Full Core；Lite 處理日常專案生命週期，Core 負責首次部署、完整治理、相容檢查與 ReadyGate 整合。

## 最小讀取面

1. 一般接續只讀本檔、`handoff.md` 與 Git 狀態。
2. 第一次部署才讀 `BOOTSTRAP.md`。
3. 只有觸發特定能力時才讀 `WORKFLOW.md` 對應段落。
4. 維護或發布才讀 `MAINTAINERS.md`、`FEATURES.json` 與 `CHANGELOG.md`。

## 生命週期路由

| 流程 | 定義 | Core／ReadyGate 接點 |
|---|---|---|
| `initial` | 新專案第一次建立治理結構、既有專案缺件修復或明確技能部署；完成後停止 | 首次完整裝置部署可讀 `BOOTSTRAP.md`；高風險外部動作另進 ReadyGate |
| `startup` | 每次工作階段的唯讀接續；回報後停止等待 | 一般開工只用 Lite，不載入完整 SOP，也不啟動 ReadyGate |
| 工作執行 | 在已確認範圍內修改與驗證 | 批次、重大返工、高風險、不可逆或外部動作先進 Requirement Gate |
| `shutdown` | 每次工作結束更新本機版本紀錄與交接 | 外部 delivery 只有在工作單涵蓋且 Delivery Gate 放行時才執行；否則停在 `LOCAL_ONLY`／`PENDING_GATE` |

ReadyGate 是橫向閘門，不是 `initial`／`startup`／`shutdown` 之後的第四個固定步驟。`READY` 是證據結論，不會自行增加外部授權。

## 權威與相依

- Full Core：本 repository。
- Lite：`FEATURES.json` 登記的 `cross-device-agent-skills`；只提供 `initial`、`startup`、`shutdown`。
- Core profile：Lite 三技能加 `readygate`，四者都必須可讀且版本相容。
- ReadyGate：`FEATURES.json` 登記的外部 repository／`~/.agents/skills/readygate` runtime 副本。
- 個人全域設定：private dotfiles；本 repository 不保存或修改其私人值。
- 專案狀態：各專案自己的 `AGENTS.md`、`README.md`、`CHANGELOG.md`、`handoff.md` 與 Git 歷史。

## 維護對齊

- 本 repository 是 Full Core 更新與發布準備的對齊點；工作 checkout 由 Git remote 與 revision 識別，不由資料夾名稱決定權威。
- 其他專案維持各自 repository；不得集中成 monorepo。
- Google Drive 是同步層，GitHub remote 是版本歷史權威，runtime 只是執行副本。
- 在此準備更新不等於授權 commit、push、tag、release、搬移或封存。

## 共用規則

1. Canonical 路徑使用 repository 相對路徑或 `~`；裝置絕對路徑只在 runtime 解析。
2. 不保存 token、credential、`.env`、私鑰、cookie、認證快取、裝置名稱或私人 vault 位置。
3. 保留既有修改；舊專案先比較與建立 rollback，再依確認工作單處理。
4. `startup` 唯讀；每次 `shutdown` 更新 `CHANGELOG.md` 與 `handoff.md`。
5. GitHub delivery 前更新 `README.md` 的安裝、使用、版本與最新變更文案。
6. commit、push、發布、刪除、搬移、封存、權限與批次操作由工作單／ReadyGate 放行。
7. Lite 與 ReadyGate 維持外部單一 canonical；本 repository 只保存相容基準與觸發契約。
8. 外部知識庫一律 `ON_DEMAND_ONLY`，不得併入 initial／startup／shutdown。

## 驗證

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1
git diff --check
```

## Portable lifecycle manifest（v2）

1. Full Core 維護共同 schema `.schemas/project-lifecycle.schema.json`、template `templates/project-lifecycle.template.json` 與唯讀 validator `scripts/project_lifecycle.py`。
2. `Part` 只是權威系統的分類／路由，不是固定 Part 9，也不等於 repository。每個實際 Project 都要以 `git rev-parse --show-toplevel` 驗證自己的 Git 邊界；一個 Part 有多個 repository 時，各自部署 `.agents/project-lifecycle.json`。
3. canonical manifest 只保存 `/` 分隔的專案相對路徑與不可變 authority tag／commit。裝置絕對路徑、名稱、credential 與登入狀態只存在 runtime 或 ignored `policy.local.yaml`。
4. checkpoint mode 預設 `manual`；只有先前經工作單核准的 `standing_scoped`，Initial／Shutdown 才能在既有 identity-matching remote、目前工作 branch、manifest allowlist、非 force push與 remote SHA readback 的限制內自動 checkpoint。
5. Startup 對專案內容唯讀：fetch 並分類 `CLEAN_SYNCED`、`DIRTY`、`AHEAD`、`BEHIND`、`DIVERGED`、`WRONG_REMOTE`，不建立空 commit，不 pull／merge／rebase。
6. 建立 repository、force push、auto merge／rebase、tag／release、PR merge、刪除／封存與權限變更永遠不在 standing scope。
7. 已發布錯誤用 `git revert`；查看舊 SHA 用 restore branch；乾淨且只有 behind 才能在獨立步驟 `pull --ff-only`；diverged 保存 local／remote refs 並停止；clone 只進空目錄。
