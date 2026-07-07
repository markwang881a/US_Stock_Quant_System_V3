import os
import pandas as pd

def run_full_resample_with_quarterly():
    base_dir = '/content/drive/MyDrive/QUANT_SYSTEM/data/processed'
    if not os.path.exists(base_dir):
        print(f"❌ 錯誤：找不到路徑 {base_dir}")
        return
        
    groups = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
    
    # 聚合規則定義
    agg_rules = {
        'Open': 'first',
        'High': 'max',
        'Low': 'min',
        'Close': 'last',
        'Volume': 'sum'
    }
    
    for group in groups:
        group_path = os.path.join(base_dir, group)
        files = [f for f in os.listdir(group_path) if f.endswith('_processed.csv')]
        
        print(f"🔄 正在為群組 [{group}] 進行強固型多時框歷史與模擬資料聚合...")
        for file in files:
            symbol = file.replace('_processed.csv', '')
            file_path = os.path.join(group_path, file)
            
            try:
                df = pd.read_csv(file_path)
                
                # 防呆：確保欄位中包含 Date，若 Date 不在欄位但存在於 index，則重設索引
                if 'Date' not in df.columns:
                    if 'Unnamed: 0' in df.columns:
                        df.rename(columns={'Unnamed: 0': 'Date'}, inplace=True)
                    else:
                        df.reset_index(inplace=True)
                        if 'index' in df.columns:
                            df.rename(columns={'index': 'Date'}, inplace=True)
                
                if 'Date' not in df.columns:
                    print(f"⚠️ {symbol} 找不到 Date 欄位結構，已跳過。")
                    continue
                
                # 強制轉換日期並過濾不合法行
                df['Date'] = pd.to_datetime(df['Date'], utc=True, errors='coerce')
                df = df.dropna(subset=['Date'])
                
                if df.empty:
                    print(f"⚠️ {symbol} 日期資料完全失效，已跳過。")
                    continue
                
                # 設定索引並確實轉為 DatetimeIndex
                df.set_index('Date', inplace=True)
                df.index = pd.DatetimeIndex(df.index)
                df = df.sort_index()  # 確保時間由舊到新排序
                
                # 執行多時框聚合
                df_weekly = df.resample('W-FRI').agg(agg_rules).dropna()
                df_monthly = df.resample('ME').agg(agg_rules).dropna()
                df_quarterly = df.resample('QE').agg(agg_rules).dropna()
                
                # 儲存檔案
                df_weekly.to_csv(os.path.join(group_path, f'{symbol}_weekly_sim.csv'))
                df_monthly.to_csv(os.path.join(group_path, f'{symbol}_monthly_sim.csv'))
                df_quarterly.to_csv(os.path.join(group_path, f'{symbol}_quarterly_sim.csv'))
            except Exception as e:
                print(f"❌ {symbol} 聚合失敗: {e}")
                
    print("✅ 所有標的之強固型多時框聚合已全面完成！")
