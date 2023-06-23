import pandas as pd


def transform_data(data):
    # Load data into pandas dataframe.
    df = pd.DataFrame.from_dict(data)

    def parse_currency_string(price_str):
        return float(price_str.replace('$', '').replace(',', ''))

    # Format price string as a numeric value.
    df['price'] = df['price'].apply(parse_currency_string)

    # Group by card name and calculate statistics.
    grouped_df = df.groupby('cardName').agg({
        'price': ['mean', 'min', 'max', 'std'],
    })

    # Replace NaN values in 'std' column with -1.
    grouped_df['price', 'std'] = grouped_df['price', 'std'].fillna(-1)

    grouped_df.columns = ['avgPrice', 'lowerBound', 'upperBound', 'priceStdDev']

    transform_output = grouped_df

    # Find peak price for each item.
    max_price_indices = df.groupby(['cardName'])[['price']].idxmax()
    df_peak_prices = df.loc[max_price_indices.values.flatten()].set_index('cardName')

    transform_output["peakPrice"] = df_peak_prices["price"].values  # Add peak prices column
    transform_output["peakPriceDate"] = df_peak_prices["txnDate"].values  # Add peak dates column

    transform_output["avgPrice"] = transform_output["avgPrice"].apply(lambda x: round(x, 3))
    transform_output["lowerBound"] = transform_output["lowerBound"].apply(lambda x: round(x, 3))
    transform_output["upperBound"] = transform_output["upperBound"].apply(lambda x: round(x, 3))
    transform_output["priceStdDev"] = (transform_output["priceStdDev"].apply(lambda x: round(x, 3)))
    transform_output["peakPrice"] = (transform_output["peakPrice"].apply(lambda x: round(x, 3)))

    columns_to_keep = ["cardName", "avgPrice", "lowerBound", "upperBound", "priceStdDev", "peakPrice", "peakPriceDate"]

    transform_output = transform_output.reset_index()[columns_to_keep]

    return transform_output.to_dict('records')