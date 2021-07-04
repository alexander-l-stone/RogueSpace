import math

halfangle = 22.5/180*math.pi

#TODO: Make all this fast with duh look ups
def convert_delta_to_theta(dx, dy):
    if dx < 0:
        return math.atan(dy/dx) + math.pi
    elif dx > 0:
        return math.atan(dy/dx)
    else:
        if (dy >= 1):
            return math.pi/2
        elif(dy <= -1):
            return 3*math.pi/2
        else:
            raise ValueError

def convert_theta_to_delta(theta):
    if ((theta <= 0 + halfangle and theta > 0 - halfangle ) or (theta <= 2*math.pi + halfangle and theta > 2*math.pi - halfangle)):
        return (1,0)
    elif (theta <= math.pi/4 + halfangle and theta > math.pi/4 - halfangle ):
        return (1,1)
    elif (theta <= math.pi/2 + halfangle and theta > math.pi/2 - halfangle ):
        return (0,1)
    elif (theta <= 3*math.pi/4 + halfangle and theta > 3*math.pi/4 - halfangle ):
        return (-1,1)
    elif (theta <= math.pi + halfangle and theta > math.pi - halfangle ):
        return (-1,0)
    elif (theta <= 5*math.pi/4 + halfangle and theta > 5*math.pi/4 - halfangle ):
        return (-1,-1)
    elif (theta <= 3*math.pi/2 + halfangle and theta > 3*math.pi/2 - halfangle ):
        return (0,-1)
    elif (theta <= 7*math.pi/4 + halfangle and theta > 7*math.pi/4 - halfangle ):
        return (1,-1)