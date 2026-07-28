# Handoff

## 目前做到哪

Full Core `v0.1.0` 已定稿為公開正式基準，提供雙層 Full／Lite 架構、十項 SOP、ReadyGate 觸發契約與只讀 Bootstrap advisor。Lite canonical 固定使用外部 `v1.1.1`，ReadyGate 固定使用外部 `v0.2.1`，本 repository 不複製兩者內容。

## 目前狀態

- 可執行：是
- 已驗證：repository validator、只讀 advisor、`FULL／LITE／NONE` 分類、Apply guard、Markdown 相對連結與公開安全掃描
- 未完成：Apply 實作與七個舊專案的逐案遷移；兩者都需要獨立工作單
- GitHub：`https://github.com/sink6985757-web/cross-device-agent-workflow-core`
- Release：`v0.1.0`

## 下一步

1. 在 disposable project 驗證未來 Apply 的 dry-run／collision／rollback 契約。
2. 另開工單評估 Lite `v1.1.2／v1.2.0` 銜接。
3. 七個舊專案維持原狀，逐案建立修復工單。

## 注意事項

- `scripts/install.ps1 -Apply` 仍會刻意停止；不得把 `PLANNED` 誤認為已實作。
- 公開核心不得加入私人 dotfiles、裝置絕對路徑、credential 或 Notion 私人內容。

## 最近更新

- 時間：2026-07-28 22:40 +08:00
- 更新者：Codex
- 成果 revision：`v0.1.0`
- Git push：`v0.1.0` release source；外部狀態以 GitHub 回讀為準
- Obsidian：由 workspace 收工紀錄管理
