from dataclasses import dataclass
import os
import sys
from selenium import webdriver
from dotenv import load_dotenv
from linkedin_scraper import Person, actions
from openai import AzureOpenAI

@dataclass
class OpenAIConfig:
    api_key: str
    api_version: str
    api_url: str
    model: str

def load_openai_config():
    return OpenAIConfig(
        api_key=load_and_verify_from_env("OPENAI_API_KEY"),
        api_version=load_and_verify_from_env("OPENAI_API_VERSION"),
        api_url=load_and_verify_from_env("OPENAI_API_URL"),
        model=load_and_verify_from_env("OPENAI_MODEL"),
    )

def login_to_linkedin(driver, email, password):
    actions.login(driver, email, password)

def get_linkedin_profile(driver, url):
    person = Person(url, driver=driver)
    experience = "\n".join([f"title={e.position_title} institution={e.institution_name}\ndescription={e.description}" for e in person.experiences])
    education = "\n".join([f"degree={e.degree} institution={e.institution_name}\ndescription={e.description}" for e in person.educations])
    return LINKEDIN_PROFILE_TEMPLATE % (person.name, person.about, experience, education)

LINKEDIN_PROFILE_TEMPLATE = """
NAME: %s

ABOUT: 
%s

EXPERIENCE:
%s

EDUCATION:
%s
"""

EMAIL_PROMPT_TEMPLATE = """
Write a brief introductory email to ask for a meeting with a target person, using their LinkedIn profile information. The email should follow this structure:

1. Salutation: Begin with "Dear [first name]."
2. Include a brief elevator pitch introducing the sender. Below is a brief bio of the sender, adapt it to better relate to the experience of the target person.
3. Express interest in the target's experience based on their LinkedIn profile. Ask 1-2 specific questions related to their background based on the LinkedIn profile.
4. Express interest in scheduling a meeting (e.g., "If you are available, I would be very grateful if we could schedule a meeting to discuss [topic of interest].").
5. Ask to schedule a meeting at the target's convenience.
6. Sign off with a polite closing (e.g., "Thank you for your time and consideration. I look forward to hearing from you soon. Best regards, [sender name]").

Make sure the tone is professional and friendly, aiming to show genuine interest in the target's experience and expertise.

Name of the sender: %s

Brief bio of the sender:
--------------------------
%s
--------------------------

LinkedIn profile for the target person:
--------------------------
%s
--------------------------
"""

def call_openai_api(open_ai_config, prompt):
    """Calls OpenAI's Chat Completion API with the given prompt and returns the response."""
    
    client = AzureOpenAI(
        api_key=open_ai_config.api_key,
        api_version=open_ai_config.api_version,
        azure_endpoint=open_ai_config.api_url,
    )

    response = client.chat.completions.create(
        model=open_ai_config.model,
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        temperature=0.7,  # Adjust temperature for creativity vs. focus
    )

    # Extract the generated email from the response
    return response.choices[0].message.content

def generate_email(openai_config, linkedin_profile, sender_name, sender_bio):
    """Given the LinkedIn profile, generate an email to ask for a meeting.
    Fills in the profile in the prompt template and calls OpenAI chat completion
    to generate the email.
    """
    prompt = EMAIL_PROMPT_TEMPLATE % (sender_name, sender_bio, linkedin_profile)
    return call_openai_api(openai_config, prompt)
    
def load_and_verify_from_env(var_name):
    """Loads a variable from the environment and verifies that it is not None."""
    value = os.getenv(var_name)
    if not value:
        print(f"Please set {var_name} in .env file.")
        sys.exit(1)
    return value

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <LinkedIn Profile URL>")
        sys.exit(1)
    linkedin_profile_url = sys.argv[1]

    load_dotenv()  # take environment variables from .env.
    email = load_and_verify_from_env("LINKEDIN_EMAIL")
    password = load_and_verify_from_env("LINKEDIN_PASSWORD")
    openai_config = load_openai_config()
    sender_name = load_and_verify_from_env("SENDER_NAME")
    sender_bio = load_and_verify_from_env("SENDER_BIO")

    driver = webdriver.Chrome()
    print("Logging in to LinkedIn...")
    login_to_linkedin(driver, email, password)
    print(f"Downloading LinkedIn profile {linkedin_profile_url}...")
    profile = get_linkedin_profile(driver, linkedin_profile_url)
    driver.quit()

    print("---------------------------------------------------")
    print(f"LinkedIn profile:")
    print(profile)
    print("---------------------------------------------------")

    print(f"Generating email...")
    email = generate_email(openai_config, profile, sender_name, sender_bio)
    print("---------------------------------------------------")
    print(email)
    print("---------------------------------------------------")
