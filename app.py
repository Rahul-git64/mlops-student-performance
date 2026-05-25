import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

# Set page configuration with a modern title and icon
st.set_page_config(
    page_title="Student Performance MLOps App",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Dark Glassmorphism Styling
st.markdown("""
<style>
    /* Main Background & Fonts */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #f8fafc;
    }
    
    /* Headers & Custom Titles */
    h1, h2, h3 {
        font-family: 'Outfit', 'Inter', sans-serif !important;
        font-weight: 700;
        background: linear-gradient(to right, #a5b4fc, #6366f1, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Cards and Glassmorphism */
    .glass-card {
        background: rgba(30, 41, 59, 0.45);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        margin-bottom: 20px;
        box-shadow: 0 10px 30px 0 rgba(0, 0, 0, 0.25);
    }
    
    /* Grade Badges */
    .badge {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 9999px;
        font-weight: bold;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-size: 1.1rem;
        box-shadow: 0 4px 14px 0 rgba(0,0,0,0.3);
    }
    .badge-fail {
        background-color: #ef4444;
        color: white;
        border: 1px solid #f87171;
        box-shadow: 0 0 15px rgba(239, 68, 68, 0.45);
    }
    .badge-pass {
        background-color: #10b981;
        color: white;
        border: 1px solid #34d399;
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.45);
    }
    .badge-distinction {
        background-color: #3b82f6;
        color: white;
        border: 1px solid #60a5fa;
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.6);
    }
    
    /* Interactive Sliders & inputs */
    .stSlider > div > div > div > div {
        background-color: #6366f1 !important;
    }
    
    /* Custom button styling */
    .stButton>button {
        background: linear-gradient(135deg, #4f46e5 0%, #3730a3 100%) !important;
        color: white !important;
        border: none !important;
        padding: 12px 28px !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3) !important;
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5) !important;
        background: linear-gradient(135deg, #6366f1 0%, #4338ca 100%) !important;
    }
</style>
""", unsafe_allow_html=True)

# App Sidebar info
st.sidebar.markdown("""
<div class='glass-card' style='padding:15px; text-align:center;'>
    <h3 style='margin: 0 0 10px 0;'>MLOps Pipeline</h3>
    <p style='font-size:0.9rem; color:#94a3b8;'>Student Performance Prediction and System Orchestration</p>
    <hr style='border: 1px solid rgba(255,255,255,0.08); margin:10px 0;'>
    <p style='font-size:0.8rem; color:#64748b;'>Model: Logistic Regression<br>Dataset: Student Records<br>Tracking: MLflow<br>Versioning: DVC<br>Orchestration: Kubernetes</p>
</div>
""", unsafe_allow_html=True)

# Title Section
st.markdown("<h1 style='text-align: center; margin-bottom: 5px;'>🎓 STUDENT PERFORMANCE MLSD SYSTEM</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 1.15rem; margin-bottom: 30px;'>Production-ready Machine Learning system predicting student grades with DVC & MLflow pipelines</p>", unsafe_allow_html=True)

# Helper function to load model artifacts with warning if not available
@st.cache_resource
def load_ml_assets():
    model_dir = "models"
    files = {
        "model": "student_model.pkl",
        "scaler": "student_scaler.pkl",
        "label_encoder": "student_label_encoder.pkl",
        "feature_columns": "feature_columns.pkl",
        "feature_encoders": "feature_encoders.pkl"
    }
    
    # Check if all files exist
    missing_files = []
    for key, val in files.items():
        if not os.path.exists(os.path.join(model_dir, val)):
            missing_files.append(val)
            
    if missing_files:
        return None, f"Missing files in '{model_dir}': " + ", ".join(missing_files)
        
    try:
        model = joblib.load(os.path.join(model_dir, files["model"]))
        scaler = joblib.load(os.path.join(model_dir, files["scaler"]))
        label_encoder = joblib.load(os.path.join(model_dir, files["label_encoder"]))
        feature_columns = joblib.load(os.path.join(model_dir, files["feature_columns"]))
        feature_encoders = joblib.load(os.path.join(model_dir, files["feature_encoders"]))
        return (model, scaler, label_encoder, feature_columns, feature_encoders), None
    except Exception as e:
        return None, str(e)

# Load artifacts
assets, err = load_ml_assets()

if err:
    st.markdown(f"""
    <div class='glass-card' style='border: 1px solid rgba(239, 68, 68, 0.4); background: rgba(239, 68, 68, 0.05);'>
        <h3 style='color: #f87171; margin: 0 0 10px 0;'>⚠️ Model Artifacts Not Available</h3>
        <p style='color: #cbd5e1; margin-bottom: 15px;'>The required trained model files could not be found or loaded.</p>
        <p style='color: #94a3b8; font-size: 0.9rem;'><b>Details:</b> {err}</p>
        <hr style='border: 1px solid rgba(255,255,255,0.05); margin: 15px 0;'>
        <p style='color: #a5b4fc; font-weight: 500;'><b>Action Required:</b> Please execute the training script first in the terminal to generate and serialize the model artifacts:</p>
        <code style='display: block; background: #0b0f19; padding: 10px; border-radius: 6px; color: #a5b4fc; border: 1px solid rgba(255,255,255,0.08);'>python train.py</code>
    </div>
    """, unsafe_allow_html=True)
else:
    model, scaler, label_encoder, feature_columns, feature_encoders = assets
    
    # Input Form Layout
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("📝 Enter Student Details for Evaluation")
    
    # Creating two tabs to organize numerical and categorical/socioeconomic data beautifully
    tab1, tab2 = st.tabs(["📊 Academic Performance Metrics", "🧑 Socio-Environmental Factors"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            study_hours = st.slider("Weekly Study Hours", min_value=0.0, max_value=24.0, value=6.0, step=0.1, help="Total number of hours studied per week")
            attendance_pct = st.slider("Attendance Percentage", min_value=0.0, max_value=100.0, value=80.0, step=0.1, help="Class attendance rate")
            prev_gpa = st.slider("Previous GPA", min_value=0.0, max_value=4.0, value=3.0, step=0.01, help="Grade Point Average in the prior term")
            assignments_done = st.slider("Assignments Completed (%)", min_value=0.0, max_value=100.0, value=75.0, step=0.5, help="Percentage of home assignments submitted")
            
        with col2:
            quiz_avg = st.slider("Quiz Average Score", min_value=0.0, max_value=100.0, value=70.0, step=0.1, help="Average percentage in school quizzes")
            midterm_score = st.slider("Midterm Exam Score", min_value=0.0, max_value=100.0, value=72.0, step=0.1, help="Percentage score achieved on the midterm exam")
            final_score = st.slider("Final Exam Score", min_value=0.0, max_value=100.0, value=75.0, step=0.1, help="Percentage score achieved on the final exam")
            sleep_hours = st.slider("Average Sleep Hours", min_value=0.0, max_value=24.0, value=7.5, step=0.5, help="Average number of hours slept per night")
            
    with tab2:
        col3, col4 = st.columns(2)
        with col3:
            gender = st.selectbox("Gender", options=["Female", "Male"], index=0)
            parent_edu = st.selectbox("Parent Education Level", options=["None", "High School", "Undergraduate", "Postgraduate"], index=2)
            school_type = st.selectbox("School Type", options=["Public", "Private"], index=0)
            distance_km = st.number_input("Distance to School (km)", min_value=0.0, max_value=100.0, value=5.0, step=0.1, help="One-way commute in kilometers")
            
        with col4:
            internet_hours = st.slider("Daily Internet Hours", min_value=0.0, max_value=24.0, value=3.0, step=0.5, help="Non-academic internet usage hours per day")
            family_support = st.slider("Family Support Scale", min_value=1, max_value=5, value=3, help="Socio-emotional family support metric (1 = Lowest, 5 = Highest)")
            part_time_job = st.radio("Has Part-Time Job?", options=["No", "Yes"], index=0, horizontal=True)
            extracurricular = st.radio("Participates in Extracurriculars?", options=["No", "Yes"], index=1, horizontal=True)
            
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Map raw options to encoded numeric inputs or model format
    inputs_dict = {
        "study_hours": study_hours,
        "attendance_pct": attendance_pct,
        "prev_gpa": prev_gpa,
        "assignments_done": assignments_done,
        "sleep_hours": sleep_hours,
        "internet_hours": internet_hours,
        "family_support": family_support,
        "part_time_job": 1 if part_time_job == "Yes" else 0,
        "extracurricular": 1 if extracurricular == "Yes" else 0,
        "parent_edu": parent_edu,
        "gender": gender,
        "school_type": school_type,
        "distance_km": distance_km,
        "quiz_avg": quiz_avg,
        "midterm_score": midterm_score,
        "final_score": final_score
    }
    
    # Make Prediction Button
    if st.button("🔮 PREDICT STUDENT GRADE"):
        # Convert dictionary to DataFrame in exact training columns order
        input_df = pd.DataFrame([inputs_dict])
        
        # Preprocess using categorical Label Encoders
        for col in feature_encoders.keys():
            try:
                encoder = feature_encoders[col]
                input_df[col] = encoder.transform(input_df[col])
            except Exception as e:
                st.error(f"Error encoding categorical column '{col}': {e}")
                
        # Ensure order matches feature columns exactly
        input_df = input_df[feature_columns]
        
        # Scale numerical features
        try:
            scaled_features = scaler.transform(input_df)
            
            # Predict class
            pred_class = model.predict(scaled_features)[0]
            pred_grade = label_encoder.inverse_transform([pred_class])[0]
            
            # Predict probabilities
            pred_probs = model.predict_proba(scaled_features)[0]
            classes = label_encoder.classes_
            
            # Display Prediction Card
            st.markdown("<div class='glass-card' style='text-align: center; border: 1px solid rgba(255,255,255,0.12);'>", unsafe_allow_html=True)
            st.markdown("<h2>🎯 PREDICTION RESULTS</h2>", unsafe_allow_html=True)
            
            # Style based on grade
            badge_class = "badge-pass"
            motivational_quote = "Great work! Keep maintaining your dedication and study habits."
            
            if pred_grade == "Fail":
                badge_class = "badge-fail"
                motivational_quote = "Additional academic counseling, tutoring, and study hour adjustments are highly recommended."
            elif pred_grade == "Distinction":
                badge_class = "badge-distinction"
                motivational_quote = "Outstanding! Exemplary academic performance. Keep leading the way!"
                
            st.markdown(f"""
                <div style='margin: 15px 0;'>
                    <span class='badge {badge_class}'>Predicted Grade: {pred_grade}</span>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"<p style='font-style: italic; font-size: 1.05rem; color: #e2e8f0; margin-bottom: 25px;'>\"{motivational_quote}\"</p>", unsafe_allow_html=True)
            
            # Display Probability Distribution Meter
            st.markdown("<h3>📊 Model Classification Probabilities</h3>", unsafe_allow_html=True)
            prob_col1, prob_col2, prob_col3 = st.columns(3)
            
            grade_colors = {
                "Fail": "#f87171",
                "Pass": "#34d399",
                "Distinction": "#60a5fa"
            }
            
            cols = [prob_col1, prob_col2, prob_col3]
            for idx, c in enumerate(classes):
                prob = pred_probs[idx]
                grade_name = c
                color = grade_colors.get(grade_name, "#818cf8")
                
                with cols[idx % 3]:
                    st.metric(label=f"Probability ({grade_name})", value=f"{prob * 100:.1f}%")
                    st.markdown(f"""
                    <div style='background-color: rgba(255,255,255,0.05); border-radius: 9999px; height: 8px; width: 100%; margin-top:5px; overflow: hidden;'>
                        <div style='background-color: {color}; width: {prob*100}%; height: 100%; border-radius: 9999px;'></div>
                    </div>
                    """, unsafe_allow_html=True)
                    
            st.markdown("</div>", unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Failed to process features or generate model prediction: {e}")
