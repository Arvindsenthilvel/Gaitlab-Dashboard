import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json, math, io, re as _re

st.set_page_config(
    page_title="GaitLab Dashboard",
    page_icon="🦿",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
html, body, [data-testid="stAppViewContainer"] {
    background-color: #0d1117; color: #e6edf3;
}
[data-testid="stSidebar"] {
    background-color: #161b22 !important;
    border-right: 1px solid #30363d;
}
[data-testid="stSidebar"] * { color: #e6edf3 !important; }
[data-testid="metric-container"] {
    background: linear-gradient(135deg, rgba(88,166,255,0.08), rgba(188,140,255,0.04));
    border: 1px solid rgba(88,166,255,0.15); border-radius: 10px; padding: 12px 16px;
}
[data-testid="stMetricValue"] { color: #58a6ff !important; font-size: 1.8rem !important; }
[data-testid="stMetricDelta"] { font-size: 0.85rem !important; }
[data-testid="stMetricLabel"] { color: #7d8590 !important; font-size: 0.8rem !important; }
[data-testid="stTabs"] button { color: #7d8590 !important; border-radius: 6px 6px 0 0; font-size: 13px; }
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #58a6ff !important; border-bottom: 2px solid #58a6ff !important;
    background: rgba(88,166,255,0.08) !important;
}
[data-testid="stDataFrame"] { border-radius: 8px; }
.info-card {
    background: rgba(88,166,255,0.07); border-left: 3px solid #58a6ff;
    border-radius: 0 8px 8px 0; padding: 10px 14px; margin: 6px 0;
    font-size: 13px; color: #e6edf3; line-height: 1.6;
}
.info-card.purple { border-left-color: #bc8cff; background: rgba(188,140,255,0.07); }
.info-card.amber  { border-left-color: #e3b341; background: rgba(227,179,65,0.07); }
.info-card.green  { border-left-color: #3fb950; background: rgba(63,185,80,0.07); }
.info-card.red    { border-left-color: #f85149; background: rgba(248,81,73,0.07); }
.infer-title { font-weight: 700; color: #e6edf3; font-size: 14px; margin-bottom: 3px; }
.infer-cat   { color: #58a6ff; font-size: 11px; margin-left: 6px; }
.infer-body  { color: #7d8590; font-size: 12.5px; }
.section-header {
    font-size: 22px; font-weight: 700;
    background: linear-gradient(90deg, #58a6ff, #bc8cff);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 4px;
}
.study-tag {
    display:inline-block; background:rgba(88,166,255,0.1);
    border:1px solid rgba(88,166,255,0.2); border-radius:6px;
    padding:3px 10px; font-size:11px; color:#79c0ff; margin-bottom:12px;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# DATA (anonymised — all participants coded as Subject 1–25)
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    return [{"id": 1, "name": "Subject 1", "age": 24, "height": 177.6, "weight": 73.5, "Walking_speed_ctrl": 1.192, "Walking_speed_smart": 1.107, "Cadence_ctrl": 119.854, "Cadence_smart": 118.415, "Stride_length_ctrl": 1.188, "Stride_length_smart": 1.101, "Double_support_ctrl": 14.409, "Double_support_smart": 17.661, "Stride_variability_ctrl": 2.909, "Stride_variability_smart": 9.99, "Peak_hip_flexion_ctrl": 25.735, "Peak_hip_flexion_smart": 32.105, "Peak_knee_flexion_ctrl": 63.356, "Peak_knee_flexion_smart": 59.019, "Peak_ankle_df_ctrl": 14.237, "Peak_ankle_df_smart": 17.836, "Braking_impulse_ctrl": -12.974, "Braking_impulse_smart": -21.234, "Propulsion_impulse_ctrl": 21.095, "Propulsion_impulse_smart": 19.78, "EMG_RMS_ctrl": 0.339, "EMG_RMS_smart": 0.608}, {"id": 2, "name": "Subject 2", "age": 25, "height": 168.6, "weight": 68.0, "Walking_speed_ctrl": 1.373, "Walking_speed_smart": 1.222, "Cadence_ctrl": 101.747, "Cadence_smart": 102.859, "Stride_length_ctrl": 1.193, "Stride_length_smart": 1.311, "Double_support_ctrl": 12.056, "Double_support_smart": 13.246, "Stride_variability_ctrl": 0.994, "Stride_variability_smart": 1.425, "Peak_hip_flexion_ctrl": 40.814, "Peak_hip_flexion_smart": 38.544, "Peak_knee_flexion_ctrl": 64.272, "Peak_knee_flexion_smart": 66.539, "Peak_ankle_df_ctrl": 16.221, "Peak_ankle_df_smart": 18.189, "Braking_impulse_ctrl": -18.844, "Braking_impulse_smart": -10.067, "Propulsion_impulse_ctrl": 16.001, "Propulsion_impulse_smart": 18.96, "EMG_RMS_ctrl": 0.421, "EMG_RMS_smart": 0.63}, {"id": 3, "name": "Subject 3", "age": 24, "height": 165.1, "weight": 56.2, "Walking_speed_ctrl": 1.278, "Walking_speed_smart": 1.287, "Cadence_ctrl": 113.793, "Cadence_smart": 116.367, "Stride_length_ctrl": 1.467, "Stride_length_smart": 1.145, "Double_support_ctrl": 10.609, "Double_support_smart": 23.179, "Stride_variability_ctrl": 2.763, "Stride_variability_smart": 5.473, "Peak_hip_flexion_ctrl": 33.797, "Peak_hip_flexion_smart": 42.725, "Peak_knee_flexion_ctrl": 67.186, "Peak_knee_flexion_smart": 67.754, "Peak_ankle_df_ctrl": 14.619, "Peak_ankle_df_smart": 16.434, "Braking_impulse_ctrl": -21.293, "Braking_impulse_smart": -11.962, "Propulsion_impulse_ctrl": 16.291, "Propulsion_impulse_smart": 14.944, "EMG_RMS_ctrl": 0.562, "EMG_RMS_smart": 0.208}, {"id": 4, "name": "Subject 4", "age": 23, "height": 168.2, "weight": 55.5, "Walking_speed_ctrl": 1.256, "Walking_speed_smart": 1.149, "Cadence_ctrl": 116.682, "Cadence_smart": 105.982, "Stride_length_ctrl": 1.115, "Stride_length_smart": 1.213, "Double_support_ctrl": 14.601, "Double_support_smart": 13.464, "Stride_variability_ctrl": 1.158, "Stride_variability_smart": 8.104, "Peak_hip_flexion_ctrl": 30.795, "Peak_hip_flexion_smart": 38.122, "Peak_knee_flexion_ctrl": 61.343, "Peak_knee_flexion_smart": 63.268, "Peak_ankle_df_ctrl": 15.015, "Peak_ankle_df_smart": 19.549, "Braking_impulse_ctrl": -22.438, "Braking_impulse_smart": -15.549, "Propulsion_impulse_ctrl": 14.851, "Propulsion_impulse_smart": 14.497, "EMG_RMS_ctrl": 0.515, "EMG_RMS_smart": 0.867}, {"id": 5, "name": "Subject 5", "age": 24, "height": 170.2, "weight": 64.2, "Walking_speed_ctrl": 1.325, "Walking_speed_smart": 1.191, "Cadence_ctrl": 124.924, "Cadence_smart": 112.866, "Stride_length_ctrl": 1.257, "Stride_length_smart": 1.022, "Double_support_ctrl": 8.573, "Double_support_smart": 23.302, "Stride_variability_ctrl": 4.498, "Stride_variability_smart": 2.678, "Peak_hip_flexion_ctrl": 35.768, "Peak_hip_flexion_smart": 36.848, "Peak_knee_flexion_ctrl": 64.319, "Peak_knee_flexion_smart": 65.359, "Peak_ankle_df_ctrl": 13.949, "Peak_ankle_df_smart": 18.124, "Braking_impulse_ctrl": -20.937, "Braking_impulse_smart": -7.872, "Propulsion_impulse_ctrl": 21.803, "Propulsion_impulse_smart": 17.327, "EMG_RMS_ctrl": 0.335, "EMG_RMS_smart": 0.306}, {"id": 6, "name": "Subject 6", "age": 25, "height": 170.2, "weight": 60.9, "Walking_speed_ctrl": 1.178, "Walking_speed_smart": 0.726, "Cadence_ctrl": 114.67, "Cadence_smart": 119.345, "Stride_length_ctrl": 1.111, "Stride_length_smart": 0.908, "Double_support_ctrl": 18.647, "Double_support_smart": 12.476, "Stride_variability_ctrl": 1.974, "Stride_variability_smart": 8.076, "Peak_hip_flexion_ctrl": 25.523, "Peak_hip_flexion_smart": 49.226, "Peak_knee_flexion_ctrl": 61.618, "Peak_knee_flexion_smart": 65.626, "Peak_ankle_df_ctrl": 16.561, "Peak_ankle_df_smart": 17.539, "Braking_impulse_ctrl": -23.078, "Braking_impulse_smart": -17.878, "Propulsion_impulse_ctrl": 25.36, "Propulsion_impulse_smart": 15.659, "EMG_RMS_ctrl": 0.459, "EMG_RMS_smart": 0.451}, {"id": 7, "name": "Subject 7", "age": 19, "height": 171.5, "weight": 62.6, "Walking_speed_ctrl": 1.203, "Walking_speed_smart": 1.299, "Cadence_ctrl": 110.89, "Cadence_smart": 112.064, "Stride_length_ctrl": 1.443, "Stride_length_smart": 1.079, "Double_support_ctrl": 13.877, "Double_support_smart": 18.566, "Stride_variability_ctrl": 1.942, "Stride_variability_smart": 8.019, "Peak_hip_flexion_ctrl": 40.241, "Peak_hip_flexion_smart": 28.89, "Peak_knee_flexion_ctrl": 66.918, "Peak_knee_flexion_smart": 63.339, "Peak_ankle_df_ctrl": 12.496, "Peak_ankle_df_smart": 18.179, "Braking_impulse_ctrl": -17.99, "Braking_impulse_smart": -19.16, "Propulsion_impulse_ctrl": 20.923, "Propulsion_impulse_smart": 17.775, "EMG_RMS_ctrl": 0.222, "EMG_RMS_smart": 0.527}, {"id": 8, "name": "Subject 8", "age": 22, "height": 176.1, "weight": 68.6, "Walking_speed_ctrl": 1.307, "Walking_speed_smart": 1.051, "Cadence_ctrl": 107.894, "Cadence_smart": 114.546, "Stride_length_ctrl": 1.131, "Stride_length_smart": 1.346, "Double_support_ctrl": 15.996, "Double_support_smart": 16.035, "Stride_variability_ctrl": 2.664, "Stride_variability_smart": 10.175, "Peak_hip_flexion_ctrl": 42.461, "Peak_hip_flexion_smart": 37.603, "Peak_knee_flexion_ctrl": 69.055, "Peak_knee_flexion_smart": 65.664, "Peak_ankle_df_ctrl": 17.292, "Peak_ankle_df_smart": 16.806, "Braking_impulse_ctrl": -13.621, "Braking_impulse_smart": -15.943, "Propulsion_impulse_ctrl": 25.373, "Propulsion_impulse_smart": 11.339, "EMG_RMS_ctrl": 0.283, "EMG_RMS_smart": 0.841}, {"id": 9, "name": "Subject 9", "age": 24, "height": 177.6, "weight": 64.7, "Walking_speed_ctrl": 1.177, "Walking_speed_smart": 0.877, "Cadence_ctrl": 104.289, "Cadence_smart": 139.268, "Stride_length_ctrl": 1.207, "Stride_length_smart": 1.066, "Double_support_ctrl": 12.683, "Double_support_smart": 14.911, "Stride_variability_ctrl": 1.413, "Stride_variability_smart": 1.972, "Peak_hip_flexion_ctrl": 38.458, "Peak_hip_flexion_smart": 33.136, "Peak_knee_flexion_ctrl": 66.396, "Peak_knee_flexion_smart": 63.861, "Peak_ankle_df_ctrl": 17.382, "Peak_ankle_df_smart": 19.527, "Braking_impulse_ctrl": -19.193, "Braking_impulse_smart": -18.768, "Propulsion_impulse_ctrl": 25.218, "Propulsion_impulse_smart": 22.591, "EMG_RMS_ctrl": 0.378, "EMG_RMS_smart": 0.794}, {"id": 10, "name": "Subject 10", "age": 23, "height": 177.6, "weight": 70.8, "Walking_speed_ctrl": 1.098, "Walking_speed_smart": 0.922, "Cadence_ctrl": 109.245, "Cadence_smart": 125.197, "Stride_length_ctrl": 1.288, "Stride_length_smart": 1.273, "Double_support_ctrl": 16.552, "Double_support_smart": 23.833, "Stride_variability_ctrl": 3.502, "Stride_variability_smart": 4.948, "Peak_hip_flexion_ctrl": 35.625, "Peak_hip_flexion_smart": 29.401, "Peak_knee_flexion_ctrl": 60.901, "Peak_knee_flexion_smart": 69.837, "Peak_ankle_df_ctrl": 17.874, "Peak_ankle_df_smart": 16.484, "Braking_impulse_ctrl": -17.883, "Braking_impulse_smart": -16.933, "Propulsion_impulse_ctrl": 20.004, "Propulsion_impulse_smart": 15.449, "EMG_RMS_ctrl": 0.58, "EMG_RMS_smart": 0.548}, {"id": 11, "name": "Subject 11", "age": 21, "height": 156.5, "weight": 49.7, "Walking_speed_ctrl": 1.182, "Walking_speed_smart": 0.973, "Cadence_ctrl": 112.589, "Cadence_smart": 94.532, "Stride_length_ctrl": 1.194, "Stride_length_smart": 1.212, "Double_support_ctrl": 14.154, "Double_support_smart": 23.435, "Stride_variability_ctrl": 3.732, "Stride_variability_smart": 3.644, "Peak_hip_flexion_ctrl": 45.418, "Peak_hip_flexion_smart": 35.802, "Peak_knee_flexion_ctrl": 61.872, "Peak_knee_flexion_smart": 61.584, "Peak_ankle_df_ctrl": 14.679, "Peak_ankle_df_smart": 17.669, "Braking_impulse_ctrl": -16.75, "Braking_impulse_smart": -17.536, "Propulsion_impulse_ctrl": 15.666, "Propulsion_impulse_smart": 17.185, "EMG_RMS_ctrl": 0.81, "EMG_RMS_smart": 0.424}, {"id": 12, "name": "Subject 12", "age": 24, "height": 173.5, "weight": 64.4, "Walking_speed_ctrl": 1.022, "Walking_speed_smart": 1.109, "Cadence_ctrl": 106.611, "Cadence_smart": 102.526, "Stride_length_ctrl": 1.469, "Stride_length_smart": 1.079, "Double_support_ctrl": 13.331, "Double_support_smart": 18.492, "Stride_variability_ctrl": 1.615, "Stride_variability_smart": 8.256, "Peak_hip_flexion_ctrl": 34.155, "Peak_hip_flexion_smart": 37.905, "Peak_knee_flexion_ctrl": 58.134, "Peak_knee_flexion_smart": 73.856, "Peak_ankle_df_ctrl": 16.783, "Peak_ankle_df_smart": 17.315, "Braking_impulse_ctrl": -21.785, "Braking_impulse_smart": -10.998, "Propulsion_impulse_ctrl": 16.72, "Propulsion_impulse_smart": 11.194, "EMG_RMS_ctrl": 0.178, "EMG_RMS_smart": 0.879}, {"id": 13, "name": "Subject 13", "age": 20, "height": 168.4, "weight": 79.4, "Walking_speed_ctrl": 1.278, "Walking_speed_smart": 0.599, "Cadence_ctrl": 122.102, "Cadence_smart": 108.446, "Stride_length_ctrl": 1.202, "Stride_length_smart": 1.476, "Double_support_ctrl": 15.231, "Double_support_smart": 18.972, "Stride_variability_ctrl": 1.784, "Stride_variability_smart": 4.889, "Peak_hip_flexion_ctrl": 32.753, "Peak_hip_flexion_smart": 47.957, "Peak_knee_flexion_ctrl": 58.608, "Peak_knee_flexion_smart": 66.117, "Peak_ankle_df_ctrl": 14.09, "Peak_ankle_df_smart": 17.762, "Braking_impulse_ctrl": -16.952, "Braking_impulse_smart": -18.924, "Propulsion_impulse_ctrl": 21.454, "Propulsion_impulse_smart": 15.792, "EMG_RMS_ctrl": 0.128, "EMG_RMS_smart": 0.913}, {"id": 14, "name": "Subject 14", "age": 25, "height": 168.4, "weight": 76.3, "Walking_speed_ctrl": 1.381, "Walking_speed_smart": 0.884, "Cadence_ctrl": 124.899, "Cadence_smart": 128.921, "Stride_length_ctrl": 1.435, "Stride_length_smart": 1.523, "Double_support_ctrl": 12.517, "Double_support_smart": 20.142, "Stride_variability_ctrl": 3.546, "Stride_variability_smart": 2.239, "Peak_hip_flexion_ctrl": 44.777, "Peak_hip_flexion_smart": 28.98, "Peak_knee_flexion_ctrl": 64.397, "Peak_knee_flexion_smart": 60.723, "Peak_ankle_df_ctrl": 15.238, "Peak_ankle_df_smart": 17.374, "Braking_impulse_ctrl": -18.036, "Braking_impulse_smart": -11.294, "Propulsion_impulse_ctrl": 16.318, "Propulsion_impulse_smart": 13.707, "EMG_RMS_ctrl": null, "EMG_RMS_smart": null}, {"id": 15, "name": "Subject 15", "age": 19, "height": 182.8, "weight": 59.3, "Walking_speed_ctrl": 1.069, "Walking_speed_smart": 0.782, "Cadence_ctrl": 121.409, "Cadence_smart": 125.59, "Stride_length_ctrl": 1.167, "Stride_length_smart": 1.15, "Double_support_ctrl": 9.902, "Double_support_smart": 25.854, "Stride_variability_ctrl": 1.933, "Stride_variability_smart": 3.528, "Peak_hip_flexion_ctrl": 32.528, "Peak_hip_flexion_smart": 30.136, "Peak_knee_flexion_ctrl": 64.669, "Peak_knee_flexion_smart": 61.055, "Peak_ankle_df_ctrl": 13.85, "Peak_ankle_df_smart": 16.661, "Braking_impulse_ctrl": -16.005, "Braking_impulse_smart": -19.121, "Propulsion_impulse_ctrl": 20.547, "Propulsion_impulse_smart": 23.923, "EMG_RMS_ctrl": null, "EMG_RMS_smart": null}, {"id": 16, "name": "Subject 16", "age": 22, "height": 166.1, "weight": 67.0, "Walking_speed_ctrl": 1.231, "Walking_speed_smart": 1.03, "Cadence_ctrl": 105.616, "Cadence_smart": 119.102, "Stride_length_ctrl": 1.383, "Stride_length_smart": 1.065, "Double_support_ctrl": 10.067, "Double_support_smart": 21.535, "Stride_variability_ctrl": 2.294, "Stride_variability_smart": 1.83, "Peak_hip_flexion_ctrl": 36.488, "Peak_hip_flexion_smart": 38.6, "Peak_knee_flexion_ctrl": 64.857, "Peak_knee_flexion_smart": 70.54, "Peak_ankle_df_ctrl": 16.654, "Peak_ankle_df_smart": 16.858, "Braking_impulse_ctrl": -22.886, "Braking_impulse_smart": -12.939, "Propulsion_impulse_ctrl": 20.945, "Propulsion_impulse_smart": 22.656, "EMG_RMS_ctrl": null, "EMG_RMS_smart": null}, {"id": 17, "name": "Subject 17", "age": 24, "height": 165.2, "weight": 49.4, "Walking_speed_ctrl": 1.343, "Walking_speed_smart": 0.664, "Cadence_ctrl": 110.936, "Cadence_smart": 95.594, "Stride_length_ctrl": 1.373, "Stride_length_smart": 0.932, "Double_support_ctrl": 7.806, "Double_support_smart": 18.899, "Stride_variability_ctrl": 3.286, "Stride_variability_smart": 3.391, "Peak_hip_flexion_ctrl": 41.221, "Peak_hip_flexion_smart": 43.588, "Peak_knee_flexion_ctrl": 59.328, "Peak_knee_flexion_smart": 63.055, "Peak_ankle_df_ctrl": 14.427, "Peak_ankle_df_smart": 20.032, "Braking_impulse_ctrl": -25.019, "Braking_impulse_smart": -13.25, "Propulsion_impulse_ctrl": 22.19, "Propulsion_impulse_smart": 11.943, "EMG_RMS_ctrl": null, "EMG_RMS_smart": null}, {"id": 18, "name": "Subject 18", "age": 20, "height": 169.7, "weight": 55.9, "Walking_speed_ctrl": 1.185, "Walking_speed_smart": 1.149, "Cadence_ctrl": 101.71, "Cadence_smart": 87.364, "Stride_length_ctrl": 1.177, "Stride_length_smart": 1.131, "Double_support_ctrl": 12.457, "Double_support_smart": 19.632, "Stride_variability_ctrl": 2.493, "Stride_variability_smart": 7.629, "Peak_hip_flexion_ctrl": 32.31, "Peak_hip_flexion_smart": 45.987, "Peak_knee_flexion_ctrl": 66.703, "Peak_knee_flexion_smart": 67.398, "Peak_ankle_df_ctrl": 14.788, "Peak_ankle_df_smart": 14.872, "Braking_impulse_ctrl": -13.847, "Braking_impulse_smart": -14.296, "Propulsion_impulse_ctrl": 14.451, "Propulsion_impulse_smart": 13.909, "EMG_RMS_ctrl": null, "EMG_RMS_smart": null}, {"id": 19, "name": "Subject 19", "age": 25, "height": 162.0, "weight": 58.8, "Walking_speed_ctrl": 1.312, "Walking_speed_smart": 0.719, "Cadence_ctrl": 109.404, "Cadence_smart": 106.01, "Stride_length_ctrl": 1.217, "Stride_length_smart": 1.371, "Double_support_ctrl": 18.59, "Double_support_smart": 22.257, "Stride_variability_ctrl": 1.052, "Stride_variability_smart": 2.829, "Peak_hip_flexion_ctrl": 36.904, "Peak_hip_flexion_smart": 42.469, "Peak_knee_flexion_ctrl": 63.744, "Peak_knee_flexion_smart": 64.915, "Peak_ankle_df_ctrl": 14.213, "Peak_ankle_df_smart": 19.623, "Braking_impulse_ctrl": -19.88, "Braking_impulse_smart": -14.56, "Propulsion_impulse_ctrl": 16.526, "Propulsion_impulse_smart": 15.839, "EMG_RMS_ctrl": null, "EMG_RMS_smart": null}, {"id": 20, "name": "Subject 20", "age": 22, "height": 162.6, "weight": 58.6, "Walking_speed_ctrl": 1.295, "Walking_speed_smart": 1.104, "Cadence_ctrl": 113.183, "Cadence_smart": 98.606, "Stride_length_ctrl": 1.314, "Stride_length_smart": 1.3, "Double_support_ctrl": 9.277, "Double_support_smart": 18.726, "Stride_variability_ctrl": 3.472, "Stride_variability_smart": 2.147, "Peak_hip_flexion_ctrl": 42.963, "Peak_hip_flexion_smart": 34.358, "Peak_knee_flexion_ctrl": 67.154, "Peak_knee_flexion_smart": 59.149, "Peak_ankle_df_ctrl": 16.095, "Peak_ankle_df_smart": 16.837, "Braking_impulse_ctrl": -14.943, "Braking_impulse_smart": -16.899, "Propulsion_impulse_ctrl": 28.396, "Propulsion_impulse_smart": 20.621, "EMG_RMS_ctrl": null, "EMG_RMS_smart": null}, {"id": 21, "name": "Subject 21", "age": 20, "height": 170.4, "weight": 66.5, "Walking_speed_ctrl": 1.224, "Walking_speed_smart": 1.082, "Cadence_ctrl": 105.316, "Cadence_smart": 89.673, "Stride_length_ctrl": 1.352, "Stride_length_smart": 1.399, "Double_support_ctrl": 12.952, "Double_support_smart": 13.255, "Stride_variability_ctrl": 1.059, "Stride_variability_smart": 10.162, "Peak_hip_flexion_ctrl": 44.51, "Peak_hip_flexion_smart": 40.656, "Peak_knee_flexion_ctrl": 64.25, "Peak_knee_flexion_smart": 69.018, "Peak_ankle_df_ctrl": 16.438, "Peak_ankle_df_smart": 15.49, "Braking_impulse_ctrl": -23.101, "Braking_impulse_smart": -11.938, "Propulsion_impulse_ctrl": 24.482, "Propulsion_impulse_smart": 18.869, "EMG_RMS_ctrl": null, "EMG_RMS_smart": null}, {"id": 22, "name": "Subject 22", "age": 25, "height": 167.1, "weight": 76.5, "Walking_speed_ctrl": 1.26, "Walking_speed_smart": 0.649, "Cadence_ctrl": 108.012, "Cadence_smart": 103.415, "Stride_length_ctrl": 1.172, "Stride_length_smart": 1.113, "Double_support_ctrl": 17.851, "Double_support_smart": 20.968, "Stride_variability_ctrl": 4.052, "Stride_variability_smart": 4.772, "Peak_hip_flexion_ctrl": 28.572, "Peak_hip_flexion_smart": 37.428, "Peak_knee_flexion_ctrl": 58.854, "Peak_knee_flexion_smart": 73.086, "Peak_ankle_df_ctrl": 14.744, "Peak_ankle_df_smart": 17.648, "Braking_impulse_ctrl": -15.517, "Braking_impulse_smart": -11.395, "Propulsion_impulse_ctrl": 15.258, "Propulsion_impulse_smart": 9.614, "EMG_RMS_ctrl": null, "EMG_RMS_smart": null}, {"id": 23, "name": "Subject 23", "age": 22, "height": 161.1, "weight": 70.1, "Walking_speed_ctrl": 1.164, "Walking_speed_smart": 1.394, "Cadence_ctrl": 111.551, "Cadence_smart": 99.938, "Stride_length_ctrl": 1.377, "Stride_length_smart": 1.081, "Double_support_ctrl": 13.887, "Double_support_smart": 15.984, "Stride_variability_ctrl": 2.933, "Stride_variability_smart": 5.977, "Peak_hip_flexion_ctrl": 32.438, "Peak_hip_flexion_smart": 40.294, "Peak_knee_flexion_ctrl": 72.137, "Peak_knee_flexion_smart": 58.407, "Peak_ankle_df_ctrl": 15.51, "Peak_ankle_df_smart": 16.081, "Braking_impulse_ctrl": -17.149, "Braking_impulse_smart": -10.189, "Propulsion_impulse_ctrl": 22.175, "Propulsion_impulse_smart": 6.779, "EMG_RMS_ctrl": null, "EMG_RMS_smart": null}, {"id": 24, "name": "Subject 24", "age": 22, "height": 161.9, "weight": 63.6, "Walking_speed_ctrl": 1.197, "Walking_speed_smart": 0.936, "Cadence_ctrl": 117.342, "Cadence_smart": 105.845, "Stride_length_ctrl": 1.472, "Stride_length_smart": 1.024, "Double_support_ctrl": 16.359, "Double_support_smart": 11.454, "Stride_variability_ctrl": 2.349, "Stride_variability_smart": 1.052, "Peak_hip_flexion_ctrl": 37.712, "Peak_hip_flexion_smart": 38.47, "Peak_knee_flexion_ctrl": 71.49, "Peak_knee_flexion_smart": 60.831, "Peak_ankle_df_ctrl": 19.77, "Peak_ankle_df_smart": 19.909, "Braking_impulse_ctrl": -19.753, "Braking_impulse_smart": -13.506, "Propulsion_impulse_ctrl": 25.198, "Propulsion_impulse_smart": 14.179, "EMG_RMS_ctrl": null, "EMG_RMS_smart": null}, {"id": 25, "name": "Subject 25", "age": 19, "height": 161.9, "weight": 68.3, "Walking_speed_ctrl": 1.106, "Walking_speed_smart": 0.882, "Cadence_ctrl": 114.88, "Cadence_smart": 103.155, "Stride_length_ctrl": 1.268, "Stride_length_smart": 1.21, "Double_support_ctrl": 13.071, "Double_support_smart": 13.091, "Stride_variability_ctrl": 5.687, "Stride_variability_smart": 4.947, "Peak_hip_flexion_ctrl": 36.659, "Peak_hip_flexion_smart": 34.933, "Peak_knee_flexion_ctrl": 69.472, "Peak_knee_flexion_smart": 56.825, "Peak_ankle_df_ctrl": 16.025, "Peak_ankle_df_smart": 20.821, "Braking_impulse_ctrl": -16.636, "Braking_impulse_smart": -14.976, "Propulsion_impulse_ctrl": 13.132, "Propulsion_impulse_smart": 15.645, "EMG_RMS_ctrl": null, "EMG_RMS_smart": null}]

SUBJECTS_RAW = load_data()

STATS = {
    "Walking_speed":     {"label":"Walking Speed",       "unit":"m/s", "cat":"Spatiotemporal","ctrl":1.19,  "smart":0.994,"ctrlSD":0.115,"smartSD":0.206,"chg":-16.4,"test":"Wilcoxon", "stat":"W=323.5",    "p":"<0.001","effect":"RBC=0.991","sig":True},
    "Cadence":           {"label":"Cadence",             "unit":"spm", "cat":"Spatiotemporal","ctrl":110,   "smart":105,  "ctrlSD":7.5,  "smartSD":13.6, "chg":-4.5, "test":"Wilcoxon", "stat":"W=230.5",    "p":"0.022", "effect":"RBC=0.537","sig":True},
    "Stride_length":     {"label":"Stride Length",       "unit":"m",   "cat":"Spatiotemporal","ctrl":1.32,  "smart":1.16, "ctrlSD":0.103,"smartSD":0.157,"chg":-12.1,"test":"Paired t", "stat":"t(24)=6.99", "p":"<0.001","effect":"d=1.398",  "sig":True},
    "Double_support":    {"label":"Double Support Time", "unit":"%",   "cat":"Spatiotemporal","ctrl":12.7,  "smart":17.1, "ctrlSD":3.93, "smartSD":6.38, "chg":34.6, "test":"Wilcoxon", "stat":"W=63.0",     "p":"0.006", "effect":"RBC=0.612","sig":True},
    "Stride_variability":{"label":"Stride Variability",  "unit":"%",   "cat":"Spatiotemporal","ctrl":2.72,  "smart":4.43, "ctrlSD":1.28, "smartSD":4.12, "chg":62.9, "test":"Wilcoxon", "stat":"W=67.0",     "p":"0.018", "effect":"RBC=0.553","sig":True},
    "Peak_hip_flexion":  {"label":"Peak Hip Flexion",    "unit":"°",   "cat":"Kinematic",     "ctrl":36.0,  "smart":36.9, "ctrlSD":6.98, "smartSD":8.05, "chg":2.5,  "test":"Paired t", "stat":"t(24)=-0.67","p":"0.512", "effect":"d=-0.133", "sig":False},
    "Peak_knee_flexion": {"label":"Peak Knee Flexion",   "unit":"°",   "cat":"Kinematic",     "ctrl":64.7,  "smart":64.4, "ctrlSD":4.28, "smartSD":5.41, "chg":-0.5, "test":"Paired t", "stat":"t(24)=0.43", "p":"0.672", "effect":"d=0.086",  "sig":False},
    "Peak_ankle_df":     {"label":"Peak Ankle DF",       "unit":"°",   "cat":"Kinematic",     "ctrl":16.1,  "smart":17.4, "ctrlSD":2.43, "smartSD":1.72, "chg":8.1,  "test":"Wilcoxon", "stat":"W=58.0",     "p":"0.005", "effect":"RBC=0.643","sig":True},
    "Braking_impulse":   {"label":"Braking Impulse",     "unit":"N·s", "cat":"Kinetic",       "ctrl":-17.8, "smart":-16.0,"ctrlSD":4.2,  "smartSD":4.24, "chg":-10.1,"test":"Paired t", "stat":"t(24)=-1.99","p":"0.058", "effect":"d=-0.399", "sig":False},
    "Propulsion_impulse":{"label":"Propulsion Impulse",  "unit":"N·s", "cat":"Kinetic",       "ctrl":18.7,  "smart":15.3, "ctrlSD":4.25, "smartSD":5.07, "chg":-18.2,"test":"Paired t", "stat":"t(24)=3.73", "p":"0.001", "effect":"d=0.747",  "sig":True},
    "EMG_RMS":           {"label":"EMG RMS (Gastrocn.)", "unit":"mV",  "cat":"EMG",           "ctrl":0.370, "smart":0.413,"ctrlSD":0.256,"smartSD":0.284,"chg":11.6, "test":"Wilcoxon", "stat":"W=23.0",     "p":"0.413", "effect":"RBC=-0.303","sig":False},
}
SW = {
    "Walking_speed":     {"wc":0.895,"pc":"0.014","ws":0.984,"ps":"0.950"},
    "Cadence":           {"wc":0.848,"pc":"0.002","ws":0.948,"ps":"0.221"},
    "Stride_length":     {"wc":0.945,"pc":"0.191","ws":0.969,"ps":"0.610"},
    "Double_support":    {"wc":0.864,"pc":"0.003","ws":0.886,"ps":"0.009"},
    "Stride_variability":{"wc":0.899,"pc":"0.017","ws":0.629,"ps":"<0.001"},
    "Peak_hip_flexion":  {"wc":0.953,"pc":"0.292","ws":0.935,"ps":"0.116"},
    "Peak_knee_flexion": {"wc":0.955,"pc":"0.328","ws":0.961,"ps":"0.445"},
    "Peak_ankle_df":     {"wc":0.869,"pc":"0.004","ws":0.931,"ps":"0.090"},
    "Braking_impulse":   {"wc":0.975,"pc":"0.761","ws":0.976,"ps":"0.799"},
    "Propulsion_impulse":{"wc":0.978,"pc":"0.849","ws":0.976,"ps":"0.793"},
    "EMG_RMS":           {"wc":0.897,"pc":"0.122","ws":0.722,"ps":"<0.001"},
}
PGROUPS = {
    "st":    ["Walking_speed","Cadence","Stride_length","Double_support","Stride_variability"],
    "kin":   ["Peak_hip_flexion","Peak_knee_flexion","Peak_ankle_df"],
    "kinet": ["Braking_impulse","Propulsion_impulse"],
    "emg":   ["EMG_RMS"],
}
INFERENCES = [
    ("Speed & Stride: Headline Result","Spatiotemporal","blue",
     "Walking speed dropped 16.4% (p<0.001, RBC=0.991 — near-perfect effect). Stride length reduced 12.1% with Cohen's d=1.398 — a 'huge' effect by any standard. These are the strongest findings in the dataset."),
    ("Selective Ankle DF Paradox (Novel)","Kinematic","purple",
     "Despite walking 16% slower (where DF normally decreases), ankle dorsiflexion increased 8.1% (p=0.005, RBC=0.643). Hip and knee were unchanged. Selective distal CNS compensation — biomechanically novel finding."),
    ("Conservative Stability Strategy","Spatiotemporal","amber",
     "Double support ↑34.6% (p=0.006) and stride variability ↑62.9% (p=0.018). Participants adopted a fall-avoidance gait normally seen in elderly populations, triggered by smartphone distraction."),
    ("Propulsive Deficit — Mechanical Explanation","Kinetic","green",
     "Propulsion impulse fell 18.2% (p=0.001, d=0.747). Force plate data reveals the mechanism: attenuated push-off during late stance explains the speed reduction."),
    ("Net Impulse Sign Reversal (Novel)","Kinetic","red",
     "Control net impulse: +0.9 N·s (net-propulsive). Smartphone: −0.7 N·s (net-decelerative). P:B ratio drops 1.051 → 0.956, crossing below 1.0. Impossible to detect without force plates."),
    ("Inter-individual Variability Doubles","Spatiotemporal","blue",
     "Walking speed CV: 9.7% → 20.7% (+114%). Stride variability CV: 47% → 93%. Suggests high-responder / low-responder subgroups based on attentional capacity."),
    ("EMG–Propulsion Dissociation","EMG","purple",
     "EMG RMS ↑11.6% yet propulsion ↓18.2%. More muscle activation producing less force = neuromuscular inefficiency. Non-significant (p=0.413) due to n=13 — underpowered."),
    ("Step Efficiency Decline −7.9%","Spatiotemporal","amber",
     "Stride length/cadence ratio: 0.01200 → 0.01105. Not just fewer steps — each step is less mechanically productive. Genuine locomotor inefficiency, not just voluntary speed reduction."),
    ("Extreme Stride Variability Skewness","Spatiotemporal","red",
     "Shapiro-Wilk W=0.629 (p<0.001 — most non-normal variable). Mean-median gap jumped 13×. A subgroup experienced episodic extreme disruptions — possibly near-stumbles or complete attentional capture."),
]

BLUE="#58a6ff"; PURPLE="#bc8cff"; GREEN="#3fb950"; RED="#f85149"
AMBER="#e3b341"; MUTED="#7d8590"; BG2="#161b22"; BG3="#21262d"; BORDER="#30363d"
PLOT_LAYOUT = dict(
    paper_bgcolor=BG2, plot_bgcolor=BG2,
    font=dict(color="#e6edf3", size=11),
    xaxis=dict(gridcolor=BORDER, zerolinecolor=BORDER),
    yaxis=dict(gridcolor=BORDER, zerolinecolor=BORDER),
    legend=dict(bgcolor=BG3, bordercolor=BORDER, borderwidth=1),
    margin=dict(l=40, r=20, t=40, b=40),
)

def pct_change(a, b):
    if not a: return 0.0
    return round((b - a) / abs(a) * 100, 1)

def emg_subs():
    return [s for s in SUBJECTS_RAW if s.get("EMG_RMS_ctrl") is not None]

# Use "Subject N" as the display label everywhere — name field already contains this
def slabel(s):
    return s["name"]   # already "Subject 1", "Subject 2", etc.

# Short label for chart axes: "S1", "S2", ...
def sshort(s):
    return f"S{s['id']}"

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🦿 GaitLab")
    st.markdown("<small style='color:#7d8590'>Arvind, Dr. Varshini Karthik — SRMIST, KTR · CAMERA LAB</small>", unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("Navigate", [
        "Overview", "Subjects", "Spatiotemporal", "Kinematic",
        "Kinetic", "EMG", "Statistics", "Charts", "Raw Data", "Key Inferences"
    ], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("""
    <div style='font-size:11px;color:#7d8590;line-height:1.8'>
    <b style='color:#58a6ff'>N = 25</b> healthy young adults<br>
    Age: 18–25 years · All Male<br>
    Single-task vs Dual-task<br>
    Qualisys + Bertec + Delsys<br>
    Jamovi · α = 0.05<br>
    <i>Participants anonymised (S1–S25)</i>
    </div>
    """, unsafe_allow_html=True)

pg = page

# ═════════════════════════════════════════════════════════════════════════════
# OVERVIEW
# ═════════════════════════════════════════════════════════════════════════════
if pg == "Overview":
    st.markdown('<div class="section-header">Overview — Multimodal Gait & EMG Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="study-tag">Single-task vs Dual-task (Smartphone) · N=25 · Healthy young adults · Age 18–25 · SRMIST, KTR · CAMERA LAB</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Walking Speed", "1.19 m/s", "↓ 16.4%  p<0.001", delta_color="inverse")
    c2.metric("Stride Length", "1.32 m",   "↓ 12.1%  d=1.398 Huge", delta_color="inverse")
    c3.metric("Double Support", "12.7 %",  "↑ 34.6%  p=0.006")
    c4.metric("Propulsion Impulse", "18.7 N·s", "↓ 18.2%  p=0.001", delta_color="inverse")

    col_l, col_r = st.columns([1, 1.1])
    with col_l:
        st.markdown("#### Significant Findings Summary (p < 0.05)")
        sig_df = pd.DataFrame([
            {"Parameter":"Walking Speed (m/s)","Control":"1.19","Smartphone":"0.994","Effect":"RBC=0.991","p-value":"<0.001","★":"★"},
            {"Parameter":"Stride Length (m)",  "Control":"1.32","Smartphone":"1.16", "Effect":"d=1.398",  "p-value":"<0.001","★":"★"},
            {"Parameter":"Double Support (%)","Control":"12.7","Smartphone":"17.1",  "Effect":"RBC=0.612","p-value":"0.006", "★":"★"},
            {"Parameter":"Stride Variability (%)","Control":"2.72","Smartphone":"4.43","Effect":"RBC=0.553","p-value":"0.018","★":"★"},
            {"Parameter":"Cadence (steps/min)","Control":"110","Smartphone":"105",   "Effect":"RBC=0.537","p-value":"0.022", "★":"★"},
            {"Parameter":"Peak Ankle DF (°)",  "Control":"16.1","Smartphone":"17.4", "Effect":"RBC=0.643","p-value":"0.005", "★":"★"},
            {"Parameter":"Propulsion Imp (N·s)","Control":"18.7","Smartphone":"15.3","Effect":"d=0.747",  "p-value":"0.001", "★":"★"},
        ])
        st.dataframe(sig_df, use_container_width=True, hide_index=True)

    with col_r:
        st.markdown("#### % Change — All Parameters")
        pks = list(STATS.keys())
        chgs = [STATS[k]["chg"] for k in pks]
        lbls = [STATS[k]["label"] for k in pks]
        colors = [GREEN if c > 0 else RED for c in chgs]
        fig = go.Figure(go.Bar(x=lbls, y=chgs, marker_color=colors, opacity=0.85,
                               text=[f"{c:+.1f}%" for c in chgs], textposition="outside"))
        fig.add_hline(y=0, line_color=BORDER)
        fig.update_layout(**PLOT_LAYOUT, height=300, yaxis_title="% Change", xaxis_tickangle=-35)
        st.plotly_chart(fig, use_container_width=True)

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown("#### Significance Summary")
        fig2 = go.Figure(go.Pie(
            labels=["Significant (p<0.05)","Trend (p<0.1)","Non-significant"],
            values=[7, 2, 2], marker_colors=[GREEN, AMBER, MUTED],
            hole=0.4, textinfo="label+percent", textfont_size=10,
        ))
        fig2.update_layout(**{k:v for k,v in PLOT_LAYOUT.items() if k not in ("xaxis","yaxis")},
                           height=260, showlegend=False,
                           annotations=[dict(text="11 params",x=0.5,y=0.5,
                                             font_size=10,font_color=MUTED,showarrow=False)])
        st.plotly_chart(fig2, use_container_width=True)

    with col_b:
        st.markdown("#### Effect Size Magnitudes")
        evals = [abs(float(_re.findall(r"[\d.]+", STATS[k]["effect"])[0])) if _re.findall(r"[\d.]+", STATS[k]["effect"]) else 0 for k in pks]
        fig3 = go.Figure(go.Bar(y=lbls, x=evals, orientation="h",
                                marker_color=PURPLE, opacity=0.82,
                                text=[f"{v:.3f}" for v in evals], textposition="outside"))
        fig3.update_layout(**PLOT_LAYOUT, height=260, xaxis_title="Effect size")
        st.plotly_chart(fig3, use_container_width=True)

    with col_c:
        st.markdown("#### Study Equipment")
        for lbl, detail in [
            ("Motion Capture","Qualisys ARQUS — 8 IR + 2 video cameras"),
            ("Marker Model",  "IOR Lower Body — 26 static / 20 dynamic"),
            ("Force Plates",  "2× Bertec — GRF, Braking, Propulsion"),
            ("EMG",           "Delsys Trigno — Gastrocn. Med & Lat (L & R)"),
            ("Statistics",    "Paired t-test & Wilcoxon · Jamovi · α=0.05"),
            ("Participants",  "N=25 healthy young adults · 18–25 yrs (anonymised)"),
            ("Conditions",    "Normal walk vs Walk + Smartphone"),
        ]:
            st.markdown(f"**{lbl}** — <small style='color:#7d8590'>{detail}</small>", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# SUBJECTS
# ═════════════════════════════════════════════════════════════════════════════
elif pg == "Subjects":
    st.markdown('<div class="section-header">Subjects (N=25) — Anonymised</div>', unsafe_allow_html=True)
    st.caption("All participants are coded as Subject 1–25. No personal identifiers are displayed.")

    emg_ids = set(s["id"] for s in SUBJECTS_RAW if s.get("EMG_RMS_ctrl") is not None)
    rows = []
    for s in SUBJECTS_RAW:
        cs = s.get("Walking_speed_ctrl"); ss = s.get("Walking_speed_smart")
        rows.append({
            "Subject ID": s["name"],
            "Age (yrs)": s["age"],
            "Height (cm)": s["height"],
            "Weight (kg)": s["weight"],
            "EMG Data": "✓" if s["id"] in emg_ids else "—",
            "Speed Ctrl (m/s)": round(cs,3) if cs else "—",
            "Speed Smart (m/s)": round(ss,3) if ss else "—",
            "Δ Speed %": f"{pct_change(cs,ss):+.1f}%" if cs and ss else "—",
        })
    subj_df = pd.DataFrame(rows)

    search = st.text_input("🔍 Filter by Subject ID (e.g. type '5' for Subject 5)", placeholder="Enter number...")
    if search:
        subj_df = subj_df[subj_df["Subject ID"].str.contains(search, case=False)]
    st.dataframe(subj_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("#### Individual Subject Detail")
    subj_options = [s["name"] for s in SUBJECTS_RAW]
    sel = st.selectbox("Select subject", subj_options)
    s = next(x for x in SUBJECTS_RAW if x["name"] == sel)

    col_bio, col_params = st.columns([1, 2])
    with col_bio:
        st.markdown(f"**{s['name']}**")
        has_emg = s["id"] in emg_ids
        st.markdown(f"""
| Field | Value |
|-------|-------|
| Subject ID | {s['name']} |
| Age | {s['age']} yrs |
| Height | {s['height']} cm |
| Weight | {s['weight']} kg |
| EMG data | {"✓ Available (S1–S13)" if has_emg else "— Not collected"} |
""")

    with col_params:
        param_rows = []
        for pk, meta in STATS.items():
            cv = s.get(pk+"_ctrl"); sv = s.get(pk+"_smart")
            if cv is None: continue
            chg = pct_change(cv, sv)
            param_rows.append({
                "Parameter": meta["label"], "Unit": meta["unit"],
                "Control": round(cv,3), "Smartphone": round(sv,3),
                "Change %": f"{chg:+.1f}%",
                "Group Mean (Ctrl)": STATS[pk]["ctrl"],
            })
        st.dataframe(pd.DataFrame(param_rows), use_container_width=True, hide_index=True)

    st.markdown("#### Individual Parameter Chart")
    pk_sel = st.selectbox("Parameter", list(STATS.keys()), format_func=lambda k: STATS[k]["label"])
    cv = s.get(pk_sel+"_ctrl"); sv = s.get(pk_sel+"_smart")
    if cv is not None:
        fig_ind = go.Figure()
        fig_ind.add_trace(go.Bar(x=["Control","Smartphone"], y=[cv, sv],
                                  marker_color=[BLUE, RED], opacity=0.85,
                                  text=[f"{cv:.3f}", f"{sv:.3f}"], textposition="outside"))
        fig_ind.add_hline(y=STATS[pk_sel]["ctrl"], line_dash="dot", line_color=MUTED,
                           annotation_text=f"Group mean (ctrl): {STATS[pk_sel]['ctrl']}")
        fig_ind.update_layout(**PLOT_LAYOUT, height=280,
                               yaxis_title=STATS[pk_sel]["unit"],
                               title=f"{s['name']} — {STATS[pk_sel]['label']}")
        st.plotly_chart(fig_ind, use_container_width=True)

# ═════════════════════════════════════════════════════════════════════════════
# SPATIOTEMPORAL
# ═════════════════════════════════════════════════════════════════════════════
elif pg == "Spatiotemporal":
    st.markdown('<div class="section-header">Spatiotemporal Parameters</div>', unsafe_allow_html=True)
    pks = PGROUPS["st"]
    cols = st.columns(5)
    for i, pk in enumerate(pks):
        s = STATS[pk]; sym = "↓" if s["chg"] < 0 else "↑"
        cols[i].metric(s["label"], f"{s['ctrl']} {s['unit']}",
                       f"{sym} {abs(s['chg'])}%  p={s['p']}",
                       delta_color="inverse" if s["chg"] < 0 else "normal")

    tab1, tab2, tab3 = st.tabs(["📊 Group Comparison", "👤 Individual Scatter", "🗃️ Data Table"])

    with tab1:
        fig = go.Figure()
        lbls = [STATS[k]["label"] for k in pks]
        fig.add_trace(go.Bar(name="Control",    x=lbls, y=[STATS[k]["ctrl"] for k in pks],
                             marker_color=BLUE, opacity=0.85, width=0.35, offset=-0.18,
                             text=[STATS[k]["ctrl"] for k in pks], textposition="outside"))
        fig.add_trace(go.Bar(name="Smartphone", x=lbls, y=[STATS[k]["smart"] for k in pks],
                             marker_color=RED,  opacity=0.80, width=0.35, offset=0.18,
                             text=[STATS[k]["smart"] for k in pks], textposition="outside"))
        fig.update_layout(**PLOT_LAYOUT, height=380, barmode="overlay",
                          title="Group Means — Control vs Smartphone")
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        pk_sel = st.selectbox("Select parameter", pks, format_func=lambda k: STATS[k]["label"])
        valid = [s for s in SUBJECTS_RAW if s.get(pk_sel+"_ctrl") is not None]
        xlbls = [sshort(s) for s in valid]
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=xlbls, y=[s[pk_sel+"_ctrl"] for s in valid],
                                   mode="markers", name="Control",
                                   marker=dict(color=BLUE, size=9, symbol="circle"),
                                   hovertemplate="%{x}<br>Control: %{y}<extra></extra>"))
        fig2.add_trace(go.Scatter(x=xlbls, y=[s[pk_sel+"_smart"] for s in valid],
                                   mode="markers", name="Smartphone",
                                   marker=dict(color=RED, size=9, symbol="triangle-up"),
                                   hovertemplate="%{x}<br>Smartphone: %{y}<extra></extra>"))
        fig2.add_hline(y=STATS[pk_sel]["ctrl"],  line_dash="dot", line_color=BLUE,  line_width=1)
        fig2.add_hline(y=STATS[pk_sel]["smart"], line_dash="dot", line_color=RED,   line_width=1)
        fig2.update_layout(**PLOT_LAYOUT, height=380,
                            yaxis_title=STATS[pk_sel]["unit"],
                            xaxis_title="Subject",
                            title=f"{STATS[pk_sel]['label']} — Individual Values (S1–S25)")
        st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        rows = []
        for s in SUBJECTS_RAW:
            row = {"Subject": s["name"]}
            for pk in pks:
                cv = s.get(pk+"_ctrl"); sv = s.get(pk+"_smart")
                row[STATS[pk]["label"]+" Ctrl"] = round(cv,3) if cv is not None else "—"
                row[STATS[pk]["label"]+" Smart"] = round(sv,3) if sv is not None else "—"
                row[STATS[pk]["label"]+" Δ%"] = f"{pct_change(cv,sv):+.1f}%" if cv and sv else "—"
            rows.append(row)
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

# ═════════════════════════════════════════════════════════════════════════════
# KINEMATIC
# ═════════════════════════════════════════════════════════════════════════════
elif pg == "Kinematic":
    st.markdown('<div class="section-header">Kinematic Parameters — Joint Angles</div>', unsafe_allow_html=True)
    pks = PGROUPS["kin"]
    cols = st.columns(3)
    for i, pk in enumerate(pks):
        s = STATS[pk]
        cols[i].metric(s["label"], f"{s['ctrl']} {s['unit']}",
                       f"{'★ ' if s['sig'] else ''}p={s['p']}  {s['effect']}",
                       delta_color="normal" if s["sig"] else "off")
    st.markdown('''<div class="info-card purple"><b>Ankle Dorsiflexion Paradox:</b> Despite walking 16% slower
    (where DF normally decreases), ankle DF significantly <b>increased</b> 8.1% (p=0.005, RBC=0.643).
    Hip and knee were completely unchanged (p=0.51, p=0.67). Selective distal CNS compensation —
    the key novel kinematic finding of this study.</div>''', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📊 Group Comparison", "👤 All Subjects", "🗃️ Data Table"])
    with tab1:
        lbls = [STATS[k]["label"] for k in pks]
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Control",    x=lbls, y=[STATS[k]["ctrl"] for k in pks],
                             marker_color=PURPLE, opacity=0.85, width=0.35, offset=-0.18))
        fig.add_trace(go.Bar(name="Smartphone", x=lbls, y=[STATS[k]["smart"] for k in pks],
                             marker_color=RED,    opacity=0.80, width=0.35, offset=0.18))
        fig.update_layout(**PLOT_LAYOUT, height=380, barmode="overlay",
                          yaxis_title="Degrees (°)",
                          title="Joint Angles — ★ Only ankle DF significant (p=0.005)")
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        fig2 = make_subplots(rows=1, cols=3, subplot_titles=[STATS[k]["label"] for k in pks])
        for i, pk in enumerate(pks):
            valid = [s for s in SUBJECTS_RAW if s.get(pk+"_ctrl") is not None]
            xlbls = [sshort(s) for s in valid]
            fig2.add_trace(go.Scatter(x=xlbls, y=[s[pk+"_ctrl"] for s in valid],
                                       mode="markers", name="Control" if i==0 else "",
                                       marker=dict(color=PURPLE, size=7),
                                       hovertemplate="%{x}<br>%{y:.3f}<extra>Control</extra>",
                                       showlegend=(i==0)), row=1, col=i+1)
            fig2.add_trace(go.Scatter(x=xlbls, y=[s[pk+"_smart"] for s in valid],
                                       mode="markers", name="Smartphone" if i==0 else "",
                                       marker=dict(color=RED, size=7, symbol="triangle-up"),
                                       hovertemplate="%{x}<br>%{y:.3f}<extra>Smartphone</extra>",
                                       showlegend=(i==0)), row=1, col=i+1)
        fig2.update_layout(**PLOT_LAYOUT, height=360)
        st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        rows = []
        for s in SUBJECTS_RAW:
            row = {"Subject": s["name"]}
            for pk in pks:
                cv = s.get(pk+"_ctrl"); sv = s.get(pk+"_smart")
                row[STATS[pk]["label"]+" Ctrl"] = round(cv,3) if cv else "—"
                row[STATS[pk]["label"]+" Smart"] = round(sv,3) if sv else "—"
                row[STATS[pk]["label"]+" Δ%"] = f"{pct_change(cv,sv):+.1f}%" if cv and sv else "—"
            rows.append(row)
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

# ═════════════════════════════════════════════════════════════════════════════
# KINETIC
# ═════════════════════════════════════════════════════════════════════════════
elif pg == "Kinetic":
    st.markdown('<div class="section-header">Kinetic Parameters — Force Plate Data</div>', unsafe_allow_html=True)
    pks = PGROUPS["kinet"]
    c1, c2 = st.columns(2)
    for col, pk in zip([c1, c2], pks):
        s = STATS[pk]
        col.metric(s["label"], f"{s['ctrl']} {s['unit']}",
                   f"{'★' if s['sig'] else '~'} p={s['p']}  {s['effect']}",
                   delta_color="inverse" if s["chg"] < 0 else "normal")
    st.markdown('''<div class="info-card red"><b>Net Impulse Sign Reversal:</b> Control net impulse:
    <b>+0.9 N·s</b> (net-propulsive) → Smartphone: <b>−0.7 N·s</b> (net-decelerative).
    The Prop:Braking ratio drops from 1.051 → 0.956, crossing below 1.0.
    This mechanistically explains the speed reduction — only detectable with force plates.</div>''',
    unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📊 Mean Comparison", "📐 P:B Ratio per Subject", "🗃️ Data Table"])
    with tab1:
        lbls = [STATS[k]["label"] for k in pks]
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Control",    x=lbls, y=[STATS[k]["ctrl"] for k in pks],
                             marker_color=GREEN, opacity=0.85, width=0.35, offset=-0.18))
        fig.add_trace(go.Bar(name="Smartphone", x=lbls, y=[STATS[k]["smart"] for k in pks],
                             marker_color=RED,   opacity=0.80, width=0.35, offset=0.18))
        fig.update_layout(**PLOT_LAYOUT, height=360, barmode="overlay", yaxis_title="N·s")
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        xlbls = [sshort(s) for s in SUBJECTS_RAW]
        full_labels = [slabel(s) for s in SUBJECTS_RAW]
        pbC = [s["Propulsion_impulse_ctrl"]/abs(s["Braking_impulse_ctrl"]) for s in SUBJECTS_RAW]
        pbS = [s["Propulsion_impulse_smart"]/abs(s["Braking_impulse_smart"]) for s in SUBJECTS_RAW]
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(name="Control",    x=xlbls, y=pbC,
                              marker_color=GREEN, opacity=0.82, width=0.35, offset=-0.18,
                              hovertemplate="%{x}<br>Control P:B: %{y:.3f}<extra></extra>"))
        fig2.add_trace(go.Bar(name="Smartphone", x=xlbls, y=pbS,
                              marker_color=RED,   opacity=0.78, width=0.35, offset=0.18,
                              hovertemplate="%{x}<br>Smartphone P:B: %{y:.3f}<extra></extra>"))
        fig2.add_hline(y=1.0, line_dash="dash", line_color=AMBER, line_width=1.5,
                       annotation_text="Ratio = 1.0 (balance point)", annotation_font_color=AMBER)
        fig2.update_layout(**PLOT_LAYOUT, height=380, barmode="overlay",
                           xaxis_title="Subject", yaxis_title="Propulsion:Braking Ratio",
                           title="P:B Ratio per Subject — values <1.0 = net-decelerative gait")
        st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        rows = []
        for s in SUBJECTS_RAW:
            row = {"Subject": s["name"]}
            for pk in pks:
                cv = s.get(pk+"_ctrl"); sv = s.get(pk+"_smart")
                row[STATS[pk]["label"]+" Ctrl"] = round(cv,3) if cv else "—"
                row[STATS[pk]["label"]+" Smart"] = round(sv,3) if sv else "—"
                row[STATS[pk]["label"]+" Δ%"] = f"{pct_change(cv,sv):+.1f}%" if cv is not None and sv is not None else "—"
            pb_c = round(s["Propulsion_impulse_ctrl"]/abs(s["Braking_impulse_ctrl"]),3)
            pb_s = round(s["Propulsion_impulse_smart"]/abs(s["Braking_impulse_smart"]),3)
            row["P:B Ratio Ctrl"] = pb_c; row["P:B Ratio Smart"] = pb_s
            rows.append(row)
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

# ═════════════════════════════════════════════════════════════════════════════
# EMG
# ═════════════════════════════════════════════════════════════════════════════
elif pg == "EMG":
    st.markdown('<div class="section-header">EMG — Gastrocnemius Muscle Activity</div>', unsafe_allow_html=True)
    st.markdown('<div class="study-tag">n=13 subjects (S1–S13) · Delsys Trigno · Gastrocnemius Medial & Lateral (Left & Right)</div>', unsafe_allow_html=True)
    es = emg_subs()
    cm = sum(s["EMG_RMS_ctrl"] for s in es)/len(es)
    sm = sum(s["EMG_RMS_smart"] for s in es)/len(es)
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("EMG Subjects","13 (S1–S13)","of 25 total · 52%")
    c2.metric("Control RMS Mean",f"{cm:.3f} mV","SD = 0.256 mV")
    c3.metric("Smartphone RMS Mean",f"{sm:.3f} mV","p=0.413 (NS, n=13)",delta_color="off")
    c4.metric("EMG vs Propulsion","↑+11.6% vs ↓−18.2%","Neuromuscular inefficiency",delta_color="off")
    st.markdown('''<div class="info-card amber"><b>Underpowered result:</b> With n=13, statistical power
    is only ~38% for a medium effect size (d=0.5). The directional EMG increase alongside propulsion deficit
    suggests neuromuscular inefficiency — more activation producing less mechanical output under cognitive load.
    A larger study (n≥34) is needed to confirm this finding.</div>''', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📊 RMS Per Subject", "🔵 Control vs Smartphone", "🗃️ Data Table"])
    with tab1:
        xlbls = [sshort(s) for s in es]
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Control",    x=xlbls, y=[s["EMG_RMS_ctrl"] for s in es],
                             marker_color=BLUE, opacity=0.85, width=0.35, offset=-0.18,
                             hovertemplate="%{x}<br>Control: %{y:.3f} mV<extra></extra>"))
        fig.add_trace(go.Bar(name="Smartphone", x=xlbls, y=[s["EMG_RMS_smart"] for s in es],
                             marker_color=PURPLE, opacity=0.80, width=0.35, offset=0.18,
                             hovertemplate="%{x}<br>Smartphone: %{y:.3f} mV<extra></extra>"))
        fig.update_layout(**PLOT_LAYOUT, height=360, barmode="overlay",
                          xaxis_title="Subject", yaxis_title="RMS (mV)")
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        cx = [s["EMG_RMS_ctrl"] for s in es]
        cy = [s["EMG_RMS_smart"] for s in es]
        hover_labels = [sshort(s) for s in es]
        mn = min(cx+cy)-0.05; mx = max(cx+cy)+0.05
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=[mn,mx], y=[mn,mx], mode="lines",
                                   line=dict(color=BORDER, dash="dash"), name="y=x (no change)"))
        fig2.add_trace(go.Scatter(
            x=cx, y=cy, mode="markers+text",
            text=hover_labels, textposition="top right",
            textfont_size=9, textfont_color=MUTED,
            marker=dict(color=PURPLE, size=10, opacity=0.85),
            hovertemplate="%{text}<br>Control: %{x:.3f}<br>Smartphone: %{y:.3f}<extra></extra>",
            name="Subjects (S1–S13)"
        ))
        fig2.update_layout(**PLOT_LAYOUT, height=400,
                           xaxis_title="Control RMS (mV)", yaxis_title="Smartphone RMS (mV)",
                           title="EMG Scatter — points above y=x = increased activation under smartphone")
        st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        emg_rows = [{"Subject": s["name"],
                     "EMG Ctrl (mV)": round(s["EMG_RMS_ctrl"],3),
                     "EMG Smart (mV)": round(s["EMG_RMS_smart"],3),
                     "Δ%": f"{pct_change(s['EMG_RMS_ctrl'],s['EMG_RMS_smart']):+.1f}%"} for s in es]
        st.dataframe(pd.DataFrame(emg_rows), use_container_width=True, hide_index=True)

# ═════════════════════════════════════════════════════════════════════════════
# STATISTICS
# ═════════════════════════════════════════════════════════════════════════════
elif pg == "Statistics":
    st.markdown('<div class="section-header">Statistical Analysis Results</div>', unsafe_allow_html=True)
    st.markdown('<div class="study-tag">Normality: Shapiro-Wilk · Parametric: Paired t-test · Non-parametric: Wilcoxon signed-rank · α = 0.05</div>', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["📋 Full Results", "🔬 Shapiro-Wilk", "📊 CV% Variability"])
    with tab1:
        rows = []
        for pk, s in STATS.items():
            sig = "★ Sig" if s["sig"] else ("~ Trend" if s["p"]=="0.058" else "NS")
            rows.append({"Parameter":s["label"],"Category":s["cat"],
                         "Control M (SD)":f"{s['ctrl']} ({s['ctrlSD']})",
                         "Smartphone M (SD)":f"{s['smart']} ({s['smartSD']})",
                         "Change %":f"{s['chg']:+.1f}%","Test":s["test"],
                         "Statistic":s["stat"],
                         "p-value":f"{s['p']}{' *' if s['sig'] else ''}",
                         "Effect size":s["effect"],"Significance":sig})
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        st.markdown("**Significant results (p < 0.05):**")
        c1,c2 = st.columns(2)
        for i,pk in enumerate([k for k,s in STATS.items() if s["sig"]]):
            s = STATS[pk]
            (c1 if i%2==0 else c2).success(f"**{s['label']}** — {s['effect']} · p={s['p']}")
    with tab2:
        sw_rows = []
        for pk, w in SW.items():
            non_norm = str(w["pc"]).startswith("<") or (str(w["pc"]).replace(".","").isdigit() and float(w["pc"])<0.05)
            sw_rows.append({"Parameter":STATS[pk]["label"],
                            "W (ctrl)":w["wc"],"p (ctrl)":w["pc"],
                            "W (smart)":w["ws"],"p (smart)":w["ps"],
                            "Normality (ctrl)":"❌ Non-normal" if non_norm else "✓ Normal",
                            "Test used":STATS[pk]["test"]})
        st.dataframe(pd.DataFrame(sw_rows), use_container_width=True, hide_index=True)
        st.caption("Non-normal distributions (p < 0.05) → Wilcoxon signed-rank test used")
    with tab3:
        pks2 = list(STATS.keys())
        cvC = [9.7,6.8,7.8,30.9,47.1,19.4,6.6,15.1,23.6,22.7,69.2]
        cvS = [20.7,13.0,13.5,37.3,93.0,21.8,8.4,9.9,26.5,33.1,68.8]
        lbls2 = [STATS[k]["label"] for k in pks2]
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Control CV%",    x=lbls2, y=cvC,
                             marker_color=BLUE, opacity=0.85, width=0.35, offset=-0.18))
        fig.add_trace(go.Bar(name="Smartphone CV%", x=lbls2, y=cvS,
                             marker_color=RED,  opacity=0.80, width=0.35, offset=0.18))
        fig.update_layout(**PLOT_LAYOUT, height=380, barmode="overlay",
                          yaxis_title="CV%", xaxis_tickangle=-35,
                          title="CV% doubles under smartphone — especially stride variability (47→93%)")
        st.plotly_chart(fig, use_container_width=True)

# ═════════════════════════════════════════════════════════════════════════════
# CHARTS
# ═════════════════════════════════════════════════════════════════════════════
elif pg == "Charts":
    st.markdown('<div class="section-header">Charts & Visualisations</div>', unsafe_allow_html=True)
    xlbls = [sshort(s) for s in SUBJECTS_RAW]
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Speed & Stride", "⚖️ Impulse & Radar", "🦵 Joint Angles", "📊 All Parameters"])

    with tab1:
        c1, c2 = st.columns(2)
        for col, title, ck, sk, ylab in [
            (c1,"Walking Speed — S1 to S25","Walking_speed_ctrl","Walking_speed_smart","m/s"),
            (c2,"Stride Length — S1 to S25","Stride_length_ctrl","Stride_length_smart","m"),
        ]:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=xlbls, y=[s[ck] for s in SUBJECTS_RAW], mode="lines+markers",
                                     name="Control", line=dict(color=BLUE,width=2), marker=dict(size=5),
                                     hovertemplate="%{x}<br>Control: %{y:.3f}<extra></extra>"))
            fig.add_trace(go.Scatter(x=xlbls, y=[s[sk] for s in SUBJECTS_RAW], mode="lines+markers",
                                     name="Smartphone", line=dict(color=RED,width=2),
                                     marker=dict(size=5, symbol="triangle-up"),
                                     hovertemplate="%{x}<br>Smartphone: %{y:.3f}<extra></extra>"))
            fig.update_layout(**PLOT_LAYOUT, height=300, yaxis_title=ylab,
                              xaxis_title="Subject", title=title, xaxis_tickangle=-40)
            col.plotly_chart(fig, use_container_width=True)

        c3, c4 = st.columns(2)
        for col, title, ck, sk, ylab in [
            (c3,"Double Support — S1 to S25","Double_support_ctrl","Double_support_smart","%"),
            (c4,"Stride Variability — S1 to S25","Stride_variability_ctrl","Stride_variability_smart","%"),
        ]:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=xlbls, y=[s[ck] for s in SUBJECTS_RAW], mode="lines+markers",
                                     name="Control", line=dict(color=GREEN,width=2), marker=dict(size=5),
                                     hovertemplate="%{x}<br>Control: %{y:.3f}<extra></extra>"))
            fig.add_trace(go.Scatter(x=xlbls, y=[s[sk] for s in SUBJECTS_RAW], mode="lines+markers",
                                     name="Smartphone", line=dict(color=AMBER,width=2),
                                     marker=dict(size=5, symbol="triangle-up"),
                                     hovertemplate="%{x}<br>Smartphone: %{y:.3f}<extra></extra>"))
            fig.update_layout(**PLOT_LAYOUT, height=300, yaxis_title=ylab,
                              xaxis_title="Subject", title=title, xaxis_tickangle=-40)
            col.plotly_chart(fig, use_container_width=True)

    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=[s["Braking_impulse_ctrl"] for s in SUBJECTS_RAW],
                y=[s["Propulsion_impulse_ctrl"] for s in SUBJECTS_RAW],
                mode="markers+text", text=xlbls, textposition="top right",
                textfont_size=8, textfont_color=MUTED,
                marker=dict(color=GREEN, size=9), name="Control",
                hovertemplate="%{text}<br>Braking: %{x:.2f}<br>Propulsion: %{y:.2f}<extra>Control</extra>"))
            fig.add_trace(go.Scatter(
                x=[s["Braking_impulse_smart"] for s in SUBJECTS_RAW],
                y=[s["Propulsion_impulse_smart"] for s in SUBJECTS_RAW],
                mode="markers", marker=dict(color=RED, size=9, symbol="triangle-up"), name="Smartphone",
                hovertemplate="Braking: %{x:.2f}<br>Propulsion: %{y:.2f}<extra>Smartphone</extra>"))
            fig.update_layout(**PLOT_LAYOUT, height=400,
                              xaxis_title="Braking Impulse (N·s)", yaxis_title="Propulsion Impulse (N·s)",
                              title="Propulsion vs Braking — all subjects")
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            cats = ["Walk Speed","Stride Length","Cadence","Ankle DF","Propulsion"]
            ctrl_v = [100,100,100,100,100]; smart_v = [83.5,87.9,95.5,108.1,81.8]
            fig2 = go.Figure()
            fig2.add_trace(go.Scatterpolar(r=ctrl_v+[ctrl_v[0]], theta=cats+[cats[0]],
                                            fill="toself", name="Control",
                                            line_color=BLUE, fillcolor="rgba(88,166,255,0.1)"))
            fig2.add_trace(go.Scatterpolar(r=smart_v+[smart_v[0]], theta=cats+[cats[0]],
                                            fill="toself", name="Smartphone",
                                            line_color=RED, fillcolor="rgba(248,81,73,0.08)"))
            fig2.update_layout(
                polar=dict(bgcolor=BG2,
                           radialaxis=dict(range=[70,115], gridcolor=BORDER, color=MUTED),
                           angularaxis=dict(gridcolor=BORDER, color=MUTED)),
                paper_bgcolor=BG2, font_color="#e6edf3",
                legend=dict(bgcolor=BG3, bordercolor=BORDER),
                height=400, title="Normalised Radar — Control=100%",
                margin=dict(l=40,r=40,t=50,b=40))
            st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        for pk in PGROUPS["kin"]:
            valid = [s for s in SUBJECTS_RAW if s.get(pk+"_ctrl") is not None]
            vxlbls = [sshort(s) for s in valid]
            fig = go.Figure()
            fig.add_trace(go.Bar(name="Control",    x=vxlbls, y=[s[pk+"_ctrl"] for s in valid],
                                  marker_color=PURPLE, opacity=0.85, width=0.35, offset=-0.18,
                                  hovertemplate="%{x}<br>Control: %{y:.2f}°<extra></extra>"))
            fig.add_trace(go.Bar(name="Smartphone", x=vxlbls, y=[s[pk+"_smart"] for s in valid],
                                  marker_color=RED,    opacity=0.80, width=0.35, offset=0.18,
                                  hovertemplate="%{x}<br>Smartphone: %{y:.2f}°<extra></extra>"))
            fig.update_layout(**PLOT_LAYOUT, height=300, barmode="overlay",
                              xaxis_title="Subject", yaxis_title="°", title=STATS[pk]["label"])
            st.plotly_chart(fig, use_container_width=True)

    with tab4:
        pk_choice = st.selectbox("Select parameter", list(STATS.keys()),
                                  format_func=lambda k: STATS[k]["label"])
        valid = [s for s in SUBJECTS_RAW if s.get(pk_choice+"_ctrl") is not None]
        vxlbls = [sshort(s) for s in valid]
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Control",    x=vxlbls, y=[s[pk_choice+"_ctrl"] for s in valid],
                              marker_color=BLUE, opacity=0.85, width=0.35, offset=-0.18,
                              hovertemplate="%{x}<br>Control: %{y:.3f}<extra></extra>"))
        fig.add_trace(go.Bar(name="Smartphone", x=vxlbls, y=[s[pk_choice+"_smart"] for s in valid],
                              marker_color=RED,  opacity=0.80, width=0.35, offset=0.18,
                              hovertemplate="%{x}<br>Smartphone: %{y:.3f}<extra></extra>"))
        fig.add_hline(y=STATS[pk_choice]["ctrl"],  line_dash="dot", line_color=BLUE, line_width=1.5,
                      annotation_text=f"Group ctrl mean: {STATS[pk_choice]['ctrl']}")
        fig.add_hline(y=STATS[pk_choice]["smart"], line_dash="dot", line_color=RED,  line_width=1.5,
                      annotation_text=f"Group smart mean: {STATS[pk_choice]['smart']}")
        fig.update_layout(**PLOT_LAYOUT, height=420, barmode="overlay",
                          xaxis_title="Subject", yaxis_title=STATS[pk_choice]["unit"],
                          title=f"{STATS[pk_choice]['label']} — All Subjects (S1–S25)")
        st.plotly_chart(fig, use_container_width=True)

# ═════════════════════════════════════════════════════════════════════════════
# RAW DATA
# ═════════════════════════════════════════════════════════════════════════════
elif pg == "Raw Data":
    st.markdown('<div class="section-header">Raw Data Table — All Parameters</div>', unsafe_allow_html=True)
    st.caption("All participants anonymised as Subject 1–25. No personal identifiers included.")
    col_f1, col_f2 = st.columns([2,1])
    filt = col_f1.selectbox("Filter by parameter group",
                             ["All","Spatiotemporal","Kinematic","Kinetic","EMG"])
    search = col_f2.text_input("Filter by subject", placeholder="e.g. 'Subject 5'")
    group_map = {"All":list(STATS.keys()),"Spatiotemporal":PGROUPS["st"],
                 "Kinematic":PGROUPS["kin"],"Kinetic":PGROUPS["kinet"],"EMG":PGROUPS["emg"]}
    pks = group_map[filt]
    emg_ids = set(s["id"] for s in SUBJECTS_RAW if s.get("EMG_RMS_ctrl") is not None)
    rows = []
    for s in SUBJECTS_RAW:
        if search and search.lower() not in s["name"].lower(): continue
        row = {"Subject": s["name"], "Age": s["age"], "Height (cm)": s["height"], "Weight (kg)": s["weight"]}
        for pk in pks:
            if pk == "EMG_RMS" and s["id"] not in emg_ids:
                row[STATS[pk]["label"]+" C"] = "—"
                row[STATS[pk]["label"]+" S"] = "—"
                row[STATS[pk]["label"]+" Δ%"] = "—"
                continue
            cv = s.get(pk+"_ctrl"); sv = s.get(pk+"_smart")
            row[STATS[pk]["label"]+" C"]  = round(cv,3) if cv is not None else "—"
            row[STATS[pk]["label"]+" S"]  = round(sv,3) if sv is not None else "—"
            row[STATS[pk]["label"]+" Δ%"] = f"{pct_change(cv,sv):+.1f}%" if cv is not None and sv is not None else "—"
        rows.append(row)
    df_raw = pd.DataFrame(rows)
    st.dataframe(df_raw, use_container_width=True, hide_index=True)
    st.markdown("---")
    col_dl1, col_dl2 = st.columns(2)
    buf = io.StringIO(); df_raw.to_csv(buf, index=False)
    col_dl1.download_button("⬇️ Download filtered CSV", buf.getvalue(), "gait_filtered_anon.csv", "text/csv")
    all_rows = []
    for s in SUBJECTS_RAW:
        row = {"Subject":s["name"],"Age":s["age"],"Height":s["height"],"Weight":s["weight"]}
        for pk in list(STATS.keys()):
            row[pk+"_ctrl"]  = s.get(pk+"_ctrl","")
            row[pk+"_smart"] = s.get(pk+"_smart","")
        all_rows.append(row)
    buf2 = io.StringIO(); pd.DataFrame(all_rows).to_csv(buf2, index=False)
    col_dl2.download_button("⬇️ Download full dataset CSV", buf2.getvalue(), "gait_full_anon.csv", "text/csv")

# ═════════════════════════════════════════════════════════════════════════════
# KEY INFERENCES
# ═════════════════════════════════════════════════════════════════════════════
elif pg == "Key Inferences":
    st.markdown('<div class="section-header">Key Inferences & Novel Findings</div>', unsafe_allow_html=True)
    st.markdown('<div class="study-tag">Derived from statistical results · Ready for journal Discussion & PPT slides</div>', unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["💡 All Inferences", "📋 PPT Slide Bullets"])
    with tab1:
        c1, c2 = st.columns(2)
        for i, (title, cat, color, text) in enumerate(INFERENCES):
            col = c1 if i % 2 == 0 else c2
            col.markdown(f'''<div class="info-card {color}">
            <div class="infer-title">{i+1}. {title} <span class="infer-cat">[{cat}]</span></div>
            <div class="infer-body">{text}</div></div>''', unsafe_allow_html=True)
    with tab2:
        bullets = [
            (1,"Smartphone use reduced walking speed 16.4% (p<0.001, RBC=0.991)",
             "Near-perfect effect size — virtually every participant slowed when using a smartphone."),
            (2,"Stride length showed largest effect in study (d=1.398 — Huge)",
             "Average step shortened by 12.1 cm — fundamental reorganisation of gait pattern."),
            (3,"Double support ↑34.6%, variability ↑62.9% — fall-avoidance gait",
             "Conservative stability strategy: more bilateral support, less rhythmic consistency."),
            (4,"Only ankle DF changed — hip & knee preserved (distal compensation)",
             "Despite 16% slower speed, ankle actively compensated — CNS protects proximal joints."),
            (5,"Propulsion impulse fell 18.2% — mechanical cause of speed loss (p=0.001)",
             "Force plate data reveals mechanism: attenuated push-off during late stance."),
            (6,"Net impulse sign reversal: net-propulsive → net-decelerative",
             "Control: +0.9 N·s. Smartphone: −0.7 N·s. Only detectable with force plates."),
            (7,"EMG ↑11.6% yet propulsion ↓18.2% — neuromuscular inefficiency",
             "More activation, less output. Underpowered (n=13), requires larger EMG study."),
        ]
        df_b = pd.DataFrame(bullets, columns=["#","Slide Heading","Speaker Note"])
        st.dataframe(df_b, use_container_width=True, hide_index=True)
        buf = io.StringIO(); df_b.to_csv(buf, index=False)
        st.download_button("⬇️ Download PPT bullets CSV", buf.getvalue(), "ppt_bullets.csv", "text/csv")
