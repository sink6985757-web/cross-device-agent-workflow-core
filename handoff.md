# Handoff

## 目前做到哪

本 checkout 被保留為目前 Cross-Device Agent Workflow Core 工作對齊點。`v0.2.0` 本機候選已完成名稱、四檔契約、Core 四技能 profile、repository 權責與外部知識庫獨立邊界更新；不複製 Lite 或 ReadyGate canonical。

## 狀態

- 可執行：`YES`
- Core validator：`PASS`（19 files）。
- Bootstrap doctor：`FULL`，建議日常仍使用 Lite，`writes_performed=false`。
- Lite：三份 Skill validator 通過，四處 SHA-256 一致。
- ReadyGate：Skill／Plugin validators 與 8 項合約測試通過；行為仍是 `v0.2.1`。
- GitHub：`LOCAL_ONLY`；已發布 Core 基準仍是 `v0.1.0`。
- commit／push／tag／release：未執行。

## Repository 關係

- GitHub `cross-device-agent-workflow-core`：版本權威。
- 本 checkout：目前工作副本，必須保留。
- workspace `cross-device-agent-workflow-core/`：命名鏡像，等待 GitHub delivery 後再同步。
- workspace `cross-file/`：舊名封存候選；未移動、未刪除。

## 下一步

1. ReadyGate 結論：本機 Core 候選已驗證；GitHub delivery 與 archive 尚未放行。
2. 取得另行授權後才分 repo commit／push。
3. 成功回讀 GitHub 後再同步 named mirror；legacy checkout 另走封存停點。

## 風險

- `v0.2.0`、Lite `v2.0.0` 都是未發布候選。
- 在 GitHub delivery 前，其他 checkout 保持原狀才是可回復策略。

## 最近更新

- 時間：2026-08-09 Asia/Taipei
- Agent：Codex
- 成果 revision：未提交工作樹
