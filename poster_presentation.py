import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from wordcloud import WordCloud
from PIL import Image, ImageEnhance, ImageFilter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import io
import random
import requests

# Set page config for better UI
st.set_page_config(
    page_title="National Poster Presentation",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
/* Main teal color scheme */
.stApp {
    background-color: #e6f2f2;
}

/* Text styling */
* {
    color: #2c3e50;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #2a9d8f;
}
[data-testid="stSidebar"] * {
    color: white !important;
}

/* Cards */
.st-emotion-cache-1y4p8pa, .st-emotion-cache-ocqkz7 {
    background-color: white;
    border-radius: 10px;
    padding: 1rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    margin-bottom: 1rem;
    border: 1px solid #b8e0d4;
}

/* Buttons */
.stButton>button {
    background-color: #2a9d8f;
    color: white !important;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    border: none;
}

/* Charts */
.plotly-chart, .stDataFrame {
    background-color: white;
    border-radius: 8px;
    padding: 8px;
    border: 1px solid #e1e4e8;
}

/* Headers */
h1, h2, h3 {
    color: #264653 !important;
    font-weight: 600;
}

/* Image containers */
.image-container {
    border: 2px solid #b8e0d4;
    border-radius: 10px;
    padding: 10px;
    margin-bottom: 20px;
    background-color: white;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

/* Make sure all button text is white */
button div p {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# =============================================
# DATA GENERATION FUNCTIONS
# =============================================

def generate_data():
    """Generate synthetic dataset for poster presentation event"""
    np.random.seed(42)
    
    tracks = {
        "Biotechnology": "Research in genetic engineering, pharmaceuticals, and biomedical applications",
        "Renewable Energy": "Innovations in solar, wind, and alternative energy technologies",
        "Artificial Intelligence": "Machine learning, neural networks, and AI applications",
        "Environmental Science": "Climate change, conservation, and sustainability research"
    }
    
    colleges = [
        "IIT Delhi", "IIT Bombay", "IIT Madras", "IIT Kharagpur", "IISc Bangalore",
        "NIT Trichy", "BITS Pilani", "University of Delhi", "University of Mumbai",
        "JNU New Delhi", "Anna University", "University of Calcutta", "University of Pune",
        "Amity University", "VIT Vellore", "SRM University", "Manipal University",
        "Christ University", "St. Xavier's College", "Presidency University"
    ] * 20
    
    states = [
        "India", "Maharashtra", "Tamil Nadu", "Karnataka", "Delhi", "West Bengal",
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

# =============================================
# MAIN APP FUNCTION
# =============================================

def main():
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.selectbox("Choose a section", 
        ["Home", "Dataset Generation", "Participation Dashboard", "Feedback Analysis", "Image Gallery"])

    if 'df' not in st.session_state:
        st.session_state.df, st.session_state.tracks = generate_data()
    
    # ========== HOME SECTION ==========
    if app_mode == "Home":
        st.title("National Poster Presentation Event Analysis")
        
        col1, col2 = st.columns([3, 2])
        with col1:
            st.markdown("""
            ## Welcome to the National Poster Presentation Dashboard
            
            This interactive platform provides comprehensive insights into the 4-day National Poster 
            Presentation event featuring 400 participants across 4 specialized tracks.
            """)
            
            st.markdown('<div class="image-container">', unsafe_allow_html=True)
            st.image("poster-competition-page-1030x687.jpg", 
                    caption="Poster Presentation Event", use_column_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown("### Event Statistics")
            
            stats = {
                "Total Participants": 400,
                "Days": 4,
                "Presentation Tracks": 4,
                "Colleges Represented": 50,
                "States Represented": 25
            }
            
            for stat, value in stats.items():
                st.metric(label=stat, value=value)

    # ========== DATASET GENERATION SECTION ==========
    elif app_mode == "Dataset Generation":
        st.title("Dataset Generation")
        
        df = st.session_state.df
        
        with st.expander("View Generated Dataset", expanded=True):
            st.dataframe(df)
        
        with st.expander("Dataset Statistics"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Participants", len(df))
                st.metric("Colleges Represented", df["College"].nunique())
            with col2:
                st.metric("States Represented", df["State"].nunique())
                st.metric("Average Score", round(df["Presentation Score"].mean(), 1))
            with col3:
                st.metric("Tracks", len(st.session_state.tracks))
                st.metric("Average Attendance (mins)", round(df["Attendance Duration (mins)"].mean()))
        
        st.download_button(
            label="Download Dataset as CSV",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name="poster_presentation_data.csv",
            mime="text/csv"
        )

    # ========== DASHBOARD SECTION ==========
    elif app_mode == "Participation Dashboard":
        st.title("Participation Dashboard")
        
        df = st.session_state.df
        
        # Filters
        selected_tracks = st.sidebar.multiselect(
            "Select Tracks", df["Track"].unique(), default=df["Track"].unique())
        selected_days = st.sidebar.multiselect(
            "Select Days", df["Day"].unique(), default=df["Day"].unique())
        selected_states = st.sidebar.multiselect(
            "Select States", df["State"].unique(), default=df["State"].unique()[:5])
        
        filtered_df = df[
            (df["Track"].isin(selected_tracks)) & 
            (df["Day"].isin(selected_days)) & 
            (df["State"].isin(selected_states))
        ]
        
        # Visualizations
        st.subheader("Track-wise Participation")
        fig = px.pie(filtered_df, names="Track", title="Participation by Track",
                    color_discrete_sequence=px.colors.qualitative.Vivid)
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Day-wise Participation")
        fig = px.bar(
            filtered_df.groupby(["Day", "Track"]).size().reset_index(name="Count"),
            x="Day", y="Count", color="Track",
            title="Participants by Day and Track",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("State-wise Participation")
        state_counts = filtered_df["State"].value_counts().reset_index()
        state_counts.columns = ["State", "Count"]
        
        if not state_counts.empty:
            fig = px.choropleth(
                state_counts,
                locations="State",
                locationmode="country names",
                scope="asia",
                color="Count",
                hover_name="State",
                color_continuous_scale="Rainbow",
                title="Participants by State",
                height=500
            )
            fig.update_geos(
                visible=False,
                resolution=50,
                showcountries=True,
                countrycolor="white",
                subunitcolor="white"
            )
            fig.update_layout(
                geo=dict(
                    bgcolor='rgba(0,0,0,0)',
                    lakecolor='#e6f2f2',
                    landcolor='#e6f2f2'
                )
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No data available for selected filters")
        
        # Additional colorful graphs
        st.subheader("Score Distribution Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.box(
                filtered_df,
                x="Track",
                y="Presentation Score",
                color="Track",
                title="Score Distribution by Track",
                color_discrete_sequence=px.colors.qualitative.Dark24
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.histogram(
                filtered_df,
                x="Presentation Score",
                nbins=20,
                color="Track",
                title="Score Distribution",
                marginal="rug",
                color_discrete_sequence=px.colors.qualitative.Light24
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Top Performing Colleges")
        top_colleges = filtered_df.groupby("College")["Presentation Score"].mean().nlargest(10).reset_index()
        fig = px.bar(
            top_colleges,
            x="College",
            y="Presentation Score",
            color="Presentation Score",
            color_continuous_scale="Viridis",
            title="Top 10 Colleges by Average Score"
        )
        st.plotly_chart(fig, use_container_width=True)

    # ========== FEEDBACK ANALYSIS SECTION ==========
    elif app_mode == "Feedback Analysis":
        st.title("Feedback Analysis")
        
        df = st.session_state.df
        selected_track = st.selectbox("Select Track", list(st.session_state.tracks.keys()))
        feedbacks = df[df["Track"] == selected_track]["Feedback"]
        
        st.subheader(f"Word Cloud for {selected_track}")
        wordcloud = WordCloud(width=800, height=400, background_color="white",
                            colormap="viridis").generate(" ".join(feedbacks))
        plt.figure(figsize=(10,5))
        plt.imshow(wordcloud)
        plt.axis("off")
        st.pyplot(plt)
        
        # Text similarity analysis
        st.subheader("Feedback Similarity Analysis")
        if len(feedbacks) > 1:
            vectorizer = TfidfVectorizer(stop_words="english")
            tfidf_matrix = vectorizer.fit_transform(feedbacks)
            similarity_matrix = cosine_similarity(tfidf_matrix)
            
            fig, ax = plt.subplots(figsize=(8,6))
            sns.heatmap(
                similarity_matrix[:10,:10],
                cmap="YlOrRd",
                annot=True,
                fmt=".2f",
                ax=ax
            )
            ax.set_title("Feedback Similarity Matrix (First 10 Entries)")
            st.pyplot(fig)

    # ========== IMAGE GALLERY SECTION ==========
    elif app_mode == "Image Gallery":
        st.title("Image Gallery")
        
        # Local image paths
        day_images = {
            "Day 1": ["Biotechnology-1024x683.jpg"],
            "Day 2": ["AI cover image.jpg"],
            "Day 3": ["images.jpeg"],
            "Day 4": ["61ltIenkqjL._AC_UF894,1000_QL80_.jpg"]
        }
        
        selected_day = st.selectbox("Select Day", list(day_images.keys()))
        
        st.subheader(f"{selected_day} Photos")
        for img_path in day_images[selected_day]:
            try:
                st.markdown('<div class="image-container">', unsafe_allow_html=True)
                img = Image.open(img_path)
                st.image(img, use_column_width=True)
                
                # Image processing
                option = st.selectbox(f"Process {img_path}", 
                                    ["Original", "Grayscale", "Contrast", "Blur", "Edges"])
                
                if option == "Grayscale":
                    processed = img.convert("L")
                elif option == "Contrast":
                    processed = ImageEnhance.Contrast(img).enhance(2.0)
                elif option == "Blur":
                    processed = img.filter(ImageFilter.BLUR)
                elif option == "Edges":
                    processed = img.filter(ImageFilter.FIND_EDGES)
                else:
                    processed = img
                
                st.image(processed, caption=f"Processed: {option}", use_column_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Error loading image: {e}")

if __name__ == "__main__":
    main()