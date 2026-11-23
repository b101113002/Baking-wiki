# Baking Wiki 專案總注意事項與目前狀態

本文件集中整理本專案已討論及實作時必須遵守的需求、決策、限制與待辦事項。新增食譜、簡報或修改 Graph 前，請先閱讀本文件。

## 1. 專案定位
- 專案名稱：Baking Wiki／烘焙食譜知識庫。
- 用途：整理公開烘焙食譜，以繁體中文教學摘要呈現，並展示 Graph Agent 管理來源、標準化、驗證、去重與保存的概念。
- 面向使用者的網站是多份簡報的瀏覽平台，不是單一簡報。
- Repository：b101113002/Baking-wiki；分支：main。

## 2. 網站與簡報架構
- 根目錄 index.html 是網站入口與簡報目錄，列出多份獨立簡報；使用者選擇主題後才進入該份簡報。
- 不可把其中一份食譜簡報直接當成網站首頁。
- 首頁分為食譜教學簡報與 Graph Agent 專題介紹。
- 每份簡報放在 presentations/，使用獨立 HTML。
- 每份食譜簡報至少包含：食譜介紹、材料、製作流程、完成判斷、操作安全與過敏原提醒、原始來源連結。
- 新增簡報時：新增 HTML、更新 index.html 卡片、更新 README 或簡報目錄、更新 log.md。
- 簡報翻頁需有上一頁／下一頁；若支援鍵盤操作，也需保留手機點擊控制。
- 內容以繁體中文摘要與改述呈現，不大量複製原文。

### 目前簡報清單
1. presentations/easiest-loaf-slides.html：新手簡易歐式麵包。
2. presentations/original-pound-cake-slides.html：經典磅蛋糕。
3. presentations/cake-pan-cake-slides.html：免奶蛋巧克力蛋糕。注意：來源蛋糕體不含奶蛋，但原糖霜含乳製品，整份配方不可直接宣稱純素。
4. presentations/vegan-cookies-cream-cake-slides.html：純素巧克力夾心餅乾蛋糕。市售替代品需查核成分及過敏原。
5. presentations/artisan-bread-slides.html：免揉鄉村手作麵包。
6. presentations/baking-agent-slides.html：Graph Agent 專題介紹，不是食譜教學簡報。

## 3. 食譜來源與內容品質
- 每份食譜保留原始 URL、作者／網站（可取得時）及查閱日期。
- 不得虛構食譜、作者、來源、材料、數量、時間、溫度、設備或步驟。
- 保留來源原始數量與單位；若換算公制，另列換算值，不可覆蓋原值。
- 區分「來源明示」、「單位換算」、「依步驟推定」及「待確認」。
- 不同網站或不同版本的配方不可自行平均或合併。
- 食譜內容以繁體中文摘要／改述，避免大量複製著作權保護的原文。
- 食譜網站可能更新；實際烘焙前應回到來源頁確認最新配方與步驟。

### 時間、溫度、安全與過敏原
- 分別記錄準備、混合／揉製、發酵／靜置、烘烤、冷卻、裝飾及總時間。
- 檢查總時間是否包含完全冷卻、延長冷藏發酵或裝飾。
- 若總時間沒有包含必要冷卻或延長發酵，標示「未含」及 WARNING，不可讓讀者誤以為能在標示時間內完成。
- 保留來源原始溫度與單位，另列換算。
- 涉及烤箱、熱鍋、沸水蒸氣、糖漿、刀具等，加入具體安全提醒。
- 標示常見過敏原；「植物性」或「純素」不等於無過敏原。
- 市售巧克力、餅乾、植物奶、植物性抹醬等替代品，依實際包裝確認成分、過敏原與交叉接觸聲明。
- 不可宣稱無麩質、無乳、無蛋或純素，除非整份配方及所用商品均已確認。

## 4. 品質狀態
- PASS：來源可追溯、核心材料與步驟完整，未發現重大矛盾，可進正式食譜區。
- WARNING：仍有明確缺漏、時間未涵蓋完整流程、推定欄位或商品標示待確認；只能放入待確認區。
- FAIL：來源無效、核心資料無法確認、重大矛盾或安全疑慮；不得發布正式食譜。
- 目前 RCP-004 因冷卻時間未計入及市售商品標示需核對而為 WARNING。
- RCP-005 的時間需再確認是否包含出爐後冷卻；若未包含，修正時間說明或調整狀態。
- 既有 PASS 4、WARNING 1 是當時人工整理紀錄，不代表未來稽核後仍必然維持相同數量。

## 5. Graph Agent 設計原則
- Graph 是有明確節點、狀態、條件分支與重試上限的工作流，不以單次長 Prompt 代替流程控制。
- 流程：PLAN → SEARCH → FETCH → SOURCE_GATE → PARSE → NORMALIZE → SCHEMA_CHECK → REPAIR（必要時）→ REASONING_CHECK → DEDUPLICATE → DUPLICATE_REVIEW（必要時）→ PERSIST → REPORT。
- WARNING 進 QUARANTINE／待確認區；FAIL 進 HUMAN_REVIEW；不得混入正式已驗證食譜。
- 來源失敗回 SEARCH；缺少原始欄位回 FETCH／SEARCH；格式錯誤只能依來源證據修正並重新驗證。
- 重複資料比較來源、材料、步驟及版本差異；不得自動覆蓋既有資料。
- 每階段重試最多 2 次，超過上限保留錯誤並交由人工處理。
- GitHub 寫入失敗要記錄，不能回報成功。
- 詳細流程以 workflows/recipe-graph.md 為準；程式骨架以 workflows/langgraph-example.py 為參考。

## 6. Graph 目前真實狀態與限制
- 既有五份食譜整理是依 Graph 節點規格進行的人工模擬／人工整理。
- 不可宣稱已實際部署 LangGraph runtime，也不可宣稱已接上自動搜尋、網頁爬取、解析、去重或 GitHub 自動寫入。
- workflows/langgraph-example.py 是示範骨架；TODO 工具尚未連接前，不能視為可投入正式環境的完整 Agent。
- 未來要稱為自動化完成，至少需接上真實搜尋、FETCH、解析、驗證、去重、GitHub 寫入，並完成測試及保留實際執行紀錄。
- 人工模擬、程式骨架、實際執行三者在文件與簡報中必須清楚區分。

## 7. GitHub 檔案維護規範
- index.html：網站首頁與簡報目錄。
- README.md：專案說明及快速入口。
- index.md：食譜 Wiki 索引。
- agent.md：Agent 規格。
- project-notes.md：本專案總注意事項與維護規範。
- raw/sources.md：原始來源登錄。
- wiki/recipes/：標準化食譜資料。
- workflows/recipe-graph.md：Graph 流程文件及 Mermaid 圖。
- workflows/langgraph-example.py：LangGraph 範例骨架。
- reports/execution-record.md：執行紀錄，須標示人工或自動執行。
- reports/reflection.md：作業反思與改進方向。
- presentations/：獨立 HTML 簡報。

每次新增或修改食譜，需同步檢查索引、來源清單、首頁簡報卡片（若有新簡報）及 log。修改既有資料時保留修改原因與日期。

## 8. GitHub Pages 部署注意事項
- 根目錄已有 index.html，但檔案存在不等於 GitHub Pages 已啟用。
- 需到 Repository Settings → Pages，選擇 Deploy from a branch、分支 main、資料夾 /(root) 並儲存。
- 未實際確認 Pages 部署狀態前，不可宣稱網站已公開上線。
- 預期網址格式為 https://b101113002.github.io/Baking-wiki/；只有部署成功後才可當成可用網站連結。

## 9. 新增食譜／簡報檢查清單
- [ ] 來源網址可開啟，且確實是對應食譜。
- [ ] 保留原始名稱、作者／網站、查閱日期。
- [ ] 材料、數量、單位與必要／可選標記正確。
- [ ] 設備、模具尺寸、時間、溫度有來源依據。
- [ ] 冷卻、延長發酵與裝飾時間是否計入已明確說明。
- [ ] 步驟沒有使用材料表不存在的材料。
- [ ] 成品判斷、安全提醒及過敏原已檢查。
- [ ] PASS／WARNING／FAIL 與問題清單一致。
- [ ] 完成去重，不覆蓋既有配方版本。
- [ ] 正式食譜、待確認資料及失敗紀錄分開保存。
- [ ] 若新增簡報，首頁與 README 已新增入口。
- [ ] log 與執行紀錄已更新，且未誇大自動化程度。
