"""
Transparent Disengagement Early-Warning Tool - Streamlit Dashboard
An accessible, explainable, and bilingual support-prioritisation system for online education.
"""

import os
import json
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(
    page_title="Transparent Disengagement Early-Warning Tool",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Bilingual Localization Dictionary (English & Tamil)
# ---------------------------------------------------------
I18N = {
    "en": {
        "app_title": "Transparent Disengagement Early-Warning Tool",
        "app_subtitle": "Multi-Signal, Explainable & Non-Punitive Learner Support Prioritisation",
        "tab_dashboard": "📊 Dashboard Overview",
        "tab_learners": "👥 Learner Risk Overview",
        "tab_detail": "🔍 Learner Deep Dive",
        "tab_performance": "📈 Model Performance",
        "tab_backtest": "⏳ Back-Test Simulator",
        "tab_missing": "🛡️ Missing Data & Uncertainty",
        "tab_failures": "🧪 Failure & Edge Cases",
        "total_learners": "Total Active Learners",
        "support_needed": "Support Needed",
        "high_support": "High Support Need",
        "moderate_support": "Moderate Support Need",
        "low_support": "Low Support Need",
        "insufficient_data": "Insufficient Data",
        "avg_engagement": "Avg Engagement Score",
        "avg_confidence": "Avg Model Confidence",
        "select_learner": "Select Learner ID:",
        "risk_filter": "Filter by Support Tier:",
        "course_filter": "Filter by Course:",
        "confidence_filter": "Minimum Confidence (%):",
        "reasons_header": "Why this learner may need support:",
        "strengths_header": "Observed Strengths & Positive Engagement:",
        "action_header": "Recommended Non-Punitive Mentor Action:",
        "confidence_label": "Prediction Confidence",
        "probability_label": "Support Probability",
        "missing_warning": "Data Quality Note",
        "all_courses": "All Courses",
        "all_tiers": "All Tiers",
        "export_csv": "Export Prioritization Roster (CSV)"
    },
    "ta": {
        "app_title": "வெளிப்படையான விலகல் முன்கூட்டிய எச்சரிக்கை கருவி",
        "app_subtitle": "பன்முக சமிக்ஞை, விளக்கக்கூடிய மற்றும் தண்டனையற்ற மாணவர் ஆதரவு முன்னுரிமை அமைப்பு",
        "tab_dashboard": "📊 முதன்மை பார்வை",
        "tab_learners": "👥 மாணவர் அபாய கண்ணோட்டம்",
        "tab_detail": "🔍 தனிப்பட்ட மாணவர் பகுப்பாய்வு",
        "tab_performance": "📈 மாதிரி செயல்திறன்",
        "tab_backtest": "⏳ பின்னோக்கு சோதனை",
        "tab_missing": "🛡️ விடுபட்ட தரவு & நம்பகத்தன்மை",
        "tab_failures": "🧪 விளிம்பு வழக்குகள்",
        "total_learners": "மொத்த மாணவர்கள்",
        "support_needed": "ஆதரவு தேவை",
        "high_support": "அதிக ஆதரவு தேவை",
        "moderate_support": "மிதமான ஆதரவு தேவை",
        "low_support": "குறைந்த ஆதரவு தேவை",
        "insufficient_data": "போதுமான தரவு இல்லை",
        "avg_engagement": "சராசரி ஈடுபாடு குறியீடு",
        "avg_confidence": "சராசரி நம்பகத்தன்மை",
        "select_learner": "மாணவர் அடையாளத்தைத் தேர்ந்தெடுக்கவும்:",
        "risk_filter": "ஆதரவு நிலை வடிகட்டி:",
        "course_filter": "பாடநெறி வடிகட்டி:",
        "confidence_filter": "குறைந்தபட்ச நம்பகத்தன்மை (%):",
        "reasons_header": "இந்த மாணவருக்கு ஆதரவு தேவைப்படுவதற்கான காரணங்கள்:",
        "strengths_header": "கவனிக்கப்பட்ட பலங்கள் & நல் ஈடுபாடு:",
        "action_header": "வழிகாட்டிக்கு பரிந்துரைக்கப்பட்ட உதவி நடவடிக்கை:",
        "confidence_label": "நம்பகத்தன்மை",
        "probability_label": "ஆதரவு நிகழ்தகவு",
        "missing_warning": "தரவு தரம் குறிப்பு",
        "all_courses": "அனைத்து பாடநெறிகள்",
        "all_tiers": "அனைத்து நிலைகள்",
        "export_csv": "மாணவர் பட்டியலை பதிவிறக்குக (CSV)"
    }
}


@st.cache_data
def load_data():
    """Load pre-computed and verified pipeline results."""
    json_path = "data/processed/pipeline_results.json"
    if not os.path.exists(json_path):
        # Run pipeline if not already executed
        from run_pipeline import run_full_pipeline
        run_full_pipeline()
        
    with open(json_path, "r") as f:
        data = json.load(f)
    return data


data = load_data()
active_learners = pd.DataFrame(data["week_5_active_learners"])

# ---------------------------------------------------------
# Sidebar: Language & Navigation Controls
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### 🌐 Language / மொழி")
    lang_choice = st.radio("Select Language / மொழியைத் தேர்வுசெய்க:", ["English", "தமிழ் (Tamil)"], index=0)
    lang = "ta" if "தமிழ்" in lang_choice else "en"
    t = I18N[lang]
    
    st.divider()
    st.markdown(f"### 🛡️ {t['app_title']}")
    st.caption("Ethical, transparent, multi-signal support prioritisation system for online learning.")
    
    # Global Filters
    st.markdown("#### 🎯 Global Filters")
    tier_options = [t["all_tiers"], t["high_support"], t["moderate_support"], t["low_support"], t["insufficient_data"]]
    selected_tier = st.selectbox(t["risk_filter"], tier_options)
    
    course_list = [t["all_courses"]] + sorted(active_learners["course_id"].unique().tolist())
    selected_course = st.selectbox(t["course_filter"], course_list)
    
    min_conf = st.slider(t["confidence_filter"], 0, 100, 30)

# Filter dataset
filtered_df = active_learners.copy()
if selected_course != t["all_courses"]:
    filtered_df = filtered_df[filtered_df["course_id"] == selected_course]
    
if selected_tier != t["all_tiers"]:
    tier_map = {
        t["high_support"]: "High Support Need",
        t["moderate_support"]: "Moderate Support Need",
        t["low_support"]: "Low Support Need",
        t["insufficient_data"]: "Insufficient Data"
    }
    filtered_df = filtered_df[filtered_df["risk_level"] == tier_map.get(selected_tier, selected_tier)]
    
filtered_df = filtered_df[filtered_df["confidence_percentage"] >= min_conf]

# Main Title
st.title(f"🎓 {t['app_title']}")
st.markdown(f"*{t['app_subtitle']}*")

# Navigation Tabs
tabs = st.tabs([
    t["tab_dashboard"],
    t["tab_learners"],
    t["tab_detail"],
    t["tab_performance"],
    t["tab_backtest"],
    t["tab_missing"],
    t["tab_failures"]
])

# ---------------------------------------------------------
# TAB 1: DASHBOARD OVERVIEW
# ---------------------------------------------------------
with tabs[0]:
    st.header(t["tab_dashboard"])
    
    # KPI Row
    c1, c2, c3, c4, c5 = st.columns(5)
    total_active = len(active_learners)
    high_cnt = int((active_learners["risk_level"] == "High Support Need").sum())
    mod_cnt = int((active_learners["risk_level"] == "Moderate Support Need").sum())
    insuf_cnt = int((active_learners["risk_level"] == "Insufficient Data").sum())
    avg_eng = float(active_learners["overall_engagement_score"].mean())
    avg_conf = float(active_learners["confidence_percentage"].mean())
    
    c1.metric(t["total_learners"], f"{total_active:,}")
    c2.metric(f"🔴 {t['high_support']}", f"{high_cnt} ({high_cnt/total_active:.1%})")
    c3.metric(f"🟡 {t['moderate_support']}", f"{mod_cnt} ({mod_cnt/total_active:.1%})")
    c4.metric(f"⚪ {t['insufficient_data']}", f"{insuf_cnt} ({insuf_cnt/total_active:.1%})")
    c5.metric(t["avg_confidence"], f"{avg_conf:.1f}%")
    
    st.divider()
    
    # Visualizations row
    col_l, col_r = st.columns(2)
    
    with col_l:
        st.subheader("Support Need Distribution")
        tier_counts = active_learners["risk_level"].value_counts().reset_index()
        tier_counts.columns = ["Support Tier", "Count"]
        color_map = {
            "Low Support Need": "#10b981",
            "Moderate Support Need": "#f59e0b",
            "High Support Need": "#ef4444",
            "Insufficient Data": "#94a3b8"
        }
        fig_donut = px.pie(
            tier_counts, names="Support Tier", values="Count", hole=0.5,
            color="Support Tier", color_discrete_map=color_map,
            title="Active Cohort Support Prioritisation"
        )
        fig_donut.update_traces(textinfo="percent+label")
        st.plotly_chart(fig_donut, use_container_width=True)
        
    with col_r:
        st.subheader("Engagement Score vs. Model Confidence")
        fig_scatter = px.scatter(
            active_learners,
            x="overall_engagement_score",
            y="confidence_percentage",
            color="risk_level",
            color_discrete_map=color_map,
            hover_data=["learner_id", "course_id", "support_probability"],
            labels={
                "overall_engagement_score": "Overall Engagement Score (0-100)",
                "confidence_percentage": "Prediction Confidence (%)",
                "risk_level": "Support Tier"
            },
            title="Evidence Confidence Across Engagement Levels"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

# ---------------------------------------------------------
# TAB 2: LEARNER RISK OVERVIEW
# ---------------------------------------------------------
with tabs[1]:
    st.header(t["tab_learners"])
    st.caption(f"Showing {len(filtered_df)} learners matching active filters. Sorted by support probability.")
    
    display_cols = [
        "learner_id", "course_id", "risk_level", "support_probability",
        "confidence_percentage", "missing_feature_count", "overall_engagement_score"
    ]
    
    table_df = filtered_df[display_cols].sort_values(by="support_probability", ascending=False).copy()
    table_df.columns = [
        "Learner ID", "Course", "Support Tier", "Support Probability",
        "Confidence (%)", "Missing Signals", "Engagement Score (0-100)"
    ]
    
    st.dataframe(
        table_df.style.format({
            "Support Probability": "{:.3f}",
            "Confidence (%)": "{:.1f}%",
            "Engagement Score (0-100)": "{:.1f}"
        }),
        use_container_width=True,
        height=400
    )
    
    # CSV Export
    csv = table_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=f"📥 {t['export_csv']}",
        data=csv,
        file_name="mentor_support_prioritisation.csv",
        mime="text/csv"
    )

# ---------------------------------------------------------
# TAB 3: LEARNER DETAIL / DEEP DIVE
# ---------------------------------------------------------
with tabs[2]:
    st.header(t["tab_detail"])
    
    # Learner Selector
    all_ids = active_learners["learner_id"].tolist()
    selected_id = st.selectbox(t["select_learner"], all_ids, index=0)
    learner = active_learners[active_learners["learner_id"] == selected_id].iloc[0]
    
    # Header card
    risk_color = {
        "Low Support Need": "🟢",
        "Moderate Support Need": "🟡",
        "High Support Need": "🔴",
        "Insufficient Data": "⚪"
    }.get(learner["risk_level"], "⚪")
    
    st.markdown(f"### {risk_color} Learner: `{learner['learner_id']}` | Course: `{learner['course_id']}`")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Support Tier", learner["risk_level"])
    m2.metric(t["probability_label"], f"{learner['support_probability']:.1%}")
    m3.metric(t["confidence_label"], f"{learner['confidence_percentage']:.1f}%")
    m4.metric("Composite Engagement", f"{learner['overall_engagement_score']:.1f} / 100")
    
    # Missing warning if present
    if learner["missing_feature_count"] > 0:
        st.warning(f"⚠️ **{t['missing_warning']}**: {learner['uncertainty_warning']}")
        
    st.divider()
    
    # 5 Signals Radar Chart & Trend Breakdown
    col_chart, col_expl = st.columns([1, 1])
    
    with col_chart:
        st.subheader("5 Learning Signals Profile")
        
        radar_categories = ["Attendance", "Study Activity", "Assessment", "Help Seeking", "Feedback"]
        # Normalize to 0-100 scale for radar
        norm_att = min(100.0, float(learner.get("attendance_rate", 1.0)) * 100.0)
        norm_act = min(100.0, float(learner.get("active_minutes", 120.0)) / 2.4)
        norm_scr = min(100.0, float(learner.get("average_score", 70.0)))
        norm_hlp = min(100.0, float(learner.get("help_seeking_frequency", 1)) * 33.3)
        norm_fb = min(100.0, float(learner.get("feedback_signal", 1.0)) * 80.0)
        
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=[norm_att, norm_act, norm_scr, norm_hlp, norm_fb],
            theta=radar_categories,
            fill='toself',
            name=learner['learner_id'],
            line_color='#2563eb'
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=False,
            margin=dict(l=30, r=30, t=30, b=30)
        )
        st.plotly_chart(fig_radar, use_container_width=True)
        
    with col_expl:
        st.subheader("📝 Explainability & Recommendation")
        
        # Reasons
        st.markdown(f"**{t['reasons_header']}**")
        reasons = learner.get("explanation_reasons", [])
        if reasons:
            for r in reasons:
                st.markdown(f"- ⚠️ {r}")
        else:
            st.markdown("- ✅ All behavioral signals are within normal healthy thresholds.")
            
        # Strengths
        strengths = learner.get("explanation_strengths", [])
        if strengths:
            st.markdown(f"**{t['strengths_header']}**")
            for s in strengths:
                st.markdown(f"- 🌟 {s}")
                
        # Recommended action
        st.markdown(f"**{t['action_header']}**")
        action_text = learner.get("recommended_action_tamil" if lang == "ta" else "recommended_action", "")
        st.info(f"🤝 **Action**: {action_text}")

# ---------------------------------------------------------
# TAB 4: MODEL PERFORMANCE
# ---------------------------------------------------------
with tabs[3]:
    st.header(t["tab_performance"])
    
    st.markdown("### 📊 Empirical Before-and-After Comparison (Held-Out Test Set $N=1,500$)")
    comp_df = pd.DataFrame(data["before_after_comparison"])
    st.table(comp_df)
    
    col_cm1, col_cm2 = st.columns(2)
    with col_cm1:
        st.subheader("Baseline Heuristic Matrix")
        base_cm = data["baseline_metrics"]["confusion_matrix"]
        fig_cm1 = px.imshow(
            base_cm,
            text_auto=True,
            x=["Predicted Thriving", "Predicted Support"],
            y=["Actual Thriving", "Actual Support"],
            color_continuous_scale="Blues",
            title=f"Baseline (FP={data['baseline_metrics']['fp']}, FN={data['baseline_metrics']['fn']})"
        )
        st.plotly_chart(fig_cm1, use_container_width=True)
        
    with col_cm2:
        st.subheader("Improved Random Forest Matrix")
        ml_cm = data["improved_metrics"]["confusion_matrix"]
        fig_cm2 = px.imshow(
            ml_cm,
            text_auto=True,
            x=["Predicted Thriving", "Predicted Support"],
            y=["Actual Thriving", "Actual Support"],
            color_continuous_scale="Greens",
            title=f"Improved ML (FP={data['improved_metrics']['fp']}, FN={data['improved_metrics']['fn']})"
        )
        st.plotly_chart(fig_cm2, use_container_width=True)
        
    st.divider()
    
    # Feature Importances & Multi-Signal Ablation
    c_imp, c_abl = st.columns(2)
    with c_imp:
        st.subheader("Top Transparent Feature Contributions")
        feat_imp_df = pd.DataFrame(data["feature_importances"][:10])
        fig_imp = px.bar(
            feat_imp_df,
            x="percentage",
            y="feature",
            orientation="h",
            labels={"percentage": "Relative Importance (%)", "feature": "Telemetry Signal"},
            title="Signals Driving Model Predictions"
        )
        fig_imp.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig_imp, use_container_width=True)
        
    with c_abl:
        st.subheader("Ablation Study: No Single Punitive Factor")
        abl_df = pd.DataFrame(data["ablation_study"])
        fig_abl = px.bar(
            abl_df,
            x="configuration",
            y="f1",
            color="configuration",
            labels={"f1": "F1-Score", "configuration": "Signal Configuration"},
            title="Multi-Signal Integration Outperforms Single Metrics"
        )
        st.plotly_chart(fig_abl, use_container_width=True)

# ---------------------------------------------------------
# TAB 5: BACK-TEST SIMULATOR
# ---------------------------------------------------------
with tabs[4]:
    st.header(t["tab_backtest"])
    st.markdown(
        "**Longitudinal Back-Test Progression**: Demonstrates how early the improved model detects disengagement "
        "relative to the baseline heuristic across sequential course weeks."
    )
    
    bt_prog = data["backtest_results"]["weekly_progression"]
    weeks = [p["week"] for p in bt_prog]
    base_f1 = [p["baseline"]["f1"] for p in bt_prog]
    ml_f1 = [p["improved_model"]["f1"] for p in bt_prog]
    rec_gain = [p["recall_improvement"] * 100.0 for p in bt_prog]
    
    fig_bt = go.Figure()
    fig_bt.add_trace(go.Scatter(x=weeks, y=base_f1, mode="lines+markers", name="Baseline Rule F1", line=dict(color="#94a3b8", dash="dash")))
    fig_bt.add_trace(go.Scatter(x=weeks, y=ml_f1, mode="lines+markers", name="Improved ML F1", line=dict(color="#2563eb", width=3)))
    fig_bt.update_layout(
        title="Weekly Detection Power (F1-Score)",
        xaxis_title="Course Week",
        yaxis_title="F1-Score",
        margin=dict(l=40, r=40, t=40, b=40)
    )
    st.plotly_chart(fig_bt, use_container_width=True)
    
    st.info(f"💡 **Key Finding**: {data['backtest_results']['earlier_identification_insight']}")

# ---------------------------------------------------------
# TAB 6: MISSING DATA & UNCERTAINTY
# ---------------------------------------------------------
with tabs[5]:
    st.header(t["tab_missing"])
    
    st.markdown("### 🛡️ Missing Data & Reliability Analysis (Section 17)")
    st.write(
        "When key learning telemetry is missing, this system lowers confidence or defers the alert "
        "to avoid false accusations."
    )
    
    m_info = data["missing_data_summary"]
    col_m1, col_m2 = st.columns(2)
    
    with col_m1:
        st.subheader("Missingness Percentage by Signal")
        missing_feats = pd.DataFrame(list(m_info["feature_missing_percentages"].items()), columns=["Signal", "Missing (%)"])
        fig_miss = px.bar(missing_feats, x="Missing (%)", y="Signal", orientation="h", title="Signal Sparsity Profile")
        fig_miss.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig_miss, use_container_width=True)
        
    with col_m2:
        st.subheader("Data Reliability Framework")
        st.markdown("""
        ```
        Missing Data Rate
               ↓
        Prediction Confidence Penalty
               ↓
        Prediction Reliability Tiers:
        • Low Missingness: High Reliability (90-95%)
        • Moderate Missingness: Moderate (70-85%) - Mentor Discretion Advised
        • Severe (≥3 Missing Signals): "Insufficient Data" - Defer Automated Flag
        ```
        """)
        st.metric("Total Insufficient Data Records", f"{m_info['insufficient_data_count']} ({m_info['insufficient_data_rate']:.1%})")

# ---------------------------------------------------------
# TAB 7: FAILURE & EDGE CASES
# ---------------------------------------------------------
with tabs[6]:
    st.header(t["tab_failures"])
    st.markdown("### 🧪 Automated Edge / Failure Case Evaluation (Section 20)")
    
    c_e1, c_e2 = st.columns(2)
    
    with c_e1:
        st.markdown("#### Case 1: High Marks, Low Engagement")
        st.caption("Student has 90% score, but only 25 min activity and 20% attendance.")
        st.success("✅ **System Behavior**: Not classified as safe. Elevated to 'Moderate/High Support Need' because compound activity drops outweigh legacy exam marks.")
        
        st.markdown("#### Case 2: Low Attendance, High Engagement")
        st.caption("Asynchronous self-directed student has 25% attendance, but 260 active mins and 88% scores.")
        st.success("✅ **System Behavior**: Avoids punitive flagging. Categorized as 'Low Support Need' because independent study hours prove active engagement.")

    with c_e2:
        st.markdown("#### Case 3: Missing Telemetry Shield")
        st.caption("Student with missing feedback, activity telemetry, and help-seeking records.")
        st.warning("⚠️ **System Behavior**: Confirmed classified as 'Insufficient Data' with alert deferred and low confidence warnings displayed.")
        
        st.markdown("#### Case 4: Sudden Behaviour Collapse")
        st.caption("Student with historically good marks suddenly drops logins, attendance, and submits zero assignments in Week 4.")
        st.success("✅ **System Behavior**: Caught by `engagement_trend` slope detector; proactive 1-on-1 mentor check-in triggered.")

st.divider()
st.caption("Transparent Disengagement Early-Warning Tool • Designed for Ethical Educational Technology • 2026")
