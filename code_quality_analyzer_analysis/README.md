## Backend Setup


1. **Create and activate a virtual environment**:

   - If you're using Python 3:

     ```bash
     python3 -m venv venv
     ```

     For Windows:

     ```bash
     python -m venv venv
     ```

     Activate the virtual environment:

     - On macOS and Linux:

       ```bash
       source venv/bin/activate
       ```

     - On Windows:

       ```bash
       .\venv\Scripts\activate
       ```

     You should see `(venv)` at the beginning of your command prompt, indicating that the virtual environment is active.

2. **Install backend dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the database** (assuming you're using Django's default SQLite for development):

   ```bash
   python manage.py migrate
   ```

## Running the Project

Make sure you're in the `code_quality_analyzer_analysis` directory and the virtual environment is active:

```bash
python manage.py runserver
```

This will start the Django development server, usually accessible at `http://localhost:8000`.
