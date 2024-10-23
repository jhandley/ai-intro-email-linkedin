# Intro Email Generator Using LinkedIn Profile

Automates writing intro emails based on a LinkedIn profile. Uses Selenium to scrape LinkedIn profiles and OpenAI's API to generate personalized introductory emails. The emails are designed to request meetings with individuals based on their LinkedIn profile information.

Please DO NOT use this to actually send emails to people. Screen scraping the profile probably violates LinkedIn terms of service and of course sending people AI generated messages is just annoying spam. I wrote this based on a conversation with my daughter to illustrate how easy it is to combine screen scraping and OpenAI calls to do things like this. It is not meant for real world use.

## Requirements

- Python
- Azure OpenAI API account
- LinkedIn account

## Installation

1. Navigate to the project directory:
    ```sh
    cd ai-intro-email-linkedin
    ```
2. Create and activate a virtual environment:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```
3. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```
5. Create a `.env` file in the project directory and add your LinkedIn and OpenAI credentials:
    ```env
    LINKEDIN_EMAIL=your_linkedin_email
    LINKEDIN_PASSWORD=your_linkedin_password
    OPENAI_API_KEY=secret key for your OpenAI account from Azure dashboard
    OPENAI_API_VERSION=API version from Azure dashboard
    OPENAI_API_URL=endpoint for your Azure OpenAI service from dashboard
    OPENAI_MODEL=name of the model e.g. gpt-4o-mini
    SENDER_NAME=your name
    SENDER_BIO=blurb about yourself to introduce yourself in the email
    ```

## Usage

1. Run the script with the LinkedIn profile URL as an argument:
    ```sh
    python main.py <LinkedIn Profile URL>
    ```
2. The script will log in to LinkedIn, scrape the profile, and generate an email based on the profile information.

