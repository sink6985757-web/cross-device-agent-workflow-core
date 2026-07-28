# Maintainers Guide

本檔供維護 Full Core、準備公開發布及規劃 Lite 後續版本的人使用。日常 Lite 專案不需要讀取。

## 權威與禁止事項

- Full Core canonical：本 repository。
- Lite 三技能 canonical：外部 `cross-device-agent-skills`。
- ReadyGate canonical：外部 ReadyGate repository／全域 Skill。
- 私人 `GLOBAL.md` 與 adapters：使用者自己的 dotfiles。

不得：

- 將 Lite 或 ReadyGate 完整複製到本 repo 後形成第二份 canonical。
- 從私人 dotfiles 直接發布檔案。
- 把 local worktree 當成 remote revision。
- 在公開檔保存帳號、裝置名稱、絕對路徑、vault 位置或 credential。
- 對舊專案執行批次覆寫。

## 版本策略

| 版本 | 意義 |
|---|---|
| `0.x` | Full Core 契約仍在收斂 |
| `1.x` | README、BOOTSTRAP、FEATURES 與模板契約穩定 |
| major | 入口、profile、模板或授權契約有破壞性變更 |

依賴採明確相容基準，不追蹤浮動的 `main`。目前：

- Lite：`v1.1.1`
- ReadyGate：`v0.2.1`

升級時先更新 `FEATURES.json`，再做 disposable project 驗證。

## Full Core 變更流程

1. 建立 Issue，寫清目標、不納入項目與相容性。
2. 更新 `FEATURES.json` 狀態。
3. 只修改本 repo 的 owner 範圍。
4. 執行：

   ```powershell
   powershell -NoProfile -File .\scripts\validate.ps1
   powershell -NoProfile -File .\scripts\install.ps1
   ```

5. 在乾淨 disposable directory 驗證 Recommend／Lite／Full 分類。
6. 檢查 personal identifier、Secret、絕對路徑與 staged diff。
7. ReadyGate Delivery Review。
8. 經確認後才 commit、push、建立 tag 或 release。

## 新專案套用

1. 預設選 Lite。
2. 既有檔案相同就保留。
3. 缺少 `AGENTS.md` 或 `handoff.md` 才從模板建立。
4. `.gitignore` 已存在時只產生差異建議。
5. Full profile 只在專案需要十項能力時啟用。
6. 個人 policy 使用 `policy.local.yaml`，且必須保持 ignored。

## 舊專案套用

舊專案只能走：

```text
inventory → classify → diff → collision check → rollback plan
→ user approval → one-project pilot → validation → batch proposal
```

不允許：

- 移動既有 `AGENTS.md`、`handoff.md` 或 `skills/` 後重新注入。
- 覆寫既有 `.archive/`。
- 以同一份 handoff 取代多個專案狀態。
- 把 Google Drive 資料夾直接視為可公開 monorepo。

## Lite vNext 銜接計畫

### 已確認現況

- Lite 公開相容基準為 `v1.1.1`。
- Lite checkout、tag 與 `origin/main` 已對齊在 `v1.1.1`。
- Full Core `v0.1.0` 只登記 Lite 相容基準，不修改 Lite canonical。
- ReadyGate 使用外部 `v0.2.1`；公開核心不複製其 Skill 內容。

### 來源分歧處理

若未來再次出現 drift：

1. 凍結 dirty worktree，保存 `git status` 與 patch 證據。
2. fetch 後重新比較 `origin/main`、live `~/.agents/skills`、dotfiles source 與 local checkout。
3. 對每個差異標成：
   - remote canonical；
   - 尚未發布的新變更；
   - 舊版回退；
   - 個人化內容，不可公開。
4. 只有人工確認後才處理 local checkout；不得使用會丟失資料的硬重設。

### 建議發布節奏

#### `v1.1.2`：修復與文件版

- 不改三個口令與日常讀取面。
- 補充 Full Core 連結、相容基準與來源檢查。
- 增加「local checkout dirty 時停止安裝」說明。
- 加入不覆寫既有檔案的回歸測試。

#### `v1.2.0`：可選橋接版

- 新增機器可讀 `compatibility.json`。
- `initial` 預設仍為 Lite，可選登記 Full Core。
- `startup` 不讀完整 Full SOP，只在高風險工作提示可用能力。
- `shutdown` 回報 Full Core／dotfiles drift，但不自動修復。

#### `v2.0.0`：授權契約變更時才需要

若要改變「收工是否自動 commit／push」、模板欄位或既有輸出契約，視為破壞性變更，另走 ReadyGate 與遷移指南。

### Lite vNext 驗收

- 每次 startup 只讀 `AGENTS.md`、`handoff.md` 與 Git 摘要。
- 不讀 Full `WORKFLOW.md`，除非觸發。
- initial 不覆寫既有檔案。
- local、dotfiles、live、remote 的 revision 可追溯。
- 不保存裝置絕對路徑、credential 或不必要的裝置識別。
- Full Core 不存在時，Lite 仍可獨立工作。

## 發布閘門

發布前全部為 `VERIFIED`：

- repository validation PASS。
- 依賴版本存在且可讀。
- 文件、FEATURES 與實際行為一致。
- Secret／個資／絕對路徑掃描無 critical 缺口。
- disposable project 的 Lite 與 Full 分類通過。
- rollback、tag 與 release notes 已準備。
- license 與公開範圍已由 maintainer 確認。

任何一項為 `UNKNOWN` 時不得宣稱可發布。
