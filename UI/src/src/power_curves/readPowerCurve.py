import pandas as pd
solar_pc = pd.read_csv("C:/Users/fabia/Documents/TUD-3/BEP/Code/UI/src/src/power_curves/solar.csv") 
wind_pc = pd.read_csv("C:/Users/fabia/Documents/TUD-3/BEP/Code/UI/src/src/power_curves/wind.csv") 


def convertSolarToPower (zonRef, U):
    # U = 10
    # zonRef = 90

    x_index = int(10*U)
    y_index = int(100- zonRef)

    power = solar_pc.values[y_index, x_index]
    return power


def convertWindToPower (windRef, U):
    # U = 10
    # U = 4.5
    # windRef = 55

    x_index = int(10*U)
    y_index = int(windRef)

    power = wind_pc.values[y_index, x_index]
    return power


