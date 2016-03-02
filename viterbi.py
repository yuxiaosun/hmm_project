import numpy as np

states = ('Healthy', 'Fever')

#list of possible observations
possible_observation = ('normal','cold', 'dizzy')

state_map = { 0 :'Healthy',1: 'Fever' }
obs_map =  { 'normal': 0 ,'cold' : 1, 'dizzy':2 }

# The observations that we observe and feed to the model
observations = ('normal', 'cold','dizzy')

# Numpy arrays of the data
start_probability = np.matrix( '0.6 0.4 ')
transition_probability = np.matrix('0.7 0.3 ;  0.4 0.6 ')
emission_probability = np.matrix( '0.5 0.4 0.1 ; 0.1  0.3  0.6 ' )


"""
Function returns the most likely path, and its associated probability
Function makes assumption that order of states is same in state,start_prob,em_prob,trans_prob
start_prob,em_prob,trans_prob are numpy objects
state,observations are both lists

"""
# TODO integrate this into the class

def viterbi(state,observations,start_prob,em_prob,trans_prob ):
   
#     initialize data
    total_stages = len(observations)
    num_states = len(state)
    
    old_path = np.zeros( (total_stages, num_states) )
    new_path = np.zeros( (total_stages, num_states) )

    # Find initial delta
    # Map observation to an index
    # delta[s] stores the probability of most probable path ending in state 's' 
    ob_ind = obs_map[ observations[0] ]
    delta = np.multiply ( np.transpose(em_prob[:,ob_ind]) , start_prob )
     
    # initialize path
    old_path[0,:] = [i for i in range(num_states) ]
    
    for curr_t in range(1,total_stages):

        # Map observation to an index
        ob_ind = obs_map[ observations[curr_t] ]
        # Find temp and take max along each row to get delta
        temp  =  np.multiply (np.multiply(delta , trans_prob.transpose()) , em_prob[:, ob_ind] )
            
        # Update delta
        delta = temp.max(axis = 1).transpose()

        # Find state which is most probable using argax
        # Convert to a list for easier processing
        max_temp = temp.argmax(axis=1).transpose()
        max_temp = np.ravel(max_temp).tolist()

        # Update path
        for s in range(num_states):
            new_path[:curr_t,s] = old_path[0:curr_t, max_temp[s] ] 

        new_path[curr_t,:] = [i for i in range(num_states) ]
        old_path = new_path.copy()


    final_max = np.argmax(np.ravel(delta))
    best_path = old_path[:,final_max].tolist()
    best_path_map = [ state_map[i] for i in best_path]

    return best_path_map,delta[0,final_max]

# ==================================================================================
    
# Program Testing
print (viterbi(states,observations,start_probability,emission_probability,transition_probability ))
