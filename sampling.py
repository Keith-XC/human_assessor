import glob
import os

import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas as pd



def get_200_digit(path, initial_idx=0):
    idx = initial_idx
    files = glob.glob(os.path.join(path, "*.npy"))
    all = []
    for digit in range(10):
        files_digit = [f for f in files if f.split('/')[-1][6] == str(digit)]
        #print(f"find {len(files_digit)} files for digit {digit}")
        select_digits = np.random.choice(files_digit, size=20)
        for digit_path in select_digits:
            method = "XAI" if path == path_c else "Random"
            info = {
                 "method": method,
                 "label": digit,
                 "path": digit_path,
                 "id": idx
                    }
            idx += 1
            csv_logger("results/log.csv", info)
        all = np.concatenate((all, select_digits))
    return all


def csv_logger(filepath: str, log_info: dict):
    if not filepath.endswith(".csv"):
        filepath += ".csv"

    # write CSV to file
    if not os.path.exists(filepath):
        # create csv file header
        with open(filepath, 'w', encoding='UTF8') as f:
            writer = csv.writer(f,
                                delimiter=',',
                                quotechar='"',
                                quoting=csv.QUOTE_MINIMAL,
                                lineterminator='\n')
            # write the header
            writer.writerow(list(log_info.keys()))

    with open(filepath, 'a', encoding='UTF8') as f:
        writer = csv.writer(f,
                            delimiter=',',
                            quotechar='"',
                            quoting=csv.QUOTE_MINIMAL,
                            lineterminator='\n')
        writer.writerow(list(log_info.values()))


def plot_400_digit():
    df = pd.read_csv('results/log.csv')
    big_image_xai = np.zeros((560, 280))
    for i in range(20):
        for j in range(10):
            index = i * 10 + j
            img = np.load(df['path'][index]).reshape(28,28)
            big_image_xai[i*28:(i+1)*28, j*28:(j+1)*28] = img

    big_image_random = np.zeros((560, 280))
    for i in range(20):
        for j in range(10):
            index = i * 10 + j + 200
            img = np.load(df['path'][index]).reshape(28,28)
            big_image_random[i*28:(i+1)*28, j*28:(j+1)*28] = img
    plt.figure(figsize=(20,10),dpi=100)
    plt.subplot(1,2,1)
    plt.imshow(big_image_xai, cmap='gray')
    plt.axis('off')
    plt.subplot(1, 2, 2)
    plt.imshow(big_image_random, cmap='gray')
    plt.axis('off')
    #plt.show()
    plt.savefig("ordered_digits.png")


def mixed_img():
    big_image = np.zeros((28, 280))
    idx_mix_order = np.random.permutation(400)
    print(idx_mix_order)
    df = pd.read_csv("results/log.csv")
    np.save(os.path.join("img",'idx_mix_order.npy'), idx_mix_order)
    for i in range(400):
        path = df[df['id']==idx_mix_order[i]]['path'].values[0]
        img = np.load(path).reshape(28, 28)
        resi = i % 10
        big_image[:, resi*28:(resi+1)*28] = img
        if i % 10 == 9:
            plt.figure(figsize=(10,1.5))
            plt.imshow(big_image, "gray")
            plt.axis('off')
            plt.savefig(os.path.join("img", str(int((i-resi)/10)) + "_mix.png"))
            plt.close()

path_c = "digit_of_sm_rr/_C_C_sm"
path_r = "digit_of_sm_rr/_R_R"

plt.style.use('dark_background')


seed = 13
np.random.seed(seed)
print(seed)

if os.path.exists("results/log.csv"):
    os.remove("results/log.csv")
xai_all = get_200_digit(path_c, initial_idx=0)
random_all = get_200_digit(path_r, initial_idx=200)
plot_400_digit()

mixed_img()

