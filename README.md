# EasyEat

EasyEat simplifies meal planning by offering a centralized recipe database where users can add, search and manage recipes collaboratively. With secure user authentication, it allows easy access and management, while future updates will introduce admin-only recipe deletion to maintain database integrity. EasyEat is built with Python, Streamlit, and uses Google Sheets for data storage, with API access managed through Google Cloud Console. The app is deployed on Streamlit Cloud for quick accessibility.

## :computer: Try it out!

Explore the application with a demo account! Use the demo credentials provided below to log in.

Click [here](https://easyeat.streamlit.app/) to access the demo.

**Demo Credentials:**

```bash
# Username
demo
# Password
P@ssw0rd123
```

**Note**: Not all features are available in the demo account.

## 🛡️ Admin Panel

EasyEat includes an admin panel available to users with the **Admin** role. The panel provides a user-friendly interface to manage the recipe database and user accounts. Below are the key features:

### Key Admin Features:

- **Delete Recipes:** Admins can permanently remove recipes from the database, ensuring content management is controlled.
- **Delete Users:** Admins have the ability to remove users from the platform if necessary.
- **Change User Roles:** Admins can promote or demote users, assigning or removing the Admin role based on need.

### Admin Panel Preview

Here's a preview of the admin panel:

![Admin Panel Screenshot](src/assets/easy_eat.png)

## ⚡️ Technologies Used

- Python
- Streamlit
- Pandas
- Google Sheets (Database)
- Google Cloud Console (API Access Management)

## 💡 What I Learned

- **Python & Streamlit Development:** Gained deeper experience building web applications with Streamlit and integrating third-party libraries.
- **Google Cloud & Sheets Integration:** Learned how to manage API access via Google Cloud Console and integrate Google Sheets as a lightweight database solution.
- **Authentication in Streamlit:** Integrated secure user authentication using the Streamlit-Authenticator module, improving my understanding of user management.
- **Collaborative Platform Development:** Built a system that handles multiple users interacting with the same recipe database, which helped me understand collaborative workflows in web apps.

## 🔮 Future Improvement Ideas

- **User-specific Recipe Collections:** Allow users to create their own collections or favorite recipes.
- **Google Sheets API Rate Limits**: The app may experience occasional delays or errors when multiple users interact with the database simultaneously, due to Google Sheets API rate limits. This issue resolves automatically after a short period. An improvement to optimize API usage is planned in a future release.

## 🛠️ Build Tools

- [Streamlit Cloud](https://streamlit.io/cloud): For deploying and hosting the application.
- [Google Cloud Console](https://console.cloud.google.com/): For managing API access to Google Sheets.

## 💭 Sources and Inspiration

My understanding of building web apps with Streamlit and integrating external APIs was greatly improved by various resources:

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit-Authenticator](https://github.com/mkhorasani/Streamlit-Authenticator)
- [Google Cloud Documentation](https://cloud.google.com/docs?hl=en)
- [Pandas Documentation](https://pandas.pydata.org/docs/index.html)

## :vertical_traffic_light: Running the Project

To run the project in your local environment, follow these steps:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/maxitech/easy_eat.git
   ```
2. **Create a Virtual Environment:**
   ```bash
   cd easy_eat
   python -m venv venv
   ```
3. **Activate the Virtual Environment:**
   - Windows:
   ```bash
   venv\Scripts\activate
   ```
   - macOS/Linux:
   ```bash
   source venv/bin/activate
   ```
4. **Install the Required Dependencies:** Install all necessary Python packages using `pip`:
   ```bash
   pip install -r requirements.txt
   ```
5. **Set Up Google Authentication:**

   - Inside the `src` folder, create a `.streamlit` directory:

   ```bash
   mkdir -p src/.streamlit
   ```

   - Within this directory, create a `secrets.toml` file and include your Google authentication credentials:

   ```toml
   [google]
   application_credentials = '''{your_downloaded_credentials.json}'''

   db_credentials = '''{your_downloaded_db_credentials.json}'''
   ```
6. **Navigate to the `src` Directory:**
   ```bash
   cd src
   ```
7. **Start the Local Development Server:** Run the Streamlit application:
   ```bash
   streamlit run main.py
   ```
8. **Open** [http://localhost:5801](http://localhost:5801) (or the address shown in your console) in your web browser to view the app.
