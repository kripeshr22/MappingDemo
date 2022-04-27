from numpy import Inf
import math

def custom_metric(A, B):
    # A and B are rows of data; the metric function outputs the distance between the two datapoints
    # Structure of a row of data: [lat, lon, propertyusecode, landbaseyear, landvalue, sqftmain]
    ainA, latA, lonA, usecodeA, lbyearA, lvalA, sqftA = A
    ainB, latB, lonB, usecodeB, lbyearB, lvalB, sqftB= B
    dist = Inf
    if usecodeA == usecodeB:      
        if abs(sqftA-sqftB) < 2000:
            dist = ((67*(latA - latB))**2 + (56*(lonA - lonB))**2)**0.5
            dist *= 1.5**abs(lbyearA - lbyearB)
    return dist
