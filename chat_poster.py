import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import random
from PIL import Image
import os

# Function to generate synthetic dataset
def generate_data():
    np.random.seed(42)
    
    # Presentation tracks with descriptions
    tracks = {
        "Biotechnology": "Research in genetic engineering, pharmaceuticals, and biomedical applications",
        "Renewable Energy": "Innovations in solar, wind, and alternative energy technologies",
        "Artificial Intelligence": "Machine learning, neural networks, and AI applications",
        "Environmental Science": "Climate change, conservation, and sustainability research"
    }
    
    # Indian colleges and states
    colleges = [
        "IIT Delhi", "IIT Bombay", "IIT Madras", "IIT Kharagpur", "IISc Bangalore",
        "NIT Trichy", "BITS Pilani", "University of Delhi", "University of Mumbai",
        "JNU New Delhi", "Anna University", "University of Calcutta", "University of Pune",
        "Amity University", "VIT Vellore", "SRM University", "Manipal University",
        "Christ University", "St. Xavier's College", "Presidency University"
    ] * 20
    
    states = [
        "Maharashtra", "Tamil Nadu", "Karnataka", "Delhi", "West Bengal",
        "Uttar Pradesh", "Gujarat", "Rajasthan", "Andhra Pradesh", "Telangana",
        "Kerala", "Madhya Pradesh", "Punjab", "Haryana", "Bihar", "Odisha",
        "Assam", "Jharkhand", "Chhattisgarh", "Uttarakhand", "Himachal Pradesh",
        "Goa", "Jammu & Kashmir", "Meghalaya", "Manipur"
    ]
    
    data = {
        "Participant ID": [f"PP-{i:03d}" for i in range(1, 401)],
        "Name": [f"Participant {i}" for i in range(1, 401)],
        "College": np.random.choice(colleges, 400, replace=True),
        "State": np.random.choice(states, 400, replace=True),
        "Track": np.random.choice(list(tracks.keys()), 400, p=[0.3, 0.2, 0.3, 0.2]),
        "Day": np.random.choice(["Day 1", "Day 2", "Day 3", "Day 4"], 400),
        "Presentation Score": np.round(np.random.normal(75, 10, 400), 1),
        "Attendance Duration (mins)": np.random.randint(30, 240, 400),
        "Feedback": [""]*400
    }
    
    feedback_samples = {
        "Biotechnology": [
            "Great insights into gene editing applications",
            "Fascinating research on cancer therapeutics",
            "Impressive work on microbial biotechnology",
            "Could improve experimental methodology",
            "Excellent presentation of pharmaceutical research"
        ],
        "Renewable Energy": [
            "Innovative solar panel designs",
            "Good analysis of wind energy potential",
            "Comprehensive study on biofuel alternatives",
            "Needs more practical implementation details",
            "Well-researched on energy storage solutions"
        ],
        "Artificial Intelligence": [
            "Cutting-edge machine learning applications",
            "Impressive neural network architecture",
            "Good explanation of AI ethics",
            "Could use more real-world case studies",
            "Excellent demonstration of computer vision"
        ],
        "Environmental Science": [
            "Important findings on climate change",
            "Good analysis of biodiversity loss",
            "Practical solutions for waste management",
            "Needs more policy recommendations",
            "Comprehensive study on water conservation"
        ]
    }
    
    for i in range(400):
        track = data["Track"][i]
        score = data["Presentation Score"][i]
        
        if score > 80:
            sentiment = random.choice(["Excellent ", "Outstanding ", "Superb "])
        elif score > 70:
            sentiment = random.choice(["Good ", "Solid ", "Well-done "])
        else:
            sentiment = random.choice(["Decent ", "Average ", "Acceptable "])
        
        data["Feedback"][i] = sentiment + random.choice(feedback_samples[track])
    
    df = pd.DataFrame(data)
    df["Presentation Score"] = np.clip(df["Presentation Score"], 50, 100)
    return df, tracks

# Streamlit UI
st.set_page_config(layout="wide", page_title="Poster Presentation Dashboard", page_icon="📊")
st.markdown("""
    <style>
    .css-18e3th9 {
        background-color: #1E1E2F;
        color: white;
    }
    .css-1d391kg {
        background-color: #2A2A3B;
    }
    h1, h2, h3, h4 {
        color: #FFD700;
    }
    </style>
    """, unsafe_allow_html=True)

df, tracks = generate_data()
st.title("🎤 National Poster Presentation Analysis")

# Sidebar Filters
st.sidebar.header("Filter Options")
track_filter = st.sidebar.multiselect("Select Track", df["Track"].unique(), default=df["Track"].unique())
day_filter = st.sidebar.multiselect("Select Day", df["Day"].unique(), default=df["Day"].unique())
college_filter = st.sidebar.multiselect("Select College", df["College"].unique(), default=df["College"].unique())
state_filter = st.sidebar.multiselect("Select State", df["State"].unique(), default=df["State"].unique())

filtered_df = df[df["Track"].isin(track_filter) & df["Day"].isin(day_filter) & df["College"].isin(college_filter) & df["State"].isin(state_filter)]

# Dashboard Visualizations
st.subheader("📊 Participation Trends")
st.bar_chart(filtered_df["Track"].value_counts())
st.bar_chart(filtered_df["Day"].value_counts())
st.bar_chart(filtered_df["College"].value_counts().head(10))
st.bar_chart(filtered_df["State"].value_counts().head(10))

# Presentation Score Distribution Over Time
st.subheader("📈 Presentation Score Trend Over Days")
score_trend = filtered_df.groupby("Day")["Presentation Score"].mean().reset_index()
fig, ax = plt.subplots()
sns.lineplot(data=score_trend, x="Day", y="Presentation Score", marker="o", ax=ax)
ax.set_title("Average Presentation Score per Day")
ax.set_xlabel("Day")
ax.set_ylabel("Score")
st.pyplot(fig)

# Word Cloud for Feedback
st.subheader("📝 Feedback Analysis")
track_selected = st.selectbox("Select Track for Word Cloud", df["Track"].unique())
feedback_text = " ".join(df[df["Track"] == track_selected]["Feedback"])
wordcloud = WordCloud(width=800, height=400, background_color="black", colormap="coolwarm").generate(feedback_text)
st.image(wordcloud.to_array(), use_column_width=True)
