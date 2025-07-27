import streamlit as st
import google.generativeai as genai
import re

def get_gemini_recommendation(df, emotion, excluded_allergens, excluded_cuisines, api_key):
    genai.configure(api_key=api_key)
    # Change the model to your liking, 2.5 pro has a limit of 1M Tokens
    model = genai.GenerativeModel("gemini-2.5-pro")

    # Convert DataFrame to readable list format
    restaurants = df.to_dict(orient='records')

    # Displaying the restaurants in a more readable format for the LLM
    restaurant_list = ""

    for r in restaurants:
        name = r['StoreName']
        cuisine_str = str(r['Cuisine']) if r['Cuisine'] else "Not specified"
        food_str = str(r['Food']) if r['Food'] and r['Food'] != '-' else "None"
        description = r['Description']
        budget_min = r['Budget_Min']
        budget_max = r['Budget_Max']

        restaurant_list += f"""
    Name: {name}
    Cuisine: {cuisine_str}
    Description: {description}
    Food Types: {food_str}
    Budget: ₱{budget_min} - ₱{budget_max}
    ---
    """

    # Create the Gemini prompt
    prompt = f"""
You are a helpful assistant that recommends restaurants based on mood and dietary preferences.

The user currently feels **{emotion}** and is looking for a restaurant to match that mood.

Please follow these rules strictly:
1. **Do NOT recommend any restaurant** that includes these allergens: {', '.join(excluded_allergens) or "None"}.
2. **Do NOT recommend any restaurant** that serves these cuisines: {', '.join(excluded_cuisines) or "None"}.
3. Only choose from the list of restaurants below.
4. Pick the best match for the mood and explain why it fits.
5. Return only ONE recommendation.
6. If there are no allergens or cuisines removed, be more creative with your response.

Here are the available restaurants:

{restaurant_list}

Please respond with:
- The restaurant name
- A short explanation why it’s a good fit based on the user's emotion and restrictions
"""

    # Ask Gemini
    response = model.generate_content(prompt)
    return response.text

def display_gemini_selected_restaurant(response_text, emotion, df):
    # Try to extract the first line or bolded name (adjust based on Gemini's style)
    lines = response_text.strip().split('\n')
    candidate_line = lines[0]

    # Try bold name or normal
    match = re.search(r"\*\*(.*?)\*\*|^Name[:\-]?\s*(.*)", candidate_line)
    if match:
        extracted_name = match.group(1) or match.group(2)
        extracted_name = extracted_name.strip()
    else:
        # fallback: use first line
        extracted_name = candidate_line.strip()

    # Try to match in DataFrame
    matched_df = df[df['StoreName'].str.strip().str.lower() == extracted_name.lower()]
    if matched_df.empty:
        st.warning("Could not find the restaurant from our model's response.")
        return

    # Get the row as a dict
    restaurant = matched_df.iloc[0]
    st.markdown(f"""
    <h1 style='font-size: 36px; color: #FFFFFF;'>🍽️ {restaurant['StoreName']}</h1>
    <p style='font-size: 18px;'><strong>Emotion matched:</strong> <span style='color: #4B9CD3;'><em>{emotion}</em></span></p>

    ---

    **🍱 Cuisine:** {', '.join(restaurant['Cuisine']) if isinstance(restaurant['Cuisine'], list) else restaurant['Cuisine']}  
    **📝 Description:** {restaurant['Description']}  
    **⚠️ Allergens Present:** {', '.join(restaurant['Food']) if isinstance(restaurant['Food'], list) else restaurant['Food']}  
    **💸 Budget Range:** ₱{restaurant['BudgetMin']} – ₱{restaurant['BudgetMax']}  
    **🏠 Dining Area:** {restaurant['DiningArea']}  
    **📍 Location:** {restaurant['Address']}
    """, unsafe_allow_html=True)

    st.write("💡 Why you should eat at this restaurant:")
    st.write(response_text)

