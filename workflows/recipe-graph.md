# 食譜蒐集 Graph 工作流（內容稽核修訂版）

> 本流程是預計採用的目標架構；Python 程式目前仍是待接真實工具的 LangGraph 骨架，不代表已部署自動化服務。本次實際核對為人工執行。

## 一、設計原則
- 每個節點只負責一類工作，輸入、輸出、狀態及錯誤可追蹤。
- 來源失敗、格式錯誤、內容邏輯錯誤、文件版本不一致、重複資料及保存失敗分開處理。
- 每個重試階段最多 2 次，避免無限循環。
- 只有來源可追溯且通過必要驗證的資料才能進正式食譜區。
- WARNING 放入待確認區；FAIL 不得發布。
- Markdown Wiki 與 HTML 簡報必須進行內容交叉核對，不能只檢查檔案是否存在。
- 不自動覆蓋既有食譜；相似項目先比較來源、材料及版本差異。
- GitHub 寫入只有收到成功回應後才能標記完成。

## 二、Graph 節點

| 節點 | 職責 |
|---|---|
| PLAN | 解析主題、數量、語言、來源限制及必要欄位 |
| SEARCH | 搜尋候選食譜網址，不得臆造 URL |
| FETCH | 讀取候選頁面，保存 URL、讀取時間、狀態及內容 |
| SOURCE_GATE | 判斷頁面是否可讀、是否為可辨識食譜來源 |
| PARSE | 擷取原始名稱、材料、份量、時間、溫度與步驟 |
| NORMALIZE | 翻譯及標準化欄位，保留原始數值與單位 |
| SCHEMA_CHECK | 檢查必要欄位、型別、單位及完整性 |
| REPAIR | 只修正可由來源證據確認的格式／欄位問題 |
| REASONING_CHECK | 檢查材料與步驟、時間、溫度、設備、安全及過敏原 |
| DOC_CONSISTENCY_CHECK | 將 Wiki Markdown 與 HTML 簡報逐項比對來源、材料、數量、烤溫、時間、步驟及狀態 |
| REPAIR_PRESENTATION | 若簡報與已驗證食譜不符，依 Wiki 的核准資料修正簡報；不得另行生成未核實資訊 |
| DEDUPLICATE | 比對標題、來源、材料及步驟相似度 |
| DUPLICATE_REVIEW | 對相似資料決定略過、保留版本或人工合併 |
| PERSIST | 寫入正式食譜、索引與更新紀錄 |
| QUARANTINE | 將 WARNING 放入待確認區，不列為已驗證食譜 |
| HUMAN_REVIEW | 將無法自動判定的 FAIL／重複衝突交由人工處理 |
| REPORT | 彙整數量、狀態、錯誤、重試及實際寫入結果 |

## 三、流程圖

為避免所有分支交錯在同一張圖，流程拆成兩個視角：第一張呈現正常通過時的主要路徑；第二張集中呈現異常處理、重試與人工介入。兩張圖合併後才是完整流程。

### 3.1 主流程總覽

~~~mermaid
flowchart LR
    subgraph A["01｜來源取得"]
        direction TB
        S([START]) --> P["PLAN<br/>拆解任務規格"]
        P --> SE["SEARCH<br/>搜尋可信來源"]
        SE --> F["FETCH<br/>讀取原始頁面"]
        F --> SG{"SOURCE_GATE<br/>來源有效？"}
    end

    subgraph B["02｜內容結構化"]
        direction TB
        PA["PARSE<br/>擷取食譜欄位"] --> N["NORMALIZE<br/>翻譯與單位標準化"]
        N --> SC{"SCHEMA_CHECK<br/>欄位完整？"}
    end

    subgraph C["03｜品質驗證"]
        direction TB
        RC{"REASONING_CHECK<br/>內容合理且安全？"} --> DC{"DOC_CONSISTENCY_CHECK<br/>Wiki／HTML 一致？"}
    end

    subgraph D["04｜去重與發布"]
        direction TB
        DD["DEDUPLICATE<br/>比對相似度"] --> DUP{"發現重複？"}
        DR["DUPLICATE_REVIEW<br/>確認版本與差異"]
        PS["PERSIST<br/>寫入正式資料區"] --> WS{"寫入成功？"}
        RP["REPORT<br/>彙整結果與紀錄"] --> E([END])
    end

    SG -->|PASS| PA
    SC -->|PASS| RC
    DC -->|PASS| DD
    DUP -->|否| PS
    DUP -->|是| DR
    DR -->|可新增／新版本| PS
    DR -->|確認重複，略過新增| RP
    DR -->|需要人工判斷| H["HUMAN_REVIEW<br/>人工審查"]
    WS -->|是| RP
    H --> RP

    classDef startEnd fill:#e5f3eb,stroke:#4f8a69,stroke-width:2px,color:#234b35
    classDef task fill:#eaf1fb,stroke:#6d8db8,stroke-width:1.5px,color:#263d5c
    classDef decision fill:#fff3d8,stroke:#c18b36,stroke-width:2px,color:#694b19
    classDef storage fill:#eeeafb,stroke:#8b79b9,stroke-width:1.5px,color:#45396a
    classDef report fill:#e7f3f1,stroke:#5b958c,stroke-width:1.5px,color:#254e49
    classDef human fill:#fbe9e8,stroke:#bf706b,stroke-width:1.5px,color:#6b302e

    class S,E startEnd
    class P,SE,F,PA,N,DD task
    class SG,SC,RC,DC,DUP,WS decision
    class DR,H human
    class PS storage
    class RP report

    style A fill:#f4f7fc,stroke:#d4dfed,stroke-width:1px
    style B fill:#f3f8f7,stroke:#cfe1dc,stroke-width:1px
    style C fill:#fbf7ef,stroke:#eadfc8,stroke-width:1px
    style D fill:#f7f4fb,stroke:#ddd4ed,stroke-width:1px
~~~

### 3.2 例外處理、重試與人工介入

~~~mermaid
flowchart TB
    subgraph SOURCE["來源讀取"]
        direction LR
        SF["SOURCE_GATE<br/>讀取失敗"] --> SR{"更換來源重試<br/>≤ 2 次？"}
        SR -->|是| SB["回 SEARCH → FETCH"]
        SR -->|否| H1["HUMAN_REVIEW"]
    end

    subgraph SCHEMA["格式與欄位"]
        direction LR
        SFMT["SCHEMA_CHECK<br/>格式可修正"] --> REP["REPAIR<br/>依來源修正"]
        REP --> SREP{"格式修正重試<br/>≤ 2 次？"}
        SREP -->|是| SCHECK["回 SCHEMA_CHECK"]
        SREP -->|否| H2["HUMAN_REVIEW"]
        SMISS["缺少原始資料"] --> FRET{"資料重取<br/>≤ 2 次？"}
        FRET -->|是| FB["回 FETCH／SEARCH"]
        FRET -->|否| H2
        SCORE["核心材料／步驟無法確認"] --> H2
    end

    subgraph QUALITY["內容合理性"]
        direction LR
        QWARN["REASONING_CHECK<br/>WARNING"] --> QU["QUARANTINE<br/>待確認區"]
        QFIX["有來源證據可釐清矛盾"] --> QRET{"內容重查<br/>≤ 2 次？"}
        QRET -->|是| QB["回 FETCH"]
        QRET -->|否| H3["HUMAN_REVIEW"]
        QFAIL["FAIL／重大安全疑慮"] --> H3
    end

    subgraph DOC["文件一致性"]
        direction LR
        DM["DOC_CONSISTENCY_CHECK<br/>Wiki／HTML 不一致"] --> RPRES["REPAIR_PRESENTATION<br/>以核准 Wiki 修正 HTML"]
        RPRES --> DRET{"簡報修正重試<br/>≤ 2 次？"}
        DRET -->|是| DCHK["重新執行 DOC_CONSISTENCY_CHECK"]
        DRET -->|否| H4["HUMAN_REVIEW"]
        DTOOL["比較工具未接通／證據不足"] --> QU
    end

    subgraph PUBLISH["去重與保存"]
        direction LR
        DUP["發現相似項目"] --> DREV{"DUPLICATE_REVIEW"}
        DREV -->|可新增／新版本| PERSIST["PERSIST"]
        DREV -->|確認重複，略過新增| REPORT["REPORT"]
        DREV -->|無法判斷| H5["HUMAN_REVIEW"]
        PFAIL["PERSIST 寫入失敗"] --> PRET{"寫入重試<br/>≤ 2 次？"}
        PRET -->|是| PERSIST
        PRET -->|否| H5
    end

    QU --> REPORT
    H1 --> REPORT
    H2 --> REPORT
    H3 --> REPORT
    H4 --> REPORT
    H5 --> REPORT

    classDef source fill:#eaf1fb,stroke:#6d8db8,stroke-width:1.5px,color:#263d5c
    classDef decision fill:#fff3d8,stroke:#c18b36,stroke-width:2px,color:#694b19
    classDef repair fill:#fff0e5,stroke:#cb8050,stroke-width:1.5px,color:#633e24
    classDef hold fill:#fff5dc,stroke:#c79b42,stroke-width:1.5px,color:#654c20
    classDef human fill:#fbe9e8,stroke:#bf706b,stroke-width:1.5px,color:#6b302e
    classDef store fill:#eeeafb,stroke:#8b79b9,stroke-width:1.5px,color:#45396a
    classDef report fill:#e7f3f1,stroke:#5b958c,stroke-width:1.5px,color:#254e49

    class SF,SB,SMISS,FB,QFIX,QB,DM,DCHK,DUP source
    class SR,SREP,FRET,QRET,DRET,DREV,PRET decision
    class REP,RPRES repair
    class QU hold
    class H1,H2,H3,H4,H5,SCORE,QFAIL human
    class PERSIST store
    class REPORT report

    style SOURCE fill:#f4f7fc,stroke:#d4dfed,stroke-width:1px
    style SCHEMA fill:#f3f8f7,stroke:#cfe1dc,stroke-width:1px
    style QUALITY fill:#fbf7ef,stroke:#eadfc8,stroke-width:1px
    style DOC fill:#fff6f0,stroke:#ecd6c8,stroke-width:1px
    style PUBLISH fill:#f7f4fb,stroke:#ddd4ed,stroke-width:1px
~~~

**圖例**
- <span style="color:#426b9c">藍色</span>：資料處理節點；**黃色**：條件判斷；**橘色**：修正節點。
- **紫色**：正式資料寫入；**米黃色**：待確認區；**紅色**：人工審查；**綠色**：完成與報告。
- 主流程圖中的 PASS 路徑不是唯一分支；所有失敗、WARNING、重試及人工處理均以第二張圖補足。

## 四、條件邊與資料規則

### SOURCE_GATE
- PASS：進 PARSE。
- 讀取失敗、頁面非食譜或來源不可辨識：回 SEARCH，改用其他候選。
- 重試超限：進 HUMAN_REVIEW，保留錯誤及候選來源。

### SCHEMA_CHECK
- PASS：進 REASONING_CHECK。
- 格式錯誤且可從原始來源確認：進 REPAIR，修正後必須重新檢查。
- 原始欄位缺漏：回 FETCH／SEARCH。
- 核心材料或步驟無法確認：進 HUMAN_REVIEW，不可自行補值。

### REASONING_CHECK
- PASS：進 DOC_CONSISTENCY_CHECK。
- WARNING：進 QUARANTINE，保留問題清單，不列為已驗證。
- 可透過重讀來源釐清的矛盾：回 FETCH。
- FAIL 或重大安全疑慮：進 HUMAN_REVIEW，不得發布正式食譜。

### DOC_CONSISTENCY_CHECK
- 必須比較對應 Markdown Wiki 與 HTML，至少檢查來源網址、食材名稱與數量、產量、模具、烤溫、主要步驟、冷卻時間及品質狀態。
- PASS：兩份文件一致，進 DEDUPLICATE。
- MISMATCH：回 REPAIR_PRESENTATION；以已驗證的 Wiki 資料為準修正 HTML，修正後重新檢查。
- WARNING：比較器尚未接通或證據不足時，不得回報 PASS；先進 QUARANTINE／人工補查。
- 同一文件最多修正及重查 2 次；仍不一致就進 HUMAN_REVIEW。

### DEDUPLICATE
- 無重複：進 PERSIST。
- 有相似項目：進 DUPLICATE_REVIEW。
- 不可因標題相同就直接刪除；不同作者、份量或配方版本要保留來源與差異。

### PERSIST
- 只有 PASS 且完成去重決策的資料可寫入正式食譜區。
- 寫入成功後才更新 persisted_files。
- 寫入失敗有限次重試；最終失敗須如實回報。
- WARNING 只寫待確認區；FAIL 只保留人工審查紀錄。

## 五、狀態定義
- PASS：來源可追溯、核心欄位足夠、內容可操作，且 Wiki／簡報一致，無重大矛盾。
- WARNING：仍有明確時間、商品標示、來源資訊或自動檢查工具缺漏；不得把未確認數據當成保證值。
- FAIL：來源無效、核心資訊無法確認、文件重大錯置或重大安全疑慮；不可發布正式食譜。

## 六、重試規則
- 來源讀取、資料重取、內容重查、格式修正、簡報修正及 GitHub 寫入分別計數。
- 每階段最多重試 2 次；達上限後進人工審查或如實回報。
- REPAIR 不得猜測補齊資料；修正後必須重新通過 SCHEMA_CHECK 與 REASONING_CHECK。
- PERSIST 前必須完成文件一致性與去重檢查，避免錯誤及重複寫入。

## 七、本專案目前執行狀態
已完成五份原始來源、五份 Wiki 食譜及五份 HTML 簡報的人工交叉核對，修正發現的錯置與缺漏。DOC_CONSISTENCY_CHECK 已納入目標設計，但 Python 範例尚未接上真實檔案讀取與自動比較工具。真實搜尋 API、網頁擷取器、解析器、去重服務、GitHub 自動寫入、自動化測試及實際 LangGraph runtime 執行尚未完成。既有修訂紀錄屬人工稽核與人工寫入，不可宣稱為自動化 Graph 執行。
