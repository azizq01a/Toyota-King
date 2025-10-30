
import pandas as pd 
import matplotlib.pyplot as plt
from PIL import Image
import os

# مجلد البيانات (نسبي إلى مكان السكريبت)
data_dir = "../data"  # ../ يعني المجلد الأعلى بالنسبة لمجلد السكريبت
df_path = os.path.join(data_dir, "barber-motorsports-park_analysis.csv")
track_img_path = os.path.join(data_dir, "Track.png")

# تحميل البيانات
df = pd.read_csv(df_path)
laps = sorted(df['lap'].unique())
vehicle = df['vehicle_id'].iloc[0]

# إنشاء مجلد outputs إذا لم يكن موجود
output_dir = "../outputs"
os.makedirs(output_dir, exist_ok=True)

# رسم Heatmap لكل Lap
for lap in laps:
    lap_data = df[df['lap'] == lap]
    
    # تحميل صورة المسار
    track_img = Image.open(track_img_path)
    plt.imshow(track_img)
    
    # رسم النقاط (يمكن تغيير اللون حسب السرعة)
    plt.scatter(lap_data['outing'], lap_data['value'], c=lap_data['value'], cmap='jet', s=50)
    
    plt.title(f"Lap {lap} - Vehicle {vehicle}")
    plt.axis('off')
    
    # حفظ الصورة
    plt.savefig(os.path.join(output_dir, f"Lap_{lap}_heatmap.png"), bbox_inches='tight', dpi=150)
    plt.close()
