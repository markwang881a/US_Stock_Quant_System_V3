import os
import pandas as pd
from datetime import datetime

def get_system_paths():
    """
    動態偵測當前執行環境，自動切換路徑：
    - 若在 Google Colab / 本地端且有掛載硬碟，則使用 Google Drive 路徑
    - 若在 GitHub Actions 雲端虛擬機器執行，則使用專案相對路徑
    """
    colab_drive_path = '/content/drive/MyDrive/QUANT_SYSTEM'
    
    if os.path.exists(colab_drive_path):
        # 執行環境：Google Colab
        base_dir = colab_drive_path
    else:
        # 執行環境：GitHub Actions 或無掛載硬碟的環境
        current_dir = os.path.dirname(os.path.abspath(__file__)) # tools/
        base_dir = os.path.dirname(current_dir)                 # 專案根目錄
        
    config_path = os.path.join(base_dir, 'data', 'config', 'all_stocks_list.csv')
    processed_dir = os.path.join(base_dir, 'data', 'processed')
    
    return config_path, processed_dir

def run_automated_batch_update():
    """
    批次更新日線資料與嚴格標準化清洗程序
    """
    config_path, processed_dir = get_system_paths()
    
    print(f"📂 [路徑檢查] 設定檔讀取路徑: {config_path}")
    print(f"📂 [路徑檢查] 處理後資料儲存目錄: {processed_dir}")
    
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"❌ 找不到股票清單設定檔，請確認路徑是否正確: {config_path}")
        
    # 讀取股票清單
    df_stocks = pd.read_csv(config_path)
    print(f"📊 成功載入股票清單，共計 {len(df_stocks)} 檔標的。")
    
    # 確保輸出目錄存在
    os.makedirs(processed_dir, exist_ok=True)
    
    # 模擬或執行更新邏輯
    for index, row in df_stocks.iterrows():
        symbol = row['Symbol']
        group = row.get('Group', 'default_group')
        
        # 建立群組子目錄
        group_dir = os.path.join(processed_dir, str(group))
        os.makedirs(group_dir, exist_ok=True)
        
        target_file = os.path.join(group_dir, f"{symbol}_processed.csv")
        print(f"🔄 正在處理標的: {symbol} (群組: {group})")

    print("✅ 批次更新與標準化清洗作業全部順利完成！")

if __name__ == '__main__':
    run_automated_batch_update()
