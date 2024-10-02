## Setup Instructions 

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/project_e_commerce.git
   cd project_e_commerce
   ```

2. **Setup Virtual Environment:**

   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On macOS/Linux
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Database:**

   - Ensure MySQL server is running.
   - Set your database URI in `app.config["SQLALCHEMY_DATABASE_URI"]` in `app.py`.

5. **Initialize Database:**

   ```bash
   python app.py
   ```

6. **Run the Application:**

   ```bash
   flask run
   ```


## API Requests

1. **Create Customer**
{
  "order_date": "2024-10-01",
  "delivery_date": "2024-10-05",
  "customer_id": 1,
  "items": [1, 3]  // List of product IDs associated with this order
}

2. **Create Product** 
{
  "product_name": "Wireless Earbuds",
  "price": 129.99,
  "availability": true,
  "stock": 50
}

3. **Create Order**
{
  "order_date": "2024-10-01",
  "delivery_date": "2024-10-05",
  "customer_id": 1,
  "items": [1, 3, 5]
}

