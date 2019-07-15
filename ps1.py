
# Problem 1
class State():
    """
    A class representing the election results for a given state. 
    Assumes there are no ties between dem and gop votes. The party with a 
    majority of votes receives all the Electoral College (EC) votes for 
    the given state.
    """
    def __init__(self, name, dem, gop, ec):
        """
        Parameters:
        name - the 2 letter abbreviation of a state
        dem - number of Democrat votes cast
        gop - number of Republican votes cast
        ec - number of EC votes a state has 

        Attributes:
        self.name - str, the 2 letter abbreviation of a state
        self.winner - str, the winner of the state, "dem" or "gop"
        self.margin - int, difference in votes cast between the two parties, a positive number
        self.ec - int, number of EC votes a state has
        """
        
        # Class parameters
        self.name = name
        self.dem = dem 
        self.gop = gop 
        self.ec = ec 
        self.margin = abs(self.dem - self.gop)
        if self.dem > self.gop:
            self.winner = "dem"
        else:
            self.winner = "gop"
        
 
    def get_name(self):
        """
        Returns:
        str, the 2 letter abbreviation of the state  
        """
        
        return str(self.name)

    def get_num_ecvotes(self):
        """
        Returns:
        int, the number of EC votes the state has 
        """
        
        return self.ec

    def get_margin(self):
        """
        Returns: 
        int, difference in votes cast between the two parties, a positive number
        """
        
        return self.margin

    def get_winner(self):
        """
        Returns:
        str, the winner of the state, "dem" or "gop"
        """

        return self.winner

    def __str__(self):
        """
        Returns:
        str, representation of this state in the following format,
        "In <state>, <ec> EC votes were won by <winner> by a <margin> vote margin."
        """

        return "In " + str(self.get_name()) + ", " + str(self.get_num_ecvotes()) +\
            " EC votes were won by " + self.get_winner() + " by a " + str(self.get_margin()) + " vote margin."
    
        
    def __eq__(self, other):
        """
        Determines if two State instances are the same.
        They are the same if they have the same state name, winner, margin and ec votes.
        Be sure to check for instance type equality as well! 

        Note: 
        1. Allows you to check if State_1 == State_2
		2. Make sure to check for instance type (Hint: look up isinstance())

        Param:
        other - State object to compare against  

        Returns:
        bool, True if the two states are the same, False otherwise
        """
        
        # Check if self and other are instances of State class
        if isinstance(self, State) and isinstance(other, State):
            
            # Compare names, dem and gop numbers, and ec votes
            if self.get_name() == other.get_name() and self.get_winner() == other.get_winner()\
                and self.get_margin() == other.get_margin() and self.get_num_ecvotes() == other.get_num_ecvotes():
                    return True
            else:
                return False
            
        else:
            return False


# Problem 2
def load_election_results(filename):
    """
    Reads the contents of a file, with data given in the following tab-delimited format,
    State   Democrat_votes    Republican_votes    EC_votes 

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a list of State instances
    """
    
    # Open file
    file = open(filename)
    
    # Read first and second lines (no need to keep the first line)
    file.readline()
    header_line = file.readline()
    
    # Create a list for storing State instances
    state_list = []
    
    # Read lines as long as file and line are not empty
    while header_line != "" and header_line != "\n":
        
        # Split the line on tabs
        header_line = header_line.split("\t")
        
        # Remove \n
        if "\n" in header_line[3]:
            header_line[3] = header_line[3][:len(header_line[3])-1]
        
        # Store State instances
        state_list.append(State(header_line[0], int(header_line[1]), int(header_line[2]), int(header_line[3])))
        
        # Read next line
        header_line = file.readline()
    
    return state_list


# Problem 3
def find_winner(election):
    """
    Finds the winner of the election based on who has the most amount of EC votes.
    Note: In this simplified representation, all of EC votes from a state go
    to the party with the majority vote.

    Parameters:
    election - a list of State instances 

    Returns:
    a tuple, (winner, loser) of the election i.e. ('dem', 'gop') if Democrats won, else ('gop', 'dem')
    """
    
    # Initialize electoral votes for dem and gop
    dem_ec, gop_ec = 0, 0
    
    # Iterate through the State instances
    for state in election:
        
        # Update electoral votes for dem and gop
        if state.get_winner() == "dem":
            dem_ec += state.get_num_ecvotes() 
        else:
            gop_ec += state.get_num_ecvotes() 
     
    # Compare electoral values, return (winner, loser)
    if dem_ec > gop_ec:
        return ("dem", "gop")
    else:
        return ("gop", "dem")
    
    
def winner_states(election):
    """
    Finds the list of States that were won by the winning candidate (lost by the losing candidate).
    
    Parameters:
    election - a list of State instances 

    Returns:
    A list of State instances won by the winning candidate
    """
    
    # Get winner
    winner, loser = find_winner(election)
    
    #Create lists for storing winner and loser states
    winner_states = []
    loser_states = []
    
    # Iterate through the State instances
    for state in election:
        
        # Save winner and loser states in their respective lists
        if state.get_winner() == winner:
            winner_states.append(state)
        else:
            loser_states.append(state)
            
    return winner_states
            
            
def ec_votes_reqd(election, total=538):
    """
    Finds the number of additional EC votes required by the loser to change election outcome.
    Note: A party wins when they earn half the total number of EC votes plus 1.

    Parameters:
    election - a list of State instances 
    total - total possible number of EC votes

    Returns:
    int, number of additional EC votes required by the loser to change the election outcome
    """
    
    # Get winner and loser candidate
    winner, loser = find_winner(election)
    
    # Initialize electoral votes for dem and gop
    dem_ec, gop_ec = 0, 0
    
    # Iterate through the State instances
    for state in election:
        
        # Update electoral votes for dem and gop
        if state.get_winner() == "dem":
            dem_ec += state.get_num_ecvotes() 
        else:
            gop_ec += state.get_num_ecvotes() 
    
    # Find the difference between votes needed to win and actual electoral votes
    if loser == "dem":
        return (total // 2 + 1) - dem_ec
    else:
        return (total // 2 + 1) - gop_ec
                    
                     
# Problem 4
def greedy_election(winner_states, ec_votes_needed):
    """
    Finds a subset of winner_states that would change an election outcome if
    voters moved into those states. First chooses the states with the smallest 
    win margin, i.e. state that was won by the smallest difference in number of voters. 
    Continues to choose other states up until it meets or exceeds the ec_votes_needed. 
    Should only return states that were originally won by the winner in the election.

    Parameters:
    winner_states - a list of State instances that were won by the winner 
    ec_votes_needed - int, number of EC votes needed to change the election outcome
    
    Returns:
    A list of State instances such that the election outcome would change if additional
    voters relocated to those states (also can be referred to as our swing states)
    The empty list, if no possible swing states
    """
    
    # Sort states (increasing margin, decreasing ec votes)
    sorted_winner_states = sorted(winner_states, key = lambda x : (x.get_margin(), x.get_num_ecvotes() * -1))
    
    # Initialize ec votes added and an empty list for saving flipped states
    ec_votes_added = 0
    flipped_states = []
    
    # Keep adding states to the "knapsack" (flipped_states) till you reach the number of ec votes needed
    while ec_votes_added < ec_votes_needed:
        state = sorted_winner_states[0]
        flipped_states.append(state)
        ec_votes_added += state.get_num_ecvotes()
        
        # Remove state already added to knapsack from original list (sorted_winner_states)
        sorted_winner_states.remove(state)
        
    return flipped_states
                

# Problem 5
def dp_move_max_voters(winner_states, ec_votes, memo = None):
    """
    Finds the largest number of voters needed to relocate to get at most ec_votes
    for the election loser. 

    Analogy to the knapsack problem:
    Given a list of states each with a weight(#ec_votes) and value(#margin),
    determine the states to include in a collection so the total weight(#ec_votes)
    is less than or equal to the given limit(ec_votes) and the total value(#voters displaced)
    is as large as possible.

	Hint: If using a top-down implementation, it may be helpful to create a helper function

    Parameters:
    winner_states - a list of State instances that were won by the winner 
    ec_votes - int, the maximum number of EC votes 
    memo - dictionary, an OPTIONAL parameter for memoization (don't delete!).
    Note: If you decide to use the memo make sure to override the default value when it's first called.

    Returns:
    A list of State instances such that the maximum number of voters need to be relocated
    to these states in order to get at most ec_votes 
    The empty list, if every state has a # EC votes greater than ec_votes
    """
    
    # Objective Function: maximize value (margin)
    # Constraint: weight (ec_votes)
    
    # Initialize memo as a dictionary
    if memo == None:
        memo = {}
        
    # Check if key already exists in memo   
    if (len(winner_states), ec_votes) in memo:
        return memo[(len(winner_states), ec_votes)]
    
    # Check if winner_states list is empty or no ec votes are needed    
    elif winner_states == [] or ec_votes == 0:
        return []
    
    # Check if state's ec votes exceed needed ec votes    
    elif winner_states[0].get_num_ecvotes() > ec_votes:
        
        # Explore right branch only (first item could not be taken)
        return dp_move_max_voters(winner_states[1:], ec_votes, memo)
    
    # If item can be taken:
    else:
        
        # Take the next state
        nextItem = winner_states[0]
        
        # Explore left branch
        withToTake = dp_move_max_voters(winner_states[1:], ec_votes - nextItem.get_num_ecvotes(), memo) + [nextItem]
        
        # Update withVal
        withVal = 0
        for state in withToTake:
            withVal += state.get_margin()
            
        # Explore right branch        
        withoutToTake = dp_move_max_voters(winner_states[1:], ec_votes, memo)
        
        # Update withoutVal
        withoutVal = 0
        for state in withoutToTake:
            withoutVal +=  state.get_margin()
        
        # Choose better branch
        if withVal > withoutVal:
            result = withToTake

        else:
            result = withoutToTake
    
    # Update memo
    memo[(len(winner_states), ec_votes)] = result
    return result


def move_min_voters(winner_states, ec_votes_needed):
    """
    Finds a subset of winner_states that would change an election outcome if
    voters moved into those states. Should minimize the number of voters being relocated. 
    Only return states that were originally won by the winner (lost by the loser)
    of the election.

    Hint: This problem is simply the complement of dp_move_max_voters

    Parameters:
    winner_states - a list of State instances that were won by the winner 
    ec_votes_needed - int, number of EC votes needed to change the election outcome

    Returns:
    A list of State instances such that the election outcome would change if additional
    voters relocated to those states (also can be referred to as our swing states)
    The empty list, if no possible swing states
    """
    
    # Get total ec votes for winner states
    ec_votes_won_by_winner = 0
    for state in winner_states:
        ec_votes_won_by_winner += state.get_num_ecvotes()
    
    # Get non swing states for the winner candidate (these are states that winner MUST win)
    nonSwing_states = dp_move_max_voters(winner_states, ec_votes_won_by_winner - ec_votes_needed, memo = None)
    
    # Find and store swing states (states that are in winner states list but not in non swing states list are swing states)
    swing_states = []
    for state in winner_states:
        if state not in nonSwing_states:
            swing_states.append(state)
     
    return swing_states

#Problem 6
def flip_election(election, swing_states):
    """
    Finds a way to shuffle voters in order to flip an election outcome. 
    Moves voters from states that were won by the losing candidate (any state not in winner_states), 
    to each of the states in swing_states. 
    To win a swing state, must move (margin + 1) new voters into that state. Any state that voters are
    moved from should still be won by the loser even after voters are moved.
    
    Also finds the number of EC votes gained by this rearrangement, as well as the minimum number of 
    voters that need to be moved.

    Parameters:
    election - a list of State instances representing the election 
    swing_states - a list of State instances where people need to move to flip the election outcome 
                   (result of move_min_voters or greedy_election)
    
    Return:
    A tuple that has 3 elements in the following order:
        - a dictionary with the following (key, value) mapping: 
            - Key: a 2 element tuple, (from_state, to_state), the 2 letter abbreviation of the State 
            - Value: int, number of people that are being moved 
        - an int, the total number of EC votes gained by moving the voters 
        - an int, the total number of voters moved 
    None, if it is not possible to sway the election
    """
   
    # Get lost states by losing candidate
    lost_states_list = winner_states(election)
    
    # Find won states by losing candidate (these states will donate voters to swing states)
    donor_states_list = []
    donor_state_margins = []
    for state in election:
        if state not in lost_states_list:
            donor_states_list.append(state)
            donor_state_margins.append(state.get_margin() - 1)
    
    # Initialize values
    from_to_dict = {}
    ec_votes_gained = 0
    voters_moved = 0
    ec_reqd = ec_votes_reqd(election)
    
    
    # Iterate through loser states (states you need to move out of)
    # As long as there are donor states left and there is need to collect more ec votes
    while ec_votes_gained < ec_reqd and donor_states_list != []:
        
        # Get first swing state
        first_swing_state = swing_states[0] 
        
        # Get swing state's margin (+1 ensures state is flipped)
        flip_margin = first_swing_state.get_margin() + 1
        
        # As long as swing state needs voters and there are donor states left
        while flip_margin != 0 and donor_states_list != []:
            
            # Get first donor state
            donor_state = donor_states_list[0]

            # Donor state has less than needed
            if donor_state_margins[0] < flip_margin:
                
                # Update dictionary, number of voters moved, and flip margin
                from_to_dict[(donor_state.get_name(), first_swing_state.get_name())] = donor_state_margins[0]
                voters_moved += donor_state_margins[0] 
                flip_margin -= donor_state_margins[0]
                
                # Remove donor state and its margin from both lists
                donor_states_list.remove(donor_state)
                donor_state_margins.remove(donor_state_margins[0])
                
            # Donor state has more than needed
            elif donor_state_margins[0] > flip_margin:
                
                # Update dictionary
                from_to_dict[(donor_state.get_name(), first_swing_state.get_name())] = flip_margin
                
                # Fully flipping the swing state
                ec_votes_gained += first_swing_state.get_num_ecvotes()
                voters_moved += flip_margin
                
                # Update donor margin and remove donor state 
                donor_state_margins[0] -= flip_margin
                swing_states.remove(first_swing_state)

                flip_margin = 0
            
            # Donor state has what's neede exactly
            else:
                # Update dictionary
                from_to_dict[(donor_state.get_name(), first_swing_state.get_name())] = flip_margin
                
                # Fully flipping the swing state
                ec_votes_gained += first_swing_state.get_num_ecvotes()
                voters_moved += flip_margin
                
                # Remove donor state, its margin, and the swing state
                donor_state_margins.remove(donor_state_margins[0])
                donor_states_list.remove(donor_state)
                swing_states.remove(first_swing_state)

                flip_margin = 0
    
    # In case election cannot be flipped (flip margin is too large)           
    if  ec_votes_gained < ec_reqd:
        return None
                
    return (from_to_dict, ec_votes_gained, voters_moved)
                


if __name__ == "__main__":
#    pass
    # Uncomment the following lines to test each of the problems

    # # tests Problem 1 and Problem 2 
     year = 2012 # Update the election year to debug
     election = load_election_results("%s_results.txt" % year) 

    # # tests Problem 3  
     winner, loser = find_winner(election)
     won_states = winner_states(election)
     names_won_states = [state.get_name() for state in won_states]
     ec_votes_needed = ec_votes_reqd(election)
     print("Winner:", winner, "\nLoser:", loser)
     print("EC votes needed:",ec_votes_needed)
     print("States won by the winner: ", names_won_states, "\n")

    # # tests Problem 4
     print("greedy_election")
     greedy_swing = greedy_election(won_states, ec_votes_needed)
     names_greedy_swing = [state.get_name() for state in greedy_swing]
     voters_greedy = sum([state.get_margin()+1 for state in greedy_swing])
     ecvotes_greedy = sum([state.get_num_ecvotes() for state in greedy_swing])
     print("Greedy swing states results:", names_greedy_swing)
     print("Greedy voters displaced:", voters_greedy, "for a total of", ecvotes_greedy, "Electoral College votes.", "\n")

     # tests Problem 5: dp_move_max_voters
     print("dp_move_max_voters")
     total_lost = sum(state.get_num_ecvotes() for state in won_states)
     move_max = dp_move_max_voters(won_states, total_lost-ec_votes_needed)
     max_states_names = [state.get_name() for state in move_max]
     max_voters_displaced = sum([state.get_margin()+1 for state in move_max])
     max_ec_votes = sum([state.get_num_ecvotes() for state in move_max])
     print("States with the largest margins:", max_states_names)
     print("Max voters displaced:", max_voters_displaced, "for a total of", max_ec_votes, "Electoral College votes.", "\n")

    # # tests Problem 5: move_min_voters
     print("move_min_voters")
     swing_states = move_min_voters(won_states, ec_votes_needed)
     swing_state_names = [state.get_name() for state in swing_states]
     min_voters = sum([state.get_margin()+1 for state in swing_states])
     swing_ec_votes = sum([state.get_num_ecvotes() for state in swing_states])
     print("Complementary knapsack swing states results:", swing_state_names)
     print("Min voters displaced:", min_voters, "for a total of", swing_ec_votes, "Electoral College votes. \n")

    # # tests Problem 6: flip_election
     print("flip_election")
     flipped_election = flip_election(election, swing_states)
     print("Flip election mapping:", flipped_election)
