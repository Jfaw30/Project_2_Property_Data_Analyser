import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Import the PropertyAnalyzer and PropertyData classes
from property_analyzer import PropertyAnalyzer
from property_data import PropertyData


def main():
    # Load the property data from a CSV file
    property_data = PropertyData('property_information.csv')  # Replace 'property_data.csv' with your data file's path

    # Extract the data from the PropertyData object
    data = property_data.extract_data()

    # Create an instance of the PropertyAnalyzer class
    analyzer = PropertyAnalyzer(data)

    # p_data = PropertyData(data)

    while True:
        print("\nProperty Analyzer Menu:")
        print("1. Property Summary")
        print("2. Average Land Size")
        print("3. Property Values")
        print("4. Sales Trend of the properties over the years")
        print("5. Locate Price")
        print("6. Currency Exchange to AUD")
        print("7. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            suburb = input("Enter the suburb name, First letter should be in caps eg: Clayton : ")
            analyzer.property_summary(suburb)
        elif choice == '2':
            suburb = input("Enter the suburb First letter should be in caps eg: Clayton ('all' for all suburbs): ")
            analyzer.average_land_size(suburb)
        elif choice == '3':
            suburb = input("Enter the suburb First letter should be in caps eg: Clayton ('all' for all suburbs): ")
            target_currency = input("Enter the target currency (e.g., AUD, USD): ")
            analyzer.prop_val_distribution(suburb, target_currency)
        elif choice == '4':
            analyzer.sales_trend()
        elif choice == '5':
            target_price = float(input("Enter the target price: "))
            target_suburb = input("Enter the target suburb First letter should be in caps eg: Clayton: ")
            result = analyzer.locate_price(target_price, target_suburb)
            if result:
                print(f"The target price {target_price} was found in {target_suburb}.")
            else:
                print(f"The target price {target_price} was not found in {target_suburb}.")
        elif choice == '6':
            print("Enter the Exchange rate, below are the exchange rate details for your reference")
            print("AUD: 1, USD: 0.66, INR: 54.25, CNY: 4.72, JPY: 93.87, HKD: 5.12, KRW: 860.92, GBP: 0.51,EUR: 0.60, "
                  "SGD: 0.88")
            exchange_rate = float(input("Enter the Exchange rate"))
            result = property_data.currency_exchange(exchange_rate)
            print(result)
        elif choice == '7':
            print("Thank you for using Property Analyzer.")
            break
        else:
            print("Invalid choice. Please enter a valid option (1-6).")


if __name__ == "__main__":
    main()


# 3.1 extracting data
# df = pd.read_csv("property_data.csv")

# 3.2 instance of the PropertyAnalyzer class with the dataframe 'df'
# pa = PropertyAnalyzer(df)

# 3.3 Currency_exchange
# pa.currency_exchange(54.25)
# displays numpy array ['$52351250.0' '$21971250.0' '$47794250.0' ... '$nan' '$nan' '$nan']

# 3.4  specific suburb, "Clayton" pa.property_summary("Clayton") Displays
# Average bathrooms available in the Clayton(Mean): 1.632
# Property in the Clayton have at least 1.112 bathrooms
# The median number of bathrooms in the Clayton: 1.0
# Lowest number of bathrooms in the Clayton: 1.0
# Highest number of bathrooms in the Clayton: 20.0

# 3.5 Test the average_land_size method for all suburbs and then for a specific suburb
# pa.average_land_size("all")
# pa.average_land_size("clayton")
# displays Average land size across all suburbs is: 650.42 m^2
# displays Average land size for the suburb Clayton is: 571.04 m^2

# 3.6 prop_val_distribution method for all suburbs and then for a specific suburb
# pa.prop_val_distribution("all")
# pa.prop_val_distribution("Melbourne")
# Pops up histogram image for the all the suburb
# Pops up histogram image for Melbourne suburb

# 3.7  sales_trend method
# pa.sales_trend()
# Pops up image of sales trend for the all year in the file

# 3.8 locate_price
# pa.locate_price(881000.0, "Clayton")
# displays Search Result for 881000.0: True
# The target price 881000.0 was found in Clayton.
