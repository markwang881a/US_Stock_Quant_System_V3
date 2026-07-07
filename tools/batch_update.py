import pandas as pd
import time
from fetch_data import fetch_and_save_daily

def run_automated_batch_update():
    config_path = '/content/drive/MyDrive/QUANT_SYSTEM/data/config/all_stocks_list.csv'
    
    # 讀取並清理資料 (去重)
    df = pd.read_csv(config_path)
    df = df.drop_duplicates(subset=['group', 'symbol'])
    
    print(f"✅ 設定檔讀取成功，開始更新程序，目標筆數: {len(df)}")
    
    # 遍歷群組進行處理
    for group_name, group_df in df.groupby('group'):
        symbols = group_df['symbol'].unique()
        print(f"📂 正在處理群組: {group_name} ({len(symbols)} 檔)")
        
        for symbol in symbols:
            try:
                fetch_and_save_daily(symbol, group_name)
                # 加入短暫延遲，避免 API 連線頻率過高
                time.sleep(0.5) 
            except Exception as e:
                print(f"❌ 更新 {symbol} 失敗: {e}")
                
    print("🚀 所有股票已更新完畢！")
