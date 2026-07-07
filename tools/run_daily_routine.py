import os
import sys

# 直接指定 Google Drive 中的 tools 絕對路徑，完美適配 Colab / Jupyter 筆記本環境
current_dir = '/content/drive/MyDrive/QUANT_SYSTEM/tools'
if current_dir not in sys.path:
    sys.path.append(current_dir)

from batch_update import run_automated_batch_update
from resample_data import run_full_resample_with_quarterly

def run_daily_full_routine():
    print("=" * 60)
    print("🚀 [開始執行] 每日美股量化數據自動化更新與聚合程序")
    print("=" * 60)
    
    print("\n--- 階段一：批次更新日線資料與嚴格標準化清洗 ---")
    run_automated_batch_update()
    
    print("\n--- 階段二：執行多時框 (週、月、季) 模擬與歷史資料聚合 ---")
    run_full_resample_with_quarterly()
    
    print("\n" + "=" * 60)
    print("🎉 [執行完畢] 所有日線與多時框模擬檔案已全面更新完成！")
    print("=" * 60)

if __name__ == '__main__':
    run_daily_full_routine()
