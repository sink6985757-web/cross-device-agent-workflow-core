# AI Bootstrap Contract

本檔是給收到 GitHub 連結的 AI 讀取。**不要一讀到連結就安裝或修改。**

## 0. 安全契約

- 先讀、再判斷、再建議，最後等待確認。
- 不讀取或輸出 token、credential、`.env`、私鑰、cookie 或認證快取內容。
- 不把裝置絕對路徑寫入 canonical 文件。
- 不覆寫既有 `AGENTS.md`、`handoff.md`、skills 或私人 dotfiles。
- 不代替使用者登入 GitHub。
- 沒有明確授權時，不 commit、push、發布、刪除或寫入外部服務。

## 1. 讀取順序

只讀檢查：

1. 目前目錄的 `AGENTS.md`、`handoff.md`、README 與 Git 狀態。
2. `~/.agents/GLOBAL.md` 是否存在。
3. `~/.agents/skills/initial`、`startup`、`shutdown`、`readygate` 是否存在。
4. Agent adapter 狀態；只辨識是否存在，不複製 Skill。
5. PowerShell、Git、GitHub CLI、chezmoi 是否可用。
6. GitHub CLI 是否已登入；只回報是／否，不顯示 token。
7. 是否存在重複 Skill、不同來源、未套用 chezmoi 狀態或 dirty worktree。

可先執行只讀建議器：

```powershell
powershell -NoProfile -File .\scripts\install.ps1
```

## 2. 分類

| 狀態 | 判準 | 建議 |
|---|---|---|
| `NONE` | 沒有共用三技能 | 提供 Lite 或 Full 的 dry-run |
| `LITE` | 三技能存在，沒有完整治理需求 | 保持 Lite，不增加讀取面 |
| `FULL` | 三技能、ReadyGate 與 Full Core 契約均可用 | 只做 doctor，不重裝 |
| `DRIFT` | live、dotfiles、checkout 或 remote 基準不一致 | 停止安裝，先產生來源比較 |
| `BLOCKED` | 權限、來源、Secret 或覆寫風險不明 | 停止並列出 owner／解法 |

## 3. 模式建議

### Lite Project

適合一般專案與低 token 接續：

- 只使用外部 `initial`、`startup`、`shutdown`。
- 專案日常只讀 `AGENTS.md`、`handoff.md` 與 Git 狀態。
- 不自動讀完整十項 SOP。
- 需要高風險操作時才按需載入 ReadyGate 或 Full Core 段落。

### Full Core

適合首次裝置部署、多人協作、公開發布、研究、PR、MCP、監控或批次治理：

- 先確認 Git、GitHub CLI、chezmoi 與登入責任。
- Lite 與 ReadyGate 使用 `FEATURES.json` 登記的相容版本。
- 私人 dotfiles 只在已驗證來源且使用者明確確認時處理。
- 新專案可套用模板；舊專案只能先輸出 patch 建議。

## 4. 固定回報

AI 必須先輸出：

```text
Bootstrap 狀態：NONE | LITE | FULL | DRIFT | BLOCKED
目前 Agent：
目前專案：
已偵測：
缺少工具：
來源分歧：
建議模式：
預計讀取：
預計寫入：
外部動作：
rollback：
需要確認：
```

使用者明確確認前，`預計寫入` 與 `外部動作` 必須保持「無」。

## 5. 依賴處理

- 起點只要求 Windows PowerShell 與網路。
- 完整部署需要 Git、GitHub CLI、chezmoi。
- 缺少工具時逐項列出用途與安裝選項；不得靜默安裝。
- GitHub 登入由使用者完成。
- 其他 Agent 無原生 Skill 支援時，只建立薄轉接或使用 `AGENTS.md` fallback。

## 6. 寫入與回復

未來 Apply 實作必須：

1. 預設 dry-run。
2. 列出精確目標與來源 revision。
3. 既有檔案不相同時停止，不直接覆寫。
4. 先建立可回復備份或 patch。
5. 寫入後逐檔回讀。
6. 執行 `scripts/validate.ps1`。
7. 只有原始授權包含 commit／push 時才執行。

目前 `scripts/install.ps1 -Apply` 會明確停止，因為 Apply 仍是 `PLANNED`。
