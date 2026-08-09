# Cross-Device Agent Workflow Core

## 目標

提供公開安全、可跨裝置重建的 Full Core；Lite 處理日常專案生命週期，Core 負責首次部署、完整治理、相容檢查與 ReadyGate 整合。

## 最小讀取面

1. 一般接續只讀本檔、`handoff.md` 與 Git 狀態。
2. 第一次部署才讀 `BOOTSTRAP.md`。
3. 只有觸發特定能力時才讀 `WORKFLOW.md` 對應段落。
4. 維護或發布才讀 `MAINTAINERS.md`、`FEATURES.json` 與 `CHANGELOG.md`。

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
