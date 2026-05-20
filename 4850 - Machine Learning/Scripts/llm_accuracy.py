import pandas as pd

data_dir = "dataset/election/data.csv"
data = pd.read_csv(data_dir, sep="\t")

data = data[data['label'] != 0]
total = len(data)
print("Total samples: {}".format(total))
correct = len(data[data['label'] == data['llm_label']])
print("Correctly predicted samples: {}".format(correct))
accuracy = correct / total
print("Accuracy: {:.2f}%".format(accuracy * 100))