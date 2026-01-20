import streamlit as st
from datetime import datetime, timedelta
import os

# =========================
# GOOGLE GEMINI (NEW SDK)
# =========================
AI_AVAILABLE = False
client = None
MODEL_NAME = "gemini-1.5-flash"

try:
    from google import genai

    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY not found")

    client = genai.Client(api_key=GOOGLE_API_KEY)
    AI_AVAILABLE = True
    print("✅ Gemini AI connected")

except Exception as e:
    AI_AVAILABLE = False
    print(f"❌ Gemini init error: {e}")

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AI Student Travel Planner",
    page_icon="🎒",
    layout="wide"
)

# =========================
# STYLES
# =========================
st.markdown("""
<style>
.big-font {
    font-size: 46px;
    font-weight: bold;
    color: #1E88E5;
}
.ai-badge {
    background-color: #2e7d32;
    color: white;
    padding: 6px 14px;
    border-radius: 18px;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown('<div class="big-font">🎒 AI Student Travel Planner</div>', unsafe_allow_html=True)

if AI_AVAILABLE:
    st.markdown('<span class="ai-badge">✨ Powered by Google Gemini AI</span>', unsafe_allow_html=True)
else:
    st.warning("⚠️ AI unavailable – using fallback mode")

st.divider()

# =========================
# SIDEBAR INPUTS
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

    travel_style = st.selectbox(
        "Travel Style",
        ["Budget Backpacker", "Balanced", "Comfort Seeker"]
    )

    interests = st.multiselect(
        "Interests",
        ["Culture", "Food", "History", "Nature", "Nightlife", "Shopping"],
        default=["Culture", "Food"]
    )

    travelers = st.number_input("Number of Travelers", 1, 10, 1)

    st.divider()
    generate = st.button("🚀 Generate AI Travel Plan", use_container_width=True)

# =========================
# AI HELPERS
# =========================
def generate_ai_text(prompt: str) -> str | None:
    if not AI_AVAILABLE:
        return None
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        return response.text
    except Exception as e:
        st.error("❌ AI request failed. Falling back to sample data.")
        print(e)
        return None

# =========================
# MAIN LOGIC
# =========================
if generate:
    days = (end_date - start_date).days

    if days <= 0:
        st.error("End date must be after start date.")
    else:
        per_day = budget // days

        with st.spinner("🤖 Generating your travel plan..."):
            recommendations = generate_ai_text(f"""
You are a student travel expert.

Destination: {destination}
From: {origin}
Duration: {days} days
Budget: ${budget}
Travel style: {travel_style}
Interests: {", ".join(interests)}

Give:
• Transport options
• Accommodation
• Must-visit places
• Budget food
• Student discounts
""")

            itinerary = generate_ai_text(f"""
Create a {days}-day student itinerary for {destination}.
Daily budget: ${per_day}
Interests: {", ".join(interests)}
""")

            safety = generate_ai_text(f"""
Give safety tips for students visiting {destination}.
Include scams, transport safety, emergency tips.
""")

        st.success("✅ Your travel plan is ready!")

        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Overview",
            "🤖 AI Recommendations",
            "🗓️ Itinerary",
            "🛡️ Safety"
        ])

        with tab1:
            st.metric("Duration", f"{days} days")
            st.metric("Total Budget", f"${budget}")
            st.metric("Budget / Day", f"${per_day}")
            st.write(f"**Route:** {origin} → {destination}")
            st.write(f"**Interests:** {', '.join(interests)}")

        with tab2:
            if recommendations:
                st.markdown(recommendations)
            else:
                st.info("Sample: Budget airlines, hostels, free walking tours.")

        with tab3:
            if itinerary:
                st.markdown(itinerary)
            else:
                st.info("Sample itinerary: museums, cafes, local markets.")

        with tab4:
            if safety:
                st.markdown(safety)
            else:
                st.info("Sample safety tips: avoid scams, keep documents safe.")

else:
    st.info("👈 Fill details in the sidebar and click **Generate AI Travel Plan**")
