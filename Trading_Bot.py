import Required_libraries
import Functions
import Technical_Analysis_Engine

# Initial values
symbol = "XAUUSD"
risk_fraction = 0.001
volume = 0.1

# mt5 initialization
if not Required_libraries.mt5.initialize():
    print("Failed to initialize MetaTrader5, error code =", Required_libraries.mt5.last_error())
    quit()

# General logic of the robot
while True:
    print("Hello world")
    # to do -> Getting signals from the technical analysis engine


    # to do -> Deciding to open a position


    # to do -> Open a position or do nothing


    # to do -> Send work report


    # to do -> Wait a little


# Shutdown mt5
Required_libraries.mt5.shutdown() 