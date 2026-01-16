import random
from datetime import datetime, timedelta

def get_transportation_options(origin, destination, start_date, preferences, budget):
    """Generate AI-based transportation options"""
    
    options = []
    
    # Flight option
    if "Flight" in preferences or budget > 500:
        options.append({
            "type": "Budget Airline",
            "emoji": "✈️",
            "price": random.randint(150, 400),
            "duration": "2-6 hours",
            "rating": 4,
            "details": f"Direct flight from {origin} to {destination}",
            "student_discount": "15% off with student ID",
            "recommended": True
        })
    
    # Train option
    if "Train" in preferences:
        options.append({
            "type": "Train",
            "emoji": "🚆",
            "price": random.randint(80, 200),
            "duration": "6-12 hours",
            "rating": 5,
            "details": f"Scenic train route with WiFi",
            "student_discount": "20% off with Eurail/Student pass",
            "recommended": True
        })
    
    # Bus option
    if "Bus" in preferences:
        options.append({
            "type": "Coach Bus",
            "emoji": "🚌",
            "price": random.randint(30, 100),
            "duration": "8-15 hours",
            "rating": 3,
            "details": f"Overnight bus with reclining seats",
            "student_discount": "10% off",
            "recommended": budget < 500
        })
    
    # Rideshare option
    if "Rideshare" in preferences:
        options.append({
            "type": "Rideshare (BlaBlaCar)",
            "emoji": "🚗",
            "price": random.randint(20, 80),
            "duration": "Variable",
            "rating": 4,
            "details": f"Share ride with verified drivers",
            "student_discount": "Student verification required",
            "recommended": budget < 300
        })
    
    return sorted(options, key=lambda x: x['price'])

def get_accommodation_options(destination, duration, acc_types, budget, travel_style):
    """Generate accommodation recommendations"""
    
    options = []
    
    if "Hostels" in acc_types:
        options.append({
            "name": f"{destination} Central Hostel",
            "type": "Hostel",
            "emoji": "🏨",
            "price_per_night": random.randint(15, 35),
            "location": "City Center",
            "rating": 4,
            "amenities": ["Free WiFi", "Kitchen", "Lounge", "Lockers"],
            "student_friendly": "Social atmosphere, meet other travelers, student discounts available",
            "recommended": True
        })
    
    if "Budget Hotels" in acc_types:
        options.append({
            "name": f"{destination} Budget Inn",
            "type": "Budget Hotel",
            "emoji": "🏩",
            "price_per_night": random.randint(40, 70),
            "location": "Near Public Transport",
            "rating": 4,
            "amenities": ["Free Breakfast", "WiFi", "Private Bath"],
            "student_friendly": "Clean, safe, and affordable with student rates",
            "recommended": travel_style in ["Comfort Seeker", "Balanced"]
        })
    
    if "Student Dorms" in acc_types:
        options.append({
            "name": f"{destination} University Dorm",
            "type": "Student Dorm",
            "emoji": "🎓",
            "price_per_night": random.randint(10, 25),
            "location": "University District",
            "rating": 3,
            "amenities": ["Shared Kitchen", "Study Room", "Laundry"],
            "student_friendly": "Perfect for students, very affordable, educational environment",
            "recommended": budget < 500
        })
    
    if "Airbnb" in acc_types:
        options.append({
            "name": f"{destination} Cozy Apartment",
            "type": "Airbnb",
            "emoji": "🏠",
            "price_per_night": random.randint(35, 90),
            "location": "Residential Area",
            "rating": 5,
            "amenities": ["Full Kitchen", "WiFi", "Washer", "Local Experience"],
            "student_friendly": "Live like a local, great for groups, kitchen saves money on food",
            "recommended": travel_style == "Balanced"
        })
    
    return sorted(options, key=lambda x: x['price_per_night'])

def generate_itinerary(destination, duration, interests, budget_per_day):
    """Generate personalized day-by-day itinerary"""
    
    itinerary = []
    
    activity_database = {
        "Museums": [
            {"activity": "Visit National Museum", "cost": 12, "emoji": "🏛️"},
            {"activity": "Art Gallery Tour", "cost": 8, "emoji": "🎨"},
        ],
        "Food": [
            {"activity": "Local Street Food Tour", "cost": 15, "emoji": "🍜"},
            {"activity": "Traditional Restaurant Lunch", "cost": 20, "emoji": "🍽️"},
        ],
        "Nature": [
            {"activity": "City Park & Gardens", "cost": 0, "emoji": "🌳"},
            {"activity": "Hiking Trail", "cost": 5, "emoji": "🥾"},
        ],
        "Culture": [
            {"activity": "Historic District Walking Tour", "cost": 10, "emoji": "🏰"},
            {"activity": "Local Market Visit", "cost": 5, "emoji": "🏪"},
        ],
        "Adventure": [
            {"activity": "Bike Tour", "cost": 18, "emoji": "🚴"},
            {"activity": "Rock Climbing", "cost": 25, "emoji": "🧗"},
        ],
        "Nightlife": [
            {"activity": "Student Bar Crawl", "cost": 20, "emoji": "🍺"},
            {"activity": "Live Music Venue", "cost": 15, "emoji": "🎵"},
        ]
    }
    
    for day_num in range(1, min(duration + 1, 8)):  # Max 7 days shown
        day_activities = []
        daily_cost = 0
        
        # Morning
        morning_interest = random.choice(interests) if interests else "Culture"
        if morning_interest in activity_database:
            activity = random.choice(activity_database[morning_interest])
            day_activities.append({
                "time": "9:00 AM",
                "activity": activity["activity"],
                "cost": activity["cost"],
                "emoji": activity["emoji"]
            })
            daily_cost += activity["cost"]
        
        # Lunch
        day_activities.append({
            "time": "12:30 PM",
            "activity": "Lunch at Local Eatery",
            "cost": 10,
            "emoji": "🍴"
        })
        daily_cost += 10
        
        # Afternoon
        afternoon_interest = random.choice([i for i in interests if i != morning_interest]) if len(interests) > 1 else morning_interest
        if afternoon_interest in activity_database:
            activity = random.choice(activity_database.get(afternoon_interest, activity_database["Culture"]))
            day_activities.append({
                "time": "2:00 PM",
                "activity": activity["activity"],
                "cost": activity["cost"],
                "emoji": activity["emoji"]
            })
            daily_cost += activity["cost"]
        
        # Evening
        day_activities.append({
            "time": "7:00 PM",
            "activity": "Dinner & Explore Night Scene",
            "cost": 15,
            "emoji": "🌆"
        })
        daily_cost += 15
        
        itinerary.append({
            "day": f"Day {day_num} - {destination}",
            "activities": day_activities,
            "daily_total": daily_cost
        })
    
    return itinerary

def get_safety_tips(destination):
    """Generate safety tips for destination"""
    
    return {
        "General Safety": {
            "emoji": "🛡️",
            "tips": [
                "Keep copies of important documents (passport, ID) in cloud storage",
                "Share your itinerary with family/friends",
                "Register with your embassy if traveling abroad",
                "Get travel insurance that covers medical emergencies"
            ]
        },
        "Money & Valuables": {
            "emoji": "💳",
            "tips": [
                "Use a money belt or hidden pouch for cash and cards",
                "Notify your bank of travel plans to avoid card blocks",
                "Keep emergency cash separate from main wallet",
                "Use ATMs inside banks during business hours"
            ]
        },
        "Health": {
            "emoji": "⚕️",
            "tips": [
                "Check if any vaccinations are required",
                "Bring necessary medications in original containers",
                "Drink bottled water if tap water isn't safe",
                "Know the location of nearest hospital/clinic"
            ]
        },
        "Local Awareness": {
            "emoji": "👁️",
            "tips": [
                "Research common scams in the destination",
                "Learn basic phrases in the local language",
                "Stay aware of your surroundings, especially at night",
                "Use licensed taxis or reputable rideshare apps"
            ]
        }
    }

def calculate_total_cost(transport, accommodation, activities):
    """Calculate total trip cost"""
    return transport + accommodation + activities
