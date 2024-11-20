from faker import Faker
import random
import pandas as pd
import uuid 

faker = Faker()

# Load job skills from CSV file and convert to list
skills_df = pd.read_csv("skills.csv")
skills_list = skills_df['skills'].tolist()

degrees_df = pd.read_csv("skills.csv")
degrees_list = degrees_df['major'].tolist()

# Randomly decide the value of k (number of skills to include in each resume)
k = random.randint(1, 25)

# Ensure k does not exceed the number of available skills
k = min(k, len(skills_list))

# Randomy decide max_nb_chars value for faker.text
nb_chars = random.randint(100, 5000)

def generate_resume():
    return {
        "id": str(uuid.uuid4()),
        "name": faker.name(),
        "email": faker.email(),
        "phone": faker.phone_number(),
        "address": faker.address(),
        "job_title": faker.job(),
        "skills": random.sample(skills_list, k=k), # sample k skills from the list of skills
        "education": f"{faker.random_int(2005, 2026)} - {faker.random_element(['B.Sc', 'M.Sc', 'Ph.D'])} in {faker.random_element(degrees_list)}",
        "experience": faker.text(max_nb_chars=nb_chars)
    }

resumes = [generate_resume() for _ in range(100)] # change 100 to number of resumes needed

# Create DataFrame with a separate column for each key
resumes_rds_df = pd.DataFrame(resumes)

# Create DataFrame with all info as a generic string for each row
resumes_messy_df = pd.DataFrame({
    "resume_data": resumes_rds_df.apply(
        lambda row: f"ID: {row['id']}, Name: {row['name']}, Email: {row['email']}, Phone: {row['phone']}, "
                    f"Address: {row['address']}, Job Title: {row['job_title']}, "
                    f"Skills: {', '.join(row['skills'])}, Education: {row['education']}, "
                    f"Experience: {row['experience']}",
        axis=1
    )
})

# Save DataFrames to CSV files
resumes_rds_df.to_csv("resumes_rds.csv", index=False)
resumes_messy_df.to_csv("resumes_messy.csv", index=False)