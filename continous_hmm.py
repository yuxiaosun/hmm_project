import numpy
class  continuoushmm():
    """for looping over states j iterator is used
    for looping over observations t iterator is used
    for looping over clusterms  k is used
    """
    def __init__(self,n,m,p,a=None,means=None,covarsmatrix=None,g=None,start_prob=None,uniform_initialize=False):
        self.n=n
        self.m=m
        self.p=p
        self.a=a
        self.meansmatrix=means
        self.covarsmatrix=covarsmatrix
        self.g=g
        self.pi=start_prob
        if uniform_initialize:
            self.initialize()


    def initialize(self):
        self.pi= numpy.ones( (self.n))* 1/self.n
        self.a = numpy.ones((self.n,self.n),dtype=numpy.double)* 1/self.n
        self.meansmatrix =  numpy.zeros( (self.n,self.m,self.p),dtype=numpy.double )
        x=numpy.zeros( (self.p,self.p),dtype=numpy.double)
        numpy.fill_diagonal(x,1)
        self.covarsmatrix= [[ numpy.matrix(x) for k in xrange(self.m)] for j in xrange(self.n)]
        self.g= numpy.ones ( (self.n,self.m),dtype=numpy.double)*1/self.m


    def gaamamixcal(self,observations):
        self.kernelvaluescal(observations)
        self.gaamamix= numpy.zeros( (len(observations), self.n, self.m),dtype=numpy.double)
        #print self.gaamamix
        gaama=self._gaamacal(observations)
        for t in xrange(0,len(observations)):
            for j in xrange(self.n):
                numer=0
                denom=0
                for k in xrange(self.m):
                    #print self.g[j][k]
                    #print self.kernelvalues[j][k][t]
                    numer=self.g[j][k]*self.kernelvalues[j][k][t]
                    #print numer
                    #print numer
                    #print numer
                    for kk in range(self.m):
                        denom=denom+self.g[j][kk]*self.kernelvalues[j][kk][t]
                    term2= numer/denom
                    #print term2
                    self.gaamamix[t][j][k]= gaama[j][t]*term2
        #print self.gaamamix
        return self.gaamamix


    def _gaamacal(self,observations):
        self.alphacal(observations)
        self.betacal(observations)
        gaama=numpy.zeros((self.n,len(observations)),dtype=numpy.double)
        #print gaama
        #print len(observations)

        for t in xrange(0,len(observations)):
            numer=0
            for j in xrange(0,self.n):
                numer= self.alpha[j][t]*self.beta[j][t]
                denom=0
                for jj in xrange(0,self.n):
                    denom=denom+self.alpha[jj][t]*self.beta[jj][t]
                #print numer
                #print denom
                gaama[j][t]= numer/denom

        return gaama

    def kernelvaluescal(self,observations):
        self.kernelvalues=numpy.zeros(( self.n,self.m,len(observations)),dtype=numpy.double)
        for j in xrange(self.n):
            for k in xrange(self.m):
                for t in xrange(len(observations)):
                    #print self.meansmatrix[j][k]
                    #print self.covarsmatrix[j][k]
                    #print observations[t]
                    self.kernelvalues[j][k][t]= self._gaussianpdf(self.meansmatrix[j][k],self.covarsmatrix[j][k],observations[t])


    def _gaussianpdf(self,mean,covarmatrix,observation):
        covar_det = numpy.linalg.det(covarmatrix)
        #print mean
        #print type(covarmatrix)
        #print observation
        #print covar_det
        c =  (2.0*numpy.pi)**(float(self.p/2.0)) * (covar_det)**(0.5)
        c=1/c
        #print (observation)
        #print (mean)
        #print numpy.dot( numpy.dot((observation-mean),covarmatrix.I), (observation-mean))
        pdf=numpy.zeros((1),dtype=numpy.double)
        #print -0.5 * numpy.dot( numpy.dot((observation-mean),covarmatrix.I), (observation-mean))
        pdfval = c *  numpy.exp(-0.5 * numpy.dot( numpy.dot((observation-mean),covarmatrix.I), (observation-mean)) )
        # returns zero for very large numbers . how to fix ?
        #print pdfval
        return pdfval


        #calucaltion of gaaussian mixture pdf



    def update_model(self,observations):
        self.gaamamixcal(observations)
        self.new_gmatrix=numpy.zeros( (self.n,self.m) )
        self.new_meansmatrix=numpy.zeros( (self.n,self.m,self.p) )
        x=numpy.zeros( (self.p,self.p),dtype=numpy.double)
        numpy.fill_diagonal(x,1)
        self.new_covarsmatrix= [[ numpy.matrix(x) for k in xrange(self.m)] for j in xrange(self.n)]
        for j in xrange(self.n):
            for k in xrange(self.m):
                term1=0
                term2=0.
                term3=numpy.zeros((self.p),dtype=numpy.double)
                term4=numpy.zeros((self.p,self.p),dtype=numpy.double)
                for t in xrange(len(observations)):
                    print self.gaamamix[t][j][k]
                    term1=term1+self.gaamamix[t][j][k]
                    #print term1
                    term3=term3+self.gaamamix[t][j][k]*observations[t]
                    term4= term4+self.gaamamix[t][j][k]*(observations[t]- self.meansmatrix[j][k])*(observations[t]-self.meansmatrix[j][k]).transpose()
                    for kk in xrange(self.m):
                        term2=term2+self.gaamamix[t][j][kk]
                    #print term1
                    #print term2
                    #print term3
                    #print term4

                    self.new_gmatrix[j][k]=term1/term2
                    self.new_meansmatrix[j][k]=term3/term1
                    self.new_covarsmatrix[j][k]=term4/term1
        #print self.new_gmatrix
        #print self.new_covarsmatrix
        #print self.new_meansmatrix

    def emissionprobcal(self,observations):
        self.b= numpy.zeros( (self.n,len(observations)) )
        for j in xrange(self.n):
            for t in xrange(len(observations)):
                bjt=0
                for k in xrange( self.m ):
                    bjt=bjt+self.g[j][k]*self.kernelvalues[j][k][t]
                self.b[j][t]=bjt
        #print self.b
        return self.b

    def alphacal(self,observations):
        self.emissionprobcal(observations)
        total_stages=len(observations)

        #initializing alphamatrix
        self.alpha= numpy.zeros( (self.n,total_stages) )
        #boundary condition
        #print self.pi
        #print numpy.transpose(self.b[:,0]).shape
        #print numpy.multiply ( numpy.transpose(self.b[:,0]) , self.pi ).transpose()
        self.alpha[:,0] = numpy.multiply ( numpy.transpose(self.b[:,0]) , self.pi ).transpose()
        #print self.alpha[:,0].shape

        for stage in xrange(1,total_stages):
            #temp column vector
            temp_col=numpy.dot(self.a,self.alpha[:,stage-1])
            #print temp_col.shape
            #print numpy.transpose(self.b[:stage]).shape
            #print numpy.multiply( numpy.transpose(self.b[:stage]), temp_col)
            self.alpha[:,stage]=numpy.multiply( numpy.transpose(self.b[:,stage]), (temp_col)).transpose()

        return self.alpha

    def betacal(self,observations):
        total_stages=len(observations)
        self.beta= numpy.zeros( (self.n,total_stages) )
        self.beta[:,-1]=1

        for stage in xrange(total_stages-2,0,-1):
            temp_col=numpy.dot(self.a,self.beta[:,stage+1])
            self.beta[:,stage]=numpy.multiply(numpy.transpose(self.b[:,stage]), (temp_col)).transpose()
        return self.beta







""""def viterbi(self,observations):
    """
