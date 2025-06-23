import streamlit as st
import os
import pickle
import pandas as pd
import base64

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

logo_path = os.path.join(os.path.dirname(__file__), "cricket_logo.png")

if os.path.exists(logo_path):
    logo_b64 = get_base64_of_bin_file(logo_path)
    logo_src = f"data:image/png;base64,{logo_b64}"

else:
    logo_src = "https://stock.adobe.com/in/search?k=cricket+logo"

st.set_page_config(

    page_title = "MyBhavishya 11 App",
    page_icon = "🏏",
    layout = "wide"
)

html = f"""

<div style = "
    display: flex;
    align-items: center;
    gap: 20px;
    padding: 10px 0;
">
    <img src = "{logo_src}" style = "width:80px; height: auto;" />
    <div>
        <div style = "font-size: 2.5rem; font-weight: bold;"> MyBhavishya 11 App </div>
        <div style = "font-size: 1.25rem; color: #555;"> Bhavishya Batayega Kis Team Ka Palda Hoga Bhaari </div>
    </div>
</div>
"""

st.markdown(html, unsafe_allow_html = True)
st.markdown("---")


try:
    filepath = os.path.join(os.path.dirname(__file__), 'pipe.pkl')

    with open(filepath, 'rb') as f:
        pipe = pickle.load(f)

except Exception as e:
    st.error(f"Can't Load Your Model Pipeline: {e}")
    st.stop()

teams = ['Sunrisers Hyderabad', 'Mumbai Indians', 'Royal Challengers Bangalore', 'Kolkata Knight Riders', 'Kings XI Punjab', 'Chennai Super Kings', 'Rajasthan Royals', 'Delhi Capitals']
cities = ['Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi', 'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth', 'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley', 'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala', 'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi', 'Sharjah', 'Mohali', 'Bengaluru']

st.markdown("## IPL Match Setup")

col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Batting Team', sorted(teams))

with col2:
    bowling_team = st.selectbox('Bowling Team', sorted(teams))

selected_city = st.selectbox('Host City', sorted(cities))

st.markdown("## Current Scenario")

target = st.number_input('Target Score', min_value = 1)

col3, col4, col5 = st.columns(3)

with col3:
    score = st.number_input('Current Score', min_value = 0)

with col4:
    overs = st.number_input('Overs Completed', min_value = 0.0, max_value = 20.0, step = 0.166)

with col5:
    wickets_out = st.number_input('Wickets Fallen', min_value = 0, max_value = 10)

if st.button('🔮 Predict Win Probability'):

    runs_left = target - score
    balls_bowled = int(overs * 6)

    balls_left = 120 - balls_bowled
    wickets_remaining = 10 - wickets_out

    if overs <= 0:
        st.error("At Least One Ball Should Be Bowled !!")

    elif balls_left <= 0:
        st.error("Match Is Already Over !!")

    else:
        crr = score / overs
        rrr = (runs_left * 6) / balls_left

        input_df = pd.DataFrame({'batting_team': [batting_team], 'bowling_team': [bowling_team], 'city': [selected_city], 'runs_left': [runs_left], 'balls_left': [balls_left], 'wickets_left': [wickets_remaining], 'total_runs_x': [target], 'crr': [crr], 'rrr': [rrr]})

        try:
            result = pipe.predict_proba(input_df)
            loss = result[0][0]
            win = result[0][1]

        except Exception as e:
            st.error(f"There Was An Error Loading Your Prediction: {e}")

        else:
            st.markdown("## 🏁 Win Probabilities")
            st.success(f"🏏 {batting_team}: **{round(win * 100)}%** Chance To Win")
            st.error(f"⚾ {bowling_team}: **{round(loss * 100)}%** Chance To Win")
