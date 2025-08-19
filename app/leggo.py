import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json

# Configure page settings
st.set_page_config(
    page_title="Diabetes Risk Predictor",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2E8B57;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #333;
        margin-bottom: 0.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .risk-low {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .risk-medium {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .risk-high {
        background: linear-gradient(135deg, #fc466b 0%, #3f5efb 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .recommendation-card {
        background: #f8f9fa;
        padding: 1rem;
        border-left: 4px solid #28a745;
        margin: 0.5rem 0;
        border-radius: 5px;
    }
    .assessment-item {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
        border-left: 4px solid #007bff;
    }
</style>
""", unsafe_allow_html=True)

class DiabetesRiskPredictor:
    """
    A comprehensive diabetes risk assessment application using Streamlit.
    
    This class handles the complete workflow from initial assessment through
    risk calculation, recommendations, and ongoing health tracking.
    """
    
    def __init__(self):
        """Initialize the app with session state management."""
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Initialize all session state variables for the application."""
        # User data storage
        if 'user_data' not in st.session_state:
            st.session_state.user_data = {}
        
        # Assessment data
        if 'assessment_completed' not in st.session_state:
            st.session_state.assessment_completed = False
        
        if 'risk_score' not in st.session_state:
            st.session_state.risk_score = 0
        
        if 'risk_level' not in st.session_state:
            st.session_state.risk_level = "Unknown"
        
        # Navigation state
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "welcome"
        
        # Assessment history
        if 'assessment_history' not in st.session_state:
            st.session_state.assessment_history = []
        
        # Health tracking data
        if 'health_data' not in st.session_state:
            st.session_state.health_data = {
                'glucose_readings': [],
                'weight_log': [],
                'exercise_log': [],
                'medication_log': []
            }
    
    def calculate_risk_score(self, user_data):
        """
        Calculate diabetes risk score based on user input.
        
        Args:
            user_data (dict): Dictionary containing user health information
            
        Returns:
            tuple: (risk_score, risk_level, risk_percentage)
        """
        score = 0
        
        # Age scoring
        age = user_data.get('age', 0)
        if age >= 45:
            score += 20
        elif age >= 35:
            score += 10
        
        # BMI scoring
        bmi = user_data.get('bmi', 0)
        if bmi >= 30:
            score += 30
        elif bmi >= 25:
            score += 20
        elif bmi >= 23:
            score += 10
        
        # Family history
        if user_data.get('family_history', False):
            score += 25
        
        # Physical activity
        if not user_data.get('regular_exercise', True):
            score += 15
        
        # High blood pressure
        if user_data.get('high_bp', False):
            score += 15
        
        # Previous high glucose
        if user_data.get('high_glucose', False):
            score += 20
        
        # Determine risk level and percentage
        if score <= 30:
            risk_level = "Low Risk"
            risk_percentage = min(score * 2, 25)
        elif score <= 60:
            risk_level = "Medium Risk"
            risk_percentage = min(30 + (score - 30) * 1.5, 60)
        else:
            risk_level = "High Risk"
            risk_percentage = min(60 + (score - 60) * 1.2, 90)
        
        return score, risk_level, int(risk_percentage)
    
    def render_welcome_page(self):
        """Render the welcome/landing page of the application."""
        st.markdown('<div class="main-header">Welcome to Your Health Journey</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            ### Diabetes Risk Predictor
            
            This tool helps you understand your risk of developing Type 2 diabetes. Early detection and diagnosis, but it can guide you towards healthier lifestyle choices.
            
            Our assessment considers multiple risk factors including:
            - Age and BMI
            - Family history
            - Lifestyle factors
            - Medical history
            
            **Ready to start your health assessment?**
            """)
            
            if st.button("🚀 Start Assessment", type="primary", use_container_width=True):
                st.session_state.current_page = "assessment"
                st.rerun()
        
        with col2:
            st.image("https://via.placeholder.com/300x400/4CAF50/FFFFFF?text=Health+Icon", 
                    caption="Your Health Matters")
    
    def render_assessment_page(self):
        """Render the risk assessment form page."""
        st.markdown('<div class="main-header">Risk Assessment</div>', unsafe_allow_html=True)
        st.markdown("**Step 1 of 10**")
        
        progress = st.progress(0.1)
        
        st.markdown("### Basic Information")
        
        with st.form("risk_assessment_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                age = st.number_input("Age (years)", min_value=18, max_value=100, value=30)
                weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=70.0, step=0.1)
                height = st.number_input("Height (cm)", min_value=120.0, max_value=220.0, value=170.0, step=0.1)
            
            with col2:
                family_history = st.selectbox("Family History of Diabetes", 
                                            ["No", "Yes - Parent", "Yes - Sibling", "Yes - Both"])
                exercise = st.selectbox("Regular Physical Activity", 
                                      ["Yes - Daily", "Yes - Weekly", "Occasionally", "Rarely"])
                high_bp = st.selectbox("High Blood Pressure", ["No", "Yes", "Don't Know"])
            
            st.markdown("### Additional Health Information")
            
            col3, col4 = st.columns(2)
            with col3:
                smoking = st.selectbox("Smoking Status", ["Never", "Former", "Current"])
                stress_level = st.selectbox("Stress Level", ["Low", "Moderate", "High"])
            
            with col4:
                sleep_hours = st.number_input("Average Sleep Hours", min_value=3, max_value=12, value=7)
                prev_high_glucose = st.selectbox("Previous High Glucose Reading", ["No", "Yes", "Don't Know"])
            
            submitted = st.form_submit_button("Calculate Risk", type="primary", use_container_width=True)
            
            if submitted:
                # Calculate BMI
                bmi = weight / ((height / 100) ** 2)
                
                # Store user data
                user_data = {
                    'age': age,
                    'weight': weight,
                    'height': height,
                    'bmi': bmi,
                    'family_history': family_history != "No",
                    'regular_exercise': exercise in ["Yes - Daily", "Yes - Weekly"],
                    'high_bp': high_bp == "Yes",
                    'smoking': smoking,
                    'stress_level': stress_level,
                    'sleep_hours': sleep_hours,
                    'high_glucose': prev_high_glucose == "Yes"
                }
                
                st.session_state.user_data = user_data
                
                # Calculate risk
                score, risk_level, risk_percentage = self.calculate_risk_score(user_data)
                st.session_state.risk_score = score
                st.session_state.risk_level = risk_level
                st.session_state.risk_percentage = risk_percentage
                st.session_state.assessment_completed = True
                
                # Add to history
                assessment_record = {
                    'date': datetime.now().strftime("%Y-%m-%d"),
                    'risk_level': risk_level,
                    'risk_percentage': risk_percentage,
                    'bmi': round(bmi, 1)
                }
                st.session_state.assessment_history.append(assessment_record)
                
                st.session_state.current_page = "results"
                st.rerun()
    
    def render_results_page(self):
        """Render the risk assessment results page."""
        if not st.session_state.assessment_completed:
            st.warning("Please complete the assessment first.")
            return
        
        risk_level = st.session_state.risk_level
        risk_percentage = st.session_state.risk_percentage
        
        st.markdown('<div class="main-header">Your Diabetes Risk</div>', unsafe_allow_html=True)
        
        # Risk level display
        if "Low" in risk_level:
            st.markdown(f'<div class="risk-low"><h2>{risk_level}</h2><p>Risk Percentage: {risk_percentage}%</p></div>', 
                       unsafe_allow_html=True)
        elif "Medium" in risk_level:
            st.markdown(f'<div class="risk-medium"><h2>{risk_level}</h2><p>Risk Percentage: {risk_percentage}%</p></div>', 
                       unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="risk-high"><h2>{risk_level}</h2><p>Risk Percentage: {risk_percentage}%</p></div>', 
                       unsafe_allow_html=True)
        
        # Risk explanation
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### Understanding Your Risk")
            
            if "Low" in risk_level:
                st.success("""
                **Great news!** You have a low risk of developing type 2 diabetes in the next 10 years. Continue to maintain a healthy lifestyle to keep your risk low.
                """)
            elif "Medium" in risk_level:
                st.warning("""
                **Attention needed.** Based on your responses, your risk is considered medium. This means you have a higher likelihood of developing type 2 diabetes compared to the general population, but there are steps you can take to reduce your risk.
                """)
            else:
                st.error("""
                **Important consultation needed.** Your risk of developing type 2 diabetes is high. This means you have several risk factors that significantly increase your likelihood of developing the condition. It's important to consult a healthcare professional for further evaluation and personalized advice.
                """)
        
        with col2:
            # Risk gauge chart
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = risk_percentage,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Risk Level"},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 30], 'color': "lightgreen"},
                        {'range': [30, 60], 'color': "yellow"},
                        {'range': [60, 100], 'color': "red"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        # Action buttons
        col3, col4, col5 = st.columns(3)
        with col3:
            if st.button("📋 View Recommendations", use_container_width=True):
                st.session_state.current_page = "recommendations"
                st.rerun()
        
        with col4:
            if st.button("📊 Health Dashboard", use_container_width=True):
                st.session_state.current_page = "dashboard"
                st.rerun()
        
        with col5:
            if st.button("🔄 New Assessment", use_container_width=True):
                st.session_state.current_page = "assessment"
                st.rerun()
    
    def render_recommendations_page(self):
        """Render personalized recommendations based on risk assessment."""
        st.markdown('<div class="main-header">Your Health Recommendations</div>', unsafe_allow_html=True)
        
        if not st.session_state.assessment_completed:
            st.warning("Please complete the assessment to view personalized recommendations.")
            return
        
        user_data = st.session_state.user_data
        risk_level = st.session_state.risk_level
        
        st.markdown("### Lifestyle Recommendations")
        
        # Physical Activity Recommendations
        st.markdown('<div class="recommendation-card">', unsafe_allow_html=True)
        st.markdown("#### 🏃‍♂️ Regular Physical Activity")
        if not user_data.get('regular_exercise', True):
            st.markdown("""
            - Aim for at least 150 minutes of moderate-intensity aerobic activity per week, such as brisk walking
            - Include muscle-strengthening activities on 2 or more days per week
            - Start slowly and gradually increase duration and intensity
            """)
        else:
            st.markdown("""
            - Excellent! Continue your current exercise routine
            - Consider adding variety with different types of activities
            - Monitor your progress and set new fitness goals
            """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Diet Recommendations
        st.markdown('<div class="recommendation-card">', unsafe_allow_html=True)
        st.markdown("#### 🥗 Adequate Sleep")
        st.markdown("""
        - Aim for 7-9 hours of quality sleep each night to support overall health and well-being
        - Maintain a consistent sleep schedule
        - Create a relaxing bedtime routine
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Stress Management
        st.markdown('<div class="recommendation-card">', unsafe_allow_html=True)
        st.markdown("#### 🧘‍♀️ Stress Management")
        if user_data.get('stress_level', 'Low') == 'High':
            st.markdown("""
            - Practice stress-reduction techniques like meditation, yoga, or deep breathing
            - Consider counseling or therapy for persistent stress
            - Engage in hobbies and activities you enjoy
            """)
        else:
            st.markdown("""
            - Continue managing stress with healthy coping strategies
            - Stay connected with friends and family
            - Maintain work-life balance
            """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Weight Management
        if user_data.get('bmi', 0) > 25:
            st.markdown('<div class="recommendation-card">', unsafe_allow_html=True)
            st.markdown("#### ⚖️ Weight Management")
            st.markdown("""
            - Focus on maintaining a healthy weight through a balanced diet and regular physical activity
            - Consider consulting with a healthcare provider or registered dietitian
            - Aim for gradual, sustainable weight loss if needed
            """)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Medical Follow-up
        if "High" in risk_level:
            st.markdown('<div class="recommendation-card">', unsafe_allow_html=True)
            st.markdown("#### 🩺 Medical Follow-up")
            st.markdown("""
            - **Important:** Consult with your healthcare provider for further evaluation
            - Regular check-ups and monitoring are recommended
            - Discuss preventive measures and early intervention strategies
            """)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Navigation
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back to Results", use_container_width=True):
                st.session_state.current_page = "results"
                st.rerun()
        with col2:
            if st.button("Health Dashboard →", use_container_width=True):
                st.session_state.current_page = "dashboard"
                st.rerun()
    
    def render_dashboard_page(self):
        """Render the health tracking dashboard."""
        st.markdown('<div class="main-header">My Health Dashboard</div>', unsafe_allow_html=True)
        
        # Past Assessments Section
        st.markdown("### Past Assessments")
        
        if st.session_state.assessment_history:
            for i, assessment in enumerate(st.session_state.assessment_history):
                st.markdown(f'<div class="assessment-item">', unsafe_allow_html=True)
                col1, col2, col3 = st.columns([2, 2, 1])
                with col1:
                    st.markdown(f"**Assessment on {assessment['date']}**")
                with col2:
                    st.markdown(f"Risk Level: **{assessment['risk_level']}**")
                with col3:
                    st.markdown(f"BMI: {assessment['bmi']}")
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No assessment history available. Complete an assessment to see your results here.")
        
        # Risk Trends Section
        st.markdown("### Risk Trends")
        
        if len(st.session_state.assessment_history) > 1:
            # Create trend chart
            df = pd.DataFrame(st.session_state.assessment_history)
            df['date'] = pd.to_datetime(df['date'])
            
            fig = px.line(df, x='date', y='risk_percentage', 
                         title='Risk Level Over Time',
                         labels={'risk_percentage': 'Risk Percentage (%)', 'date': 'Date'})
            fig.update_traces(line_color='#2E8B57', line_width=3)
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            # Risk level indicator
            current_risk = st.session_state.risk_level
            if "Low" in current_risk:
                st.success(f"Current Risk Level: **{current_risk}**")
            elif "Medium" in current_risk:
                st.warning(f"Current Risk Level: **{current_risk}**")
            else:
                st.error(f"Current Risk Level: **{current_risk}**")
        else:
            # Sample trend chart for demonstration
            dates = pd.date_range(start='2024-01-01', periods=6, freq='M')
            sample_data = [25, 30, 28, 32, 29, st.session_state.risk_percentage if st.session_state.assessment_completed else 30]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=dates, y=sample_data[:5], 
                                   mode='lines+markers',
                                   name='Past Trend',
                                   line=dict(color='lightgray', dash='dash')))
            if st.session_state.assessment_completed:
                fig.add_trace(go.Scatter(x=[dates[-1]], y=[sample_data[-1]], 
                                       mode='markers',
                                       name='Current',
                                       marker=dict(color='red', size=10)))
            
            fig.update_layout(title='Risk Level Over Time', 
                            xaxis_title='Date', 
                            yaxis_title='Risk Percentage (%)',
                            height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown(f'<div class="risk-medium"><h3>Risk Level Over Time</h3><p>Medium</p><p>Last 12 Months: -10%</p></div>', 
                       unsafe_allow_html=True)
        
        # Quick Actions
        st.markdown("### Quick Actions")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 New Assessment", use_container_width=True):
                st.session_state.current_page = "assessment"
                st.rerun()
        
        with col2:
            if st.button("📋 View Recommendations", use_container_width=True):
                st.session_state.current_page = "recommendations"
                st.rerun()
        
        with col3:
            if st.button("👤 Profile Settings", use_container_width=True):
                st.session_state.current_page = "profile"
                st.rerun()
    
    def render_profile_page(self):
        """Render user profile and settings page."""
        st.markdown('<div class="main-header">Profile Settings</div>', unsafe_allow_html=True)
        
        if st.session_state.user_data:
            st.markdown("### Your Information")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Age", f"{st.session_state.user_data.get('age', 'N/A')} years")
                st.metric("Height", f"{st.session_state.user_data.get('height', 'N/A')} cm")
                st.metric("BMI", f"{st.session_state.user_data.get('bmi', 0):.1f}")
            
            with col2:
                st.metric("Weight", f"{st.session_state.user_data.get('weight', 'N/A')} kg")
                st.metric("Sleep Hours", f"{st.session_state.user_data.get('sleep_hours', 'N/A')}")
                st.metric("Stress Level", st.session_state.user_data.get('stress_level', 'N/A'))
        
        st.markdown("### App Settings")
        
        # Notification settings
        notifications = st.checkbox("Enable Assessment Reminders", value=True)
        
        # Data export
        if st.button("📊 Export Assessment Data"):
            if st.session_state.assessment_history:
                df = pd.DataFrame(st.session_state.assessment_history)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="diabetes_risk_assessments.csv",
                    mime="text/csv"
                )
            else:
                st.warning("No assessment data to export.")
        
        # Reset data
        if st.button("🗑️ Clear All Data", type="secondary"):
            if st.button("Confirm Reset", type="secondary"):
                # Reset session state
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.success("All data cleared successfully!")
                st.rerun()
        
        # Navigation
        if st.button("← Back to Dashboard", use_container_width=True):
            st.session_state.current_page = "dashboard"
            st.rerun()
    
    def render_navigation(self):
        """Render the sidebar navigation menu."""
        with st.sidebar:
            st.markdown("## 🩺 Diabetes Risk Assessement App")
            st.markdown("---")
            
            # Navigation menu
            menu_items = {
                "🏠 Home": "welcome",
                "📝 Assessment": "assessment", 
                "📊 Results": "results",
                "💡 Recommendations": "recommendations",
                "📈 Dashboard": "dashboard",
                "👤 Profile": "profile"
            }
            
            for label, page in menu_items.items():
                if st.button(label, use_container_width=True, 
                           type="primary" if st.session_state.current_page == page else "secondary"):
                    st.session_state.current_page = page
                    st.rerun()
            
            st.markdown("---")
            
            # Show current risk level if assessment completed
            if st.session_state.assessment_completed:
                st.markdown("### Current Status")
                risk_level = st.session_state.risk_level
                risk_percentage = st.session_state.risk_percentage
                
                if "Low" in risk_level:
                    st.success(f"Risk: {risk_level}")
                elif "Medium" in risk_level:
                    st.warning(f"Risk: {risk_level}")
                else:
                    st.error(f"Risk: {risk_level}")
                
                st.metric("Risk Percentage", f"{risk_percentage}%")
    
    def run(self):
        """Main application runner."""
        # Render navigation
        self.render_navigation()
        
        # Render current page
        if st.session_state.current_page == "welcome":
            self.render_welcome_page()
        elif st.session_state.current_page == "assessment":
            self.render_assessment_page()
        elif st.session_state.current_page == "results":
            self.render_results_page()
        elif st.session_state.current_page == "recommendations":
            self.render_recommendations_page()
        elif st.session_state.current_page == "dashboard":
            self.render_dashboard_page()
        elif st.session_state.current_page == "profile":
            self.render_profile_page()

# Application entry point
if __name__ == "__main__":
    """
    Main entry point for the Diabetes Risk Assessment Application.
    
    This Streamlit app provides:
    1. Comprehensive risk assessment based on multiple health factors
    2. Personalized recommendations based on risk level
    3. Health tracking dashboard with trend analysis
    4. User profile management and data export capabilities
    
    To run this application:
    1. Save this code as 'diabetes_app.py'
    2. Install required packages: pip install streamlit plotly pandas numpy
    3. Run: streamlit run diabetes_app.py
    """
    
    # Initialize and run the application
    app = DiabetesRiskPredictor()
    app.run()