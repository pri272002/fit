import streamlit as st
from google import genai

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
    "Ask me anything about fitness, nutrition, workouts, weight loss, muscle gain and healthy living."
)

# ----------------------
# Sidebar
# ----------------------
st.sidebar.title("Settings")
api_key = st.secrets["api"]
st.sidebar.markdown("---")

if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# ----------------------
# Chat History
# ----------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ----------------------
# User Input
# ----------------------
user_input = st.chat_input(
    "Ask a fitness question..."
)

if user_input:

    if not api_key:
        st.error("Please enter your Gemini API Key.")
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

        client = genai.Client(
            api_key=api_key
        )

        conversation = ""

        for msg in st.session_state.messages:
            conversation += (
                f"{msg['role']}: {msg['content']}\n"
            )

        prompt = f"""
You are an expert Fitness and Health Coach.

You help users with:
- Workout plans
- Weight loss
- Muscle gain
- Nutrition
- Meal planning
- Cardio
- Strength training
- Healthy habits

Rules:
- Give professional advice.
- Use bullet points.
- Be supportive and motivating.
- If the topic is medical, recommend consulting a healthcare professional.

Conversation:
{conversation}

Assistant:
"""

        response = client.models.generate_content(
            model="gemini-flash-lite-latest",
            contents=prompt
        )

        answer = response.text

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
