# EasyEat
EasyEat is a user-friendly platform designed to eliminate the daily struggle of deciding what to eat. It features a centralized recipe database where users can search for, add, and manage recipes collaboratively. All users share the same recipe collection, making it a communal space for culinary inspiration. Authentication is required, allowing users to log in, log out, and manage their accounts securely. While all users can currently add and search for recipes, the ability to delete recipes will soon be restricted to admins to ensure the integrity of the shared database. EasyEat is powered by Python, Streamlit and with Google Sheets as lightweight database. The authentication and database management are handled through the Google Cloud Console, and the app is deployed on Streamlit Cloud.
Click [here](https://easyeat.streamlit.app/) to visit the deployed app!

## :computer: Try it out!
Explore the application with a demo account! Use the demo credentials provided below to log in.

Click [here](https://memoryproto.netlify.app/) to access the demo.
  
  **Demo Credentials:**
   ```bash
   # Username
   demo
   # Password
   P@ssw0rd123
   ```

## :vertical_traffic_light: Running the Project
To run the project in your local environment, follow these steps: 
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/maxitech/easy_eat.git
2. **Create a Virtual Environment:**
   ```bash
   cd easy_eat
   python -m venv venv
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
 6. **Configure Local Development:**
    For local development, you need to update the path to `config.yaml` in the `config.py` module located in the `utils` folder. Open `src/utils/config.py` and change the path to:
    ```python
    config_path = '../config.yaml'
    ```
 7. **Navigate to the `src` Directory:**
    ```bash
    cd src
    ```
 8. **Start the Local Development Server:** Run the Streamlit application:
    ```bash
    streamlit run main.py
    ```
 9. **Open** [http://localhost:5801](http://localhost:5801) (or the address shown in your console) in your web browser to view the app.
