import pandas as pd 
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from PIL import Image
import os

# مسار مجلد البيانات
data_dir = "../data"  # ../ تعني المجلد الأعلى بالنسبة لمجلد السكريبت
df_path = os.path.join(data_dir, "barber-motorsports-park_analysis.csv")
track_img_path = os.path.join(data_dir, "Track.png")

# قراءة البيانات
df = pd.read_csv(df_path)
laps = sorted(df['lap'].unique())
vehicle = df['vehicle_id'].iloc[0]

# مجلد حفظ الفيديوهات
output_dir = "../outputs/animations"
os.makedirs(output_dir, exist_ok=True)

for lap in laps:
    lap_data = df[df['lap'] == lap]
    
    track_img = Image.open(track_img_path)
    
    fig, ax = plt.subplots()
    ax.imshow(track_img)
    sc = ax.scatter([], [], c=[], cmap='jet', s=50)
    
    def update(frame):
        ax.clear()
        ax.imshow(track_img)
        current = lap_data.iloc[:frame+1]
        sc = ax.scatter(current['outing'], current['value'], c=current['value'], cmap='jet', s=50)
        ax.set_title(f"Lap {lap} - Vehicle {vehicle}")
        ax.axis('off')
        return sc,
    
    anim = FuncAnimation(fig, update, frames=len(lap_data), interval=100)
    anim.save(os.path.join(output_dir, f"Lap_{lap}_animation.mp4"), fps=10, extra_args=['-vcodec', 'libx264'])
    plt.close()
