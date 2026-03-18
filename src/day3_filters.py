import pandas as pd

df = pd.read_csv("data/test_market_data.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])

df = df.sort_values("timestamp")

df["spread"] = df["ask"] - df["bid"]
df["mid"] = (df["bid"] + df["ask"]) / 2
df["event_id"] = range(len(df))
df["delta_seconds"] = df["timestamp"].diff().dt.total_seconds()

df["price_change"] = df["price"].diff()
#fino a qua nulla di nuovo, leggo i dati csv, trasformo in variabile di tempo da stringa, ordino per tempo e calcolo le colonne utili

#cominciamo ora a creare mini segnali
df["direction"] = df["price_change"].apply(lambda x: 1 if x > 0 else (-1 if x < 0 else 0)) #"applica la funzione (lambda) se, condizioni, return 1/-1/0" 

df["exhaustion"] = (df["volume"] > 15) & (df["price_change"].abs() < 0.1)

signals = df[(df["volume"] > 15) | (df["price_change"].abs() > 0.25)]

print(signals)