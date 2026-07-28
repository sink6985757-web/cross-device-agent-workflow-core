# <PROJECT_NAME>

## 目標

<一句話說明接收者能用本專案完成什麼；未知就寫「待確認」。>

## Workflow profile

- Profile：`lite`
- Full Core：`NOT_CONFIGURED`
- ReadyGate：`ON_DEMAND`

## 路線圖

- [ ] <階段一與驗收>
- [ ] <階段二與驗收>

## 專案結構

- `<relative/path>`：<用途>

## 權威

- 程式與專案規則：本 repository
- 交接：`handoff.md`
- 長期知識：`<vault-relative-path>` 或 `NOT_CONFIGURED`
- 個人全域設定：repository 外的私人 dotfiles

## 共用規則

1. 每個 Agent 開工先讀本檔、`handoff.md` 與 Git 狀態。
2. Canonical 路徑只使用專案相對路徑。
3. 保留既有修改；不覆寫未知檔案。
4. 不提交 Secret、credential、認證快取、裝置絕對路徑或私人識別資訊。
5. 一般工作使用 Lite；只有觸發特定能力時才讀 Full SOP。
6. 公開發布、刪除、批次遷移與權限變更使用 ReadyGate。
7. Notion 只有使用者明確要求時才寫入。

## 整合

- GitHub：`<remote-relative-reference>` 或 `NOT_CONFIGURED`
- Obsidian：`<vault-relative-path>` 或 `NOT_CONFIGURED`
- Notion：`EXPLICIT_ONLY`
- 其他：`<integration>` 或 `NONE`

## 專案 policy

個人或團隊差異寫入 ignored 的 `policy.local.yaml`；不要把私人值填回本模板。
