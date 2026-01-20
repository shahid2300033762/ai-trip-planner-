import streamlit as st
from datetime import datetime, timedelta
import random
import os

# =========================
# LOAD ENVIRONMENT VARIABLES
# =========================
from dotenv import load_dotenv
load_dotenv()

# =========================
# GOOGLE GEMINI AI SETUP
# =========================
try:
    import google.generativeai as genai

    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY not found")

    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel("gemini-pro")
    AI_AVAILABLE = True
    print("✅ AI is connected!")

except Exception as e:
    AI_AVAILABLE = False
    print(f"❌ AI Error: {e}")

# =========================
# PAGE CONFIGURATION
# =========================
st.set_page_config(
    page_title="Student Travel Planner",
    page_icon="🎒",
    layout="wide"
)

# =========================
# CUSTOM STYLING
# =========================
st.markdown("""
<style>
.big-font {
    font-size: 50px !important;
    font-weight: bold;
    color: #1E88E5;
    text-align: center;
}
.ai-badge {
    background-color: #4CAF50;
    color: white;
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 14px;
    display: inline-block;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown('<p class="big-font">🎒 AI Student Travel Planner</p>', unsafe_allow_html=True)

if AI_AVAILABLE:
    st.markdown(
        '<div style="text-align:center;"><span class="ai-badge">✨ Powered by Google Gemini AI</span></div>',
        unsafe_allow_html=True
    )
else:
    st.warning("⚠️ AI is offline - using backup mode")

st.markdown("---")

# =========================
# SIDEBAR INPUT
# =========================
with st.sidebar:
    st.header("📝 Trip Details")

    origin = st.text_input("📍 From City", "New York")
    destination = st.text_input("🌍 To City", "Paris")

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime.now() + timedelta(days=7))
    with col2:
        end_date = st.date_input("End Date", datetime.now() + timedelta(days=14))

    budget = st.slider("💰 Total Budget (USD)", 100, 5000, 1000, 50)

    st.subheader("Preferences")

    travel_style = st.selectbox(
        "Travel Style",
        ["Budget Backpacker", "Balanced", "Comfort Seeker"]
    )

    interests = st.multiselect(
        "Your Interests",
        ["Museums", "Food", "Nature", "Nightlife", "Culture", "Adventure", "Shopping", "History"],
        default=["Culture", "Food"]
    )

    num_travelers = st.number_input("Number of Travelers", 1, 10, 1)

    st.markdown("---")
    generate_btn = st.button("🚀 Generate AI Travel Plan", type="primary", use_container_width=True)

# =========================
# AI FUNCTIONS
# =========================
def get_ai_recommendations(destination, origin, days, budget, interests, travel_style):
    if not AI_AVAILABLE:
        return None

    prompt = f"""
You are a student travel expert. Create a budget-friendly travel plan.

Destination: {destination}
From: {origin}
Duration: {days} days
Budget: ${budget}
Travel Style: {travel_style}
Interests: {', '.join(interests)}

Include:
1. Transportation options with prices
2. Accommodation options
3. Must-visit places
4. Budget food
5. Money-saving tips
6. Student discounts
"""
    return model.generate_content(prompt).text


def get_ai_itinerary(destination, days, interests, budget_per_day):
    if not AI_AVAILABLE:
        return None

    prompt = f"""
Create a {days}-day itinerary for {destination}.

Daily Budget: ${budget_per_day}
Interests: {', '.join(interests)}

For each day include:
- Morning
- Lunch
- Afternoon
- Evening
- Daily total cost
"""
    return model.generate_content(prompt).text


def get_ai_safety_tips(destination):
    if not AI_AVAILABLE:
        return None

    prompt = f"""
Provide safety tips for students traveling to {destination}.
Include scams, health, emergency numbers, transport safety, and etiquette.
"""
    return model.generate_content(prompt).text

# =========================
# MAIN LOGIC
# =========================
if generate_btn:
    days = (end_date - start_date).days

    if days <= 0:
        st.error("❌ End date must be after start date")
    else:
        budget_per_day = budget // days

        with st.spinner("🤖 Generating your AI travel plan..."):
            ai_recommendations = get_ai_recommendations(
                destination, origin, days, budget, interests, travel_style
            )
            ai_itinerary = get_ai_itinerary(
                destination, days, interests, budget_per_day
            )
            ai_safety = get_ai_safety_tips(destination)

        st.success("✅ Your travel plan is ready!")

        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Overview",
            "🤖 AI Recommendations",
            "🗓️ Itinerary",
            "🛡️ Safety"
        ])

        with tab1:
            st.metric("Duration", f"{days} days")
            st.metric("Budget", f"${budget}")
            st.metric("Budget / Day", f"${budget_per_day}")
            st.write(f"**Route:** {origin} → {destination}")
            st.write(f"**Interests:** {', '.join(interests)}")

        with tab2:
            if ai_recommendations:
                st.markdown(ai_recommendations)

        with tab3:
            if ai_itinerary:
                st.markdown(ai_itinerary)

        with tab4:
            if ai_safety:
                st.markdown(ai_safety)

else:
    st.info("👈 Fill details in the sidebar and click **Generate AI Travel Plan**")
