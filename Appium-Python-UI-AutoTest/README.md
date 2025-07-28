# AI 驅動的 Appium UI 自動化測試生成器

## 總覽

本專案展示了一個創新的測試自動化流程，利用 AI 技術分析 Android 應用的 UI 畫面，並自動生成 Appium 測試腳本。系統會讀取由 Appium 提供的 UI XML 佈局文件和畫面截圖，透過 AI 模型理解畫面元素與可能的操作，最終產出可直接執行的 BDD (行為驅動開發) 風格測試案例。

這個專案的目標是：
- 減少手動編寫 UI 測試腳本的重複性工作。
- 加速測試案例的開發流程。
- 讓不懂程式的測試人員也能參與自動化測試的建立。

---

## 核心概念

整個自動化流程分為三個主要階段：

1.  **UI 畫面擷取**:
    - 使用 Appium Inspector 或其他工具，連接到指定的 Android 應用程式 (`.apk`)。
    - 抓取當前 UI 畫面的 XML 原始碼 (`ui_source.xml`) 和對應的螢幕截圖 (`ui_screenshot.png`)。

2.  **AI 自動生成測試腳本**:
    - 執行核心的 AI 生成腳本 (`ai_generate.py`)。
    - 此腳本會將 `ui_source.xml` 和 `ui_screenshot.png` 作為輸入，傳送給 AI 模型進行分析。
    - AI 模型會識別畫面上的可互動元件（如按鈕、輸入框），並生成一組符合 Gherkin 語法的測試情境 (`generated_test.feature`) 以及對應的 Python 步驟定義 (`generated_steps.py`)。

3.  **執行自動化測試**:
    - 生成的測試腳本會被放置在 `Appium_Tests` 目錄下。
    - 使用 Behave 測試框架，在 Android 模擬器或實體裝置上啟動應用程式，並執行自動化 UI 測試。

---

## 專案結構

```
Appium-Python-UI-AutoTest/
├── Mobile-UI-AutoTest/
│   ├── Appium_Tests/
│   │   ├── features/
│   │   │   └── generated_test.feature  # AI 生成的 BDD 測試案例
│   │   ├── steps/
│   │   │   └── generated_steps.py      # AI 生成的測試步驟實現
│   │   └── test_generator/
│   │       ├── ai_generate.py          # 核心 AI 生成腳本
│   │       ├── ui_source.xml           # Appium 導出的 UI 佈局文件
│   │       └── ui_screenshot.png       # 對應的 UI 截圖
│   └── assets/
│       └── app-debug.apk               # 待測試的應用程式
└── RNCalculator/                         # 範例用的 React Native 計算機 App
```

---

## 如何開始

### 1. 環境準備
請確保你的開發環境已安裝以下工具：
- Python 3.8+
- Appium Server
- Android Studio (包含 Android SDK 與模擬器)
- Node.js (用於建置 `RNCalculator` 範例 App)

### 2. 安裝依賴
專案的 Python 依賴可能包含 `Appium-Python-Client`, `behave` 等。 (建議建立 `requirements.txt`)
```bash
pip install -r requirements.txt
```

### 3. 準備測試目標
1.  將你要測試的 Android 應用程式 `.apk` 檔案放入 `Mobile-UI-AutoTest/assets/` 目錄。
2.  使用 Appium Inspector 連接到你的 App，並將目標測試畫面的 XML 內容儲存為 `Mobile-UI-AutoTest/Appium_Tests/test_generator/ui_source.xml`。
3.  同時擷取該畫面的截圖，並儲存為 `Mobile-UI-AutoTest/Appium_Tests/test_generator/ui_screenshot.png`。

### 4. 生成測試腳本
執行 AI 生成腳本來建立測試檔案。
```bash
python Mobile-UI-AutoTest/Appium_Tests/test_generator/ai_generate.py
```
執行成功後，新的測試案例將會出現在 `features` 和 `steps` 目錄中。

### 5. 執行測試
啟動 Appium Server，並在專案目錄下執行 Behave 指令來運行測試。
```bash
cd Mobile-UI-AutoTest/Appium_Tests/
behave
```
測試將會自動在指定的 Android 裝置上執行。

---

## 技術棧

- **測試框架**: Appium, Behave (Python)
- **程式語言**: Python
- **AI整合**: 透過 API 呼叫大型語言模型 (例如：OpenAI GPT, Google Gemini)
- **目標平台**: Android
- **範例應用**: React Native
