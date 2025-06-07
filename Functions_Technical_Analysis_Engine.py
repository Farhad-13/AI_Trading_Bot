import Required_libraries

# Initial values
symbol = "XAUUSD"
risk_fraction = 0.001
volume = 0.1

# mt5 initialization
if not Required_libraries.mt5.initialize(): 
    print("Failed to initialize MetaTrader5, error code =", Required_libraries.mt5.last_error())
    quit()

def send_signal(value, path="signal.txt"):
    with open(path, "w") as f:
        f.write(str(value))


