import streamlit as st

# Emotion to food mapping
emotion_to_food = {
    "Happy": ["Sushi 🍣", "Cake 🎂", "Pizza 🍕"],
    "Sad": ["Ice cream 🍦", "Chocolate 🍫", "Soup 🍲"],
    "Angry": ["Spicy wings 🌶️", "Steak 🥩", "Burger 🍔"],
    "Anxious": ["Herbal tea 🍵", "Banana 🍌", "Dark chocolate 🍫"],
    "Bored": ["Snacks 🍿", "Ramen 🍜", "Fries 🍟"],
    "Excited": ["Fusion food 🍱", "Bubble tea 🧋", "Nachos 🌮"],
    "Tired": ["Coffee ☕", "Protein bar 🍫", "Oatmeal 🥣"],
    "Lonely": ["Mac & cheese 🧀", "Cookies 🍪", "Warm bread 🥖"],
    "Stressed": ["Green tea 🍵", "Nuts 🥜", "Yogurt 🍦"]
}

# Session state
if "selected_emotion" not in st.session_state:
    st.session_state.selected_emotion = None

def main():
    st.set_page_config(page_title="Emotion-Based Food Recommender")
    st.title("🍽️ Emotion-Based Food Recommender")
    st.write("How are you feeling today? Select an emotion:")

    # Emotion buttons
    cols = st.columns(3)
    emotions = list(emotion_to_food.keys())

    for i, emotion in enumerate(emotions):
        with cols[i % 3]:
            if st.button(emotion):
                st.session_state.selected_emotion = emotion

    # Show suggestions if emotion is selected
    if st.session_state.selected_emotion:
        emotion = st.session_state.selected_emotion
        default_food = emotion_to_food[emotion]

        st.subheader(f"💬 You selected: `{emotion}`")
        st.write("Here are some food suggestions:")

        # Filter food
        food_to_remove = st.multiselect("❌ Remove specific items you don't like:", default_food)
        filtered_food = [item for item in default_food if item not in food_to_remove]

        if filtered_food:
            st.subheader("🍲 Final Suggestions")
            st.success(", ".join(filtered_food))

            # Feedback checkbox
            feedback = st.checkbox("✅ Are these suggestions good for how you're feeling?")

            if feedback:
                st.info("Thanks for your feedback! 😊")
        else:
            st.warning("You've removed all suggestions. Try selecting another emotion or refreshing.")

if __name__ == "__main__":
    main()
