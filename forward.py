import numpy as np

states = ('Healthy', 'Fever')

#list of possible observations
possible_observation = ('normal','cold', 'dizzy')

obs_map =  { 'normal': 0 ,'cold' : 1, 'dizzy':2 }

# The observations that we observe and feed to the model
observations = ('normal', 'dizzy','cold')

# Numpy arrays of the data
start_probability = np.matrix( '0.6 0.4 ')
transition_probability = np.matrix('0.7 0.3 ;  0.4 0.6 ')
emission_probability = np.matrix( '0.5 0.4 0.1 ; 0.1  0.3  0.6 ' )

def forward_algo(state,observations,start_prob,em_prob,trans_prob ):

    total_stages = len(observations)

    ob_ind = obs_map[ observations[0] ]
    alpha = np.multiply ( np.transpose(em_prob[:,ob_ind]) , start_prob )

    for curr_t in range(1,total_stages):
        ob_ind = obs_map[observations[curr_t]]
        alpha = np.dot( alpha , trans_prob)
        alpha = np.multiply( alpha , np.transpose( em_prob[:,ob_ind] ))

    total_prob = alpha.sum()
    return ( observations ,total_prob )


# To print the results
x1 , x2 =  my_forward(states,observations , start_probability,emission_probability, transition_probability)
print (x1)
print(x2)


