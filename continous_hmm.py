class  continuoushmm():
    """for looping over states j iterator is used
    for looping over observations t iterator is used
    for looping over clusterms  k is used
    """
    def __init__(self,n,m,p,a,means,covars,g,start_prob):
        self.p=p
        self.a=a
        self.means=means
        self.covars=covars
        self.g=g
        self.pi=start_prob

    def initialize(self):
        self.pi= numpy.ones( (self.n) )* (1/self.n)
        self.a = numpy.ones((self.n,self.n))* (1/self.n)
        self.mean = numpy.ones( numpy.zeros( (self.n,self.m,self.p) ) )
        self.covars= [ [numpy.ones(self.p,self.p) for k in xrange(self.m) ] for j in xrange(self.n) ]


    def gaamamixcal(self,alpha,beta,observations):
        self.gaamamix= numpy.zeros( (len(observations), self.n, self.m) )
        gaama=self._gaamacal(alpha,beta)
        for t in xrange(0,len(observations)):
            for j in xrange(self.n):
                numer=0
                denom=0
                for k in xrange(self.m):
                    numer=g[j][k]*self.kernerlvalues[j][k][t]
                    for kk in range(self.m):
                        denom=denom+g[j][kk]*self.kernerlvalues[j][kk][t]
                    term2= numer/denom
                    gaamamix[t][j][k]= gaama[j][t]*term2
        return self.gaamamix


    def _gaamacal(self,alpha,beta):
        gaama=numpy.zeros((self.n,self.m))

        for t in xrange(0,len(observations)):
            numer=0
            for j in xrange(0,self.n):
                numer= alpha[j][t]*beta[j][t]
                denom=0
                for jj in xrange(0,self.n):
                    denom=+ alpha[jj][t]*beta[jj][t]
                gaama[j][t]= numer/denom

        return gaama

    def kernelvaluescal(self,observations):
        self.kernelvalues=numpy.zeros(( self.n,self.m,len(observations)))
        for j in xrange(self.n):
            for k in xrange(self.m):
                for t in xrange(len(observations)):
                    self.kernelvalues[j][k][t]= self._gaussianpdf(mean,covarmatrix,observation)

        return self.kernelvalues

    def _gaussianpdf(self,mean,covarmatrix,observation):
        covar_det = numpy.linalg.det(covarmatrix)
        c =  (2.0*numpy.pi)**(float(self.p/2.0)) * (covar_det)**(0.5)
        c=1/c
        pdfval = c * numpy.exp(-0.5 * numpy.dot( numpy.dot((observation-mean),covarmatrix.I), (observation-mean)) )


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
                self.meansmatrix[j][k]=term3/term1
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
