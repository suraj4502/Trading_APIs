from fastapi import FastAPI, HTTPException, Query
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from database.db import database

app = FastAPI()



# Pydantic models
class TradeDetails(BaseModel):
    buySellIndicator: str = Field(description="A value of BUY for buys, SELL for sells.")
    price: float = Field(description="The price of the Trade.")
    quantity: int = Field(description="The amount of units traded.")

class Trade(BaseModel):
    asset_class: Optional[str] = Field(alias="assetClass", default=None, description="The asset class of the instrument traded. E.g. Bond, Equity, FX...etc")
    counterparty: Optional[str] = Field(default=None, description="The counterparty the trade was executed with. May not always be available")
    instrument_id: str = Field(alias="instrumentId", description="The ISIN/ID of the instrument traded. E.g. TSLA, AAPL, AMZN...etc")
    instrument_name: str = Field(alias="instrumentName", description="The name of the instrument traded.")
    trade_date_time: datetime = Field(alias="tradeDateTime", description="The date-time the Trade was executed")
    trade_details: TradeDetails = Field(alias="tradeDetails", description="The details of the trade, i.e. price, quantity")
    trade_id: str = Field(alias="tradeId", default=None, description="The unique ID of the trade")
    trader: str = Field(description="The name of the Trader")




# API endpoints

## output on the root page
@app.get("/")
def read_root():
    return {"Message": "Hello Team 👋🏼 Suraj here and this is the API that you asked for. Please look into the instructions below ", 
            "👉🏼Instructions":{
                "🟢To get all trades": "http://127.0.0.1:8000/trades",
                "🟢To get trade by id" : "http://127.0.0.1:8000/trades/{id [from 1 to 102]} ,eg == 'http://127.0.0.1:8000/trades/45'",
                "🟢Trade by Specific condition" : "http://127.0.0.1:8000/specificTrades?{condition}={condition_value}, eg == 'http://127.0.0.1:8000/specificTrades?trader=Suraj%20Yadav'",
                "🟢Advance_Filetering" : "http://127.0.0.1:8000/advancedSearch?{condition}={condition_value}, eg == 'http://127.0.0.1:8000/advancedSearch?assetClass=FX'",
                "🟢pagination" : " http://127.0.0.1:8000/trades/?page={page_no}&limit={number_of_records}, eg == 'http://127.0.0.1:8000/trades/?page=1&limit=10'",
                },
            "Thak You" : "☺️"
            }


# for fetching all trades
@app.get("/trades")
def get_trades() -> List[dict]:
    return database


# Pagination
@app.get("/trades/")
def get_trades(page: int = 1, limit: int = 10):
    # Calculate the start and end indices for pagination
    start_index = (page - 1) * limit
    end_index = start_index + limit

    # Slice the trade data based on the indices
    paginated_trades = database[start_index:end_index]

    return paginated_trades


# getting trades by id
@app.get("/trades/{trade_id}")
def get_trade_by_id(trade_id: str):
    for trade in database:
        if trade["trade_id"] == trade_id:
            return trade
    return {"message": "Trade not found"}


#getting Trades based on specific conditions    
@app.get("/specificTrades")
def get_trades_specific(
    counterparty: str = Query(None),
    instrumentId: str = Query(None),
    instrumentName: str = Query(None),
    trader: str = Query(None)
):
    filtered_trades = []

    for trade in database:
        if (
            (counterparty is None or trade["counterparty"] == counterparty) and
            (instrumentId is None or trade["instrument_id"] == instrumentId) and
            (instrumentName is None or trade["instrument_name"] == instrumentName) and
            (trader is None or trade["trader"] == trader)
        ):
            filtered_trades.append(trade)

    return filtered_trades



# Advance Filtering
@app.get("/advancedSearch")
def advanced_search(
    assetClass: str = Query(None),
    start: str = Query(None),
    end: str = Query(None),
    maxPrice: float = Query(None),
    minPrice: float = Query(None),
    tradeType: str = Query(None)
) -> List[dict]:
    filtered_trades = []

    for trade in database:
        if (
            (assetClass is None or assetClass in trade["asset_class"]) and
            # 2023-05-26 14:00 sample data input
            (start is None or datetime.fromisoformat(str(trade["trade_date_time"])) >= datetime.strptime(start, "%Y-%m-%d %H:%M")) and
            (end is None or datetime.fromisoformat(str(trade["trade_date_time"]) )<= datetime.strptime(end, "%Y-%m-%d %H:%M")) and
            (maxPrice is None or float(trade["trade_details"]["price"]) <= maxPrice) and
            (minPrice is None or float(trade["trade_details"]["price"]) >= minPrice) and
            (tradeType is None or trade["trade_details"]["buySellIndicator"] == tradeType)
        ):
            filtered_trades.append(trade)

    return filtered_trades



