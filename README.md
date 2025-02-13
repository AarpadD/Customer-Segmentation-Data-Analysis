## **Customer Segmentation and Data Analysis**
This project analyzes customer purchasing behavior and generates insights using data analysis and visualization tools. It performs database operations to store and query data, generates statistical insights, and implements machine learning (in progress) to predict customer behaviors.

---

## **Project Features**

### **1. Database Operations**
- MySQL database setup and population with customer, item, and purchase data.
- Complex SQL queries to retrieve aggregated insights:
  - Total and average spending per customer.
  - Impact of discounts on sales data.

### **2. Data Analysis**
- Processed large datasets using `pandas` for detailed **customer segmentation**.
- Extracted spending patterns and behavior trends like:
  - Distribution of spending over time.
  - Comparison of spending by customer groups.
- Visualized results using `matplotlib` (e.g., bar plots, histograms).

### **3. Data Structures**
- Custom-built **HashMap** implementation for faster and efficient data indexing during analytics.

### **4. Machine Learning (Work in Progress)**
- **Objective**: Build predictive models for customer purchasing behavior.
- **Plan**:
  - Use clustering algorithms like `K-Means` for segmentation.
  - Implement classification models (e.g., Random Forest, Logistic Regression) for predicting customer churn or future purchase propensity.
- **Progress**:
  - Data preprocessing pipeline setup.
  - Early experimentation with clustering methods.

---

## **Technology Stack**

### **1. Programming**
- Python 3.11

### **2. Libraries and Tools**
- `pandas`: Data manipulation and analysis.
- `matplotlib`: Data visualization.
- `scikit-learn` (to be utilized in ML module).
- `SQLAlchemy`: Database ORM for Python.
- `seaborn`: Advanced visualizations (e.g., heatmaps, pair plots).

### **3. Database**
- MySQL: For database storage and insights.

---

## **Future Improvements**
- Finish implementation of machine learning models for behavioral prediction.
- Build an API for external access to customer insights.
- Deploy dashboards to visualize results in real time using tools like `Dash` or `Streamlit`.

---

## **How to Run the Project**
1. Clone this repository:
   ```bash
   git clone https://github.com/AarpadD/Customer-Segmentation-Data-Analysis.git
   cd Customer-Segmentation-Data-Analysis
   ```

2. Set up the virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For macOS/Linux
   venv\Scripts\activate  # For Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure MySQL database:
   - Update `config.py` with your database credentials.
   - Run the database scripts in `/db_scripts/` to set up the schema.

5. Run the Python scripts:
   ```bash
   python analytics_api.py
   ```

---
