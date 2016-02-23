import numpy as np

class hmm:

    def __init__(self, states, observations, start_prob , trans_prob,  em_prob):
    
# State and observations are tuples or lists
# start, em and trans_prob 
        self.states = states
        self.observations = observations
        self.start_prob = start_prob
        self.trans_prob = trans_prob
        self.em_prob = em_prob
        
# Raise error if it is wrong data-type

        if(type(self.em_prob) != numpy.matrixlib.defmatrix.matrix):
            raise TypeError("Emission probability is not a numpy Matrix")

        if(type(self.trans_prob) != numpy.matrixlib.defmatrix.matrix):
            raise TypeError("Transition probability is not a numpy Matrix")
        
        if(type(self.start_prob) != numpy.matrixlib.defmatrix.matrix):
            raise TypeError("Start probability is not a numpy Matrix")

        if(type(self.states)!=list or type(self.states)!=tuple):
            raise TypeError("States is not a list/tuple")

        if(type(self.observations)!=list or type(self.observations)!=tuple):
            raise TypeError("Observations is not a list/tuple")

# Convert everything to lists
        self.states=list(self.states)
        self.observations=list(self.observations)

#Dimension Check
        s_len = len(states)
        o_len = len(observations)

        if( (s_len,o_len)!= self.em_prob.shape ):
            print("Input has incorrect dimensions, Correct dimensions is (%d,%d)" % (s_len,o_len))
            raise ValueError("Emission probability has incorrect dimensions")

        if( (s_len,s_len)!= self.trans_prob.shape ):
            print("Input has incorrect dimensions, Correct dimensions is (%d,%d)" % (s_len,s_len))
            raise ValueError("Transition probability has incorrect dimensions")

        if( s_len!= len(self.start_prob)):
            print("Input has incorrect dimensions, Correct dimensions is %d" % s_len)
            raise ValueError("Start probability has incorrect dimensions")

#No negative numbers
        if(not( (self.start_prob>=0).all() )):
            raise ValueError("Negative probabilities are not allowed")

        if(not( (self.em_prob>=0).all() )):
            raise ValueError("Negative probabilities are not allowed")

        if(not( (self.trans_prob>=0).all() )):
            raise ValueError("Negative probabilities are not allowed")

# Summation of probabilities is 1
        # create a list of 1's
        tmp2 = [ 1 for i in range(s_len) ]

        # find summation of emission prob
        summation = np.sum(em_prob,axis=1)
        tmp1 = list (np.squeeze(np.asarray(sum)))

        #Compare
        if(tmp1 != tmp2):
            raise ValueError("Probabilities entered for emission matrix are invalid")
            
        # find summation of transition prob
        summation = np.sum(trans_prob,axis=1)
        tmp1 = list (np.squeeze(np.asarray(sum)))

        #Compare
        if(tmp1 != tmp2):
            raise ValueError("Probabilities entered for transition matrix are invalid")

        summation = np.sum(start_prob,axis=1)
        if (summation[0,0]!=1):
            raise ValueError("Probabilities entered for start state are invalid")

#=========================================================
