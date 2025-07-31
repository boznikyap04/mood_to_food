import streamlit as st
from PIL import Image
from restaurants import generate_restaurant_df
from emotions import load_emotion_image_pairs
from gemini import get_gemini_recommendation, display_gemini_selected_restaurant

#Please use your own api key for testing
gemini_key = st.secrets["api_keys"]["gemini"]

# Initialize emotion image pairs only once
if 'emotion_image_pairs' not in st.session_state:
    st.session_state['emotion_image_pairs'] = load_emotion_image_pairs("images")

if 'df' not in st.session_state:
    st.session_state['df'] = generate_restaurant_df(filepath="restaurant_data/restaurant_data.xlsx")

# Initialize state variables
# allergens, cuisines, and preferences are set to none/false when the emotion is changed
st.session_state.setdefault('selected_emotion', None)
st.session_state.setdefault('submitted_allergens', False)
st.session_state.setdefault('selected_allergens', [])
st.session_state.setdefault('excluded_cuisines', [])
st.session_state.setdefault('submitted_cuisine_preferences', False)

# Callback to update selected emotion
# Sets allergens, cuisines, and preferences to none/false as emotion is changed
def set_selected_emotion(emotion):
    st.session_state['selected_emotion'] = emotion
    st.session_state['submitted_allergens'] = False
    st.session_state['excluded_cuisines'] = []
    st.session_state['submitted_cuisine_preferences'] = False

def set_allergens(allergens):
    st.session_state['selected_allergens'] = [key for key, val in allergens.items() if val]
    st.session_state['submitted_allergens'] = True

def set_cuisines(cuisines):
    st.session_state['excluded_cuisines'] = [k for k, v in cuisine_checks.items() if v]
    st.session_state['submitted_cuisine_preferences'] = True

# Title
st.markdown("""
# 🟢 **LasallEats**  
### _An Emotion-Based Food Recommender System_

Discover the perfect meal that matches your mood.  
Whether you're feeling joyful, stressed, or adventurous —  
**LasallEats** finds the flavor your emotions crave. 🍽️💚

---

### 👉 Please select the image that best fits your emotions to get started.
""")

# Emotion grid
emotion_image_pairs = st.session_state['emotion_image_pairs']
cols = st.columns(3) + st.columns(3)

for idx, (emotion, img_path) in enumerate(emotion_image_pairs):
    col = cols[idx]
    with col:
        with st.container():
            img = Image.open(img_path).resize((200, 200))
            st.image(img)

            button_label = "✅ Selected" if st.session_state['selected_emotion'] == emotion else "Select"
            st.button(
                button_label,
                key=f"select_{emotion}",
                on_click=set_selected_emotion,
                args=(emotion,)
            )

# Step 2: Food Allergen Form
st.markdown("---")
st.subheader("Any food allergens we should avoid?")
with st.form("allergen_form"):
    allergens = {
        "Chicken": st.checkbox("Chicken"),
        "Pork": st.checkbox("Pork"),
        "Beef": st.checkbox("Beef"),
        "Seafood": st.checkbox("Seafood"),
        "Nuts": st.checkbox("Nuts")
    }

    submitted = st.form_submit_button("Set Allergens", on_click=set_allergens(allergens))
    if submitted:
        st.success("Allergen preferences saved!")

# Step 3: Cuisine Preference Form
st.markdown("---")
st.subheader("Which cuisines would you like to avoid?")

cuisines = ["Filipino", "Chinese", "Korean", "Mongolian", "Variety", "Japanese", "French", "Vietnamese", "Thai"]
with st.form("cuisine_form"):
    cuisine_checks = {
        cuisine: st.checkbox(f"{cuisine}", key=f"cuisine_{cuisine}")
        for cuisine in cuisines
    }

    submitted =  st.form_submit_button("Set Cuisine Preferences", on_click=set_cuisines(cuisine_checks))
    if submitted:
        st.success("Cuisine preferences saved!")

# Step 4: Generate Response
st.markdown("---")

if st.session_state['selected_emotion'] is not None:
    if st.session_state['submitted_cuisine_preferences'] is not False and st.session_state['submitted_allergens'] is not False:
        if st.button("Suggest a restaurant based on mood, food, and preferences"):
            with st.spinner("Getting the best match for your mood..."):
                df = st.session_state['df']
                selected_emotion = st.session_state['selected_emotion']
                excluded_allergens = st.session_state['selected_allergens']
                excluded_cuisines = st.session_state['excluded_cuisines']
                response = get_gemini_recommendation(df, selected_emotion, excluded_allergens, excluded_cuisines, gemini_key)
                display_gemini_selected_restaurant(response, selected_emotion, df)

    else:
        st.button(
            "Suggest recommended restaurant based on mood, food, and preferences",
            key="suggest_button_disabled",
            disabled=True,
            help="Please ensure you have filled in all the previous details"
        )
else:
    st.button(
        "Suggest recommended restaurant based on mood, food, and preferences",
        key="suggest_button_disabled",
        disabled=True,
        help="Please ensure you have filled in all the previous details"
    )