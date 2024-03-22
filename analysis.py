import pandas as pd
import numpy as np


result_path = "results/Stefano Lambertenghi_result.csv"
human = "Stefano"

df_res = pd.read_csv(result_path)
print(df_res)

def convert_to_int(val):
    try:
        return np.int_(val)
    except ValueError:
        return np.nan

df_res = df_res.applymap(convert_to_int)

res_array = df_res.values.flatten()

order = np.load("img/idx_mix_order.npy")
sorted_id = np.argsort(order)
sorted_res = res_array[sorted_id]

# map df_res to log.csv
df_log = pd.read_csv("log.csv")

df_log[human] = sorted_res

df_log["preservation_" + human] = df_log['label'] == df_log[human]

print(df_log[df_log['method'] == "XAI"]["preservation_" + human].sum()/200)
print(df_log[df_log['method'] == "Random"]["preservation_" + human].sum()/200)

df_log.to_csv(human+"_log.csv")

