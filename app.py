import streamlit as st
from datetime import datetime, timedelta
import os

# =========================
# GOOGLE GEMINI (FIXED)
# =========================
AI_AVAILABLE = False
model = None

try:
    import google.generativeai as genai
    
    GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY", os.getenv("GOOGLE_API_KEY"))
    
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY not found")
    
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    AI_AVAILABLE = True

except Exception as e:
    AI_AVAILABLE = False
    print(f"❌ Gemini init error: {e}")

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
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    .metric-value {
        font-size: 32px;
        font-weight: bold;
    }
    .metric-label {
        font-size: 14px;
        opacity: 0.9;
    }
    .section-header {
        font-size: 24px;
        font-weight: 600;
        color: #1E88E5;
        margin: 20px 0 10px 0;
        border-left: 4px solid #1E88E5;
        padding-left: 15px;
    }
    .tip-box {
        background-color: #e3f2fd;
        border-left: 4px solid #1E88E5;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
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
    st.markdown('<span class="ai-badge">✨ Powered by Google Gemini AI</span>', unsafe_allow_html=True)
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
# AI FUNCTION (FIXED)
# =========================
def generate_ai_text(prompt: str) -> str | None:
    if not AI_AVAILABLE or model is None:
        return None
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"❌ AI error: {str(e)[:100]}")
        return None

# =========================
# FALLBACK CONTENT
# =========================
def get_fallback_content(content_type: str, destination: str, days: int = 3, budget: int = 500) -> str:
    per_day = budget // days
    
    fallbacks = {
        "recommendations": f"""
## 🎒 Budget Travel Tips for {destination}

### ✈️ Transportation
- Budget airlines (Ryanair, EasyJet, etc.)
- Book trains in advance for discounts
- Get multi-day transit passes

### 🏨 Accommodation
- **Hostels**: $15-40/night
- **Airbnb**: $30-60/night (shared)
- **Couchsurfing**: Free!

### 🍕 Budget Food
- Street food: $3-8/meal
- Local markets
- Supermarket meals
- Lunch specials

### 🎟️ Student Discounts
- Bring student ID everywhere!
- Museum free days
- ISIC card for international discounts
        """,
        
        "itinerary": f"""
## 📅 {days}-Day Itinerary for {destination}

### Day 1: Arrival
- Morning: Arrive, check-in
- Afternoon: Free walking tour
- Evening: Local market dinner
- **Cost: ~$40**

### Day 2: Culture
- Morning: Top attraction
- Afternoon: Museums
- Evening: Local restaurant
- **Cost: ~$50**

### Day 3+: Explore
- Mix of sights & hidden gems
- Day trips nearby
- Local experiences
- **Cost: ~$45/day**

**Total Estimate: ${days * 45}-${days * 65}**
        """,
        
        "safety": f"""
## 🛡️ Safety Tips for {destination}

### ⚠️ Common Scams
- Petition/charity scams
- Taxi overcharging
- Fake police

### 🚨 Emergency Prep
- Save embassy contact
- Keep document copies
- Get travel insurance

### 💡 General Tips
- Stay aware in crowds
- Use hotel safes
- Share itinerary with family
        """
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
        
        recommendations = generate_ai_text(f"""
You are a student travel expert. Give practical budget travel advice.

Trip: {origin} → {destination}
Duration: {days} days
Budget: ${budget} total (${per_day}/day)
Travelers: {travelers}
Style: {clean_style}
Interests: {", ".join(clean_interests)}
Student ID: {student_id}

Provide:
1. 🚂 Transportation options
2. 🏨 Budget accommodation
3. 📍 Must-visit places
4. 🍕 Cheap food spots
5. 🎟️ Student discounts
6. 💡 Money-saving tips

Use markdown with emojis.
""")
        progress.progress(50)

        status.text("📅 Creating itinerary...")
        itinerary = generate_ai_text(f"""
Create a {days}-day itinerary for {destination}.
Budget: ${per_day}/day
Interests: {", ".join(clean_interests)}

Format:
## Day X: Theme
### 🌅 Morning
### ☀️ Afternoon  
### 🌙 Evening
Daily cost estimate.
""")
        progress.progress(75)

        status.text("🛡️ Getting safety tips...")
        safety = generate_ai_text(f"""
Safety tips for students visiting {destination}:
- Common scams
- Transport safety
- Emergency contacts
- Night safety
- Health tips
""")
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
    
    st.markdown(f"**🗺️ Route:** {meta['origin']} → {meta['destination']}")
    st.divider()

    tab1, tab2, tab3 = st.tabs(["🤖 Recommendations", "🗓️ Itinerary", "🛡️ Safety"])

    with tab1:
        st.markdown(plan["recommendations"])
    with tab2:
        st.markdown(plan["itinerary"])
    with tab3:
        st.markdown(plan["safety"])
    
    st.divider()
    st.download_button(
        "📥 Download Plan",
        f"# Trip to {meta['destination']}\n\n{plan['recommendations']}\n\n{plan['itinerary']}\n\n{plan['safety']}",
        f"travel_plan_{meta['destination']}.md",
        use_container_width=True
    )

else:
    st.info("👈 Fill in your trip details and click **Generate AI Travel Plan**")

st.divider()
st.caption("🎒 AI Student Travel Planner | Streamlit + Google Gemini")
