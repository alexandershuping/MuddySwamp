import json

# TODO: consider adding a "CharacterClass" property
# that restricts who can use an exit
class Exit:
    '''Class representing an Exit
    Exits link a set of names with a particular location
    Contains: 
        a list of strings [exit names]
        destination [the location this points to]
    The list can be accessed by treating the this as an iterable
    For instance:
        "exit_name" in myExit [returns true if "exit_name" is in exit]
        for exit_name in myExit:
            [iterates over all the possible exit names]
    '''
    def __init__(self, destination, primary_name, *other_names):
        '''Constructor for Exit
        Takes as input:
            location [location it points to]
            at least one name is required [primary name]
            additional names are optional
        '''
        self._destination = destination
        self._names = [primary_name] + list(other_names)
    
    def get_destination(self):
        return self._destination
    
    def __eq__(self, other):
        '''Overriding ==
        Returns True if:
            other is an Exit that points to the same location
            other is a string that is in the list
        '''
        try:
            return self._destination == other._destination
        except AttributeError:
            return other in self._names

    def __contains__(self, other):
        return other in self._names

    def __iter__(self):
        for name in self._names:
            yield name
    
    def __str__(self):
        return "%s: %s" % (self._names[0], self._destination.name)


class Location:
    '''Class representing an in-game Location
    Maintains a list of players
    Contains a list of exits to other locations
    Has a name and description
    '''
    def __init__(self, name, description):
        self._player_list = []
        self._exit_list = []
        self.name = name
        self.description = description
        # this will come into play later
        self.owner = None

    #TODO: players are currently added based upon id
    # this should be swapped out for a Player object
    # call Player.location = self
    def add_player(self, id):
        self._player_list.append(id)
    
    def remove_player(self, id):
        self._player_list.remove(id)
    
    def get_player_list(self):
        return list(self._player_list)
    
    def add_exit(self, exit_to_add):
        for exit_name in exit_to_add:
            assert exit_name not in self._exit_list, "\nLocation:\t%s\nExit:\t\t%s" % (self.name, exit_to_add)
        self._exit_list.append(exit_to_add)

    def exit_list(self):
        '''returns a copy of private exit list'''
        return list(self._exit_list)

    def __eq__(self, other):
        return self.name == other

    def __contains__(self, other):
        '''Overriding in operator
        Returns True if:
            if it is an exit or string:
                there exists an exit in _exit_list that matches
            if it is a Player or id:
                there exists a player with that id
        '''
        if isinstance(other, Exit) or isinstance(other, str):
            return other in self._exit_list
        #replace int with Player
        elif isinstance(other, int):
            return other in self._player_list
        else:
            raise ValueError("Received %s, expected Exit/string, "
                             "Player/int" % type(other))

    def __str__(self, verbose=False):
        '''supplies a string
        if verbose is selected, description also supplied
        '''
        if verbose:
            return "%s:\n%s" % (self.name, self.description)
        else:
            return self.name