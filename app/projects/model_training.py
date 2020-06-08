''' Set up logging '''
import logging

logger = logging.getLogger('Riot_Logger')
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('debug.log')
file_handler.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.ERROR)

logging_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(logging_formatter)
stream_handler.setFormatter(logging_formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)



''' Import modules '''
%matplotlib inline
import matplotlib.pyplot as plt
from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers import Dense, LeakyReLU, Dropout
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score, train_test_split, StratifiedKFold, KFold
import numpy as np
from sklearn.preprocessing import LabelEncoder
from keras.utils import np_utils
import pickle



''' Instantiate connection to database '''
from pymongo import MongoClient
client = MongoClient()
db = client['riot_games']



seed = 0
np.random.seed(seed)



''' Set up features and labels '''

# (Initialize arrays)
X = []
Y = []

# Get list of all champion IDs
games = db.games
champion_id_set = set()
for g in games.find({}):
    for id in g['team100champions']:
        champion_id_set.add(id)
    for id in g['team200champions']:
        champion_id_set.add(id)    
champion_ids = sorted(list(champion_id_set))

# Populate features/labels with data from database
for g in games.find({}):
    x = [0] * len(champion_ids)
    for id in g['team100champions']:
        x[champion_ids.index(id)] = 1
    for id in g['team200champions']:
        x[champion_ids.index(id)] = -1
    X.append(x)
    
    y = str(g['victoriousTeam'])
    Y.append(y)

# Convert features/labels to numpy arrays
X = np.array(X)
Y = np.array(Y)

# Train/Test split the data set
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.1, random_state=seed)

# Encode categorical labels
original_labels = Y_train.copy()
label_encoder = LabelEncoder()
Y_train = label_encoder.fit_transform(Y_train)
Y_train = np_utils.to_categorical(Y_train)
Y_test = label_encoder.transform(Y_test)
Y_test = np_utils.to_categorical(Y_test)

# Save various objects to be used later in the website script
to_pickle = {
    'champion_ids': champion_ids,
    'label_encoder': label_encoder
}
pickle_file = open('Riot_Pickle.pkl', 'wb')
pickle.dump(to_pickle, pickle_file)
pickle_file.close()



''' Function to construct Keras model '''
def build_model(model_params):
    
    # Unpack model parameters
    activation = model_params['activation']
    num_layers = model_params['num_layers']
    learning_rate = model_params['learning_rate']
    beta_1 = model_params['beta_1']
    beta_2 = model_params['beta_2']
    dropout = model_params['dropout']
    
    # Instantiate model
    model = Sequential()
    model.add(Dense(X_train.shape[1], input_dim=X_train.shape[1], activation=activation))
    if dropout:
        model.add(Dropout(dropout))
    model.add(Dense(32, activation=activation))
    model.add(Dense(Y_train.shape[1], activation='softmax'))
    
    optimizer = Adam(learning_rate=learning_rate, beta_1=beta_1, beta_2=beta_2, amsgrad=False)
    model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
    
    return model



''' Function to plot model metrics as it's trained '''
def plot_model(model_history,
               num_epochs,
               graph_name):
 
    # Unpack metrics from model history
    all_acc_histories = model_history['all_acc_histories']
    all_loss_histories = model_history['all_loss_histories']
    all_val_acc_histories = model_history['all_val_acc_histories']
    all_val_loss_histories = model_history['all_val_loss_histories']
    
    # Calculate average metrics
    average_acc_history = [np.mean([x[i] for x in all_acc_histories]) for i in range(num_epochs)]
    average_loss_history = [np.mean([x[i] for x in all_loss_histories]) for i in range(num_epochs)]
    average_val_acc_history = [np.mean([x[i] for x in all_val_acc_histories]) for i in range(num_epochs)]
    average_val_loss_history = [np.mean([x[i] for x in all_val_loss_histories]) for i in range(num_epochs)]
    
    # Initialize plot
    plt.figure(figsize=(14, 7))
    plt.xlim(0,num_epochs+1)
    plt.ylim(0.4, 0.8)

    # Plot loss of each fold
    for fold in all_loss_histories:
        plt.plot(np.array(range(len(fold))) + 1,
                 fold,
                 color='#00BA1C',
                 alpha=0.4,
                 linestyle='dotted',
                 zorder=1)
    # Plot average loss of all folds
    plt.plot(np.array(range(len(average_loss_history))) + 1,
             average_loss_history,
             label='Training Loss',
             color='#00BA1C',
             zorder=2)

    # Plot each accuracy fold
    for fold in all_acc_histories:
        plt.plot(np.array(range(len(fold))) + 1,
                 fold,
                 color='#0000FF',
                 alpha=0.4,
                 linestyle='dotted',
                 zorder=1)
    # Plot average of accuracy folds
    plt.plot(np.array(range(len(average_acc_history))) + 1,
             average_acc_history,
             label='Training Accuracy',
             color='#0000FF',
             zorder=2)

    # Plot each validation loss fold
    for fold in all_val_loss_histories:
        plt.plot(np.array(range(len(fold))) + 1,
                 fold,
                 color='#FF7B00',
                 alpha=0.4,
                 linestyle='dotted',
                 zorder=1)
    # Plot average of validation loss folds
    plt.plot(np.array(range(len(average_val_loss_history))) + 1,
             average_val_loss_history,
             label='Validation Loss',
             color='#FF7B00',
             zorder=2)

    # Plot each validation accuracy fold
    for fold in all_val_acc_histories:
        plt.plot(np.array(range(len(fold))) + 1,
                 fold,
                 color='#FF0000',
                 alpha=0.4,
                 linestyle='dotted',
                 zorder=1)
    # Plot average of validation accuracy folds
    plt.plot(np.array(range(len(average_val_acc_history))) + 1,
             average_val_acc_history,
             label='Validation Accuracy',
             color='#FF0000',
             zorder=2)

    # Generate and save plot
    plt.title(graph_name)
    plt.xlabel('Epochs')
    plt.ylabel('Metric')
    plt.legend(loc='upper left')
    plt.savefig('figures/{}.png'.format(graph_name))



''' Function to run and evaluate model '''
def evaluate_model(label, **kwargs):

	# Initialize default model parameters; overwrite them if included in function kwargs
    model_params = {
        'num_epochs': 30,
        'batch_size': 100,
        'num_layers': 3,
        'num_folds': 3,
        'activation': 'linear',
        'num_layers': 2,
        'dropout': False,
        'learning_rate': 0.001,
        'beta_1': 0.9,
        'beta_2': 0.999
    }    
    for (key, value) in kwargs.items():
        model_params[key] = value
    
    kf = StratifiedKFold(n_splits=model_params['num_folds'], shuffle=True, random_state=seed)    
    
    model_history = {
        'all_acc_histories': [],
        'all_loss_histories': [],
        'all_val_acc_histories': [],
        'all_val_loss_histories': []
    }
    
    # Train model for each validation split
    for index, (train_indices, val_indices) in enumerate(kf.split(X_train, original_labels)):
        print('processing fold #', index)

        xtrain, xval = X_train[train_indices], X_train[val_indices]
        ytrain, yval = Y_train[train_indices], Y_train[val_indices]

        # Build the model
        estimator = KerasRegressor(build_fn=build_model,
                                   model_params=model_params,
                                   epochs=model_params['num_epochs'],
                                   batch_size=model_params['batch_size'],
                                   verbose=1)      
        
        # Train the model
        history = estimator.fit(xtrain, ytrain, validation_data=(xval, yval))

        # Record model metrics
        acc_history = history.history['accuracy']
        loss_history = history.history['loss']
        model_history['all_acc_histories'].append(acc_history)
        model_history['all_loss_histories'].append(loss_history)

        # Record model validation metrics
        val_acc_history = history.history['val_accuracy']
        val_loss_history = history.history['val_loss']
        model_history['all_val_acc_histories'].append(val_acc_history)
        model_history['all_val_loss_histories'].append(val_loss_history)

    # Plot model metrics
    plot_model(model_history,
               model_params['num_epochs'],
               label)



''' After evaluating different hyperparameters, train the final model'''
model_params = {
    'num_epochs': 30,
    'batch_size': 100,
    'num_layers': 3,
    'num_folds': 3,
    'activation': 'linear',
    'num_layers': 2,
    'dropout': False,
    'learning_rate': 0.001,
    'beta_1': 0.9,
    'beta_2': 0.999
}    
estimator = KerasRegressor(build_fn=build_model,
                           model_params=model_params,
                           epochs=model_params['num_epochs'],
                           batch_size=model_params['batch_size'],
                           verbose=1)
estimator.fit(X_train, Y_train)

# Save the model to be used to make predictions in the future
estimator.model.save('Riot_Model.h5')
