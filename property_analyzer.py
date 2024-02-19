import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class PropertyAnalyzer:

    # Class initialized with data frame as argument
    def __init__(self, data):
        self.data = data  # storing data frame as instance of a variable

    # Method to display summary of properties
    def property_summary(self, suburb):

        # Filtering columns which have nulls
        filtered = self.data[(pd.notna(self.data['bedrooms'])) & (pd.notna(self.data['bathrooms'])) & (
            pd.notna(self.data['parking_spaces']))
                             & (self.data['suburb'] == suburb)]
        # Filter to select specific suburb
        if suburb.lower() != "all":
            filtered = filtered[filtered['suburb'] == suburb]

        # for dataframe which is not empty
        if not filtered.empty:
            columns = {
                'bedrooms', 'bathrooms', 'parking_spaces'
            }

            print(f"\n Summary of the property in {suburb}:")
            # Mean, SD, MAX, MIN , Median for each column values
            for values in columns:
                mean_val = filtered[values].mean()
                standard_dev = filtered[values].std()
                median_value = filtered[values].median()
                min_value = filtered[values].min()
                max_value = filtered[values].max()

                print(f"- Average {values} available in the {suburb}(Mean): {mean_val:.3f}")
                print(f"- Property in the {suburb} have at least {standard_dev:.3f} {values}")
                print(f"- The median number of {values} in the {suburb}: {median_value}")
                print(f"- Lowest number of {values} in the {suburb}: {min_value}")
                print(f"- Highest number of {values} in the {suburb}: {max_value}")
                print(f"---------------------------------------------------------\n")

        else:
            print(f"\nNo data available for {suburb} after filtering.")

    # Method to compute average land size
    def average_land_size(self, suburb):
        # Checking existence of the column
        #if 'land_size' not in self.data.columns or 'land_size_unit' not in self.data.columns or 'suburb' not in self.data.columns:
            # raise ValueError("Dataframe must contain 'land_size', 'land_size_unit', and 'suburb' columns.")

        # copy of dataframe to avoid manipulation in the file
        filtered_df = self.data.copy()

        # Filter and convert land size
        filtered_df = filtered_df.dropna(subset=['land_size', 'land_size_unit'])  # Exclude if land_size is null
        # land size in hectors conversion
        filtered_df.loc[filtered_df['land_size_unit'] == 'ha', 'land_size'] *= 10000
        # print(filtered_df['land_size'])

        # Average land size for the all the suburbs
        if suburb.lower() == 'all':
            avg_land_size_all = filtered_df['land_size'].mean()
            print(f"Average land size across all suburbs is: {avg_land_size_all:.2f} m^2")
        elif suburb not in filtered_df['suburb'].values:
            print("Invalid Suburb. Please enter a valid suburb.")
        else:
            avg_land_size_suburb = filtered_df.loc[filtered_df['suburb'] == suburb, 'land_size'].mean()
            print(f"Average land size for the suburb {suburb} is: {avg_land_size_suburb:.2f} m^2")

    # Histogram for the property values
    def prop_val_distribution(self, suburb, target_currency="AUD"):
        currency_dict = {
            "AUD": 1, "USD": 0.66, "INR": 54.25, "CNY": 4.72,
            "JPY": 93.87, "HKD": 5.12, "KRW": 860.92, "GBP": 0.51,
            "EUR": 0.60, "SGD": 0.88
        }

        target_currency = target_currency.upper()

        # Checking user input with dictionary
        if target_currency not in currency_dict:
            print(f"Currency {target_currency} not found. Using AUD for the histogram.")
            conversion_rate = 1 # else AUD exchange rate will be returned
        else:
            conversion_rate = currency_dict[target_currency]

        print(f"Using conversion rate: {conversion_rate} for currency: {target_currency}")  # Validation print

        # Filter of prices and file copy to avoid data manipulation
        filtered_df = self.data.dropna(subset=['price']).copy()

        # Conversion
        filtered_df['converted_price'] = (filtered_df['price'] * conversion_rate) / 1000000

        # for specific suburb
        if suburb.lower() != "all":
            filtered_df = filtered_df[filtered_df['suburb'] == suburb]

        # Plotting
        plt.figure()  # Create a new figure
        plt.hist(filtered_df['converted_price'], bins=50, edgecolor='black', alpha=0.7)
        plt.title(f"Property Value Distribution in {suburb} ({target_currency})")
        plt.xlabel(f"Property Value ({target_currency}) in millions")
        plt.ylabel("Number of Properties")
        filename = f"{suburb}_property_value_distribution_{target_currency}.png"
        plt.savefig(filename)
        plt.show()

    def sales_trend(self):
        # Filter dataframe to only include rows where land_size is -1 and make a copy
        filtered_df = self.data[(self.data['land_size'] != ' ') & (self.data['land_size'] != -1)].copy()
        # print(filtered_df.head())

        # sold_date column to date and time
        filtered_df['sold_date'] = pd.to_datetime(filtered_df['sold_date'], errors='coerce', format='%d/%m/%Y')

        # Picking year from the sold_dates
        filtered_df['year'] = filtered_df['sold_date'].dt.year

        # counting number of properties per year
        yearly_sales = filtered_df.groupby('year').size()

        sales_difference = yearly_sales.diff()
        # Setting up the plot
        fig, ax = plt.subplots()

        # Plotting each segment of the line
        # start_year = yearly_sales.index[0]

        # iterating over year sales with the i+1 year
        for i in range(1, len(yearly_sales)):
            if sales_difference.iloc[i] >= 0: # assigning color for dip and jump
                color = 'green'
            else:
                color = 'red'
            ax.plot([yearly_sales.index[i - 1], yearly_sales.index[i]],
                    [yearly_sales.iloc[i - 1], yearly_sales.iloc[i]],
                    marker='o', color=color)

        ax.set_title('Sales Trend Over the Years for properties')
        ax.set_xlabel('Year')
        ax.set_ylabel('Number of Properties Sold')
        ax.grid(True)

        # plotting line segments between year and year+1
        ax.legend(handles=[plt.Line2D([0], [0], color='green', label='Raise in Sales'),
                           plt.Line2D([0], [0], color='red', label='Dip in Sales')], loc='best')  # label formatting

        plt.tight_layout()
        plt.savefig('sales_trend.png')
        plt.show()

        # Plotting
        # yearly_sales.plot(kind='line', marker='o')
        # plt.title('Sales Trend Over the Years for properties ')
        # plt.xlabel('Year')
        # plt.ylabel('Number of Properties Sold')
        # plt.grid(True)
        # plt.tight_layout()
        # plt.savefig('sales_trend.png')
        # plt.show()

    def reverse_insertion_sort(self, arr):
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and key > arr[j]:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
        return arr

    # repeated search
    def recursive_binary_search(self, arr, low, high, x):
        if high >= low:
            mid = (high + low) // 2
            if arr[mid] == x:
                return True
            elif arr[mid] < x:
                return self.recursive_binary_search(arr, low, mid - 1, x)
            else:
                return self.recursive_binary_search(arr, mid + 1, high, x)
        else:
            return False

    def locate_price(self, target_price, target_suburb):
        # Filtering data frame from blanks and -1
        filtered_df = self.data[(self.data['land_size'] != -1) & (self.data['land_size'] != ' ')].copy()
        print(f"Filtered Dataframe Size: {len(filtered_df)}")

        if target_suburb not in filtered_df['suburb'].unique():
            return False

        suburb_prices = filtered_df[filtered_df['suburb'] == target_suburb]['price'].tolist()
        print(f"Number of Prices in {target_suburb}: {len(suburb_prices)}")

        # Sorting filtered data
        sorted_prices = self.reverse_insertion_sort(suburb_prices)
        # print(f"Top 5 Sorted Prices: {sorted_prices[:5]}")

        # recursive search on the sorted data for designated value
        result = self.recursive_binary_search(sorted_prices, 0, len(sorted_prices) - 1, target_price)
        print(f"Search Result for {target_price}: {result}")

        return result
