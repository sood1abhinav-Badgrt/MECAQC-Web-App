import pandas as pd

df = pd.read_csv('../untrolled_bpt.csv')

aggregated = df.groupby('Facility ID').agg(
    facilityID = ('Facility ID', 'first'),
    facilityName = ('Facility Name', 'first'),
    state = ('State', 'first'),
    capacity = ('capacity', 'sum'),
    annualGeneration = ('Gross_Load_MWh', 'sum'),
    heatInput = ('Heat Input (mmBtu)', 'sum'),
    operatingHours = ('Sum of the Operating Time', 'max'),
    so2Rate = ('SO2 Rate (lbs/mmBtu)', 'first'),
    so2Mass = ('SO2(short tons)', 'sum'),
    noxMass = ('NOx (short tons)', 'sum'),
    co2Mass = ('CO2 (short tons)', 'sum'),
    pm25 = ('PM2.5', 'sum'),
    voc = ('VOC', 'sum')
).reset_index(drop=True)


aggregated.to_csv('../backend/data/plants.csv')
print(f'Done. {len(aggregated)} plants written.')