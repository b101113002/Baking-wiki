# Graph 執行紀錄（人工模擬）

- 日期：2026-11-23
- 主題：蒐集不同類型的入門烘焙食譜
- 目標：5 篇食譜，欄位含材料、設備、時間、教學步驟與問題檢查
- 執行方式：依 Graph 節點規格人工模擬，使用已查閱的公開食譜頁整理；**不是已部署的 LangGraph runtime 實際執行**。

## 節點紀錄
| 節點 | 結果 | 備註 |
|---|---|---|
| PLAN | PASS | 確認繁中、5 篇及欄位 |
| SEARCH | PASS | 取得 5 個來源候選 |
| FETCH | PASS | 5 個來源頁可讀取 |
| SOURCE_GATE | PASS | 均為公開食譜頁 |
| PARSE | PASS | 擷取材料、時間、步驟 |
| NORMALIZE | PASS | 轉繁中並保留原單位 |
| SCHEMA_CHECK | PASS | 五篇均有來源、材料及步驟 |
| REASONING_CHECK | WARNING | RCP-004 冷卻時間未計入；商品純素標示需核對 |
| DEDUPLICATE | PASS | 未發現完全重複 |
| PERSIST | PASS | 檔案已提交 GitHub |
| REPORT | PASS | 紀錄與反思已建立 |

## 統計
- 來源頁：5
- 食譜頁：5
- PASS：4
- WARNING：1
- FAIL：0
- 完全重複：0

## 可重現性限制
這是人工依 Graph 節點及分支規則完成的模擬，未聲稱程式已自動連接搜尋 API、爬取服務或 GitHub 寫入節點。程式骨架在 `workflows/langgraph-example.py`，仍需補上真實工具並執行測試。