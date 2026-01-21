import streamlit as st
from datetime import datetime, timedelta
import os

# =========================
# GOOGLE GEMINI - DISCOVERY MODE
# =========================
@st.cache_resource
def setup_genai():
    """Discovers available models to prevent 404 errors."""
    available_model = None
    is_ready = False
    
    try:
        import google.generativeai as genai
        
        # Get API Key from secrets or environment
        api_key = st.secrets.get("GOOGLE_API_KEY", os.getenv("GOOGLE_API_KEY"))
        if not api_key:
            return None, False

        genai.configure(api_key=api_key)

        # 1. DISCOVERY: Get models actually available to your API Key
        supported_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # 2. SELECTION: Prioritize the best available models
        priority_list = [
            'models/gemini-1.5-flash-latest',
            'models/gemini-1.5-flash',
            'models/gemini-1.5-pro-latest',
            'models/gemini-pro'
        ]
        
        target_model_name = None
        for priority in priority_list:
            if priority in supported_models:
                target_model_name = priority
                break
        
        # Fallback to the first available if priority list fails
        if not target_model_name and supported_models:
            target_model_name = supported_models[0]

        if target_model_name:
            available_model = genai.GenerativeModel(target_model_name)
            # Test ping to ensure the key is active
            available_model.generate_content("Hi", generation_config={"max_output_tokens": 1})
            is_ready = True
            
        return available_model, is_ready

    except Exception as e:
        print(f"Discovery Error: {e}")
        return None, False

# Initialize AI
model, AI_AVAILABLE = setup_genai()

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AI Student Travel Planner",
    page_icon="🎒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# STYLES
# =========================
st.markdown("""
<style>
    .big-font {
        font-size: 48px;
        font-weight: bold;
        background: linear-gradient(90deg, #1E88E5, #7C4DFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    .ai-badge {
        background: linear-gradient(90deg, #2e7d32, #43a047);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: 500;
        display: inline-block;
        margin-bottom: 20px;
    }
    .offline-badge {
        background: linear-gradient(90deg, #f44336, #e91e63);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: 500;
        display: inline-block;
        margin-bottom: 20px;
    }
    .section-header {
        font-size: 24px;
        font-weight: 600;
        color: #1E88E5;
        margin: 20px 0 10px 0;
        border-left: 4px solid #1E88E5;
        padding-left: 15px;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE
# =========================
if 'travel_plan' not in st.session_state:
    st.session_state.travel_plan = None
if 'plan_generated' not in st.session_state:
    st.session_state.plan_generated = False

# =========================
# HEADER
# =========================
st.markdown('<div class="big-font">🎒 AI Student Travel Planner</div>', unsafe_allow_html=True)

if AI_AVAILABLE:
    st.markdown(f'<span class="ai-badge">✨ Powered by {model.model_name}</span>', unsafe_allow_html=True)
else:
    st.markdown('<span class="offline-badge">⚠️ AI Offline - Demo Mode</span>', unsafe_allow_html=True)

st.caption("Plan budget-friendly adventures with AI-powered recommendations tailored for students!")
st.divider()

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.header("📝 Trip Details")
    
    origin = st.text_input("📍 Departure City", "New York")
    destination = st.text_input("🌍 Destination City", "Paris")

    st.subheader("📅 Travel Dates")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start", datetime.now() + timedelta(days=7))
    with col2:
        end_date = st.date_input("End", datetime.now() + timedelta(days=14))

    st.subheader("💰 Budget")
    budget = st.slider("Total Budget (USD)", 100, 5000, 1000, 50)
    
    days = (end_date - start_date).days if end_date > start_date else 1
    daily_budget = budget // days
    st.info(f"💵 ${daily_budget}/day")

    st.subheader("🎯 Preferences")
    travel_style = st.selectbox(
        "Travel Style",
        ["🎒 Budget Backpacker", "⚖️ Balanced Explorer", "✨ Comfort Seeker"]
    )

    interests = st.multiselect(
        "Interests",
        ["🏛️ Culture", "🍕 Food", "📜 History", "🌲 Nature", 
         "🎉 Nightlife", "🛍️ Shopping", "🎨 Art", "⚽ Sports"],
        default=["🏛️ Culture", "🍕 Food"]
    )

    travelers = st.number_input("👥 Travelers", 1, 10, 1)

    with st.expander("⚙️ More Options"):
        dietary = st.multiselect("Dietary", ["Vegetarian", "Vegan", "Halal", "Kosher", "Gluten-Free"])
        student_id = st.checkbox("🎓 Have student ID", value=True)

    st.divider()
    generate = st.button("🚀 Generate AI Travel Plan", use_container_width=True, type="primary")
    
    if st.session_state.plan_generated:
        if st.button("🔄 Start New Plan", use_container_width=True):
            st.session_state.travel_plan = None
            st.session_state.plan_generated = False
            st.rerun()

# =========================
# AI FUNCTION
# =========================
def generate_ai_text(prompt: str) -> str | None:
    if not AI_AVAILABLE or model is None:
        return None
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # Log to console rather than UI to keep it clean
        print(f"AI error: {e}")
        return None

# =========================
# FALLBACK CONTENT
# =========================
def get_fallback_content(content_type: str, destination: str, days: int = 3, budget: int = 500) -> str:
    per_day = budget // days
    fallbacks = {
        "recommendations": f"## 🎒 Budget Travel Tips for {destination}\n- Use student ID for discounts.\n- Opt for hostels or shared Airbnbs.",
        "itinerary": f"## 📅 {days}-Day Itinerary for {destination}\n- Day 1: City Walk & Local Food.\n- Day 2: Major landmarks.\n- Day 3: Local markets.",
        "safety": f"## 🛡️ Safety Tips for {destination}\n- Stay aware of surroundings.\n- Keep digital copies of documents."
    }
    return fallbacks.get(content_type, "Content unavailable")

# =========================
# MAIN LOGIC
# =========================
if generate:
    days = (end_date - start_date).days

    if days <= 0:
        st.error("❌ End date must be after start date.")
    elif not destination.strip():
        st.error("❌ Please enter a destination.")
    elif not interests:
        st.warning("⚠️ Please select at least one interest.")
    else:
        per_day = budget // days
        clean_interests = [i.split(' ', 1)[-1] for i in interests]
        clean_style = travel_style.split(' ', 1)[-1]

        progress = st.progress(0)
        status = st.empty()

        status.text("🔍 Getting recommendations...")
        progress.progress(20)
        
        recommendations = generate_ai_text(f"Student travel expert: Provide transport, budget stay, and food for {destination} on ${per_day}/day.")
        progress.progress(50)

        status.text("📅 Creating itinerary...")
        itinerary = generate_ai_text(f"Create a {days}-day itinerary for {destination} with interests: {clean_interests}.")
        progress.progress(75)

        status.text("🛡️ Getting safety tips...")
        safety = generate_ai_text(f"Safety and scam tips for students in {destination}.")
        progress.progress(100)
        
        status.empty()
        progress.empty()

        st.session_state.travel_plan = {
            "recommendations": recommendations or get_fallback_content("recommendations", destination, days, budget),
            "itinerary": itinerary or get_fallback_content("itinerary", destination, days, budget),
            "safety": safety or get_fallback_content("safety", destination, days, budget),
            "meta": {
                "origin": origin, "destination": destination,
                "days": days, "budget": budget, "per_day": per_day,
                "style": travel_style, "interests": interests, "travelers": travelers
            }
        }
        st.session_state.plan_generated = True

# =========================
# DISPLAY RESULTS
# =========================
if st.session_state.plan_generated and st.session_state.travel_plan:
    plan = st.session_state.travel_plan
    meta = plan["meta"]
    
    st.success("✅ Your travel plan is ready!")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📅 Days", meta['days'])
    col2.metric("💰 Budget", f"${meta['budget']}")
    col3.metric("💵 Per Day", f"${meta['per_day']}")
    col4.metric("👥 Travelers", meta['travelers'])
    
    tab1, tab2, tab3 = st.tabs(["🤖 Recommendations", "🗓️ Itinerary", "🛡️ Safety"])

    with tab1:
        st.markdown(plan["recommendations"])
    with tab2:
        st.markdown(plan["itinerary"])
    with tab3:
        st.markdown(plan["safety"])
    
    st.download_button("📥 Download MD Plan", f"# {meta['destination']} Plan\n{plan['itinerary']}", "plan.md")
else:
    st.info("👈 Fill in details and click **Generate AI Travel Plan**")
