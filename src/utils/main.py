from src.preprocessing.data_preprocessing import preprocessing
from src.core.engine import run_engine

df = preprocessing("output/kdjlk.json")

results = run_engine(df)

for r in results:
    print("data",r)
