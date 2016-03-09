import numpy as np

states = ('s1', 's2')

#list of possible observations
possible_observation = ('R','W', 'B')

obs_map =  { 'R': 0 ,'W' : 1, 'B':2 }

# The observations that we observe and feed to the model
observations = ('R', 'W','B','B')

# Numpy arrays of the data
start_probability = np.matrix( '0.8 0.2 ')
transition_probability = np.matrix('0.6 0.4 ;  0.3 0.7 ')
emission_probability = np.matrix( '0.3 0.4 0.3 ; 0.4  0.3  0.3 ' )


"""
start_prob, em_prb and trans_prob are all numpy arrays
observations, is a list of strings

"""

def alpha_cal(start_prob,em_prob,trans_prob,observations):

    # Find number of states.stages
    num_states = em_prob.shape[0]
    total_stages = len(observations)

    # Initialize values
    ob_ind = obs_map[ observations[0] ]
    alpha = np.asmatrix(np.zeros((num_states,total_stages)))

    # Handle alpha base case
    alpha[:,0] = np.multiply ( np.transpose(em_prob[:,ob_ind]) , start_prob ).transpose()

    # Iteratively calculate alpha(t) for all 't'
    for curr_t in range(1,total_stages):
        ob_ind = obs_map[observations[curr_t]]
        alpha[:,curr_t] = np.dot( alpha[:,curr_t-1].transpose() , trans_prob).transpose()
        alpha[:,curr_t] = np.multiply( alpha[:,curr_t].transpose() , np.transpose( em_prob[:,ob_ind] )).transpose()

    # return the computed alpha
    return alpha 

def beta_cal(start_prob,em_prob,trans_prob,observations):

    # Find number of states.stages
    num_states = em_prob.shape[0]
    total_stages = len(observations)

    # Initialize values
    ob_ind = obs_map[ observations[total_stages-1] ]
    beta = np.asmatrix(np.zeros((num_states,total_stages)))

    # Handle beta base case
    beta[:,total_stages-1] = 1

    # Iteratively calculate alpha(t) for all 't'
    for curr_t in range(total_stages-1,0,-1):
        ob_ind = obs_map[observations[curr_t]]
        beta[:,curr_t-1] = np.multiply( beta[:,curr_t] , em_prob[:,ob_ind] )
        beta[:,curr_t-1] = np.dot( trans_prob, beta[:,curr_t-1] )

    # return the computed beta
    return beta

def forward_backward(start_prob,em_prob,trans_prob,observations):
    
    num_states = em_prob.shape[0]
    num_obs = len(observations)

    alpha = alpha_cal(start_probability ,emission_probability,transition_probability,observations)
    beta = beta_cal(start_probability ,emission_probability,transition_probability,observations)
    
    # Calculate sum [alpha(num_obs)]
    prob_obs_seq = np.sum(alpha[:,num_obs-1])

    # Calculate delta1
    delta1 = np.multiply(alpha,beta)/ prob_obs_seq 

    delta2 = np.zeros(( num_obs-1, num_states, num_states))
    for curr_t in range(num_obs-1):  

        ob_ind = obs_map[observations[curr_t+1]]
        # temp(i,j) = alpha(i)*beta(j)
        temp = np.multiply(alpha[:,curr_t].transpose(),beta[:,curr_t+1])

        # Calculate delta(i,j)
        delta2[curr_t] = np.multiply ( np.multiply(temp,trans_prob) , em_prob[:,ob_ind].transpose() )
        delta2[curr_t] = delta2[curr_t] / prob_obs_seq

    return delta1, delta2


def train_emission(start_prob,em_prob,trans_prob,observations):
    
    
    new_em_prob = np.asmatrix(np.zeros(em_prob.shape))
    
    # Indexing position of unique observations in the observation sequence    
    selectCols=[]
    for i in range(em_prob.shape[1]):
        selectCols.append([])
    for i in range(len(observations)):
        selectCols[ obs_map[observations[i]] ].append(i)
    print selectCols
    
    delta = forward_backward(start_prob,em_prob,trans_prob,observations)
    
    for i in range(em_prob.shape[0]):
        totalProb = np.sum(delta[i,:])
        
        for j in range(em_prob.shape[1]):
            
            new_em_prob[i,j] = np.sum(delta[i,selectCols[j]])/totalProb
            
    return new_em_prob

#%%

# TODO : Complete the below function using above used sub-routines
# def train_model():


#----------------Program test------------------------
# TODO : Check if z1,z2 are giving correct values, with some other examples
x = alpha_cal(start_probability ,emission_probability,transition_probability,observations)
y = beta_cal(start_probability ,emission_probability,transition_probability,observations)
z1,z2 = forward_backward(start_probability ,emission_probability,transition_probability,observations)
new_em_prob = train_emission(start_probability ,emission_probability,transition_probability,observations)

print(x)
print('')
print (y)
print('')
print (z1)
print('\n')
print (z2)
print(new_em_prob)
