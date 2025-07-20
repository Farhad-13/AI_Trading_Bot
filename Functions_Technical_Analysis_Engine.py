import Required_libraries

# mt5 initialization
if not Required_libraries.mt5.initialize(): 
    print("Failed to initialize MetaTrader5, error code =", Required_libraries.mt5.last_error())
    quit()

# Initial value of variables
models_and_scalers = {}

# def create_model:

def save_model_and_scaler(model, scaler, symbol):
    models_and_scalers[symbol] = {
        "model": model,
        "scaler": scaler
    }

    with open("all_models.pkl", "wb") as f:
        Required_libraries.pickle.dump(models_and_scalers, f)

def load_model_and_scaler(symbol): 
    with open("all_models.pkl", "rb") as f:
        loaded_data = Required_libraries.pickle.load(f)

    model = loaded_data[symbol]["model"]
    scaler = loaded_data[symbol]["scaler"]

    return model, scaler

def has_model_and_scaler(symbol):
    try:
        with open("all_models.pkl", "rb") as f:
            loaded_data = Required_libraries.pickle.load(f)
        return symbol in loaded_data
    except (FileNotFoundError, EOFError):
        return False


def get_data(symbol, timeframe, months):
    # Calculation of start and end time
    utc_to = Required_libraries.datetime.now()
    utc_from = utc_to - Required_libraries.timedelta(days=30 * months)

    # Receive data
    rates = Required_libraries.mt5.copy_rates_range(symbol, timeframe, utc_from, utc_to)

    if rates is None or len(rates) == 0:
        raise ValueError(f"دیتا برای {symbol} دریافت نشد.")

    df = Required_libraries.pd.DataFrame(rates)
    df['time'] = Required_libraries.pd.to_datetime(df['time'], unit='s')
    return df


# def get_recent_candles:

# def train_model:

# def warm_train:

# def predict_future_price:

def send_signal(predicted_price, symbol, risk_fraction, volume):
    signal = {
        "predicted_price": predicted_price,
        "symbol": symbol,
        "risk_fraction": risk_fraction,
        "volume": volume
    }

    path = f"signals/{symbol}.txt"

    try:
        # Create signals directory if it doesn't exist
        Required_libraries.os.makedirs("signals", exist_ok=True)

        with open(path, "w") as f:
            Required_libraries.json.dump(signal, f)

    except Exception as e:
        print(f"[{symbol}] Error writing signal:", e)


