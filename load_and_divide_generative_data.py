import pickle
import pandas as pd

#template to prompt the model
def prompt_template(user, review, reply):
    return f"### Bruger:\n{user}\n\n### Anmeldelse:\n{review}\n\n### Svar: \n{reply}\n\n"

# Load list of strings from the pickle file
data_path = "./data/combined_reviews_cleaned.csv"

input_texts = pd.read_csv(data_path, sep=";")
input_texts = input_texts.drop('Unnamed: 0', axis=1)
input_texts = input_texts[input_texts['useful'] == 1]

# Shuffle the DataFrame with a fixed random seed for reproducibility
random_seed = 42
shuffled_input_texts = input_texts.sample(frac=1, random_state=random_seed).reset_index(drop=True)


#convert the dataframe entries to strings using the prompt_template function
prompts= []
for i in range(len(shuffled_input_texts)):
    user = shuffled_input_texts.iloc[i]['name']
    review = shuffled_input_texts.iloc[i]['review']
    reply = shuffled_input_texts.iloc[i]['reply'] 
    prompts.append(prompt_template(user, review, reply))

print(len(prompts))
print(prompts[:5])


# Define the ratio for splitting (80% for training, 10% for validation, 10% for testing)
train_ratio = 0.8
val_ratio = 0.1
test_ratio = 0.1

total_samples = len(prompts)

train_samples = int(train_ratio * total_samples)
val_samples = int((total_samples - train_samples)//2)
test_samples = int(total_samples - train_samples - val_samples)

print(f"Total samples: {total_samples}", 
      f"Train samples: {train_samples}",
      f"Validation samples: {val_samples}",
      f"Test samples: {test_samples}", sep="\n")


# Split the list into training and validation data
train_data = prompts[:train_samples]
val_data = prompts[train_samples:(train_samples+val_samples)]
test_data = prompts[train_samples+val_samples:]


# Write to a text file, preserving newlines within each training instance
with open("new_corpus_train_final.txt", "w") as f:
    for line in train_data:
        f.write(line + "\n")

with open("new_corpus_val_final.txt", "w") as f:
    for line in val_data:
        f.write(line + "\n")

with open("new_corpus_test_final.txt", "w") as f:
    for line in test_data:
        f.write(line + "\n")
        

#save the training and validation data to separate pickle files

#train_data_path = './data/new_train_data_80p.pkl' ... no need to save the training data to a pickle file
#val_data_path = './data/new_val_data_10p.pkl'  ... no need to save the validation data to a pickle file
test_data_path = './data/new_test_data_10p.pkl' # path to save the test data

# Save the training and validation data to pickle files

#with open(train_data_path, "wb") as file:
#    pickle.dump(train_data, file)

#with open(val_data_path, "wb") as file:
#    pickle.dump(val_data, file)

with open(test_data_path, "wb") as file:
    pickle.dump(test_data, file)
