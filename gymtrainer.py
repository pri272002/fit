import streamlit as st
from groq import Groq

# ----------------------
# Page Config
# ----------------------
st.set_page_config(
    page_title="Fitness & Health AI Coach",
    page_icon="💪",
    layout="wide"
)

st.title("💪 Fitness & Health AI Coach")

st.write(
    "Ask me anything about fitness, nutrition, workouts, weight loss, muscle gain, supplements, and healthy living."
)

# ----------------------
# Sidebar
# ----------------------
st.sidebar.title("Settings")

try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = ""

st.sidebar.markdown("---")

if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# ----------------------
# Session State
# ----------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ----------------------
# Display Chat History
# ----------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ----------------------
# Chat Input
# ----------------------
user_input = st.chat_input(
    "Ask a fitness, nutrition, or workout question..."
)

if user_input:

    if not api_key:
        st.error("GROQ_API_KEY not found in secrets.toml")
        st.stop()

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    try:

        client = Groq(
            api_key=api_key
        )

        messages = [
            {
                "role": "system",
                "content": """
You are an Expert Fitness and Health Coach.

You help users with:

• Weight Loss
• Muscle Gain
• Workout Plans
• Nutrition
• Fat Loss
• Cardio
• Strength Training
• Bodybuilding
• Protein Intake
• Supplements
• Healthy Lifestyle

Rules:

1. Be professional.
2. Use bullet points whenever possible.
3. Provide actionable fitness advice.
4. Stay motivational and supportive.
5. Do not diagnose medical conditions.
6. If symptoms seem serious, suggest consulting a healthcare professional.
7. Keep answers easy to understand.
8. Give workout and diet examples when useful.
"""
            }
        ]

        for msg in st.session_state.messages:
            messages.append(
                {
                    "role": msg["role"],
                    "content": msg["content"]
                }
            )

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            temperature=0.7,
            max_tokens=1500
        )

        answer = response.choices[0].message.content

        with st.chat_message("assistant"):
            st.markdown(answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

    except Exception as e:
        st.error(f"Error: {str(e)}")
