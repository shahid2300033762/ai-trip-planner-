🎒 AI Student Travel Planner
An AI-powered travel planning application built with Streamlit and Google Gemini AI. This tool is specifically designed for students to generate budget-friendly itineraries, safety tips, and travel recommendations based on real-time AI discovery.

🌟 Features
Intelligent Model Discovery: Automatically detects available Gemini models (1.5 Flash, 1.5 Pro, etc.) to ensure high availability and prevent 404 errors.

Student-Centric Budgeting: Calculates daily allowances and prioritizes student discounts and budget-friendly activities.

Dynamic Itineraries: Generates day-by-day plans including morning, afternoon, and evening activities based on user interests.

Safety First: Provides localized safety advice and common scam alerts for specific destinations.

Offline Fallback: Includes a robust fallback system to provide general travel tips even if the AI API is unreachable.

Exportable Plans: Download your complete travel plan as a Markdown file for offline use.

🛠️ Tech Stack
Frontend: Streamlit

AI Engine: Google Gemini API (google-generativeai)

Language: Python 3.9+

DevOps: Docker ready (optional)

🚀 Getting Started
Prerequisites
Python installed on your machine.

A Google Gemini API Key (Get it from Google AI Studio).

Installation
Clone the repository:

Bash
git clone https://github.com/your-username/ai-student-travel-planner.git
cd ai-student-travel-planner
Install dependencies:

Bash
pip install -r requirements.txt
Set up your API Key:

Create a .env file or export it to your terminal:

Bash
export GOOGLE_API_KEY='your_api_key_here'
Run the application:

Bash
streamlit run app.py
☁️ Deployment
Streamlit Community Cloud
Push your code to a GitHub repository.

Connect the repository to Streamlit Cloud.

Add your GOOGLE_API_KEY in the Advanced Settings > Secrets section of the Streamlit dashboard:

Ini, TOML
GOOGLE_API_KEY = "your_actual_key_here"
🐳 Docker (Optional)
For those interested in containerization:

Bash
docker build -t travel-planner .
docker run -p 8501:8501 -e GOOGLE_API_KEY='your_key' travel-planner
📜 License
Distributed under the MIT License.
