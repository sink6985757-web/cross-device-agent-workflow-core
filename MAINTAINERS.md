# Maintainers Guide

本檔供 Full Core 維護、相容性升級與公開發布使用。一般專案不需要日常讀取。

## Repository 責任

| Repository／位置 | 狀態 | 責任 |
|---|---|---|
| `sink6985757-web/cross-device-agent-workflow-core` | Canonical remote | Full Core 發行與版本歷史 |
| 任一由該 remote clone 的工作 checkout | Working copy | 本機修改與驗證；以 remote＋revision 識別 |
| `sink6985757-web/cross-device-agent-skills` | Canonical remote | Lite 三技能發行；不得複製進 Core |
| `sink6985757-web/readygate-skill-chatgpt-app` | Canonical remote | ReadyGate Skill／Plugin 發行 |
| private `sink6985757-web/dotfiles` | Canonical remote | chezmoi source 的遠端歷史 |
| `chezmoi source-path` | Active local source | 目前裝置的個人核心來源 |
| `~/.agents/skills` | Runtime | Agent 執行副本，不是公開發行來源 |

同一 remote 的多個 checkout 是鏡像／工作副本，不是新專案。舊名稱 checkout 可在 Delivery Gate 後封存，但不得在未確認前移動或刪除。

## 版本策略

| 元件 | 已發布基準 | 本機候選 |
|---|---|---|
| Full Core | `v0.1.0` | `v0.2.0` |
| Lite | `v1.1.1` | `v2.0.0` |
| ReadyGate | `v0.2.1` | 無行為變更 |

候選版在 commit／push／tag 前只能標示 `LOCAL_ONLY`，不得寫成已發布。

## Full Core 變更流程

1. 確認工作 checkout 的 Git top level、remote、revision 與髒狀態。
2. 更新 `FEATURES.json`、受影響文件、`CHANGELOG.md` 與 `handoff.md`。
3. 若準備 GitHub delivery，更新 README 的安裝、使用、版本與最新變更文案。
4. 執行 `scripts/validate.ps1`、只讀 `scripts/install.ps1`、JSON 解析、連結與 `git diff --check`。
5. 比對 Lite／ReadyGate 的來源、runtime 與 dotfiles 副本；未知差異標 `PARTIAL`。
6. 執行 Secret／個資／絕對路徑檢查。
7. ReadyGate Delivery Review；只有另行授權後才 commit、push、tag 或 release。

## 新專案套用

1. 預設使用 Lite。
2. 只補齊缺少的 `AGENTS.md`、`README.md`、`CHANGELOG.md`、`handoff.md`。
3. 不覆寫既有檔；資料不足保留 `<待確認>`。
4. Full profile 需要四技能，且只在首次部署、完整治理或高風險工作啟用。
5. 外部知識庫不屬於專案生命週期。

## 舊專案套用

```text
inventory → classify → diff → collision check → rollback plan
→ confirmed work order → one-project pilot → validation → delivery gate
```

不得移動既有治理檔後重新注入、覆寫 `.archive/`、把多個專案合併成一份 handoff，或把 Google Drive 根目錄當成可發布 monorepo。

## 相依升級

1. 比較 remote、工作 checkout、`~/.agents/skills`、active chezmoi source 與 Google Drive mirror。
2. 將差異分類為已發布 canonical、未發布候選、舊版、或私人內容。
3. 只有人工確認後才同步；不以硬重設清除未知工作。
4. Lite 升級必須驗證三技能各只有一個 `SKILL.md`；Core profile 另驗證 ReadyGate。
5. 所有 profile 必須在沒有外部知識庫時仍可獨立運作。

## 發布閘門

以下全部有可回讀證據才可標 `READY`：repository validator、依賴版本、文件與行為一致、Secret／個資檢查、rollback、README／CHANGELOG、tag／release notes 與公開範圍。任何 critical 項為 `UNKNOWN` 時不得宣稱可發布。
