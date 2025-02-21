import yfinance as yf
import pandas as pd


# Function to load the industry EBITDA data from the Excel file
def load_industry_ebitda_data(file_path):
    df = pd.read_excel(file_path, usecols=[0, 1], header=None)
    industry_ebitda_map = pd.Series(df[1].values, index=df[0]).to_dict()
    return industry_ebitda_map


# Function to get financial information from Yahoo Finance
def get_financial_info(ticker):
    ticker_data = yf.Ticker(ticker)

    # Retrieve financial data from Yahoo Finance
    current_price = ticker_data.info.get('currentPrice')
    dividend_rate = ticker_data.info.get('dividendRate')
    dividend_yield = ticker_data.info.get('dividendYield')
    closing_price = ticker_data.info.get('previousClose')
    EBITDA = ticker_data.info.get('ebitda')
    revenue = ticker_data.info.get('totalRevenue')

    # Calculate EBITDA margin
    EBITDA_margin = (EBITDA / revenue) * 100 if revenue else 0

    return {
        'current_price': current_price,
        'dividend_rate': dividend_rate,
        'dividend_yield': dividend_yield,
        'closing_price': closing_price,
        'EBITDA': EBITDA,
        'revenue': revenue,
        'EBITDA_margin': EBITDA_margin,
        'industry': ticker_data.info.get('industryDisp')
    }


# Function to calculate the average stock growth over the last 5 years
def calculate_average_growth(data_history):
    stock_closing_record = data_history['Close'].tolist()
    changes = [
        (stock_closing_record[x] - stock_closing_record[x - 1]) / stock_closing_record[x - 1]
        for x in range(1, len(stock_closing_record))
    ]
    average_growth = sum(changes) / len(changes) if changes else 0
    return average_growth


# Function to display the company's financial information
def display_financial_info(user_input, financial_info, industry_average_EBITDA, average_growth):
    print(f"-----{user_input} financial info-----")
    print(f"Current price: {financial_info['current_price']}")
    print(f"Day -1 closing price: {financial_info['closing_price']}")
    print(f"Dividend rate: {financial_info['dividend_rate']}")
    print(f"Dividend yield: {financial_info['dividend_yield']}")
    print(f"EBITDA: {financial_info['EBITDA']}")
    print(f"Revenue: {financial_info['revenue']}")
    print(f"EBITDA margin: {financial_info['EBITDA_margin']:.2f} %")
    print(f"{financial_info['industry']} industry EBITDA margin average: {industry_average_EBITDA * 100:.2f} %")
    print(f"Stock average growth: {average_growth * 100:.2f} %")


# Main function to run the program
def main():
    excel_file = 'industry_average_ebitda_margin.xlsx'
    industry_ebitda_map = load_industry_ebitda_data(excel_file)

    user_input = input("Enter the company symbol here: ")
    financial_info = get_financial_info(user_input)

    industry = financial_info['industry']
    industry_average_EBITDA = industry_ebitda_map.get(industry, 0)

    data_history = yf.Ticker(user_input).history(period="5y", interval="1wk")
    average_growth = calculate_average_growth(data_history)

    display_financial_info(user_input, financial_info, industry_average_EBITDA, average_growth)


# Run the program
if __name__ == '__main__':
    main()
