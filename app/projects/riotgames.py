from tensorflow.keras.models import load_model
import numpy as np
from sklearn.preprocessing import LabelEncoder
import pickle



class MatchPredictor(object):

    def __init__(self):
        with open('app/projects/Riot_Pickle.pkl', 'rb') as pickle_file:
            p = pickle.load(pickle_file)
            self.champion_ids = p['champion_ids']
            self.label_encoder = p['label_encoder']
        self.model = load_model('app/projects/Riot_Model.h5')

    def make_prediction(self, match):
        team100 = [
            match['champion0'],
            match['champion1'],
            match['champion2'],
            match['champion3'],
            match['champion4']
        ]
        team200 = [
            match['champion5'],
            match['champion6'],
            match['champion7'],
            match['champion8'],
            match['champion9']
        ]

        x = [0] * len(self.champion_ids)
        for id in team100:
            x[self.champion_ids.index(int(id))] = 1
        for id in team200:
            x[self.champion_ids.index(int(id))] = -1
        x = np.array(x)
        x = x.reshape(1, -1)


    # Fix for where '' is in team100, etc.
        prediction = self.model.predict(x)[0]
        confidence = np.max(prediction)
        winner_label = np.argmax(prediction)
        winning_team = self.label_encoder.inverse_transform([winner_label])[0]

        results = {
            'winningTeam': winning_team,
            'confidence': str(int(confidence*100))
        }
        return results

