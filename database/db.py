from datetime import datetime , timedelta
import random
# Mocked database records
database = [
    {
        "trade_id": "1",
        "asset_class": "Equity",
        "counterparty": "ABC Corp",
        "instrument_id": "AAPL",
        "instrument_name": "Apple Inc.",
        "trade_date_time": datetime(2023, 5, 26, 10, 30),
        "trade_details": {
            "buySellIndicator": "Buy",
            "price": 200.0,
            "quantity": 100
        },
        "trader": "John Doe"
    },
    # will add more records
]






# Generating 100 more similar trades with unique trade IDs and traders
for i in range(2, 102):
    trade = database[0].copy()  # Copy the structure of the first trade record
    trade["trade_id"] = str(i)
    
    trade["asset_class"] = random.choice(["Equity","Bonds", "Commodities", "FX","Options"]),
    
    trade["counterparty"] = random.choice(["ABC Corp", "XYZ Inc", "DEF Ltd", "GHI Company", "JKL Enterprises"])
    
    trade["instrument_id"] = random.choice(["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"])
    
    trade["instrument_name"] = random.choice(["Apple Inc.", "Alphabet Inc.", "Microsoft Corporation", "Amazon.com, Inc.", "Tesla, Inc."])
    
    trade["trade_date_time"] = random.choice(['2023-05-26T10:00:00', '2023-05-26T12:00:00',
                                              '2023-05-26T14:00:00', '2023-05-26T15:30:00',
                                              '2023-05-26T11:30:00', '2023-05-26T15:59:00'])
    
    trade["trade_details"]["buySellIndicator"] = random.choice(['Buy','Sell'])
    trade["trade_details"]["price"] += random.uniform(-10.0, 10.0)  # Add random variation to the price
    trade["trade_details"]["quantity"] += random.randint(-10, 10)
    
    trade["trader"] = random.choice(["John Doe", "Suraj Yadav", "Zayn Malik", "Charles Olivera", "Colby Covington"])
    database.append(trade)
    
    


# print(len(database))
# print(database[0])