import pandas as pd

df = pd.read_csv("data/test_market_data.csv")   # leggo 
df["timestamp"] = pd.to_datetime(df["timestamp"])  # il tempo non è più una stringa ma una variabile temporale

df = df.sort_values("timestamp")   # ordine temporale

df["spread"] = df["ask"] - df["bid"]    # market data ci da ask e bid, posso dunque calcolare spread
df["mid"] = (df["bid"] + df["ask"]) / 2     # spread/2; spesso più utile del last price per la microstruttura
df["event_id"] = range(len(df))     # per l'analisi microstrutturale mi è più utile organizzare in base ad "eventi", non "secondi" 
df["delta_time"] = df["timestamp"].diff()
df["delta_seconds"] = df["timestamp"].diff().dt.total_seconds()  # quanti secondi passano tra gli eventi; posso avere 40 eventi e setup in 3 secondi oppure 40 eventi e setup in 40 secondi
df["price_change"] = df["price"].diff() #esercizio ChatGPT, "fai colonna con differenza prezzo"

print(df[["timestamp", "event_id", "price", "mid", "spread", "delta_seconds"]]) #esercizio ChatGPT
print(df)
print("\nTIPI DATI:")
print(df.dtypes)
print("\nDIMENSIONI:")
print(df.shape)