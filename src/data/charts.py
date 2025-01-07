import matplotlib.pyplot as plt


def plot_age_range_piechart(age_range_map):
    # Extract data from HashMap
    labels = []
    sizes = []

    for pair in age_range_map.map:
        if pair:
            for age_range, total_purchase_amount in pair:
                labels.append(age_range)
                sizes.append(total_purchase_amount)

    # Plot the pie chart
    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title("Spending Distribution by Age Range")
    plt.show()


def plot_discount_piechart(discount_map):
    # Extract data from HashMap
    labels = []
    sizes = []

    for pair in discount_map.map:
        if pair:
            for discount_applied, data in pair:
                labels.append(discount_applied)
                sizes.append(data["Total"])

    # Plot the pie chart
    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title("Spending Distribution by Discounts")
    plt.show()