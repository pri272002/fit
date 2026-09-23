import streamlit as st
from openai import OpenAI

# ----------------------
# Page Configuration
# ----------------------
st.set_page_config(
    page_title="Fitness & Health AI Coach",
    page_icon="💪",
    layout="wide"
)

st.title("💪 Fitness & Health AI Coach")
st.write(
    "Ask me anything about fitness, nutrition, workouts, muscle gain, weight loss, and healthy living."
)

# ----------------------
# Sidebar
# ----------------------
st.sidebar.title("Settings")

# Nmedia API Key
api_key = "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"

st.sidebar.markdown("---")
st.sidebar.info("""
Examples:
- Create a workout plan
- Help me lose weight
- Calculate protein needs
- Muscle building tips
- Healthy diet suggestions
""")

# ----------------------
# Chat History
# ----------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ----------------------
# Chat Input
# ----------------------
user_input = st.chat_input("Ask a fitness question...")

if user_input:

    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        client = OpenAI(
        api_key=api_key,
        base_url="https://integrate.api.nvidia.com/v1"
    )

        system_prompt = """
You are an expert fitness and health coach.

You help users with:
- Workout plans
- Weight loss
- Muscle gain
- Nutrition
- Cardio training
- Strength training
- Healthy lifestyle habits

Rules:
- Give professional advice.
- Use bullet points whenever possible.
- Be motivating and supportive.
- If a question is medical, advise consulting a healthcare professional.
"""

        response = client.chat.completions.create(
            model="meta/llama-3.1-70b-instruct",   # Replace with actual Nmedia model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
        )

        answer = response.choices[0].message.content

        with st.chat_message("assistant"):
            st.markdown(answer)

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

    except Exception as e:
        st.error(f"Error: {e}")
