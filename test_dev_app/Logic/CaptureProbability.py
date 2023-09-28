def calculateCaptureprobability(k):
    if k<0:
        raise Exception("k is smaller than 0, please provide a k value bigger than 0")
    if k==1:
        return 1/10
    if k==0:
        return 0
    else:
        return ((9**(k-1))/((10**k)))+calculateCaptureprobability(k-1)