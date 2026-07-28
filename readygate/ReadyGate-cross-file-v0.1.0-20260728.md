---
readygate_version: 1
profile: general
subject: Cross-File AI Workflow Core v0.1.0
scope: public repository, main branch, v0.1.0 tag, README landing, and GitHub Release
revision: v0.1.0
evidence_cutoff: 2026-07-28 22:47 +08:00
status: READY
workflow_state: DELIVERY_REVIEW
work_order: WO-DIRECT-RELEASE-SHUTDOWN-20260728-v2
cycles_used: 3
reviewer: Codex; human approver: user confirmed work order
---

# ReadyGate：Cross-file v0.1.0 公開發布

## 結論

**READY** — 公開核心已去除個人 workspace 稽核資料，版本、依賴、只讀 advisor、Apply guard、連結與公開安全檢查均已用本輪證據驗證，可依已確認工作單建立 public repository 並發布 `v0.1.0`。

## 五道閘門

| 閘門 | 狀態 | 一句話證據／缺口 |
|---|---|---|
| G1 目的與範圍 | `VERIFIED` | 工作單限定公開 Full Core，不修改 Lite canonical、不寫 Notion、不建立 Pages |
| G2 輸入與版本 | `VERIFIED` | Lite public `v1.1.1` 與 ReadyGate private `v0.2.1` Release 已回讀 |
| G3 耦合與風險 | `VERIFIED` | 私人 dotfiles、舊專案、裝置路徑與個人稽核報告均排除於公開範圍 |
| G4 驗證與證據 | `VERIFIED` | validator、`FULL／LITE／NONE`、Apply guard、Markdown links 與 secret-pattern scan 通過 |
| G5 交付與回復 | `VERIFIED` | README GitHub landing、tag／Release、外部備份與 public-to-private 緊急回復已定義 |

## Critical 證據

| 項目 | 狀態 | 證據／來源 | 範圍與版本 | 缺口 |
|---|---|---|---|---|
| Repository validator | `VERIFIED` | `scripts/validate.ps1` PASS | 15-file release candidate | 無 |
| Bootstrap advisor | `VERIFIED` | `scripts/install.ps1` | `0.1.0`、目前環境 `FULL`、writes false | 無 |
| 分類契約 | `VERIFIED` | disposable agent roots | `NONE／LITE／FULL` 全部符合 | 無 |
| Apply 安全鎖 | `VERIFIED` | `scripts/install.ps1 -Apply` exit 1 | `0.1.0` | Apply 刻意為 `PLANNED` |
| 文件連結 | `VERIFIED` | Markdown 相對連結檢查 | 8 份 Markdown，0 missing | 無 |
| 公開安全 | `VERIFIED` | 檔名／內容／裝置識別 pattern scan | 全 release candidate | validator 內的路徑 regex 是掃描規則，不是持久化裝置路徑 |
| 依賴 revision | `VERIFIED` | GitHub／Git tag 回讀 | Lite `v1.1.1`、ReadyGate `v0.2.1` | 無 |

## 最短補強路徑

1. 不需要發布前補強。
2. 發布後回讀 visibility、default branch、tag、Release 與 source archive。
3. 若公開安全回讀不符，立即把新 repository 改為 private 並停止，不刪除或改寫歷史。

## 例外與責任

- Apply 尚未實作 — 明確標為 `PLANNED`；owner：Full Core maintainer；期限：另開版本工作單。
- ReadyGate 來源可為 private 或使用者自備 — README 與 `FEATURES.json` 不嵌入私人內容。

## 放行決定

- 決定：依已確認工作單建立 public repository 並發布 `v0.1.0`。
- override：無。

## 回復／交棒

- rollback：本機外部備份與 SHA-256 manifest；公開範圍錯誤時先改 private，錯誤 commit 使用 revert。
- 下一位：workspace shutdown owner 回讀 GitHub、Google Drive 與 Obsidian。
- 重新檢查條件：README、版本、依賴、Apply 行為、repository visibility 或 release source 變更。

> 本卡只涵蓋列出的版本、範圍與證據截止點；任何輸入變更都需要重新檢查受影響的閘門。
