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
        self.pi= numpy.ones( (self.n) )* (1/self.n)
        self.a = numpy.ones((self.n,self.n))* (1/self.n)
        self.meansmatrix =  numpy.zeros( (self.n,self.m,self.p) )
        x=numpy.zeros( (self.p,self.p))
        numpy.fill_diagonal(x,1)
        self.covarsmatrix= [[ numpy.matrix(x) for k in xrange(self.m)] for j in xrange(self.n)]
        self.g= numpy.ones ( (self.n,self.m))*1/self.m


    def gaamamixcal(self,alpha,beta,observations):
        self.kernelvaluescal(observations)
        self.gaamamix= numpy.zeros( (len(observations), self.n, self.m) )
        #print self.gaamamix
        gaama=self._gaamacal(alpha,beta,observations)
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


    def _gaamacal(self,alpha,beta,observations):
        gaama=numpy.zeros((self.n,len(observations)))
        #print gaama
        #print len(observations)

        for t in xrange(0,len(observations)):
            numer=0
            for j in xrange(0,self.n):
                numer= alpha[j][t]*beta[j][t]
                denom=0
                for jj in xrange(0,self.n):
                    denom=denom+alpha[jj][t]*beta[jj][t]
                #print numer
                #print denom
                gaama[j][t]= numer/denom

        return gaama

    def kernelvaluescal(self,observations):
        self.kernelvalues=numpy.zeros(( self.n,self.m,len(observations)))
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
        print c
        print numpy.dot( numpy.dot((observation-mean),covarmatrix.I), (observation-mean))
        pdfval = c *  numpy.exp(-0.5 * numpy.dot( numpy.dot((observation-mean),covarmatrix.I), (observation-mean)) )
        # returns zero for very large numbers . how to fix ?
        print pdfval
        return pdfval


        #calucaltion of gaaussian mixture pdf



    def update_model(self,observations):
        self.new_gmatrix=numpy.zeros( (self.n,self.m) )
        self.new_meansmatrix=numpy.zeros( (self.n,self.m,self.p) )
        self.new_covarsmatrix=[[numpy.matrix(numpy.zeros(self.p,self.p)) for k in xrange(self.m)]for j in xrange(self.n)]
        for j in xrange(self.n):
            for k in xrange(self.m):
                term1=0
                term2=0
                for t in xrange(len(observations)):
                    term1=term1+self.gaamamix[j][k][t]
                    term3=term3+self.gaamamix[j][k][t]*observations[t]
                    term4= term4+self.gaamamix[j][k][t]*(observations[t]- meansmatrix[j][k])*(observations[t]-meansmatrix[j][k]).transpose()
                    for kk in xrange(self.m):
                        term2=term2+self.gaamamix[j][kk][t]
                self.new_gmatrix[j][k]=term1/term2
                self.new_meansmatrix[j][k]=term3/term1
                self.new_covarsmatrix[j][k]=term4/term1

    def emissionprobcal(self):
        self.b= numpy.zeros( (self.n,len(observations)) )
        for j in xrange(self.n):
            for t in xrange(len(observations)):
                bjt=0
                for k in xrange( self.m ):
                    bjt=bjt+self.g[j][k]*self.kernelvalues[j][k][t]
                b[j][t]=bjt
        return self.b
