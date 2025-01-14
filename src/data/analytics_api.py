from flask import Flask, jsonify, Response
from sqlalchemy import create_engine
from data_analysis import fetch_aggregated_data, analyze_discounts
from HashMap import HashMap
from charts import plot_age_range_piechart, plot_discount_piechart
import io
import matplotlib
import matplotlib.pyplot as plt

# http://127.0.0.1:5000/charts/age-distribution
# http://127.0.0.1:5000/charts/discount-performance


# Use Flask-compatible matplotlib backend
matplotlib.use('Agg')  # Ensure charts render in non-interactive mode

app = Flask(__name__)

DATABASE_URL = 'mysql+pymysql://arpad:NewStr0ngP%40ssword!@localhost/customer_segmentation'
engine = create_engine(DATABASE_URL)


@app.route('/charts/age-distribution', methods=['GET'])
def age_distribution_chart():
    age_range_map = HashMap()
    with engine.connect() as connection:
        age_range_map = fetch_aggregated_data(connection, age_range_map)

    # Debug: Print data
    print("Age Distribution Data:")
    for pair in age_range_map.map:
        if pair:
            for age_range, total_purchase_amount in pair:
                print(f"{age_range}: {total_purchase_amount}")

    # Generate the chart
    plt.figure()
    plot_age_range_piechart(age_range_map)

    # Save in-memory chart to a stream
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return Response(img.getvalue(), mimetype='image/png')


@app.route('/charts/discount-performance', methods=['GET'])
def discount_performance_chart():
    discount_map = HashMap()
    with engine.connect() as connection:
        discount_map = analyze_discounts(connection, discount_map)

    print("Discount Performance Data:")
    for pair in discount_map.map:
        if pair:
            for discount_applied, data in pair:
                print(f"{discount_applied}: {data}")

    # Generate the chart
    plt.figure()
    plot_discount_piechart(discount_map)

    # Save in-memory chart to a stream
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return Response(img.getvalue(), mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)