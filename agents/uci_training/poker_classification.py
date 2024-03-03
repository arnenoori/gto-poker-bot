import os
import uuid
from datetime import datetime
import pickle
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import KFold, train_test_split, StratifiedKFold

# Model Base Types
Sequential = tf.keras.models.Sequential

# Layers
Dense = tf.keras.layers.Dense
Dropout = tf.keras.layers.Dropout

# Optimizers
Adam = tf.keras.optimizers.Adam

# Function reorders the data so that simular data represenations are near each other.
def reorder_data_cols(data):
    df = data.copy()
    dfc = df[['C1', 'C2', 'C3', 'C4', 'C5']]
    dfc.values.sort()
    df[['C1', 'C2', 'C3', 'C4', 'C5']] = dfc
    df = df[['C1', 'C2', 'C3', 'C4', 'C5', 'S1', 'S2', 'S3', 'S4', 'S5', 'Label']]
    return df

# Function generates the confusion matrics data as a graphic
def print_cmat(cm, labels=None):
  """ Helper function to visualize confusion matrices. """
  ax = plt.subplot()
  sns.heatmap(cm, annot=True, fmt="g", cmap="YlGnBu", linewidths=0.5, ax=ax)
  
  ax.set_title("Confusion Matrix")
  ax.set_xlabel("Predicted Labels")
  ax.set_ylabel("True Labels")
  
  if labels:
      ax.xaxis.set_ticklabels(labels)
      ax.yaxis.set_ticklabels(labels)
  plt.show()

train_data = pd.read_csv('data/poker-hand-training-true.data', header=None)
train_data.columns = ['S1', 'C1','S2', 'C2','S3', 'C3','S4', 'C4','S5', 'C5','Label']
train_data = reorder_data_cols(train_data)


test_data = pd.read_csv('data/poker-hand-testing.data', index_col=None)
test_data.columns = ['S1', 'C1','S2', 'C2','S3', 'C3','S4', 'C4','S5', 'C5','Label']
test_data = reorder_data_cols(test_data)

train_data.describe()

sns.histplot(data=train_data['Label'], binwidth=1, color="purple")
sns.distplot(train_data['Label'], color="purple")

# Split the data into training and testing sets# Group data based on feature and label status.

x_train = train_data[train_data.columns[:10]]
y_train = train_data[train_data.columns[10]]
x_test = test_data[test_data.columns[:10]]
y_test = test_data[test_data.columns[10]]

x_train = x_train.to_numpy()
y_train = y_train.to_numpy()
x_test = x_test.to_numpy()
y_test = y_test.to_numpy()

criterion_options = ['entropy','gini']
splitter_options = ['best','random']
max_depth_options = [None,1,5,10,20,30,40,50,100,200]
min_samples_split_options = [2,5,7,10,20,40,50]
max_leaf_nodes_options = [None,2,5,7,10,20,30,50,100,200]

total_models_to_generate = len(criterion_options) * len(splitter_options) * len(max_depth_options) * len(min_samples_split_options) * len(max_leaf_nodes_options)
models_generated = 0

# Create instance of the classical model and test
tree_model_results_df = pd.DataFrame(columns=['criterion','splitter','max_depth','min_samples','max_leaf_nodes','accuracy'])
now_folder_name = datetime.now().strftime("%Y%m%d-%H%M%S")


# Run test for a verity of diffrent configurations
for criterion in criterion_options:
    for splitter in splitter_options:
        for max_depth in max_depth_options:
            for min_samples_split in min_samples_split_options:
                for max_leaf_nodes in max_leaf_nodes_options:
                    print(f'{models_generated} / {total_models_to_generate}')
                    tree_model = DecisionTreeClassifier(random_state=1, criterion=criterion, splitter=splitter, max_depth=max_depth, min_samples_split=min_samples_split, max_leaf_nodes=max_leaf_nodes)
                    tree_model.fit(x_train, y_train)
                    y_pred = tree_model.predict(x_test)
                    accuracy = accuracy_score(y_test, y_pred, normalize=True,)
                    filename = 'tree_model-' + uuid.uuid4().hex + '.pickle'
                    row = {
                        'criterion':criterion,
                        'splitter':splitter,
                        'max_depth':max_depth,
                        'min_samples_split':min_samples_split,
                        'max_leaf_nodes':max_leaf_nodes,
                        'accuracy':accuracy,
                        'filename':filename
                    }
                    tree_model_results_df = tree_model_results_df.append(row, ignore_index=True)
                    models_generated += 1
                    save_path = f'pickled_models/{now_folder_name}/{filename}'
                    if os.path.exists(f'pickled_models/{now_folder_name}') == False:
                        os.makedirs(f'pickled_models/{now_folder_name}')

                    pickle.dump(tree_model, open(save_path, 'wb'))
tree_model_results_df.to_csv(f'pickled_models/{now_folder_name}/model_meta_data.csv')

tree_model_results_df.sort_values('accuracy', ascending=False)

for index in range(5):
    top_model_stats = tree_model_results_df.sort_values('accuracy', ascending=False).iloc[index]
    criterion = top_model_stats['criterion']
    splitter = top_model_stats['splitter']
    max_depth = top_model_stats['max_depth']
    min_samples = top_model_stats['min_samples']
    max_leaf_nodes = top_model_stats['max_leaf_nodes']
    accuracy = top_model_stats['accuracy']
    tree_model = DecisionTreeClassifier(random_state=1, criterion=criterion, splitter=splitter, max_depth=max_depth, min_samples_split=min_samples_split, max_leaf_nodes=max_leaf_nodes)
    tree_model.fit(x_train, y_train)
    y_pred = tree_model.predict(x_test)

    cmat = confusion_matrix(y_true=y_test, 
                            y_pred=y_pred)
    print(f'criterion: {criterion} | splitter: {splitter} | max_depth: {max_depth} | min_samples_split: {min_samples_split} | max_leaf_nodes: {max_leaf_nodes} | accuracy: {accuracy}')
    print_cmat(cmat)

# Deep Learning Model

# Layer Creation

input_layer = Dense(10, activation="linear")

dense_layer_1 = Dense(30, activation="relu")

dropout_layer_1 = Dropout(.05)

dense_layer_2 = Dense(20, activation="relu")

dropout_layer_2 = Dropout(.05)

dense_layer_3 = Dense(15, activation="relu")

output_layer = Dense(10, activation="linear")

# Sequential Model Architecture Design
model = Sequential()

# Add All Initialized Layers in Effective Sequence
model.add(input_layer)
model.add(dense_layer_1)
model.add(dropout_layer_1)
model.add(dense_layer_2)
model.add(dropout_layer_2)
model.add(dense_layer_3)
model.add(output_layer)

# Define Adam optimization
optimizer = Adam(lr=0.001)
model.compile(optimizer=optimizer,
              loss="sparse_categorical_crossentropy",
              metrics=["accuracy"])

batch_size, epochs = 5000, 10

# Fit Learning Model Using Training Data and Configured Hyperparameters
history = model.fit(x_train,
                    y_train,
                    epochs=epochs,
                    batch_size=batch_size,
                   verbose=True)

# Get Model Summary for Confirmation
model.summary()

# Evaluate the model
score = model.evaluate(x_test, y_test, verbose=0)
print(f"Test loss: {score[0]}")
print(f"Test accuracy: {score[1]}")

loss, accuracy = model.evaluate(x_test, y_test)
print(f"Accuracy: {accuracy}\nLoss: {loss:.4f}")

# Get Our Predicted Labels
y_pred = np.argmax(model.predict(x_test), axis=1)

# Create Simple Confusion Matrix as 2D Array
cmat = confusion_matrix(y_true=y_test, 
                        y_pred=y_pred)

cmat = confusion_matrix(y_true=y_test, 
                        y_pred=y_pred)
print_cmat(cmat)