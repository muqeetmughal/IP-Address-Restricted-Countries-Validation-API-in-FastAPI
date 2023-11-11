# IP Address Restricted Countries Validation API in FastAPI

## Running the FastAPI Project

1. **Go to Project Folder:**
   - Chage directory to project folder.

   ```bash
   cd <project_folder_name>
   ```

2. **Create a Virtual Environment:**
   - Create a virtual environment to isolate project dependencies.

   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment:**
   - Activate the virtual environment based on your operating system.

   - On Windows:

     ```bash
     .\venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies:**
   - Install the required dependencies from the `requirements.txt` file.

   ```bash
   pip install -r requirements.txt
   ```

5. **Run the FastAPI Application:**
   - Run the FastAPI application using the `uvicorn` server.

   ```bash
   uvicorn app:app --reload
   ```

   Replace `app` with the filename of your FastAPI application if it's different.

6. **Access the API:**
   - Open your web browser and navigate to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to access the interactive API documentation (Swagger UI). Alternatively, you can use [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) for the ReDoc documentation.

### Testing the `check_country` API

1. **Open API Documentation:**
   - Navigate to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your web browser.

2. **Input IP Address:**
   - In the Swagger UI, find the `/check_country` endpoint and click on it.
   - Click on the "Try it out" button.

3. **Provide IP Address:**
   - Enter a valid IP address in the `ip_address` field.

4. **Execute the Request:**
   - Click on the "Execute" button to send the request.

5. **Review the Response:**
   - Examine the response in the "Response" section. If the request is successful, you should see a JSON response containing information about the IP address.

   **Note:** Ensure that the provided IP address is valid and follows the required format. If the IP address is restricted, the API will return a 403 error with details about the restriction.
