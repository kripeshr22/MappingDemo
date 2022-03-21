from numpy import Inf

def custom_metric(A, B):
    # A and B are rows of data; the metric function outputs the distance between the two datapoints
    # Structure of a row of data: [lat, lon, propertyusecode]
    if A[2] == B[2]:
        dist = ((67*(A[0] - B[0]))**2 + (56*(A[1] - B[1]))**2)**0.5
        return dist

    else:
        return Inf
