

import json

#methods to handle JSON serialization and deserialization (I cant import them for some reason...)
def set_player_pictures(self, pictures_dict):
        """Sets the player's picture dictionary."""
        self.player_pictures = json.dumps(pictures_dict)

def get_player_pictures(self):
        """Returns the player's picture dictionary."""
        return json.loads(self.player_pictures)