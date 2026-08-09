# Handoff

## 目前做到哪

本 checkout 被保留為目前 Cross-Device Agent Workflow Core 工作對齊點。`v0.2.0` GitHub `main` 候選已完成名稱、四檔契約、Core 四技能 profile、repository 權責與外部知識庫獨立邊界更新；不複製 Lite 或 ReadyGate canonical。

## 狀態

- 可執行：`YES`
- Core validator：`PASS`（19 files）。
- Bootstrap doctor：`FULL`，建議日常仍使用 Lite，`writes_performed=false`。
- Lite：三份 Skill validator 通過，四處 SHA-256 一致。
- ReadyGate：Skill／Plugin validators 與 8 項合約測試通過；行為仍是 `v0.2.1`。
- GitHub：`VERIFIED`；治理 commit `b6e27e330c5e07a1b1d8d41077d28b1a21811331` 已推送 `main` 並回讀一致。
- tag／Release：未執行；正式 release 基準仍是 `v0.1.0`。

## Repository 關係

- GitHub `cross-device-agent-workflow-core`：版本權威。
- 本 checkout：目前工作副本，必須保留。
- workspace `cross-device-agent-workflow-core/`：命名鏡像，等待 GitHub delivery 後再同步。
- workspace `cross-file/`：舊名封存候選；未移動、未刪除。

## 下一步

1. 將 named mirror 安全快轉到 GitHub `main` 並回讀。
2. 若要正式發布 `v0.2.0`，另走 tag／Release Gate。
3. `cross-file/` legacy checkout 仍維持獨立封存停點。

## 風險

- `v0.2.0`、Lite `v2.0.0` 都是未發布候選。
- 在 GitHub delivery 前，其他 checkout 保持原狀才是可回復策略。

## 最近更新

- 時間：2026-08-09 Asia/Taipei
- Agent：Codex
- 成果 revision：未提交工作樹
