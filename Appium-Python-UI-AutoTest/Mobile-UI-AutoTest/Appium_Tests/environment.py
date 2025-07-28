import os
from appium import webdriver
from appium.options.android import UiAutomator2Options

# --- Behave Hooks ---

def before_all(context):
    """
    在所有測試場景開始前執行一次
    """
    print("🚀 正在啟動 Appium Driver...")

    # --- 重要：設定 Appium 連線資訊 ---
    # 根據您的專案結構，計算出 app-debug.apk 的絕對路徑
    # __file__ 是 'environment.py' 的路徑
    # 我們需要往上兩層找到 'Mobile-UI-AutoTest' 的根目錄，再往下找到 'assets'
    script_dir = os.path.dirname(__file__) # '.../Appium_Tests'
    project_root = os.path.abspath(os.path.join(script_dir, '..')) # '.../Mobile-UI-AutoTest'
    app_path = os.path.join(project_root, 'assets', 'app-debug.apk')
    
    print(f"正在使用 App: {app_path}")

    # 使用 Appium 2.x 推薦的 Options 物件來設定
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    # 這裡填寫您模擬器的名稱，可透過 `adb devices` 指令查詢
    # 例如： "emulator-5554" 或 "Pixel_6_API_34"
    options.device_name = "Android Emulator" 
    options.app = app_path
    
    # 確保 Appium Server 正在 'http://127.0.0.1:4723' 運行
    try:
        context.driver = webdriver.Remote('http://127.0.0.1:4723', options=options)
        # 設定一個隱性等待，讓測試在找不到元素時，能多等一下，增加穩定性
        context.driver.implicitly_wait(15) 
        print("✅ Appium Driver 啟動成功")
    except Exception as e:
        print(f"❌ Appium Driver 啟動失敗: {e}")
        # 如果啟動失敗，直接結束測試
        raise

def after_all(context):
    """
    在所有測試場景結束後執行一次
    """
    # 檢查 driver 是否存在，如果存在就關閉它
    if hasattr(context, 'driver') and context.driver:
        print("👋 正在關閉 Appium Driver...")
        context.driver.quit()
        print("✅ Appium Driver 已關閉")


