import os
import matplotlib.pyplot as plt
import matplotlib.image as mping
import csv
import sys


def img_path(i: int):
    return os.path.join("img", str(i)+"_mix.png")


def invalid_input(string: str):
    if string == "q":
        sys.exit()
    if len(string.split(",")) == 10:
        return False
    else:
        return True


def csv_logger(filepath: str, input_list: list):
    if not os.path.exists(filepath):
        # create csv file header
        with open(filepath, 'w', encoding='UTF8') as f:
            writer = csv.writer(f,
                                delimiter=',',
                                quotechar='"',
                                quoting=csv.QUOTE_MINIMAL,
                                lineterminator='\n')
            # write the header
            writer.writerow([1,2,3,4,5,6,7,8,9,10])

    with open(filepath, 'a', encoding='UTF8') as f:
        writer = csv.writer(f,
                            delimiter=',',
                            quotechar='"',
                            quoting=csv.QUOTE_MINIMAL,
                            lineterminator='\n')
        writer.writerow(input_list)


assessor = input("Hi, Human assessor, may I know your name: ")

path = assessor + "_result.csv"
if os.path.exists(path):
    os.remove(path)

plt.style.use('dark_background')

fig, ax = plt.subplots(figsize=(10, 2))
img = mping.imread(img_path(0))
img_plot = ax.imshow(img)
ax.axis('off')
ax.set_title("Questionnaire 1")
plt.show(block=False)
input_digits = []

for i in range(1, 21):
    plt.pause(0.5)
    input_human = input(f"Q{i} Please give your prediction separated by commas: ")
    while invalid_input(input_human):
        input_human = input(f"Q{i} Invalid input. Please give your prediction separated by commas again: ")
    csv_logger(path, input_human.split(','))
    plt.pause(0.5)

    if i == 20:
        break
    img = mping.imread(img_path(i))
    # print(img.shape)
    ax.axis('off')
    img_plot.set_data(img)
    ax.autoscale()
    ax.set_title(f"Questionnaire {i+1}")

print(input_digits)

