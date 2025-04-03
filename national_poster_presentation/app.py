import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
data = pd.read_csv('poster_presentation_data.csv')

# Title of the app
st.markdown("<h1 style='color: #4CAF50;'>National Poster Presentation Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #FF5722;'>Welcome to the National Poster Presentation Dashboard</h3>", unsafe_allow_html=True)
st.markdown("This dashboard provides insights into the participation trends and feedback for the event.")

# Sidebar for filters
st.sidebar.markdown("<h3 style='color: #2196F3;'>Filters</h3>", unsafe_allow_html=True)
selected_track = st.sidebar.selectbox("Select Track", data['Track'].unique())
selected_day = st.sidebar.selectbox("Select Day", data['Day'].unique())

# Filter data based on selections
filtered_data = data[(data['Track'] == selected_track) & (data['Day'] == selected_day)]

# Display filtered data
st.subheader("Filtered Data")
st.write(filtered_data[['Participant ID', 'Name', 'Email', 'Rating', 'Feedback']])

# Participation trends visualization
st.subheader("Participation Trends")
fig, ax = plt.subplots()
sns.countplot(data=filtered_data, x='Day', hue='Track', ax=ax, palette='Set2')
plt.title("Participation by Day and Track")
st.pyplot(fig)

# Show the dataset
if st.checkbox("Show Full Dataset"):
    st.write(data)

# Image Gallery
st.sidebar.markdown("<h3 style='color: #2196F3;'>Image Gallery</h3>", unsafe_allow_html=True)
if st.sidebar.checkbox("Show Image Gallery"):
    from image_processing import display_image_gallery
    display_image_gallery()

# Footer
st.write("Developed by the Website Development Team for National Poster Presentation Event.")
