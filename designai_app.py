import streamlit as st
import requests

# ---- CONFIG ----
DEEPSEEK_API_KEY = st.secrets["sk-3d2c9be49bc24ab2af28c0675b9cb72a"]  # Add your DeepSeek API key in .streamlit/secrets.toml

BRAND_PROMPTS = {
    "ManMatters": "You are a senior product designer at ManMatters. Use practical UX language. Suggest design workflows, key components, and layout improvements. Prioritize men's wellness across mobile and web.",
    "BeBodywise": "You are a product designer at BeBodywise. Focus on women's wellness, self-care, and habit-building. Design suggestions should be empathetic, clear, and conversion-focused.",
    "ourLittleJoys": "You are the designer at ourLittleJoys. Think playful, modern, and supportive. Focus on wellness routines for children and parents. Suggest gentle UX with guided interactions."
}

# ---- UI ----
st.title("DesignAI: Workflow Generator")
st.markdown("Give me a brand and a design problem — I'll suggest flows and UX directions.")

brand = st.selectbox("Select Brand", list(BRAND_PROMPTS.keys()))
problem = st.text_area("Describe the design problem", placeholder="e.g. Users are dropping off at checkout on mobile")

if st.button("Generate Suggestions"):
    if not problem:
        st.warning("Please enter a problem statement.")
    else:
        with st.spinner("Thinking like a product designer..."):
            headers = {
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": BRAND_PROMPTS[brand]},
                    {"role": "user", "content": problem}
                ],
                "temperature": 0.6,
                "max_tokens": 700
            }

            response = requests.post("https://api.deepseek.com/v1/chat/completions", headers=headers, json=payload)

            if response.status_code == 200:
                suggestion = response.json()["choices"][0]["message"]["content"].strip()
                st.markdown("### ✨ Suggested Design Workflows")
                st.write(suggestion)
            else:
                st.error(f"API call failed: {response.status_code} - {response.text}")
