# Baking Wiki 專案總注意事項與目前狀態

本文件集中整理本專案已討論及實作時必須遵守的需求、決策、限制與待辦事項。新增食譜、簡報或修改 Graph 前，請先閱讀本文件。

## 1. 專案定位
- 專案名稱：Baking Wiki／烘焙食譜知識庫。
- 用途：整理公開烘焙食譜，以繁體中文教學摘要呈現，示範 Graph Agent 如何管理來源蒐集、標準化、驗證、去重與保存。
- LLM Wiki 主題：**烘焙食譜知識庫與 Graph Agent 食譜蒐集流程**。
- 網站是多份獨立簡報的瀏覽平台，不是單一簡報。
- Repository：b101113002/Baking-wiki；分支：main。

## 2. 網站與簡報架構
- 根目錄 index.html 是網站入口及簡報目錄，列出多份獨立 HTML 簡報。
- 不可把某一份食譜簡報直接當成網站首頁。
- 首頁分為食譜教學簡報與 Graph Agent 專題介紹。
- 每份簡報至少包含食譜介紹、材料、詳細製作流程、完成判斷、操作安全／過敏原提醒及來源連結。
- 新增簡報時需新增 HTML、更新 index.html 卡片、README／目錄與 log.md。
- 翻頁保留上一頁／下一頁；若支援鍵盤，也需保留手機點擊控制。
- 以繁體中文摘要與改述呈現，不大量複製原文。

### 目前簡報清單
1. presentations/easiest-loaf-slides.html：新手簡易歐式麵包，原站 2 小時 10 分鐘為估時；第一次發酵 1–2 小時、實際依麵糰狀態變動，冷卻另計；時間限制已清楚揭露，標 PASS。
2. presentations/original-pound-cake-slides.html：經典磅蛋糕，粉液交替與熟度判斷已補足。
3. presentations/cake-pan-cake-slides.html：Cake Pan Cake 蛋糕本體不含奶蛋；原始糖霜含乳，非乳替代品需查核巧克力成分。
4. presentations/vegan-cookies-cream-cake-slides.html：純素巧克力夾心餅乾蛋糕；原站 prep 30 分鐘、cook 35 分鐘，完全冷卻後才能抹糖霜，冷卻時間未提供且另計；限制已清楚揭露，標 PASS。
5. presentations/artisan-bread-slides.html：Sally's Baking 免揉鄉村手作麵包；不得與 RCP-001 的揉麵版本混用。
6. presentations/baking-agent-slides.html：Graph Agent 專題介紹。

## 3. 食譜來源與內容品質
- 每篇保留原始 URL、作者／網站（可取得時）及查核日期；來源更新資訊只在原站明確提供時記錄。
- 不得虛構食譜、作者、來源、材料、數量、時間、溫度、設備或步驟。
- 保留來源原始數量與單位；換算另列，不覆蓋原值。
- 區分來源明示、單位換算、依步驟推定及待確認。
- 不同網站或版本的配方不可自行平均或合併。
- 以繁體中文摘要／改述，避免大量複製著作權保護的原文。
- 食譜網站可能更新；實際製作前應回到來源確認。

### 時間、溫度、安全與過敏原
- 分別記錄準備、混合／揉製、發酵／靜置、烘烤、冷卻、裝飾及總時間。
- 保留來源公布的總時間，另對照分段時間；如無法加總，指出差異，不自行替換來源時間。
- 來源未提供冷卻或裝飾時間時，標示未計入且不虛構分鐘數；若限制已清楚揭露、不影響配方可重現性，可維持 PASS；若時間描述仍會誤導，才設為 WARNING。
- 保留來源原始溫度與單位，另列換算。
- 烤箱、熱鍋、沸水蒸氣、糖漿、刀具等需有具體安全提醒。
- 標示常見過敏原；「植物性」或「純素」不等於無過敏原。
- 巧克力、餅乾、植物奶、植物性抹醬等依實際包裝確認成分、過敏原與交叉接觸。
- 不可在未確認全部配方及商品前宣稱無麩質、無乳、無蛋或純素。

## 4. 本次食譜狀態（2026-11-23）
- RCP-001：PASS，原站 2 小時 10 分鐘為估時；第一次發酵 1–2 小時，較久時實際時間延長，冷卻另計。
- RCP-002：PASS，已補足粉液交替、奶油打發與熟度判斷；模中靜置及完全冷卻另計。
- RCP-003：PASS，已區分免蛋奶蛋糕本體與含乳原始糖霜。
- RCP-004：PASS，步驟中的一小撮鹽已補回材料表；原站 prep 30 分鐘、cook 35 分鐘，完全冷卻時間未提供並另計。
- RCP-005：PASS，已依 Sally's Baking 改正免揉、冷水、475°F 及 3–4 杯可選蒸氣水流程。
- 本次狀態：PASS 5、WARNING 0、FAIL 0；這是補充時間說明後的人工來源稽核結果，並非自動測試分數。

## 5. Graph Agent 設計原則
- Graph 是有節點、狀態、條件分支及重試上限的工作流，不以單次長 Prompt 代替。
- 流程：PLAN → SEARCH → FETCH → SOURCE_GATE → PARSE → NORMALIZE → SCHEMA_CHECK → REPAIR（必要時）→ REASONING_CHECK → DOC_CONSISTENCY_CHECK → DEDUPLICATE → DUPLICATE_REVIEW（必要時）→ PERSIST → REPORT。
- DOC_CONSISTENCY_CHECK 必須比對 Wiki Markdown 與 HTML 的來源、材料、數量、模具、烤溫、主要步驟、時間及狀態；錯誤時先修正簡報再重驗。
- WARNING 進 QUARANTINE；FAIL 進 HUMAN_REVIEW；不混入已驗證食譜。
- 來源失敗回 SEARCH；缺原始資料回 FETCH／SEARCH；格式錯誤只依來源證據修正。
- 重複資料比對來源、材料、步驟及版本差異；不得自動覆蓋。
- 每階段最多重試 2 次；GitHub 寫入失敗須記錄，不能回報成功。
- 詳細流程以 workflows/recipe-graph.md 為準；程式以 workflows/langgraph-example.py 為示範骨架。

## 6. Graph 目前真實狀態與限制
- 五份食譜的來源核對及本次修訂是人工查核／人工整理，不是自動化 Graph 執行。
- 不可宣稱已部署 LangGraph runtime，也不可宣稱已接上搜尋、網頁擷取、解析、文件比對、去重或 GitHub 自動寫入。
- Python 檔仍含 TODO；未連接工具前不可視為完整 Agent。
- 本機執行環境尚未安裝 LangGraph 套件，本次未進行 runtime 編譯或呼叫測試。
- 人工稽核、程式骨架、真正自動化執行三者須清楚區分。

## 7. 檔案維護規範
- index.html：網站首頁與簡報目錄；README.md：專案說明。
- index.md：食譜索引；agent.md：Agent 規格；project-notes.md：注意事項。
- raw/sources.md：來源登錄；wiki/recipes/：食譜頁。
- workflows/recipe-graph.md：Graph 流程圖；workflows/langgraph-example.py：程式骨架。
- reports/execution-record.md：人工稽核／模擬紀錄。
- reports/recipe-audit-2026-11-23.md：逐篇食譜稽核。
- reports/reflection.md：作業反思；presentations/：獨立 HTML 簡報。
- 修改食譜需同步檢查來源、索引、對應簡報、README 及 log，並保留修改原因。

## 8. GitHub Pages 部署注意事項
- 根目錄已有 index.html，不代表 GitHub Pages 已啟用。
- 手動啟用方式：Repository Settings → Pages → Deploy from a branch → main → /(root) → Save。
- 未確認 Pages 部署狀態前，不可宣稱網站已公開上線。
- 預期網址為 https://b101113002.github.io/Baking-wiki/；只有部署成功後才可當作正式網站連結。

## 9. 新增食譜／簡報檢查清單
- [ ] 來源網址有效且確實對應食譜；記錄作者及查核日期。
- [ ] 材料、數量、單位、必要／可選及替代品說明正確。
- [ ] 材料表與步驟雙向核對，沒有漏列步驟食材。
- [ ] 設備、模具尺寸、時間、溫度及換算有來源依據。
- [ ] 冷卻、延長發酵及裝飾時間是否計入已明確說明。
- [ ] 步驟提供操作方式及可觀察完成指標，不只寫「拌勻／烤熟」。
- [ ] 成品判斷、安全提醒及過敏原已檢查。
- [ ] Wiki Markdown 與 HTML 簡報來源、材料、數量、烤溫、時間及狀態一致。
- [ ] PASS／WARNING／FAIL 與問題清單一致。
- [ ] 去重完成，不覆蓋不同配方版本。
- [ ] 正式、待確認及失敗紀錄分開保存。
- [ ] 首頁、README、索引、log、執行紀錄同步更新；未誇大自動化程度。