"""
Use with
from voltage2percentage import voltage2percentage
"""
def volatage2percentage(voltage):
    """
    Input: voltage (float, typically in the range 2.5 to 4.2)
    Output: percentage as a float between 0 and 1
    """
    percentiles = [[3.95 ,90.00],
    [3.9,80.00],
    [3.85,50.00],
    [3.8,40.00],
    [3.72,30.00],
    [3.68,20.00],
    [3.6,10.00],
    [3.0, 0.00]]

    if voltage>4.0:
        return 1.0;

    for perc in percentiles:
        if voltage>perc[0]:
            return perc[1]/100
        return 0.0