# Changelog

## [Unreleased 0.2.0] - 2026-08-09

### Changed
- 專案名稱統一為 Cross-Device Agent Workflow Core；GitHub repository 名稱不變。
- Core profile 明確要求 Lite 三技能加 ReadyGate，共四技能。
- 專案生命週期改用 `AGENTS.md`、`README.md`、`CHANGELOG.md`、`handoff.md` 四檔契約。
- 移除 initial／startup／shutdown 對 Notion、Obsidian 與 Knowledge Master 的耦合。
- 補齊 GitHub、工作 checkout、chezmoi source、runtime 與 mirror 的權責定義。

### Validation
- Core validator `PASS`（19 files）；Bootstrap doctor 回報 `FULL` 且 `writes_performed=false`。
- `FEATURES.json` 解析通過；Lite 三技能 validator 與跨來源 SHA-256 對齊通過。
- ReadyGate Skill／Plugin validators 與 8 項合約測試通過。

### Delivery
- GitHub：`VERIFIED`，治理 commit `b6e27e330c5e07a1b1d8d41077d28b1a21811331` 已推送 `main` 並回讀一致。
- tag／Release：未執行；正式 release 基準仍是 `v0.1.0`。

## [0.1.0] - 2026-07-28

### Added
- 發布 Full Core、雙層 Lite 架構、十項 SOP、ReadyGate 觸發契約與只讀 Bootstrap advisor。

### Delivery
- GitHub：tag `v0.1.0`
