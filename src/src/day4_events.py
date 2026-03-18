import pandas as pd

df = pd.read_csv("data/test_market_data.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])

df = df.sort_values("timestamp")

df["price_change"] = df["price"].diff()
df["direction"] = df["price_change"].apply(lambda x: 1 if x > 0 else (-1 if x < 0 else 0))

#Gli sweep avvengono nei pressi dei minimi/massimi locali, dobbiamo trovarli
df["prev_price"] = df["price"].shift(1)
df["next_price"] = df["price"].shift(-1)
df["local_low"] = (df["price"] < df["prev_price"]) & (df["price"] < df["next_price"]) #Minimo in quanto più basso del prezzo di ora e del precedente


df["recent_low"] = df["price"].rolling(3).min() #prendi le ultime tre righe includa l'attuale e trova il minimo, poi shiftato di 1 per escludere l'attuale
df["sweep_down"] = df["price"] < df["recent_low"].shift(1) #è uno sweep se siamo andati sotto il recent low
df["reclaim"] = df["price"] > df["recent_low"].shift(1) #è un reclaim invece se dopo torniamo sopra il recent lowù

df["failed_break"] = df["sweep_down"] & df["reclaim"] #abbiamo dunque ora tutto per un reversal base, siamo andati sotto il minimo ma poi ritornati sopra

reversal_candidates = df[df["failed_break"]] #ora filtriamo perché non vogliamo analizzare tutte le candele, ma solo quelle dove c'è stato un reversal
print(reversal_candidates)

df["valid_reversal"] = df["failed_break"] & (df["volume"] > 10) #sostenuto da volume? se si valido, al contrario non ci interessa

print(df[[
    "timestamp",
    "price",
    "recent_low",
    "sweep_down",
    "reclaim",
    "failed_break",
    "valid_reversal"
]])