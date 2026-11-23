# Baking Wiki｜烘焙食譜知識庫

以繁體中文建立的烘焙食譜 LLM Wiki 專題，示範如何將公開食譜轉化為可追溯、可檢查的知識條目，並以 Graph Agent 流程管理來源蒐集、標準化、品質驗證、去重與保存。

## 網站入口
- **[烘焙食譜教學簡報館（首頁 HTML）](index.html)**：瀏覽多份獨立食譜教學簡報與 Graph Agent 專題介紹。
- [食譜 Wiki 索引](index.md)
- [GitHub 專案成果](https://github.com/b101113002/Baking-wiki)

## 作業繳交與檢查
- [六項作業成果與連結](reports/submission-summary.md)
- [食譜內容稽核紀錄](reports/recipe-audit-2026-11-23.md)
- [人工來源稽核／Graph 模擬執行紀錄](reports/execution-record.md)
- [作業反思](reports/reflection.md)

## 專案維護規範
- [專案總注意事項與維護規範](project-notes.md)
- [Agent 規格](agent.md)
- [來源清單](raw/sources.md)
- [Graph 工作流與流程圖](workflows/recipe-graph.md)
- [LangGraph 程式骨架](workflows/langgraph-example.py)

## 簡報目錄
- [新手簡易歐式麵包](presentations/easiest-loaf-slides.html)
- [經典磅蛋糕](presentations/original-pound-cake-slides.html)
- [免蛋奶巧克力蛋糕本體與糖霜選項](presentations/cake-pan-cake-slides.html)
- [純素巧克力夾心餅乾蛋糕](presentations/vegan-cookies-cream-cake-slides.html)
- [免揉鄉村手作麵包](presentations/artisan-bread-slides.html)
- [Graph Agent 專題介紹](presentations/baking-agent-slides.html)

## 專案目錄
- `raw/`：來源登錄
- `wiki/recipes/`：標準化食譜
- `workflows/`：Graph 流程與程式骨架
- `reports/`：稽核、執行紀錄、反思及繳交總表
- `presentations/`：各主題獨立 HTML 簡報

## 執行狀態聲明
本次五份食譜的來源核對與內容稽核為人工執行；LangGraph 程式仍是尚未連接真實搜尋、網頁擷取、文件一致性比較及 GitHub 寫入工具的示範骨架。不可將人工稽核紀錄表述成自動化 Graph runtime 的成功執行。GitHub Pages 是否啟用尚未確認，請勿直接將預期網址視為已上線網站。

食譜內容以繁體中文摘要改寫，保留來源連結與必要數值。實際製作前請回到原站確認最新內容。