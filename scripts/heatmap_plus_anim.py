import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from PIL import Image
import seaborn as sns
import cv2

# ------------------------
# CONFIGURATION
# ------------------------
DATA_FILE = os.path.join("..", "data", "barber-motorsports-park_analysis.csv")
TRACK_IMG_FILE = os.path.join("..", "data", "Track.png")
OUTPUT_DIR = os.path.join("..", "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

VIDEO_PATH = os.path.join(OUTPUT_DIR, "heatmap_animation.mp4")

# ------------------------
# LOAD DATA
# ------------------------
print(f"🔍 Using data file: {DATA_FILE}")
df = pd.read_csv(DATA_FILE)
print(f"ℹ️ Columns: {list(df.columns)}")

# تحديد الأعمدة الرقمية والنصية تلقائيًا
numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
value_col = "telemetry_value" if "telemetry_value" in df.columns else numeric_cols[-1]
x_col = "outing" if "outing" in df.columns else numeric_cols[0]
y_col = "expire_at" if "expire_at" in df.columns else None

print(f"🎯 Value column for coloring: {value_col}")
print(f"📍 Spatial columns chosen: X = {x_col} , Y = {y_col}")

laps = sorted(df['lap'].unique())
print(f"🏁 Detected laps: {len(laps)} (sample: {laps[:5]})")

# ------------------------
# LOAD TRACK IMAGE
# ------------------------
track_img = Image.open(TRACK_IMG_FILE)
track_width, track_height = track_img.size
print(f"📐 Track image size: {track_width}x{track_height}")

# ------------------------
# CREATE HEATMAP IMAGES
# ------------------------
heatmap_images = []

for lap in laps:
    lap_df = df[df['lap'] == lap]
    
    # X values
    x_vals = lap_df[x_col].to_numpy(dtype=float)
    
    # Y values
    if y_col and y_col in lap_df.columns:
        try:
            y_vals = lap_df[y_col].to_numpy(dtype=float)
            if np.all(y_vals == y_vals[0]):  # إذا كانت ثابتة
                y_vals = np.linspace(0, 1, len(x_vals))
        except:
            y_vals = np.linspace(0, 1, len(x_vals))
    else:
        y_vals = np.linspace(0, 1, len(x_vals))
    
    values = lap_df[value_col].to_numpy(dtype=float)
    
    plt.figure(figsize=(10, 8))
    plt.imshow(track_img)
    
    # KDE فقط إذا هناك تباين
    if np.var(x_vals) > 0 and np.var(y_vals) > 0:
        sns.kdeplot(
            x=x_vals, y=y_vals, weights=values, cmap='jet', fill=True, bw_adjust=0.5, warn_singular=False
        )
    else:
        plt.scatter(x_vals, y_vals, c=values, cmap='jet', s=50)
    
    plt.axis('off')
    plt.title(f"Lap {lap}")
    
    lap_img_path = os.path.join(OUTPUT_DIR, f"Lap_{int(lap)}.png")
    plt.savefig(lap_img_path, bbox_inches='tight', dpi=150)
    plt.close()
    
    heatmap_images.append(lap_img_path)
    print(f"✅ تم إنشاء Heatmap للفة {lap}")

# ------------------------
# CREATE VIDEO
# ------------------------
print("🎞️ إنشاء فيديو من اللفات...")

# اقرأ أول صورة لتحديد حجم الفيديو
first_img = cv2.imread(heatmap_images[0])
height, width, layers = first_img.shape

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter(VIDEO_PATH, fourcc, 10, (width, height))

for img_path in heatmap_images:
    img = cv2.imread(img_path)
    video.write(img)

video.release()
print(f"✅ تم إنشاء الفيديو بنجاح: {VIDEO_PATH}")
