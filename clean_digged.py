import pandas as pd

path = 'test.csv'


links = pd.read_csv(path)

links['digged'] = False

links.to_csv(path)