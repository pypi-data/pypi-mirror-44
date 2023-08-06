import numpy as np 


# DEFINE FUNCTIONS
def generate_elevation(t, themu, thesigma):
    '''
    make the elevation record, start of the model run

    requires a mean and std dev for normal distribution to work
    '''
    nt = len(t)
    elev = np.zeros(nt)
    elev[0] = 0
    for j in np.arange(1,nt):
        jt = t[j]
        jump = np.random.normal(themu, thesigma, 1)
        elev[j] = elev[j-1] + jump

    return elev


def generate_stratigraphy(t, elev):
    '''
    make the final stratigraphy by applying the stratigraphic filter

    loop from end to beginning of time to check if elevation was ever lower
    '''
    nt = len(t)
    strat = np.zeros(nt)
    strat[-1] = elev[-1]
    for j in np.flipud(np.arange(0, nt-1)):
        strat[j] = np.array([elev[j], strat[j+1]]).min()

    return strat


def compute_bedthickness(strat):
    '''
    compute the thicknesses of beds preserved in the stratigraphy
    '''
    diff = strat[1:] - strat[:-1]
    thicks = diff[np.nonzero(diff)]
    if len(thicks) > 0:
        meanthick = np.mean(np.array(thicks))
    else:
        meanthick = 0

    return meanthick


def compute_statistics(T, elev, strat):
    '''
    function to compute statistics of the model run

    add more stats by appending to end of list and adding to table setup
    this really needs to be rewritten to use a dictionary
    '''
    stats = []
    stats.append( elev[-1] )                            # final elevation
    stats.append( (sum( elev == strat )-1) / T )        # fraction of time preserved
    stats.append( compute_bedthickness(strat) )         # thickness of beds preserved
    return stats
