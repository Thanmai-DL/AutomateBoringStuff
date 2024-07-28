# AutomateBoringStuff
## Cold Email
### Prerequisites
### 1. Enable Gmail API in Google Cloud Console
1. **Go to the Google Cloud Console**:
   - Navigate to [Google Cloud Console](https://console.cloud.google.com/) and log in using the email you wish to send the emails from.
   - Update the value of the sender variable in `compose.py`.  
     ![image](https://github.com/Thanmai-DL/AutomateBoringStuff/assets/76940939/b66a64e8-7b16-4ab9-a61f-c3c3009c4554)
2. **Create a New Project**:
   - Click on the project drop-down at the top of the page.
   - Select "New Project" and give it a name.
   - Click "Create".
3. **Enable Gmail API**:
   - In the Google Cloud Console, go to "APIs & Services" > "Library".
   - Search for "Gmail API" and click on it.
   - Click "Enable".
4. **Create OAuth 2.0 Credentials**:
   - Go to "APIs & Services" > "Credentials".
   - Click "Create Credentials" and select "OAuth 2.0 Client IDs".
   - Configure the consent screen if you haven't already.
   - Fill in the required information and save.
   - Choose "Desktop app" as the application type.
   - Click "Create".
   - Download the `credentials.json` file into the same folder containing the code.
### 2. Install Python 3.12 and Necessary Python Libraries
Open your terminal or command prompt and run the following command to install the required libraries:
```bash
pip install --upgrade google google-api-core google-api-python-client google-auth google-auth-httplib2 google-auth-oauthlib googleapis-common-protos
```
### 3. Additional Files
Create and save the following files in the same folder containing the code:
  1. `template.html` file containing the HTML code of the message to be sent as the body of the email.
  2. `info.txt` file containing the details required to compose the email as shown below:
     - If the full name of the person contains a middle name.  
       ![image](https://github.com/Thanmai-DL/AutomateBoringStuff/assets/76940939/c62044c5-38d2-40bd-baa7-95d77f3e1b63)
     - If the full name of the person does not contain a middle name.  
       ![image](https://github.com/Thanmai-DL/AutomateBoringStuff/assets/76940939/d1666d4b-8988-4166-b320-f4080e31e083)  
     - To send email to a known email address.  
       ![image](https://github.com/user-attachments/assets/ce5f6623-6b19-411c-bd1c-9f5db60bafa6)  
    _Note: Save the file with a new line after the last entry as shown in the images._  
  3. `[FirstnameLastname]_Resume.pdf` resume file and update the value of the attachment variable in `compose.py`.  
     ![image](https://github.com/Thanmai-DL/AutomateBoringStuff/assets/76940939/437b2f2b-5a61-4f54-bb0d-a9559ab900e6)
### Sending the Mail
- Update the details in `info.txt`.
- Run the below commands:
  ```bash
  chmod +x ./send.sh
  sh ./send.sh
  ```
