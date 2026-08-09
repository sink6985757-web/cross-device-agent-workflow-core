# AI Workflow SOP

本 SOP 是 Full Core 的按需工作面。一般專案預設維持 Lite；只有工作觸發某一能力時才讀該段。

## 共通生命週期

每項工作都使用同一條最小狀態線：

```text
INTAKE → PLAN → CONFIRMED → EXECUTION → VERIFICATION → DELIVERY → HANDOFF
```

必須保存：

- 目標與明確不納入項目。
- owner、檔案或系統邊界。
- 驗收條件與證據來源。
- 停止條件、rollback 與唯一續跑點。
- 外部寫入或不可逆動作的授權。

小型、可回復、單檔工作可以縮短流程；公開發布、刪除、批次遷移、權限變更或多系統寫入不得略過確認。

## ReadyGate 橫向閘門

ReadyGate 主要屬於第 10 項 Human-in-the-loop，同時支援第 1、3、4、9 項。完整方法保留在外部 ReadyGate Skill；本檔只保存觸發契約。

### 必須啟動

- 使用者明確要求 ReadyGate。
- 公開發布、刪除、批次移動／改名／遷移。
- 權限、付款、敏感資料或外部多系統寫入。
- 大型任務需求仍會造成重大返工。
- 要判斷是否能交付、release 或 handoff。

### 不自動啟動

- 一般 Lite 開工。
- 純知識問答。
- 小型、範圍明確且可回復的單檔修改。

### 與工作流的接點

```text
Requirement Gate
  → WORK_ORDER_DRAFT
  → 使用者確認
  → EXECUTION
  → Delivery Review
  → READY / CONDITIONAL / NOT_READY / BLOCKED
```

不得把 `WORK_ORDER_CONFIRMED` 當成測試證據，也不得把 `READY` 當成未授權的發布許可。

## 1. 長時段 Agent 任務拆解與自主續跑

### 觸發

預估需要多階段、跨多次對話、背景執行或無法一次驗收。

### 必要工作卡

| 欄位 | 規則 |
|---|---|
| 目標 | 一句話，可驗收 |
| 階段 | 每階段產出獨立證據 |
| Checkpoint | 完成、驗證、風險與下一步 |
| 停止條件 | 權限不足、測試失敗、來源變更、成本超限 |
| 續跑點 | 下一次可直接執行的唯一第一步 |
| 完成條件 | 不是「寫完程式」，而是驗收條件有證據 |

### 規則

1. 一次只讓一個階段處於 `in_progress`。
2. Checkpoint 必須能由下一個 Agent 單獨讀懂。
3. 長 log 只保存摘要與可追溯位置，不塞進 `handoff.md`。
4. 遇到停止條件立即保存狀態，不自行擴張權限。

## 2. 多 Agent 平行分工與工作樹隔離

開始前建立：

| 分工 | Owner | 檔案／目錄邊界 | 工作樹／分支 | 驗收 | 合併順序 |
|---|---|---|---|---|---|
| `<task>` | `<agent>` | `<relative-path>` | `<branch>` | `<test>` | `<n>` |

硬規則：

1. 同一時間只有一位 owner 修改同一 canonical 檔。
2. 不確定邊界時先切成只讀研究，不平行寫入。
3. 共用 schema、manifest、lockfile 最後由整合 owner 修改。
4. 子任務完成只代表可合併，不代表整體完成。
5. 合併後由整合 owner 重跑跨模組測試與 Secret 檢查。

## 3. Issue → 實作 → 測試 → Review → PR 閉環

```text
Issue
  → 驗收條件
  → 分支／工作樹
  → 最小實作
  → 測試與負向測試
  → 自我 Review
  → Secret／diff 檢查
  → Draft PR
  → Review 修正
  → ReadyGate Delivery Review
```

PR 至少包含：

- 問題、範圍與不納入項目。
- 實際變更。
- 測試命令與結果。
- 風險、相容性與 rollback。
- 尚未完成或需要人工驗收的項目。

測試失敗、diff 包含未知檔案或來源 revision 不明時停止，不得只為了建立 PR 而略過。

## 4. 可重用 Skills 與團隊規則

### 單一來源

- 個人全域 Skill：`~/.agents/skills/<skill>`。
- 平台不原生支援時使用 symlink、junction、external directory 或薄轉接。
- 不在每個 Agent 目錄複製第二份 canonical Skill。

### 每個能力的狀態

- `IMPLEMENTED`：有工具或可驗證流程。
- `PROMPT_ONLY`：只有受控 SOP，不能假裝已自動化。
- `PLANNED`：只有需求與相依。

新增或修改 Skill 時：

1. 更新來源與版本。
2. 驗證 frontmatter、觸發條件與安全邊界。
3. 檢查所有 adapter。
4. 更新 `FEATURES.json`。
5. 在 disposable project 測試。
6. 再依授權處理 dotfiles 或發布。

## 5. 背景排程與持續監控 Agent

每個監控必須定義：

```text
monitor:
  purpose:
  owner:
  schedule:
  source:
  expected_state:
  alert_condition:
  allowed_actions:
  forbidden_actions:
  stop_condition:
  last_verified:
```

預設只讀與通知。自動修復、關閉 Issue、重新部署或刪除紀錄需另外授權。無變化不是錯誤；持續失敗才升級給 owner。

## 6. Plugins／Apps／MCP 跨工具工作流

先建立系統邊界：

| 系統 | 權威資料 | 讀取 | 寫入 | 核准 |
|---|---|---|---|---|
| GitHub | 程式、Issue、PR、版本 | 可 | 依任務 | commit／push／發布 |
| 專案 repository | 四檔、程式與交接 | 可 | 依專案生命週期 | 工作單／ReadyGate |
| 外部知識庫 | 明確指定的獨立資料 | 只有獨立任務才讀 | 只有獨立任務才寫 | 每次明確授權 |
| 其他 Plugin／MCP | 由使用者指定 | 最小必要 | 最小必要 | 依外部影響 |

規則：

1. 先用目的專用 connector，再用通用瀏覽器。
2. 工具可用不等於已授權寫入。
3. 不把一個系統的登入狀態當成另一個系統的權限。
4. 每次跨系統寫入記錄來源、目標、revision、結果與 rollback。

## 7. 限定可信來源的 Deep Research

研究前先寫：

- 問題與決策用途。
- 來源白名單與排除來源。
- 時效截止點。
- 所需原始證據。
- 引用格式。
- 無法驗證時的標記。

來源優先順序：

1. 官方文件、標準與原始資料。
2. 同儕審查論文與出版社資料。
3. 官方技術 repository／release。
4. 高品質二手分析；必須與原始來源交叉驗證。

報告把「來源聲稱」「本輪驗證」「推論」分開，不用搜尋摘要冒充原文。

## 8. 文件、試算表、簡報與知識成果物

每個成果物都記錄：

| 項目 | 內容 |
|---|---|
| 接收者 | 誰使用 |
| 來源 revision | 由哪一版資料產生 |
| 格式 | docx／xlsx／pptx／pdf／markdown 等 |
| 驗證 | 結構、公式、連結、字型、渲染、列印 |
| 敏感資訊 | 公開／私人／需遮蔽 |
| 回復 | 原始檔、匯出檔、上一版 |

不能只產生檔案；必須用實際接收方式回讀或渲染驗證。

## 9. Secret、憑證與提交前保護

`.gitignore` 是第一層，不是完整防線。

提交前依序：

1. `git status --short`：確認只有已知檔案。
2. `git diff --check`：檢查格式。
3. 檔名掃描：`.env`、key、pem、credential、token、cookie、認證快取。
4. 內容掃描：只回報檔名與類型，不在 log 顯示值。
5. 檢查 staged diff 與公開／私人邊界。
6. 若疑似 Secret 已進 Git，停止 push；先撤銷／輪替，再處理歷史。

公開模板只放 `.example` 與虛構值。裝置路徑、帳號、電腦名稱與 vault 位置也視為個人化資料。

## 10. Human-in-the-loop、權限與稽核

| 動作 | 預設 |
|---|---|
| 專案內可回復修改 | 依已確認工作單 |
| 安裝工具 | 先顯示工具、來源、影響 |
| GitHub 登入 | 使用者親自完成 |
| commit | 需在任務或 policy 內授權 |
| push／PR／發布 | 顯示 revision、範圍與 rollback |
| 外部知識庫讀寫 | 與生命週期分離；每次獨立明確授權 |
| 刪除／批次遷移／權限變更 | ReadyGate＋精確目標＋rollback |

稽核紀錄至少包含：

```text
action:
scope:
source_revision:
authorized_by:
executed_by:
evidence:
result:
rollback:
timestamp:
```

## 交棒

Lite `handoff.md` 只保留：

- 最後完成的成果。
- 已驗證與未完成。
- 下一步最多三項。
- 風險與唯一續跑點。
- Git／外部同步的實際狀態。

長篇決策移至 Git 歷史或專案內專用文件；外部知識庫另開獨立任務。輸入、版本或權限變更後，重新檢查受影響的 SOP 與 ReadyGate 閘門。
