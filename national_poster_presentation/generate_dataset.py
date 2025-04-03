import pandas as pd
import random
from faker import Faker
import os

fake = Faker()

# Define categories
tracks = ["AI & ML", "Healthcare Tech", "Renewable Energy", "Cybersecurity"]
days = ["Day 1", "Day 2", "Day 3", "Day 4"]

# Generate dataset
data = []
for i in range(400):
    participant_id = f"P{i+1:03d}"
    name = fake.name()
    email = fake.email()
    track = random.choice(tracks)
    day = random.choice(days)
    rating = random.randint(1, 5)  # Feedback rating (1-5)
    feedback = fake.sentence()  # Random feedback text
    
    data.append([participant_id, name, email, day, track, rating, feedback])

# Create DataFrame
df = pd.DataFrame(data, columns=["Participant ID", "Name", "Email", "Day", "Track", "Rating", "Feedback"])

# Save to CSV in the current directory
output_file = os.path.join(os.getcwd(), "poster_presentation_data.csv")

try:
    df.to_csv(output_file, index=False)
    print(f"Dataset generated and saved as '{output_file}'")
except Exception as e:
    print(f"Error saving dataset: {e}")

# Debug information
print(f"Current working directory: {os.getcwd()}")
