# <PROJECT_NAME>

## 目標

<一句話說明接收者能用本專案完成什麼；未知就寫「待確認」。>

## Workflow profile

- Profile：`lite`
- Full Core：`NOT_CONFIGURED`
- ReadyGate：`ON_DEMAND`

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
