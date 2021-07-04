from source.helper_functions.circle_conversions import *

def test_can_convert_delta_to_theta():
    assert convert_delta_to_theta(1,0) == 0 or 2*math.pi
    assert convert_delta_to_theta(1,1) == math.pi/4
    assert convert_delta_to_theta(0,1) == math.pi/2
    assert convert_delta_to_theta(-1,1) == 3*math.pi/4
    assert convert_delta_to_theta(-1,0) == math.pi
    assert convert_delta_to_theta(-1,-1) == 5*math.pi/4
    assert convert_delta_to_theta(0,-1) == 3*math.pi/2
    assert convert_delta_to_theta(1,-1) == -math.pi/4
    
def test_can_convert_theta_to_delta():
    assert convert_theta_to_delta(math.pi/180*337.6) == (1,0)
    assert convert_theta_to_delta(math.pi/180*22.4) == (1,0)
    assert convert_theta_to_delta(math.pi/180*22.6) == (1,1)
    assert convert_theta_to_delta(math.pi/180*67.4) == (1,1)
    assert convert_theta_to_delta(math.pi/180*67.6) == (0,1)
    assert convert_theta_to_delta(math.pi/180*112.4) == (0,1)
    assert convert_theta_to_delta(math.pi/180*112.6) == (-1,1)
    assert convert_theta_to_delta(math.pi/180*157.4) == (-1,1)
    assert convert_theta_to_delta(math.pi/180*157.6) == (-1,0)
    assert convert_theta_to_delta(math.pi/180*202.4) == (-1,0)
    assert convert_theta_to_delta(math.pi/180*202.6) == (-1,-1)
    assert convert_theta_to_delta(math.pi/180*247.4) == (-1,-1)
    assert convert_theta_to_delta(math.pi/180*247.6) == (0,-1)
    assert convert_theta_to_delta(math.pi/180*292.4) == (0,-1)
    assert convert_theta_to_delta(math.pi/180*292.6) == (1,-1)
    assert convert_theta_to_delta(math.pi/180*337.4) == (1,-1)
