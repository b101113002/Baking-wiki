# 食譜內容稽核報告｜2026-11-23

## 稽核目的與方法

本次針對五份原始公開食譜、五份 Wiki Markdown、五份對應 HTML 簡報進行人工逐項檢查。核對欄位包括來源及作者、材料與數量、單位、產量、模具、烤溫、操作順序、發酵／冷卻時間、成品判斷、過敏原及安全提醒。

本報告為人工來源稽核紀錄，不是自動化 LangGraph 程式測試。原始食譜可能更新，實際烘焙前仍應開啟來源頁再次確認。

## 主要問題總表

| 類別 | 發現 | 影響 | 修正 |
|---|---|---|---|
| 跨文件配方錯置 | RCP-005 Artisan Bread 簡報原本使用 RCP-001 的揉麵配方 | 標題、來源與材料／步驟不相符，讀者可能做錯食譜 | 依 Sally's Baking 重寫 Markdown 與 HTML，統一改為免揉、偏涼水及 475°F 配方 |
| 材料表漏項 | RCP-004 的製作步驟有一小撮鹽，但材料表原先未列 | 讀者可能漏加材料 | 補回材料表，註明來源未提供重量 |
| 飲食標示不精確 | RCP-003 蛋糕本體不含奶蛋，但原始糖霜含 half-and-half | 容易將整份含乳糖霜版本誤認為純素／無乳 | 將蛋糕本體、原始糖霜及非乳替代選項分開標示 |
| 時間資訊未充分區分 | RCP-001 的總時間與可變發酵時間、RCP-004 的準備／烘烤與冷卻時間原先未清楚拆開 | 使用者可能把來源估時誤認為保證的完整上桌時間 | 保留原站公布數值，分別標示發酵範圍、冷卻未提供及實際時間限制，不自行補造分鐘數 |
| 操作步驟過度簡略 | 多篇曾以「混合均勻」「烘烤至熟」概括關鍵動作 | 新手無法判斷如何操作及何時進下一步 | 補足混合順序、揉製／整形方法、發酵觀察、粉液比例、牙籤／中心溫度等指標 |
| 安全資訊不完整 | 蒸氣、熱模具、巧克力糖霜、刀具等風險提醒不足 | 可能造成燙傷或工具傷害 | 逐篇補充隔熱手套、蒸氣方向、耐熱容器及刀具安全 |

## 逐篇稽核

### RCP-001｜新手簡易歐式麵包
- 來源：[King Arthur Baking – The Easiest Loaf of Bread You'll Ever Bake](https://www.kingarthurbaking.com/recipes/the-easiest-loaf-of-bread-youll-ever-bake-recipe)
- 主要問題：原站公布總計 2 小時 10 分鐘，但第一次發酵有 1–2 小時範圍；若發酵較久，實際完成時間就會延長。來源未列固定冷卻分鐘數。
- 修正：保留原站 hands-on、烘烤及總時間，清楚標示第一次發酵 1–2 小時、第二次 45 分鐘、烘烤 20–25 分鐘及關火留爐 5 分鐘；說明 2 小時 10 分鐘是原站估時、冷卻另計。同步核對揉麵、整形、蒸氣與熟度步驟。
- 狀態：**PASS**。時間資訊已完整揭露，不將來源估時當成保證完成時間。

### RCP-002｜經典磅蛋糕
- 來源：[King Arthur Baking – King Arthur's Original Pound Cake](https://www.kingarthurbaking.com/recipes/king-arthurs-original-pound-cake-recipe)
- 主要問題：奶油打發程度、雞蛋加入順序、乾濕材料交替方式及熟度判斷需要更明確。
- 修正：補充奶油顏色與質地、分次加糖及逐顆加蛋、乾料／液體分開、粉液交替、避免過度攪拌、牙籤／回彈測試、出爐靜置及網架冷卻。
- 狀態：**PASS**。冷卻時間另外註明，不宣稱一定包含在原站 1 小時 15 分鐘總時間內。

### RCP-003｜Cake Pan Cake 免蛋奶巧克力蛋糕本體
- 來源：[King Arthur Baking – King Arthur's Original Cake Pan Cake](https://www.kingarthurbaking.com/recipes/king-arthurs-original-cake-pan-cake-recipe)
- 主要問題：原配方蛋糕本體未使用奶蛋，但糖霜使用 half-and-half；只用「免奶蛋巧克力蛋糕」作標題容易使讀者誤會整份配方皆無乳。
- 修正：標題強調「蛋糕本體」，將原始含乳糖霜與來源提供的非乳替代分開；提醒替代巧克力豆仍須核對成分。
- 狀態：**PASS**。標示僅限蛋糕本體，不宣稱市售巧克力或整份甜點自動符合純素。

### RCP-004｜純素巧克力夾心餅乾蛋糕
- 來源：[BBC Good Food – Vegan cookies & cream cake](https://www.bbcgoodfood.com/recipes/vegan-cookies-cream-cake)
- 主要問題：原步驟有一小撮鹽，但原材料清單漏列；來源列準備 30 分鐘、烘烤 35 分鐘，並要求蛋糕完全冷卻後才能抹糖霜。
- 修正：材料表已補回一小撮鹽並註明來源未提供重量；將準備 30 分鐘、烘烤 35 分鐘與未提供的冷卻時間分開標示，並細分冷卻、餅乾處理、糖霜及裝飾步驟。
- 狀態：**PASS**。65 分鐘僅是原站準備與烘烤時間，不視為完整上桌時間；市售餅乾、植物奶、植物性優格及抹醬仍需確認成分與交叉接觸。

### RCP-005｜免揉鄉村手作麵包
- 來源：[Sally's Baking – Artisan Bread Recipe (4 Ingredients)](https://sallysbakingaddiction.com/homemade-artisan-bread/)
- 主要問題：原簡報曾混入另一篇麵包食譜的材料及流程，包括較高麵粉量、糖、溫水、揉麵及 450°F，與本篇免揉食譜不一致。
- 正確來源要點：高筋麵粉 430 g、即發酵母 6 g、粗鹽 9 g、水 360 ml（約 70°F／21°C）；不揉麵；第一次發酵約 2–3 小時；可選冷藏 12 小時至 3 天；整形後休息約 45 分鐘；475°F（約 246°C）烘烤約 20–25 分鐘；蒸氣法可用 3–4 杯沸水；出爐至少冷卻 20 分鐘。
- 修正：重新撰寫 Wiki 及 HTML 簡報，刪除混入的糖、溫水、揉麵及 450°F 流程，並補足分割、整形、割線、蒸氣安全及熟度判斷。
- 狀態：**PASS**。冷藏熟成需另加 12 小時至 3 天；冷卻時間另計。

## 修訂後品質統計

| 狀態 | 篇數 | 食譜 |
|---|---:|---|
| PASS | 5 | RCP-001、RCP-002、RCP-003、RCP-004、RCP-005 |
| WARNING | 0 | 無 |
| FAIL | 0 | 無 |

## 後續仍需處理
1. 將來源擷取與欄位證據保存做成實際工具，讓每個材料、時間與溫度可回溯到來源。
2. 實作 Markdown／HTML 自動一致性比較器；目前是人工逐篇核對。
3. 安裝 LangGraph 並連接搜尋、FETCH、解析、驗證、去重與 GitHub 寫入，測試成功、WARNING、FAIL 三種情境。
4. GitHub Pages 是否啟用仍需由 Repository Settings → Pages 確認。

## 參考來源
- SRC-001：King Arthur Baking，The Easiest Loaf of Bread You'll Ever Bake。
- SRC-002：King Arthur Baking，King Arthur's Original Pound Cake。
- SRC-003：King Arthur Baking，King Arthur's Original Cake Pan Cake。
- SRC-004：BBC Good Food，Vegan cookies & cream cake。
- SRC-005：Sally's Baking，Artisan Bread Recipe (4 Ingredients)。
