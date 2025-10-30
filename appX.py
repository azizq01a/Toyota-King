import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import os
import zipfile

st.set_page_config(page_title="Race Dashboard Pro", layout="wide")
st.title("🏁 Race Dashboard Interactive - Enhanced Version")

# --- رفع ملفات ZIP للتليمترية ---
st.sidebar.header("Upload Telemetry Data (ZIP)")
uploaded_file = st.sidebar.file_uploader("Upload a ZIP file containing CSV telemetry", type=["zip"])

df = None
if uploaded_file:
    st.info("🔄 Processing telemetry files...")
    
    with zipfile.ZipFile(uploaded_file) as z:
        csv_files = [f for f in z.namelist() if f.endswith(".csv")]
        if csv_files:
            dfs = []
            for f in csv_files:
                for sep in [',', ';']:
                    try:
                        df_temp = pd.read_csv(z.open(f), sep=sep, encoding='utf-8')
                        dfs.append(df_temp)
                        break
                    except Exception:
                        continue
            if dfs:
                df = pd.concat(dfs, ignore_index=True)
                # تنظيف أسماء الأعمدة: حذف الفراغات وتحويلها لصغير
                df.columns = [c.strip().lower() for c in df.columns]
                st.success(f"Telemetry loaded: {len(df)} rows")
            else:
                st.error("No valid CSV files found in ZIP.")
        else:
            st.error("No CSV files found in ZIP.")

# --- عرض تحليل البيانات ---
if df is not None:
    st.header("📊 Telemetry Analysis")
    st.subheader("Data Preview")
    st.dataframe(df.head(10))

    # اختيار العمود الرقمي للرسم
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if numeric_cols:
        selected_col = st.selectbox("Choose column to visualize", numeric_cols)
        st.subheader(f"Distribution of {selected_col}")
        fig, ax = plt.subplots()
        df[selected_col].hist(ax=ax, bins=50)
        st.pyplot(fig)
    else:
        st.info("No numeric columns available for plotting.")

    # --- Heatmap لكل قطاع ---
    sector_cols = [c for c in df.columns if 's' in c or 'sector' in c]  # حاول العثور على أعمدة القطاع
    if sector_cols:
        st.subheader("Sector Heatmaps")
        selected_sector = st.selectbox("Select sector column", sector_cols)
        try:
            fig, ax = plt.subplots()
            sns.heatmap(df[[selected_sector]].corr(), annot=True, ax=ax)
            st.pyplot(fig)
        except Exception as e:
            st.warning(f"Could not generate heatmap: {e}")

    # --- مقارنة أداء السائقين ---
    driver_col_candidates = [c for c in df.columns if 'vehicle' in c or 'driver' in c]
    if driver_col_candidates:
        driver_col = driver_col_candidates[0]
        st.subheader("Driver Comparison")
        selected_driver = st.selectbox("Select driver", df[driver_col].unique())
        driver_data = df[df[driver_col] == selected_driver]
        st.write(driver_data.head())

# --- عرض خرائط الحلبات ---
st.header("🗺️ Circuit Maps")
maps_folder = "maps"
if os.path.exists(maps_folder):
    map_files = [f for f in os.listdir(maps_folder) if f.lower().endswith(".png")]
    
    if map_files:
        selected_map = st.selectbox("Select Circuit Map", map_files)
        map_path = os.path.join(maps_folder, selected_map)
        image = Image.open(map_path)
        
        st.subheader(selected_map.replace("_", " ").replace(".png", ""))
        st.image(image, use_container_width=True)
    else:
        st.warning("No PNG maps found in 'maps/' folder.")
else:
    st.info(f"Maps folder '{maps_folder}' does not exist. Please convert PDFs to PNGs first.")