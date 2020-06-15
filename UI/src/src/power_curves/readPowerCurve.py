import pandas as pd
solar_pc = pd.read_csv("C:/Users/fabia/Documents/TUD-3/BEP/Code/UI/src/src/power_curves/solar.csv") 
wind_pc = pd.read_csv("C:/Users/fabia/Documents/TUD-3/BEP/Code/UI/src/src/power_curves/wind.csv") 

shapeSolar = solar_pc.shape
shapeWind  = wind_pc.shape

def convertSolarToPower (zonRef, U):
    # U = 10
    # zonRef = 90

    x_index = int(10*U)
    y_index = int(100- zonRef)
    if y_index > shapeSolar[0]: y_index = shapeSolar[0]-1
    if y_index < 0: y_index = 0
    if x_index > shapeSolar[1]: x_index = shapeSolar[1]-1
    if x_index < 0: x_index = 0

    power = solar_pc.values[y_index, x_index]
    return power*1000


def convertWindToPower (windRef, U):
    # U = 10
    # U = 4.5
    # windRef = 55

    x_index = int(10*U)
    y_index = int(windRef)
    if y_index > shapeWind[0]: y_index = shapeWind[0]-1
    if y_index < 0: y_index = 0
    if x_index > shapeWind[1]: x_index = shapeWind[1]-1
    if x_index < 0: x_index = 0

    power = wind_pc.values[y_index, x_index]
    return power


