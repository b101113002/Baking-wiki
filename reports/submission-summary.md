# Baking Wiki 作業繳交總表

查核／整理日期：2026-11-23

以下內容依照六項繳交要求整理，可直接作為作業提交說明。網站入口目前已建立為 GitHub 專案內的多簡報目錄；GitHub Pages 是否啟用尚未確認，因此同時提供 GitHub 檔案連結作為可查驗成果。

## 1. LLM Wiki 主題與簡短介紹

**主題：Baking Wiki｜烘焙食譜知識庫與 Graph Agent 自動蒐集流程**

本專題以烘焙食譜為知識管理主題，將不同網站的公開食譜整理成繁體中文 Wiki 條目。每筆資料保留作者、原始網址、材料、份量、設備、時間、烤溫、詳細步驟、成品判斷、過敏原與安全提醒。專題並設計 Graph Agent 流程，示範如何將來源蒐集、資料擷取、標準化、品質檢查、錯誤修正、文件一致性比對、去重及保存拆成可追蹤的節點，避免只依賴單次 LLM 生成。

目前 Wiki 收錄五份不同類型的食譜：酵母麵包、磅蛋糕、免蛋奶巧克力蛋糕本體、純素巧克力夾心餅乾蛋糕及免揉鄉村麵包。

## 2. LLM Wiki 連結或成果

- **GitHub 專案：** https://github.com/b101113002/Baking-wiki
- **Wiki 食譜索引：** https://github.com/b101113002/Baking-wiki/blob/main/index.md
- **專案首頁 HTML（簡報目錄）：** https://github.com/b101113002/Baking-wiki/blob/main/index.html
- **專案總注意事項：** https://github.com/b101113002/Baking-wiki/blob/main/project-notes.md
- **原始來源清單：** https://github.com/b101113002/Baking-wiki/blob/main/raw/sources.md

## 3. 教學 HTML 簡報連結

網站首頁是「多份獨立簡報的瀏覽目錄」，選擇主題後才會進入個別簡報。

| 簡報主題 | HTML 原始檔 |
|---|---|
| 新手簡易歐式麵包 | https://github.com/b101113002/Baking-wiki/blob/main/presentations/easiest-loaf-slides.html |
| 經典磅蛋糕 | https://github.com/b101113002/Baking-wiki/blob/main/presentations/original-pound-cake-slides.html |
| Cake Pan Cake 免蛋奶巧克力蛋糕本體 | https://github.com/b101113002/Baking-wiki/blob/main/presentations/cake-pan-cake-slides.html |
| 純素巧克力夾心餅乾蛋糕 | https://github.com/b101113002/Baking-wiki/blob/main/presentations/vegan-cookies-cream-cake-slides.html |
| 免揉鄉村手作麵包 | https://github.com/b101113002/Baking-wiki/blob/main/presentations/artisan-bread-slides.html |
| Graph Agent 專題介紹 | https://github.com/b101113002/Baking-wiki/blob/main/presentations/baking-agent-slides.html |

## 4. Loop／Graph 流程圖或文字說明

正式 Mermaid 流程圖：  
https://github.com/b101113002/Baking-wiki/blob/main/workflows/recipe-graph.md

程式骨架：  
https://github.com/b101113002/Baking-wiki/blob/main/workflows/langgraph-example.py

主要流程：

```text
START
  → PLAN
  → SEARCH
  → FETCH
  → SOURCE_GATE
  → PARSE
  → NORMALIZE
  → SCHEMA_CHECK
      ├─ 格式可修正 → REPAIR → SCHEMA_CHECK
      ├─ 缺少原始資料 → FETCH／SEARCH
      └─ 核心資料不可確認 → HUMAN_REVIEW
  → REASONING_CHECK
      ├─ PASS → DOC_CONSISTENCY_CHECK
      ├─ WARNING → QUARANTINE
      └─ 可補查矛盾 → FETCH
  → DOC_CONSISTENCY_CHECK
      ├─ PASS → DEDUPLICATE
      ├─ MISMATCH → REPAIR_PRESENTATION → 重新檢查
      └─ WARNING／重試超限 → QUARANTINE／HUMAN_REVIEW
  → DEDUPLICATE
  → DUPLICATE_REVIEW（必要時）
  → PERSIST
  → REPORT
  → END
```

各階段重試最多 2 次。WARNING 不可當成已驗證內容；FAIL 需人工審查。文件一致性檢查特別比對 Markdown 與 HTML 的來源、材料、數量、模具、烤溫、步驟、時間及品質狀態。

## 5. 一次實際執行的結果或檢查紀錄

本次已於 2026-11-23 實際逐篇開啟五個原始食譜來源頁，對照五份 Wiki 條目及五份 HTML 簡報，並將修訂提交至 GitHub。執行結果：

| 檢查項目 | 結果 |
|---|---:|
| 原始食譜來源頁 | 5／5 可讀取 |
| Wiki 條目 | 5／5 完成核對 |
| HTML 食譜簡報 | 5／5 完成核對 |
| 發現重大配方錯置 | 1 件（RCP-005 簡報） |
| 修訂後品質狀態 | PASS 3、WARNING 2、FAIL 0 |
| 重複食譜 | 0 件（人工比對） |

最重要的錯誤是免揉鄉村麵包簡報錯用了另一篇需要揉麵的配方；此外也補回 RCP-004 漏列的鹽，釐清 RCP-003 原始糖霜含乳，並補充 RCP-001、RCP-004 的時間限制。

完整紀錄：  
https://github.com/b101113002/Baking-wiki/blob/main/reports/execution-record.md

逐篇問題與修訂內容：  
https://github.com/b101113002/Baking-wiki/blob/main/reports/recipe-audit-2026-11-23.md

**執行方式說明：** 來源查核、內容比對及 GitHub 檔案修訂為實際人工完成；Graph 節點紀錄是依設計流程整理的人工模擬，不是已部署 LangGraph runtime 的自動化成功紀錄。目前程式骨架尚未安裝／連接 LangGraph 及搜尋、擷取、文件比較與持久化工具，因此不宣稱程式已完成 runtime 測試。

## 6. 反思：哪個節點最常出錯？如何調整檢查流程？

本次最容易出現問題的是 **REASONING_CHECK（內容邏輯與品質檢查）**，其次是跨文件一致性。食譜即使名稱、材料及步驟欄位都存在，也可能出現時間互相矛盾、材料表漏列、飲食標籤誤導，或簡報內容被錯誤複製成另一份食譜。

因此新增及加強以下檢查：
1. 材料表與步驟雙向核對，確保步驟使用的食材都有列在材料表。
2. 對照官方總時間與發酵、烘烤、冷卻及裝飾等分段時間；有歧義就標 WARNING，不自行猜測。
3. 把蛋糕本體、糖霜及替代材料分開判定飲食標籤與過敏原。
4. 增加 DOC_CONSISTENCY_CHECK，比對 Wiki Markdown 和 HTML 簡報的來源、材料、數量、烤溫、時間、步驟及品質狀態。
5. 修正後重新檢查；同一階段最多重試 2 次，仍無法確認便交由人工審查。

詳細反思：  
https://github.com/b101113002/Baking-wiki/blob/main/reports/reflection.md

---

## 提交前提醒
本專案 GitHub Repository 檔案已更新；GitHub Pages 是否已啟用尚未確認。正式展示網站時，請先到 Repository Settings → Pages 確認 Deploy from a branch、分支 main、資料夾 /(root) 並完成部署。未確認之前，請使用上方 GitHub 專案及檔案連結，不要把預期 Pages 網址當成已上線成果。
