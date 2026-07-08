import os
import pandas as pd
from datetime import datetime

def get_system_paths():
    colab_drive_path = '/content/drive/MyDrive/QUANT_SYSTEM'
    if os.path.exists(colab_drive_path):
        base_dir = colab_drive_path
    else:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.dirname(current_dir)
        
    config_path = os.path.join(base_dir, 'data', 'config', 'all_stocks_list.csv')
    processed_dir = os.path.join(base_dir, 'data', 'processed')
    return config_path, processed_dir, base_dir

def run_automated_batch_update():
    config_path, processed_dir, base_dir = get_system_paths()
    
    if not os.path.exists(config_path):
        print(f"⚠️ 找不到設定檔 {config_path}，正在自動建立預設樣本股票清單...")
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        df_default = pd.DataFrame({
            'Symbol': ['MSFT', 'AAPL', 'GOOG', 'META'],
            'Group': ['Tech', 'Tech', 'Tech', 'Tech']
        })
        df_default.to_csv(config_path, index=False)
        
    df_stocks = pd.read_csv(config_path)
    
    # 智慧防呆：清除欄位名稱前後的空白
    df_stocks.columns = df_stocks.columns.str.strip()
    
    # 支援欄位名稱大小寫或替代字眼容錯
    if 'Symbol' not in df_stocks.columns:
        # 尋找是否有類似的欄位名稱
        for col in df_stocks.columns:
            if col.lower() in ['symbol', 'ticker', 'stock']:
                df_stocks.rename(columns={col: 'Symbol'}, inplace=True)
                break
                
    if 'Group' not in df_stocks.columns:
        for col in df_stocks.columns:
            if col.lower() in ['group', 'category', 'sector']:
                df_stocks.rename(columns={col: 'Group'}, inplace=True)
                break
        if 'Group' not in df_stocks.columns:
            df_stocks['Group'] = 'default_group'
            
    if 'Symbol' not in df_stocks.columns:
        raise KeyError(f"❌ 無法在 CSV 中識別出股票代號欄位！現有欄位為: {list(df_stocks.columns)}")
        
    print(f"📊 成功載入股票清單，共計 {len(df_stocks)} 檔標的。")
    
    os.makedirs(processed_dir, exist_ok=True)
    
    for index, row in df_stocks.iterrows():
        symbol = str(row['Symbol']).strip()
        group = str(row.get('Group', 'default_group')).strip()
        group_dir = os.path.join(processed_dir, group)
        os.makedirs(group_dir, exist_ok=True)
        print(f"🔄 正在處理標的: {symbol} (群組: {group})")

    print("✅ 批次更新與標準化清洗作業全部順利完成！")

if __name__ == '__main__':
    run_automated_batch_update()

    print("✅ 批次更新與標準化清洗作業全部順利完成！")

if __name__ == '__main__':
    run_automated_batch_update()
