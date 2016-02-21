import tensorflow as tf
import numpy as np


states = ('Healthy', 'Fever')

#list of possible observations
possible_observation = ('normal','cold', 'dizzy')

obs_map =  { 'normal': 0 ,'cold' : 1, 'dizzy':2 }

# The observations that we observe and feed to the model
observations = ('normal', 'dizzy','cold')


# start_probability = {'Healthy': 0.6, 'Fever': 0.4}
#
# transition_probability = {
#    'Healthy' : {'Healthy': 0.7, 'Fever': 0.3},
#    'Fever' : {'Healthy': 0.4, 'Fever': 0.6}
#    }
#
# emission_probability = {
#    'Healthy' : {'normal': 0.5, 'cold': 0.4, 'dizzy': 0.1},
#    'Fever' : {'normal': 0.1, 'cold': 0.3, 'dizzy': 0.6}
#    }

# Numpy arrays of the data
start_probability = np.matrix( '0.6 0.4 ')
transition_probability = np.matrix('0.7 0.3 ;  0.4 0.6 ')
emission_probability = np.matrix( '0.5 0.4 0.1 ; 0.1  0.3  0.6 ' )



def my_forward_theano(state,observations,start_prob,em_prob,trans_prob ):

    # Convert to TensorFlow objects
    em_prob = tf.constant(em_prob)
    trans_prob = tf.constant(trans_prob)
    start_prob = tf.constant ( start_prob )


    total_stages = len(observations)

    ob_ind = obs_map[ observations[0] ]
    alpha = tf.mul ( tf.transpose(em_prob[:,ob_ind]) , start_prob )

    for curr_t in range(1,total_stages):
        ob_ind = obs_map[observations[curr_t]]
        alpha = tf.matmul( alpha , trans_prob)
        alpha = tf.mul( alpha , tf.transpose( em_prob[:,ob_ind] ))

    total_prob = tf.reduce_sum(alpha)
    return ( observations ,total_prob )


# To print the results
x1 , x2 =  my_forward_theano(states,observations , start_probability,emission_probability, transition_probability)
print (x1)
sess = tf.Session()
print(sess.run(x2))


