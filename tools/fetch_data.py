import os
import pandas as pd
import yfinance as yf

def fetch_and_save_daily(symbol, group_name):
    """
    從 yfinance 抓取歷史日線資料，並以最嚴格的標準化格式存入指定群組資料夾
    """
    base_dir = '/content/drive/MyDrive/QUANT_SYSTEM/data/processed'
    group_path = os.path.join(base_dir, group_name.strip())
    
    # 確保群組資料夾存在
    if not os.path.exists(group_path):
        os.makedirs(group_path)
        
    file_path = os.path.join(group_path, f'{symbol}_processed.csv')
    
    try:
        # 1. 抓取最長歷史日線資料
        ticker = yf.Ticker(symbol)
        df = ticker.history(period='max')
        
        if df.empty:
            print(f"⚠️ {symbol} 抓取不到任何 yfinance 資料，已略過。")
            return
            
        # 2. 嚴格格式重構：將原本在 index 的日期拉回欄位
        df.reset_index(inplace=True)
        
        # 尋找並統一日期欄位名稱
        date_col = None
        for col in df.columns:
            if str(col).lower() in ['date', 'datetime']:
                date_col = col
                break
                
        if date_col is None:
            print(f"❌ {symbol} 找不到日期欄位結構。")
            return
            
        # 3. 執行最嚴格的日期格式化：統一轉為無時區的純日期字串 (YYYY-MM-DD)
        df['Date'] = pd.to_datetime(df[date_col], errors='coerce').dt.strftime('%Y-%m-%d')
        df = df.dropna(subset=['Date'])
        
        # 4. 保留並對齊標準欄位，強制轉換數值格式避免型態混亂
        standard_cols = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        available_cols = [c for c in standard_cols if c in df.columns]
        df = df[available_cols]
        
        # 數值型態強制轉為 float / int
        for col in ['Open', 'High', 'Low', 'Close']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        if 'Volume' in df.columns:
            df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce').fillna(0).astype('int64')
            
        # 5. 依據日期由舊到新嚴格排序，並移除任何可能重複的日期
        df = df.sort_values('Date').drop_duplicates(subset=['Date']).reset_index(drop=True)
        
        # 6. 以最乾淨的格式寫入 CSV
        df.to_csv(file_path, index=False)
        print(f"✅ {symbol} 源頭日線已完成極致標準化建置。")
        
    except Exception as e:
        print(f"❌ 處理 {symbol} 發生例外錯誤: {e}")
