# Changelog

## [Unreleased] - 2026-09-05 authority pin

- 三個 source checkpoint 已以 Git 與 GitHub API 回讀；補上本專案 manual manifest。
- newday Initial 保留四檔、Startup 保留五檔 hash 與 HEAD、Shutdown scoped push／readback 均通過。
- dotfiles active source／Drive mirror 與 runtime 四技能 hash 已對齊。
- FEATURES 移除 LOCAL_ONLY 舊狀態；template 使用已發布的固定 SHA。

## [Unreleased] - 2026-09-05

- `WO-DRIVE-GITHUB-ALIGN-20260905-v2`：完成portable lifecycle schema、template、唯讀 Git classifier 與 Full Core 維護流程；保留既有功能與治理差異。
- 已確認工作單持續授權其列出的動作，manual 不重複索取相同授權。
- 驗證：Core validator 25 files PASS；project lifecycle unittest 9/9 PASS。 提交前重跑 validator 與 diff whitespace 檢查。
- Delivery：本輪 source checkpoint；不建立新 tag／Release。

## [Unreleased 0.2.0] - 2026-08-13

### Changed
- 專案名稱統一為 Cross-Device Agent Workflow Core；GitHub repository 名稱不變。
- Core profile 明確要求 Lite 三技能加 ReadyGate，共四技能。
- 專案生命週期改用 `AGENTS.md`、`README.md`、`CHANGELOG.md`、`handoff.md` 四檔契約。
- 移除 initial／startup／shutdown 對 Notion、Obsidian 與 Knowledge Master 的耦合。
- 補齊 GitHub、工作 checkout、chezmoi source、runtime 與 mirror 的權責定義。
- 明確對齊 `initial → startup → 工作 → shutdown` 的縱向生命週期與 ReadyGate 橫向雙閘門，補上每個流程的停止點與外部授權邊界。
- 更新 Full Core README、WORKFLOW、repository guidance 與專案 AGENTS 模板；仍只保存整合契約，不複製 Lite／ReadyGate canonical Skill。
- 新增 `.schemas/project-lifecycle.schema.json`、`templates/project-lifecycle.template.json` 與唯讀 `scripts/project_lifecycle.py`，統一 Part→Project 路由、專案相對路徑、authority revision、content／large-file policy、checkpoint 與 rollback。
- 定義 `manual`／`standing_scoped`：Initial bootstrap、Startup fetch／remote SHA 對照、Shutdown scoped checkpoint；建立 repository、force push、auto merge／rebase、tag／release、PR merge、刪除／封存與權限變更固定拒絕。
- 新增 clean、dirty、ahead、behind、diverged、wrong remote、絕對路徑與 malformed allowlist 的正反例測試。

### Validation
- Core validator `PASS`（19 files）；Bootstrap doctor 回報 `FULL` 且 `writes_performed=false`。
- `FEATURES.json` 解析通過；Lite 三技能 validator 與跨來源 SHA-256 對齊通過。
- ReadyGate Skill／Plugin validators 與 8 項合約測試通過。
- 2026-08-13 Core validator `PASS`（19 files）；Bootstrap doctor 回報 `FULL`、建議日常使用 Lite、`writes_performed=false`。
- `git diff --check` 通過；Lite 三技能與 ReadyGate runtime 雜湊回讀一致。
- v2 Core validator `PASS`（25 files）；project lifecycle 9／9 測試 `PASS`；template custom validation `PASS`；Bootstrap doctor=`FULL`、建議 Lite、`writes_performed=false`。
- 三個 authority repository `git diff --check` 全部通過；Lite 三技能與 ReadyGate canonical／runtime SHA-256 逐一一致。

### Delivery
- 本輪生命週期邊界更新：`LOCAL_ONLY／PENDING_GATE`，未 commit、未 push。
- v2 schema／checkpoint 更新：`LOCAL_ONLY／PENDING_GATE`；沒有部署個別 Project manifest，未 stage、未 commit、未 push。
- 基底 GitHub：本機 `HEAD` 與 `origin/main`／`ls-remote` 均為 `0868a4cc157ae16be32084284450d7e20f6fa341`。
- tag／Release：未執行；正式 release 基準仍是 `v0.1.0`。

## [0.1.0] - 2026-07-28

### Added
- 發布 Full Core、雙層 Lite 架構、十項 SOP、ReadyGate 觸發契約與只讀 Bootstrap advisor。

### Delivery
- GitHub：tag `v0.1.0`
