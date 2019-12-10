import dask.array as da

from .scipy_stats_sampling import sample_distribution, virtually_sample_distribution
from .sampling import change_virtual_samples

def from_scipy(stats_distribution, *args, samples=1, sample_chunksize=None, sample=False, **kwargs):
    """Create a virtual distribution into dask from scipy.stats with parameters given as xarray objects

    For the virtual sampling idea look at :py:func`xrrandom.sampling.generate_virtual_samples``

    Parameters
    ----------
    stats_distribution : str or scipy.stats.rv_continuous or scipy.stats.rv_discrete
        name of a scipy.sats distribution or a specific distribution object
    samples : int, optional
        number of samples to draw, defaults to 1
    sample_chunksize : ints, optional
        if given, the sample dimension will have this chunksize
    *args, **kwargs : scalar or  array_like or xarray objects
        positional and keyword arguments to the rvs() method of *stats_distribution*


    Returns
    -------
    samples : xarray object
        xarray representing the given distribution with arguments broadcasted according to dimensions
        and a new dimension 'sample' with size *samples*
        the data will be a dask Array

    Raises
    ------
    ValueError
        if the *stats_distribution* cannot be found or is not a valid distribution object
    """
    if sample:
        # TODO: warn or raise exception if sample_chunksize is not None?
        return sample_distribution(stats_distribution, samples, *args, **kwargs)
    else:
        return virtually_sample_distribution(stats_distribution, samples, *args, 
                                             sample_chunksize=sample_chunksize, **kwargs)

def sample(distribution, samples=None):
    """Sample virtual distribution

    Parameters
    ----------
    distribution : xarray.DataArray
        xarray representing the virtual distribution
    samples : int, optional
        number of samples to be generated, defaults to the number of samples specified
        when creating the distribution


    Returns
    -------
    samples : xarray object
        samples from the given distribution
    """
    if not isinstance(distribution.data, da.Array):
        raise TypeError('`distribution` must be dask xarray')
    if samples is not None:
        distribution = change_virtual_samples(distribution, new_sample_count=samples)
    
    return distribution.compute()