import google.generativeai as genai
import PIL.Image
import os
import re

os.environ['GOOGLE_API_KEY'] = "AIzaSyCfugpM7dz5rmJn-JIzk0Grpnbji8dFZBY"

try:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
except (KeyError, AttributeError):
    print("錯誤：無法讀取 API 金鑰。請確認您已設定 'GOOGLE_API_KEY' 環境變數。")
    exit()

model_instance = genai.GenerativeModel(
       model_name="gemini-2.5-pro-preview-06-05", 
   )

def analyze_ui_and_generate_tests(image_path: str, xml_path: str):
    """
    使用 Gemini 分析 UI 截圖 和 XML 原始碼，生成穩定且專業的測試檔案。
    """
    # --- 智慧路徑設定 (保持不變) ---
    script_dir = os.path.dirname(__file__)
    appium_tests_root = os.path.abspath(os.path.join(script_dir, '..'))
    features_dir = os.path.join(appium_tests_root, "features")
    steps_dir = os.path.join(appium_tests_root, "steps")
    
    # --- 讀取檔案 (保持不變) ---
    print(f"正在讀取圖片: {image_path}...")
    try:
        img = PIL.Image.open(image_path)
    except FileNotFoundError:
        print(f"❌ 錯誤：找不到圖片檔案 '{image_path}'")
        return
    print(f"正在讀取 XML 原始碼: {xml_path}...")
    try:
        with open(xml_path, "r", encoding="utf-8") as f:
            xml_content = f.read()
    except FileNotFoundError:
        print(f"❌ 錯誤：找不到 XML 檔案 '{xml_path}'")
        return

    prompt = f"""
    你是一位頂尖的 App 自動化測試專家，專精於 Python、Appium、Behave 和 React Native。
    你的任務是分析使用者提供的 App UI **XML 原始碼** 和對應的 **UI 截圖**，並生成**穩定且可以直接運行的** BDD 測試檔案。

    **分析與生成準則 (非常重要)：**

    1.  **以 XML 為絕對真理**：你必須從 XML 原始碼中識別 UI 元素的類型（`class`）、屬性及定位器。截圖僅作為視覺情境參考。

    2.  **定位器策略 (決定性規則)**：根據我們的偵錯結果，在這個專案中，React Native 的 `testID` **被編譯成了 `resource-id`**。因此，你生成定位器時**必須**遵循以下規則：
        * **首選策略**：使用 **XPath**。這是最精確且最穩定的方法。請產生類似 `(AppiumBy.XPATH, "//android.widget.EditText[@resource-id='principalInput']")` 的定位器。
        * **XPath 格式**: `//<class>[@resource-id='<value>']`。`<class>` 和 `<value>` 都必須從 XML 中提取。

    3.  **程式碼穩定性**：
        * **必須加入等待**：所有尋找元素和與元素互動的操作，都**必須**被 `WebDriverWait` 包裹，以處理 App 載入延遲問題。超時時間（TIMEOUT）設定為 15 或 20 秒。
        * **匯入正確的模組**：確保 Python 腳本匯入了所有必要的模組，例如 `AppiumBy` (從 `appium.webdriver.common.appiumby`)、`WebDriverWait` 和 `EC` (從 `selenium.webdriver.support`)。

    4.  **輸出格式**：
        * 生成 `.feature` 和 `.steps.py` 兩個檔案的內容。
        * **嚴格使用 `FEATURE_FILE` 和 `PYTHON_FILE` 作為標記，且標記後直接換行開始程式碼，不要使用 Markdown 的 ``` 符號。**

    --- XML 原始碼如下 ---
    ```xml
    {xml_content}
    ```
    ---結束---

    請嚴格遵守以上所有準則，開始分析並生成檔案。
    """

    print("🧠 正在呼叫 Gemini API 進行分析...")
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    response = model.generate_content([prompt, img])
    
    # --- 檔案處理程式碼 (使用更穩健的解析方法) ---
    try:
        full_response_text = response.text
        
        # 使用 split 來分離由關鍵字標記的區塊
        # 我們以 PYTHON_FILE 為分界點，前面是 feature，後面是 python
        parts = re.split(r'PYTHON_FILE', full_response_text, flags=re.IGNORECASE)
        
        if len(parts) < 2:
            raise ValueError("回應中未找到 PYTHON_FILE 分隔符。")

        feature_content = parts[0].replace("FEATURE_FILE", "").strip()
        python_content = parts[1].strip()

        # 移除可能仍然存在於內容開頭或結尾的 Markdown 程式碼區塊符號
        feature_content = re.sub(r'^\s*```(?:gherkin)?\s*|\s*```\s*$', '', feature_content, flags=re.MULTILINE).strip()
        python_content = re.sub(r'^\s*```(?:python)?\s*|\s*```\s*$', '', python_content, flags=re.MULTILINE).strip()

        if not feature_content or not python_content:
            raise ValueError("解析後，feature 或 python 內容為空。")

        # --- 寫入檔案 (保持不變) ---
        os.makedirs(features_dir, exist_ok=True)
        feature_filename = os.path.join(features_dir, "generated_test.feature")
        with open(feature_filename, "w", encoding="utf-8") as f:
            f.write(feature_content)
        print(f"✅ 成功生成檔案: {feature_filename}")

        os.makedirs(steps_dir, exist_ok=True)
        python_filename = os.path.join(steps_dir, "generated_steps.py")
        with open(python_filename, "w", encoding="utf-8") as f:
            f.write(python_content)
        print(f"✅ 成功生成檔案: {python_filename}")

    except Exception as e:
        print(f"❌ 處理 API 回應時發生錯誤: {e}")
        print("--- Gemini 回應原文 ---")
        print(full_response_text)


if __name__ == "__main__":
    script_dir = os.path.dirname(__file__)
    screenshot_path = os.path.join(script_dir, "ui_screenshot.png")
    xml_source_path = os.path.join(script_dir, "ui_source.xml")
    analyze_ui_and_generate_tests(screenshot_path, xml_source_path)