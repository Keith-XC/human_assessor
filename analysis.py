import os.path

import pandas as pd
import numpy as np


def add_one_assessor(human_result_path, summary_path):
    human = human_result_path.split("/")[-1].split("_")[0]

    df_res = pd.read_csv(human_result_path)
    #print(df_res)

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
    df_log = pd.read_csv(summary_path)

    df_log[human] = sorted_res

    df_log["validity_" + human] = pd.notna(df_log[human])
    df_log["preservation_" + human] = df_log['label'] == df_log[human]

    print(f"XAI validity rate by {human} is {df_log[df_log['method']=='XAI']['validity_' + human].sum() / 200}")
    print(f"XAI preservation rate by {human} is {df_log[df_log['method']=='XAI']['preservation_' + human].sum() / 200}")

    print(f"Random validity rate by {human} is {df_log[df_log['method'] == 'Random']['validity_' + human].sum() / 200}")
    print(
        f"Random preservation rate by {human} is {df_log[df_log['method'] == 'Random']['preservation_' + human].sum()/200}")


    df_log.to_csv(summary_path)


results = ["AS_result.csv",
           "Stefano_result.csv",
           "Thao_result.csv"]

for res in results:
    add_one_assessor(human_result_path=os.path.join("results", res),
                     summary_path=os.path.join("results", "log.csv"))