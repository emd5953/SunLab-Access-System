## Brief Summary

The **SUN Lab Access System** is a desktop application that tracks and manages access to the SUN Lab using student ID cards. The system logs access records, stores them in Firebase, and allows authorized admins to search, browse, and manage these records via a user-friendly GUI.

This Desktop Application Project Demonstrates CRUD Operations, GUI Interface, and Database Implementation.

## Technologies Used/Pre-Installations

Before you can run the **SUN Lab Access System**, ensure you have the following software and tools installed on your machine:

1. **Python 3.8 or higher**:
   - You can download Python from the official site: [Python Downloads](https://www.python.org/downloads/)

2. **Virtual Environment Tool (venv)**:
   - This comes with Python 3, so you don't need to install it separately.

3. **Firebase Account**: (I used Firebase but you can use any Database Implementation Of Your Choice)

   - Create a Firebase project at [Firebase Console](https://console.firebase.google.com/) and set up your database configuration.
   - You will need to install <code>firebase-admin</code>
   - Open the terminal in your IDE and type in the following commands:
   - <code> pip install firebase-admin </code>
   - Set up your database configuration as needed, and then generate your key for your firebase.
   - The Firebase Generated Key should be pasted in the database folder.
   - Initialize your Firebase Admin using credentials from your key and database URL.
   - If you plan to push your local repo to your GitHub repo, you can use files such as .env and .gitignore to avoid exposing your API key.
   - To set up .env you have to install is using <code> pip install python-dotenv </code>

4. **Git**:
   - Git is needed to clone the repository. Install it from the official site: [Git Downloads](https://git-scm.com/downloads).
   - Next, clone this repository using the following git command: <br> 
   <code>git clone https://github.com/emd5953/SunLab-Access-System.git </code>

5. **GUI Library (Tkinter, PyQt, or Kivy)**:
   - Make sure you have the necessary Python GUI framework installed. I used <code> PyQt5 </code> for this project. 
   - Install it using the command : <code> pip install pyqt5 </code>


6. **IDE or Code Editor** (Optional):
   - Any Python IDE or text editor like VS Code, PyCharm, or Sublime Text.


