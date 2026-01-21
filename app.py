import streamlit as st
from datetime import datetime, timedelta
import os

# =========================
# GOOGLE GEMINI (FIXED SDK)
# =========================
AI_AVAILABLE = False
model = None

try:
    import google.generativeai as genai
    
    # For Streamlit Cloud, use st.secrets
    GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY", os.getenv("GOOGLE_API_KEY"))
    
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY not found")
    
    genai.configure(api_key=GOOGLE_API_KEY)
    
    # Use the correct model
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Test the connection
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
# ENHANCED STYLES
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
# INITIALIZE SESSION STATE
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
# SIDEBAR INPUTS
# =========================
with st.sidebar:
    st.header("📝 Trip Details")
    st.caption("Fill in your travel preferences")

    origin = st.text_input("📍 Departure City", "New York", help="Where are you traveling from?")
    destination = st.text_input("🌍 Destination City", "Paris", help="Where do you want to go?")

    st.subheader("📅 Travel Dates")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "Start Date",
            datetime.now() + timedelta(days=7),
            min_value=datetime.now()
        )
    with col2:
        end_date = st.date_input(
            "End Date",
            datetime.now() + timedelta(days=14),
            min_value=start_date + timedelta(days=1) if start_date else datetime.now()
        )

    st.subheader("💰 Budget")
    budget = st.slider(
        "Total Budget (USD)",
        min_value=100,
        max_value=5000,
        value=1000,
        step=50,
        help="Drag to set your total trip budget"
    )
    
    days = (end_date - start_date).days if end_date > start_date else 1
    daily_budget = budget // days
    
    if daily_budget < 50:
        st.warning(f"💡 ${daily_budget}/day - Very tight budget!")
    elif daily_budget < 100:
        st.info(f"💰 ${daily_budget}/day - Budget traveler")
    else:
        st.success(f"💎 ${daily_budget}/day - Comfortable budget")

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

    travelers = st.number_input("👥 Number of Travelers", min_value=1, max_value=10, value=1)

    with st.expander("⚙️ Additional Options"):
        dietary = st.multiselect(
            "Dietary Restrictions",
            ["Vegetarian", "Vegan", "Halal", "Kosher", "Gluten-Free"],
            default=[]
        )
        accessibility = st.checkbox("♿ Accessibility needs")
        student_id = st.checkbox("🎓 Have student ID (for discounts)", value=True)

    st.divider()
    
    generate = st.button(
        "🚀 Generate AI Travel Plan",
        use_container_width=True,
        type="primary"
    )
    
    if st.session_state.plan_generated:
        if st.button("🔄 Start New Plan", use_container_width=True):
            st.session_state.travel_plan = None
            st.session_state.plan_generated = False
            st.rerun()

# =========================
# AI HELPERS
# =========================
def generate_ai_text(prompt: str) -> str | None:
    """Generate AI text using Gemini."""
    if not AI_AVAILABLE:
        return None
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        return response.text
    except Exception as e:
        st.error(f"❌ AI request failed: {str(e)[:100]}")
        return None

def get_fallback_content(content_type: str, destination: str, days: int = 3, budget: int = 500) -> str:
    """Provide fallback content when AI is unavailable."""
    per_day = budget // days
    
    fallbacks = {
        "recommendations": f"""
## 🎒 Budget Travel Tips for {destination}

### ✈️ Transportation Options
- **Budget Airlines**: Look for Ryanair, EasyJet, Norwegian, or similar low-cost carriers
- **Trains**: Book in advance for up to 50% off on rail passes
- **Buses**: FlixBus and similar services for intercity travel
- **Local Transit**: Get multi-day passes for public transportation

### 🏨 Accommodation Recommendations
- **Hostels**: $15-40/night - Great for meeting other travelers
- **Airbnb**: $30-60/night - Look for shared apartments
- **Couchsurfing**: Free! Great cultural exchange
- **Student Housing**: Check university dorms during summer

### 📍 Must-Visit Places
- Main historical/cultural attractions
- Free walking tour (tip-based)
- Local markets and neighborhoods
- Parks and public spaces

### 🍕 Budget Food Guide
- **Street Food**: $3-8 per meal
- **Local Markets**: Fresh produce and local specialties
- **Supermarkets**: Prepare your own meals
- **Lunch Specials**: Many restaurants offer deals

### 🎟️ Student Discounts
- Bring your student ID everywhere!
- ISIC card for international discounts
- Museum free days (often first Sunday)
- Youth hostel memberships

### 💡 Money-Saving Hacks
- Travel during shoulder season
- Book attractions online in advance
- Use free WiFi instead of data roaming
- Carry a reusable water bottle
        """,
        
        "itinerary": f"""
## 📅 {days}-Day Itinerary for {destination}

---

### Day 1: Arrival & Orientation
**Daily Budget: ${per_day}**

#### 🌅 Morning (9:00-12:00)
- Arrive and check into accommodation
- Get oriented with a neighborhood walk
- Pick up local SIM card/transit pass
- *Cost: $10-20 (transit pass)*

#### ☀️ Afternoon (12:00-18:00)
- Join a FREE walking tour (tip-based)
- Explore the main square/downtown area
- Coffee break at a local café
- *Cost: $10-15 (tour tip + coffee)*

#### 🌙 Evening (18:00-22:00)
- Visit a local market for dinner
- Evening stroll through historic area
- Early night to recover from travel
- *Cost: $10-15 (dinner)*

**Day 1 Total: ~$30-50**

---

### Day 2: Culture & Landmarks
**Daily Budget: ${per_day}**

#### 🌅 Morning (9:00-12:00)
- Visit top attraction (use student discount!)
- Take photos and explore thoroughly
- *Cost: $8-15 (discounted entry)*

#### ☀️ Afternoon (12:00-18:00)
- Lunch at a budget-friendly local spot
- Explore museum or cultural site
- Wander through artsy neighborhood
- *Cost: $15-25 (lunch + museum)*

#### 🌙 Evening (18:00-22:00)
- Sunset at a scenic viewpoint
- Dinner at recommended local restaurant
- Optional: bar hopping with hostel friends
- *Cost: $15-25 (dinner + drinks)*

**Day 2 Total: ~$40-65**

---

### Day 3+: Explore & Discover
**Daily Budget: ${per_day}**

#### 🌅 Morning
- Day trip to nearby attraction OR
- Visit remaining must-see spots
- *Cost: $10-30*

#### ☀️ Afternoon
- Shopping at local markets
- Try regional specialty foods
- *Cost: $20-35*

#### 🌙 Evening
- Farewell dinner at favorite spot
- Pack and prepare for departure
- *Cost: $15-25*

**Day 3 Total: ~$45-90**

---

## 💰 Budget Summary
- **Accommodation**: ${int(days * 25)}-${int(days * 40)} ({days} nights)
- **Food**: ${int(days * 25)}-${int(days * 35)}
- **Activities**: ${int(days * 15)}-${int(days * 25)}
- **Transport**: $20-50
- **Buffer**: $30-50

**Estimated Total: ${int(days * 65)}-${int(days * 100)}**
        """,
        
        "safety": f"""
## 🛡️ Safety Guide for {destination}

### ⚠️ Common Scams to Avoid
- **Petition Scams**: People asking you to sign petitions, then demanding money
- **Friendship Bracelet**: Someone ties a bracelet on your wrist, demands payment
- **Fake Police**: Always ask for official ID; real police won't ask for your wallet
- **Taxi Overcharging**: Use ride apps or agree on price beforehand
- **"Free" Gifts**: Nothing is free - politely decline and walk away
- **Distraction Theft**: One person distracts while another pickpockets

### 🚇 Transportation Safety
- Keep bags in front of you on public transit
- Avoid empty train cars late at night
- Use official taxi stands or ride-sharing apps
- Don't accept rides from unmarked vehicles
- Keep a hand on your belongings at all times

### 📍 Areas & Times to Be Careful
- Tourist hotspots (prime pickpocket areas)
- Train stations and airports
- ATM areas (especially at night)
- Avoid poorly lit streets after dark
- Be extra cautious on weekends/holidays

### 🆘 Emergency Information
- **EU Emergency**: 112
- **Police**: Contact local authorities
- **Embassy**: Save your country's embassy contact
- **Travel Insurance**: ALWAYS have it - keep policy number handy

### 🏥 Health Tips
- Check if tap water is safe to drink
- Bring basic medications from home
- Locate nearest pharmacy and hospital
- Keep prescription meds in original packaging
- EU Health Insurance Card (for EU citizens)

### 📱 Digital Safety
- Use VPN on public WiFi
- Don't access banking on public networks
- Keep phone charged (portable battery!)
- Share location with trusted contact
- Back up important documents to cloud

### 🌙 Night Safety Tips
- Stick to well-lit, busy areas
- Travel in groups when possible
- Share your location with friends
- Trust your instincts - if it feels wrong, leave
- Have your accommodation address saved offline

### 💡 General Tips
- Make copies of passport & important docs
- Keep emergency cash separate from wallet
- Learn a few local phrases
- Dress to blend in (avoid looking too touristy)
- Be confident - scammers target confused tourists
        """
    }
    return fallbacks.get(content_type, "Content unavailable")

# =========================
# MAIN LOGIC
# =========================
if generate:
    days = (end_date - start_date).days

    if days <= 0:
        st.error("❌ End date must be after start date. Please adjust your dates.")
    elif not destination.strip():
        st.error("❌ Please enter a destination city.")
    elif not interests:
        st.warning("⚠️ Please select at least one interest.")
    else:
        per_day = budget // days
        clean_interests = [i.split(' ', 1)[-1] for i in interests]
        clean_style = travel_style.split(' ', 1)[-1]

        progress_bar = st.progress(0)
        status_text = st.empty()

        # Step 1: Recommendations
        status_text.text("🔍 Analyzing destination...")
        progress_bar.progress(10)
        
        recommendations = generate_ai_text(f"""
You are an expert student travel advisor. Create detailed, practical recommendations.

**Trip Details:**
- From: {origin} → To: {destination}
- Duration: {days} days
- Total Budget: ${budget} (${per_day}/day)
- Travelers: {travelers}
- Style: {clean_style}
- Interests: {", ".join(clean_interests)}
- Has Student ID: {student_id}
- Dietary: {", ".join(dietary) if dietary else "None"}

**Provide detailed sections for:**
1. 🚂 **Transportation** - Cheapest ways to get there & around
2. 🏨 **Accommodation** - Budget-friendly options with price ranges
3. 📍 **Must-Visit Places** - Top attractions matching interests
4. 🍕 **Budget Food** - Where to eat cheap & delicious
5. 🎟️ **Student Discounts** - Specific discounts available
6. 💡 **Money-Saving Hacks** - Insider tips

Use markdown formatting with headers, bullet points, and emojis.
""")
        progress_bar.progress(40)

        # Step 2: Itinerary
        status_text.text("📅 Creating your itinerary...")
        
        itinerary = generate_ai_text(f"""
Create a detailed {days}-day itinerary for {destination}.

**Parameters:**
- Daily budget: ${per_day}
- Interests: {", ".join(clean_interests)}
- Travel style: {clean_style}
- Travelers: {travelers}

**Format each day as:**
## Day X: [Theme]
### 🌅 Morning (9:00-12:00)
- Activity with location
- Estimated cost: $X

### ☀️ Afternoon (12:00-18:00)
- Activity with location
- Estimated cost: $X

### 🌙 Evening (18:00-22:00)
- Activity with location
- Estimated cost: $X

**Daily Total: $X**

Include walking times between locations and practical tips.
""")
        progress_bar.progress(70)

        # Step 3: Safety
        status_text.text("🛡️ Gathering safety information...")
        
        safety = generate_ai_text(f"""
Provide comprehensive safety information for students visiting {destination}.

**Include:**
1. ⚠️ **Common Scams** - Specific to this destination
2. 🚇 **Transportation Safety** - Public transit tips
3. 📍 **Areas to Avoid** - Neighborhoods, times
4. 🆘 **Emergency Contacts** - Local numbers
5. 🏥 **Health Tips** - Vaccinations, water safety
6. 📱 **Digital Safety** - WiFi, cards
7. 🌙 **Night Safety** - For solo and group travelers

Be specific to {destination} with practical, actionable advice.
""")
        progress_bar.progress(100)

        status_text.empty()
        progress_bar.empty()

        # Store in session state
        st.session_state.travel_plan = {
            "recommendations": recommendations or get_fallback_content("recommendations", destination, days, budget),
            "itinerary": itinerary or get_fallback_content("itinerary", destination, days, budget),
            "safety": safety or get_fallback_content("safety", destination, days, budget),
            "meta": {
                "origin": origin,
                "destination": destination,
                "days": days,
                "budget": budget,
                "per_day": per_day,
                "style": travel_style,
                "interests": interests,
                "travelers": travelers
            }
        }
        st.session_state.plan_generated = True

# =========================
# DISPLAY RESULTS
# =========================
if st.session_state.plan_generated and st.session_state.travel_plan:
    plan = st.session_state.travel_plan
    meta = plan["meta"]
    
    st.success("✅ Your personalized travel plan is ready!")
    
    st.markdown('<div class="section-header">📊 Trip Overview</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{meta['days']}</div>
            <div class="metric-label">Days</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <div class="metric-value">${meta['budget']}</div>
            <div class="metric-label">Total Budget</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
            <div class="metric-value">${meta['per_day']}</div>
            <div class="metric-label">Per Day</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
            <div class="metric-value">{meta['travelers']}</div>
            <div class="metric-label">Travelers</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f"**🗺️ Route:** {meta['origin']} → {meta['destination']}")
    st.markdown(f"**🎯 Interests:** {', '.join(meta['interests'])}")
    
    st.divider()

    tab1, tab2, tab3 = st.tabs([
        "🤖 AI Recommendations",
        "🗓️ Daily Itinerary", 
        "🛡️ Safety Guide"
    ])

    with tab1:
        st.markdown(plan["recommendations"])

    with tab2:
        st.markdown(plan["itinerary"])

    with tab3:
        st.markdown(plan["safety"])
    
    st.divider()
    col_dl1, col_dl2, col_dl3 = st.columns([1, 2, 1])
    with col_dl2:
        full_plan = f"""
# 🎒 Travel Plan: {meta['origin']} → {meta['destination']}
## Generated on {datetime.now().strftime('%Y-%m-%d')}

---

# Overview
- **Duration:** {meta['days']} days
- **Budget:** ${meta['budget']} total (${meta['per_day']}/day)
- **Travelers:** {meta['travelers']}
- **Style:** {meta['style']}
- **Interests:** {', '.join(meta['interests'])}

---

{plan['recommendations']}

---

{plan['itinerary']}

---

{plan['safety']}
        """
        
        st.download_button(
            label="📥 Download Full Travel Plan",
            data=full_plan,
            file_name=f"travel_plan_{meta['destination'].lower().replace(' ', '_')}.md",
            mime="text/markdown",
            use_container_width=True
        )

else:
    # Welcome screen
    st.markdown("""
    <div class="tip-box">
        <h3>👋 Welcome, Student Traveler!</h3>
        <p>This AI-powered planner creates personalized, budget-friendly travel itineraries just for you.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🎯 Personalized
        AI recommendations based on YOUR interests, budget, and travel style.
        """)
    
    with col2:
        st.markdown("""
        ### 💰 Budget-Friendly
        Focused on student budgets with tips for discounts and savings.
        """)
    
    with col3:
        st.markdown("""
        ### 🛡️ Safe Travels
        Local safety tips and scam awareness for solo student travelers.
        """)
    
    st.info("👈 **Get Started:** Fill in your trip details in the sidebar and click **Generate AI Travel Plan**")

# =========================
# FOOTER
# =========================
st.divider()
st.caption("🎒 AI Student Travel Planner | Built with Streamlit & Google Gemini")
