import streamlit as st
import openai
import requests

# ---- CONFIG ----
openai.api_key = st.secrets["OPENAI_API_KEY"]  # Add your OpenAI API key in .streamlit/secrets.toml

BRAND_PROMPTS = {
    "ManMatters": "You are a senior product designer at ManMatters. Use practical UX language. Suggest design workflows, key components, and layout improvements. Prioritize men's wellness across mobile and web.",
    "BeBodywise": "You are a product designer at BeBodywise. Focus on women's wellness, self-care, and habit-building. Design suggestions should be empathetic, clear, and conversion-focused.",
    "ourLittleJoys": "You are the designer at ourLittleJoys. Think playful, modern, and supportive. Focus on wellness routines for children and parents. Suggest gentle UX with guided interactions."
}

# ---- Load Personas from GitHub ----
def load_personas(brand):
    if brand == "ManMatters":
        try:
            url = "https://raw.githubusercontent.com/suchitpoojari/design-ai-agent/main/brand_data/ManMatters/personas.txt"
            response = requests.get(url)
            if response.status_code == 200:
                return response.text.strip()
        except:
            pass
    return ""

# ---- UI ----
st.title("DesignAI: Workflow Generator")
st.markdown("Give me a brand and a design problem — I'll suggest flows and UX directions.")

brand = st.selectbox("Select Brand", list(BRAND_PROMPTS.keys()))
personas = load_personas(brand)
problem = st.text_area("Describe the design problem", placeholder="e.g. Users are dropping off at checkout on mobile")

if st.button("Generate Suggestions"):
    if not problem:
        st.warning("Please enter a problem statement.")
    else:
        with st.spinner("Thinking like a product designer..."):
            system_prompt = BRAND_PROMPTS[brand] + "\n\n" + personas

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": problem}
                    ],
                    temperature=0.6,
                    max_tokens=700
                )
                suggestion = response.choices[0].message.content.strip()
                st.markdown("### ✨ Suggested Design Workflows")
                st.write(suggestion)
            except Exception as e:
                st.error(f"OpenAI API call failed: {e}")
