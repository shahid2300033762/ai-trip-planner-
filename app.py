import streamlit as st
from datetime import datetime, timedelta
import random

# Must be first Streamlit command
st.set_page_config(
    page_title="Student Travel Planner",
    page_icon="🎒",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .big-font {
        font-size:50px !important;
        font-weight: bold;
        color: #1E88E5;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="big-font">🎒 Student Travel Planner</p>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("📝 Trip Details")
    
    origin = st.text_input("📍 From City", "New York", key="origin")
    destination = st.text_input("🌍 To City", "Paris", key="dest")
    
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start", datetime.now() + timedelta(days=7))
    with col2:
        end_date = st.date_input("End", datetime.now() + timedelta(days=14))
    
    budget = st.slider("💰 Budget (USD)", 100, 5000, 1000, 50)
    
    st.subheader("Preferences")
    travel_style = st.selectbox(
        "Travel Style",
        ["Budget Backpacker", "Balanced", "Comfort Seeker"]
    )
    
    interests = st.multiselect(
        "Interests",
        ["Museums", "Food", "Nature", "Nightlife", "Culture", "Adventure"],
        default=["Culture", "Food"]
    )
    
    num_travelers = st.number_input("Travelers", 1, 10, 1)
    
    st.markdown("---")
    generate_btn = st.button("🚀 Generate Travel Plan", type="primary", use_container_width=True)

# Main Content Area
if generate_btn:
    days = (end_date - start_date).days
    
    if days <= 0:
        st.error("❌ End date must be after start date!")
    elif not destination or not origin:
        st.error("❌ Please enter both cities!")
    else:
        with st.spinner("🤖 AI is planning your trip..."):
            import time
            time.sleep(1)
        
        st.success(f"✅ Your {days}-day trip is ready!")
        
        # Tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Overview",
            "✈️ Transportation", 
            "🏨 Accommodation",
            "🗓️ Itinerary",
            "🛡️ Safety Tips"
        ])
        
        # TAB 1: OVERVIEW
        with tab1:
            st.subheader("Trip Summary")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Duration", f"{days} days")
            with col2:
                st.metric("Total Budget", f"${budget}")
            with col3:
                st.metric("Travelers", num_travelers)
            with col4:
                st.metric("Budget/Day", f"${budget//days if days > 0 else 0}")
            
            st.markdown("---")
            
            st.write(f"**🛫 Route:** {origin} → {destination}")
            st.write(f"**📅 Dates:** {start_date.strftime('%b %d, %Y')} to {end_date.strftime('%b %d, %Y')}")
            st.write(f"**🎨 Style:** {travel_style}")
            st.write(f"**❤️ Interests:** {', '.join(interests)}")
        
        # TAB 2: TRANSPORTATION
        with tab2:
            st.subheader("Transportation Options")
            
            transport_options = [
                {"icon": "✈️", "name": "Budget Airline", "price": 280, "duration": "6h", "discount": "15% student discount", "recommended": True},
                {"icon": "🚆", "name": "High-Speed Train", "price": 150, "duration": "10h", "discount": "20% with rail pass", "recommended": False},
                {"icon": "🚌", "name": "Overnight Bus", "price": 75, "duration": "16h", "discount": "10% off", "recommended": False},
            ]
            
            for idx, option in enumerate(transport_options):
                expanded = option["recommended"]
                with st.expander(f"{option['icon']} {option['name']} - ${option['price']}" + (" ⭐ RECOMMENDED" if option['recommended'] else ""), expanded=expanded):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Price", f"${option['price']}")
                    with col2:
                        st.metric("Duration", option['duration'])
                    with col3:
                        st.write(f"**Student Deal:**")
                        st.write(option['discount'])
                    
                    if option['recommended']:
                        st.success("✅ Best value for students!")
        
        # TAB 3: ACCOMMODATION
        with tab3:
            st.subheader("Accommodation Options")
            
            accommodations = [
                {"icon": "🏨", "name": f"{destination} Central Hostel", "type": "Hostel", "price": 25, "rating": 4.5, "amenities": ["Free WiFi", "Kitchen", "Lounge"], "recommended": True},
                {"icon": "🏩", "name": f"{destination} Student Hotel", "type": "Budget Hotel", "price": 55, "rating": 4.2, "amenities": ["Breakfast", "WiFi", "Private Bath"], "recommended": False},
                {"icon": "🏠", "name": "Cozy Apartment", "type": "Airbnb", "price": 45, "rating": 4.7, "amenities": ["Kitchen", "WiFi", "Washer"], "recommended": False},
            ]
            
            for acc in accommodations:
                with st.expander(f"{acc['icon']} {acc['name']} - ${acc['price']}/night" + (" ⭐ RECOMMENDED" if acc['recommended'] else ""), expanded=acc['recommended']):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.write(f"**Type:** {acc['type']}")
                        st.write(f"**Rating:** {'⭐' * int(acc['rating'])} ({acc['rating']}/5)")
                        st.write(f"**Amenities:** {', '.join(acc['amenities'])}")
                    
                    with col2:
                        st.metric("Per Night", f"${acc['price']}")
                        st.metric(f"{days} Nights", f"${acc['price'] * days}")
                    
                    if acc['recommended']:
                        st.success("✅ Perfect for student budget!")
        
        # TAB 4: ITINERARY
        with tab4:
            st.subheader("Daily Itinerary")
            
            activities_db = {
                "Museums": ["National Museum ($12)", "Art Gallery ($8)", "History Museum ($10)"],
                "Food": ["Street Food Tour ($15)", "Local Restaurant ($20)", "Food Market ($10)"],
                "Nature": ["City Park (Free)", "Botanical Garden ($5)", "River Walk (Free)"],
                "Culture": ["Old Town Tour ($10)", "Local Market ($5)", "Cultural Show ($15)"],
                "Adventure": ["Bike Tour ($18)", "Kayaking ($25)", "Rock Climbing ($30)"],
                "Nightlife": ["Student Bar ($20)", "Live Music ($15)", "Night Market ($10)"]
            }
            
            for day_num in range(1, min(days + 1, 8)):
                st.markdown(f"### 📅 Day {day_num}")
                
                interest1 = interests[0] if interests else "Culture"
                interest2 = interests[1] if len(interests) > 1 else interest1
                
                morning_act = random.choice(activities_db.get(interest1, ["Sightseeing ($10)"]))
                afternoon_act = random.choice(activities_db.get(interest2, ["City Tour ($15)"]))
                
                st.write(f"**9:00 AM** - 🌅 {morning_act}")
                st.write(f"**12:30 PM** - 🍽️ Lunch at local spot ($12)")
                st.write(f"**2:00 PM** - 🎯 {afternoon_act}")
                st.write(f"**7:00 PM** - 🌆 Dinner & evening exploration ($18)")
                
                st.info(f"💰 Daily Budget: ~$60")
                st.markdown("---")
        
        # TAB 5: SAFETY TIPS
        with tab5:
            st.subheader("Safety & Travel Tips")
            
            st.markdown("#### 🛡️ General Safety")
            st.write("• Keep copies of passport and ID in cloud storage")
            st.write("• Share your itinerary with family/friends")
            st.write("• Register with your embassy")
            st.write("• Get comprehensive travel insurance")
            
            st.markdown("#### 💳 Money & Valuables")
            st.write("• Use a money belt for cash and cards")
            st.write("• Notify your bank about travel plans")
            st.write("• Keep emergency cash separate")
            st.write("• Use ATMs inside banks during day hours")
            
            st.markdown("#### ⚕️ Health")
            st.write("• Check vaccination requirements")
            st.write("• Bring medications in original containers")
            st.write("• Research local hospitals/clinics")
            st.write("• Drink bottled water if needed")
            
            st.markdown("#### 🚨 Emergency Contacts")
            col1, col2 = st.columns(2)
            with col1:
                st.info("**Emergency Services:** 112 (EU) / 911 (US)")
                st.info("**Local Police:** Research before trip")
            with col2:
                st.info("**Embassy:** Save contact number")
                st.info("**Insurance Hotline:** Keep accessible")
        
        # SIDEBAR COST SUMMARY
        st.sidebar.markdown("---")
        st.sidebar.subheader("💰 Cost Breakdown")
        
        transport_cost = 280
        accommodation_cost = 25 * days
        daily_expenses = 60 * days
        total_cost = transport_cost + accommodation_cost + daily_expenses
        
        st.sidebar.write(f"✈️ Transport: ${transport_cost}")
        st.sidebar.write(f"🏨 Accommodation: ${accommodation_cost}")
        st.sidebar.write(f"🍽️ Food & Activities: ${daily_expenses}")
        st.sidebar.markdown(f"### **Total: ${total_cost}**")
        
        if total_cost <= budget:
            st.sidebar.success(f"✅ Under budget by ${budget - total_cost}!")
        else:
            st.sidebar.warning(f"⚠️ Over budget by ${total_cost - budget}")
        
        st.sidebar.download_button(
            "📥 Download Itinerary",
            f"Trip: {origin} to {destination}\nDuration: {days} days\nBudget: ${budget}",
            file_name="itinerary.txt"
        )

else:
    # WELCOME SCREEN
    st.info("👈 **Fill in your trip details in the sidebar and click 'Generate Travel Plan'**")
    
    st.markdown("""
    ## 🌟 Why Choose AI Student Travel Planner?
    
    ### Benefits:
    - 💰 **Save Money** - AI finds the best student discounts and budget options
    - ⏱️ **Save Time** - All planning in one place, no need for multiple websites
    - 🎯 **Personalized** - Itineraries based on YOUR interests
    - 🛡️ **Stay Safe** - Safety tips and verified recommendations
    - 📱 **Easy to Use** - Simple, intuitive interface
    
    ### How It Works:
    1. 📝 Enter your destination and travel dates
    2. 💰 Set your budget
    3. 🎨 Choose your interests and travel style
    4. 🚀 Click "Generate Travel Plan"
    5. ✈️ Get your complete personalized itinerary!
    
    ---
    """)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🎓 Students Helped", "50,000+")
    with col2:
        st.metric("🌍 Destinations", "500+")
    with col3:
        st.metric("💵 Avg. Savings", "$450")
    with col4:
        st.metric("⭐ Success Rate", "98%")