**Download requirements**
- Set Up Google Cloud Vision
    - Create a Google Cloud Project:
        - Go to the Google Cloud Console.
        - Create a new project (or use an existing one).
- Enable the Vision API:
        - In your Google Cloud project, navigate to APIs & Services.
        - Search for Vision API and enable it.
  - Generate Service Account Credentials:
        - Go to IAM & Admin > Service Accounts.
        - Create a service account and generate a JSON key file.
        - Download the JSON key file to your local machine.
- Install python 3
- From a terminal in the working directory, set the following:
      ```bash
  set GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\your\service-account-file.json"
  ```
  In other words, set GOOGLE_APPLICATION_CREDENTIALS equal to the directory where your JSON key is stored.
- From the same terminal in the working directory, run the following:
    ```bash
    python3 -m venv venv
    .\venv\Scripts\activate
    pip install -r requirements.txt
    python main.py
    ```
This is how to run the code from a local machine. Feel free to reach out if you have questions to robinxbaker@gmail.com
