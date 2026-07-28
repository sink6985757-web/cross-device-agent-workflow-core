# Cross-File AI Workflow Core

## 目標

提供一套公開安全、個人與團隊皆可重用的雙層 AI 工作流：Full Core 負責首次部署與治理，Lite Project 負責低 token 的日常初始化、開工與收工。

## 最小讀取面

1. 一般開工只讀本檔、`handoff.md` 與 Git 狀態。
2. 第一次部署才讀 `BOOTSTRAP.md`。
3. 只有觸發特定能力時才讀 `WORKFLOW.md` 的對應段落。
4. 維護或發布才讀 `MAINTAINERS.md` 與 `FEATURES.json`。

## 權威

- Full Core：本 repository。
- Lite 三技能：`FEATURES.json` 登記的外部版本。
- ReadyGate：`~/.agents/skills/readygate` 或其登記來源。
- 個人全域設定：使用者自己的私人 dotfiles；本 repo 不保存或修改。
- 專案狀態：專案自己的 `AGENTS.md` 與 `handoff.md`。

## 共用規則

1. Canonical 路徑一律相對 repository 或使用 `~` 表示家目錄；裝置綁定只在 runtime 解析。
2. 不保存 token、credential、`.env`、私鑰、cookie、認證快取、裝置名稱或私人 vault 絕對路徑。
3. 不靜默覆寫既有檔案；舊專案先 dry-run，再產生差異與 rollback。
4. 不把「收工」自動擴張成未確認的公開發布、刪除或批次遷移。
5. 外部寫入、commit、push、發布、刪除與權限變更依 policy 與 ReadyGate 決定。
6. Lite 與 ReadyGate 保持單一外部 canonical；本 repo 只保存相容基準與觸發契約。
7. Notion 只有使用者明確要求時才寫入。

## 驗證

修改後執行：

```powershell
powershell -NoProfile -File .\scripts\validate.ps1
powershell -NoProfile -File .\scripts\install.ps1
```

第一個命令驗證 repository；第二個命令只做環境偵測與建議，不會寫入。
