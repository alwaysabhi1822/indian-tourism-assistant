
# Incredible India Tourism Assistant


An AI-powered chatbot that helps users discover and plan trips across India. Features include:
- Destination recommendations
- Personalized travel planning
- Voice input support
- PDF itinerary generation
- Preference-based suggestions

## Features
- 🗣️ Voice-enabled queries
- 📄 PDF export for itineraries
- 🧑 User preference profiles
- 📱 Mobile-responsive design
- 🌐 Real-time information retrieval

✅ 3. Installation & Usage (Reformatted for Clarity)
Use clear sections with bash code blocks.

md
Copy
Edit
## 🚀 Getting Started

### 🔧 Prerequisites
- Python 3.8+
- GROQ API key (create at [groq.com](https://groq.com))

### 📦 Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/india-tourism-chatbot.git
cd india-tourism-chatbot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
🔑 Set Environment Variables
Create a .env file in the root directory:

env
Copy
Edit
GROQ_API_KEY=your_groq_api_key_here
▶️ Run the App
bash
Copy
Edit
uvicorn main:app --reload
Open your browser: http://localhost:8000

🧠 Vector Store Setup
To use your own tourism data:

bash
Copy
Edit
# Replace 'your_data.txt' with your custom tourism content
# Run the vector generation script (provide if available)

python generate_vectors.py
Make sure vectors.pkl is generated and placed in the root directory.

🛠️ Tech Stack
Layer	Technology
Frontend	HTML, Bootstrap, Animate.css, JS
Backend	FastAPI, LangChain, Groq API
AI Models	Llama3-70B via Groq
Embeddings	HuggingFace - all-MiniLM-L6-v2
Storage	FAISS Vector Store (Pickle format)

