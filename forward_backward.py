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
    num_states = em_prob.shape[0]
    # Find number of states.stages
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

    num_states = em_prob.shape[0]
    # Find number of states.stages
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

    alpha = alpha_cal(start_prob ,em_prob,trans_prob,observations)
    beta = beta_cal(start_prob ,em_prob,trans_prob,observations)
    
    # Calculate sum [alpha(num_obs)]
    prob_obs_seq = np.sum(alpha[:,num_obs-1])

    # each row corresponds to a state
    # Calculate delta1
    delta1 = np.multiply(alpha,beta)/ prob_obs_seq 

    return delta1


def train_emission(start_prob,em_prob,trans_prob,observations):
    new_em_prob = np.asmatrix(np.zeros(em_prob.shape))
    
    # Indexing position of unique observations in the observation sequence    
    selectCols=[]
    for i in range(em_prob.shape[1]):
        selectCols.append([])
    for i in range(len(observations)):
        selectCols[ obs_map[observations[i]] ].append(i)
    
    delta = forward_backward(start_prob,em_prob,trans_prob,observations)
    
    totalProb = np.sum(delta,axis=1)

    for i in range(em_prob.shape[0]):
        for j in range(em_prob.shape[1]):
            new_em_prob[i,j] = np.sum(delta[i,selectCols[j]])/totalProb[i]
            
    return new_em_prob


def train_transition(start_prob,em_prob,trans_prob,observations):
    new_trans_prob = np.asmatrix(np.zeros(trans_prob.shape))
    
    alpha = alpha_cal(start_probability ,emission_probability,transition_probability,observations)
    beta = beta_cal(start_probability ,emission_probability,transition_probability,observations)
    
    for t in range(len(observations)-1):
        temp1 = np.multiply(alpha[:,t],beta[:,t+1].transpose())
        temp1 = np.multiply(trans_prob,temp1)
        new_trans_prob = new_trans_prob + np.multiply(temp1,em_prob[:,obs_map[observations[t+1]]].transpose())

    # Normalize
    for i in range(trans_prob.shape[0]):
        new_trans_prob[i,:] = new_trans_prob[i,:]/np.sum(new_trans_prob[i,:])
    
    return new_trans_prob


def train_hmm(start_prob,em_prob,trans_prob,observations,iterations):
    emProbOld,transProbOld = em_prob,trans_prob
    
    for i in range(iterations):
        em_prob = train_emission(start_prob,emProbOld,transProbOld,observations)
        trans_prob = train_transition(start_prob,emProbOld,transProbOld,observations)
        emProbOld,transProbOld = em_prob,trans_prob
        
    return em_prob,trans_prob


# Generae random transition,start and emission probabilities
def randomize(observations,states,poss_obs):
    num_obs = len(poss_obs)
    num_states = len(states)

    a = np.random.random(num_states)
    a /= a.sum()
    start_probability = a

    transition_probability = np.asmatrix(np.zeros((num_states,num_states)))
    for i in range(num_states):
        a = np.random.random(num_states)
        a /= a.sum()
        transition_probability[i,:] = a
            
    emission_probability = np.asmatrix(np.zeros((num_states,num_obs)))
    for i in range(num_states):
        a = np.random.random(num_obs)
        a /= a.sum()
        emission_probability[i,:] = a

    return start_probability,transition_probability,emission_probability



#----------------Program test------------------------
# TODO : Check if z1,z2 are giving correct values, with some other examples
x = alpha_cal(start_probability ,emission_probability,transition_probability,observations)
y = beta_cal(start_probability ,emission_probability,transition_probability,observations)
z1 = forward_backward(start_probability ,emission_probability,transition_probability,observations)


print('===alpha===')
print(x)
print('\n===beta===')
print (y)
print('\n===delta===')
print (z1)

########## Training HMM ####################


start_prob,em_prob,trans_prob=start_probability,emission_probability,transition_probability
forward1 = alpha_cal(start_prob,em_prob,trans_prob,observations)
print "probability of sequence with original parameters : %f"%( np.sum(forward1[:,3]))

num_iter=5
em_prob1,trans_prob1 = train_hmm(start_prob,em_prob,trans_prob,observations,num_iter)
forward1 = alpha_cal(start_prob,em_prob1,trans_prob1,observations)
print "probability of sequence after %d iterations : %f"%(num_iter,np.sum(forward1[:,3]))

