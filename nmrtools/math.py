"""In-progress: math routines used across modules found here."""


def add_peaks(plist):
    """
    Reduces a list of (frequency, intensity) tuples to an
    (average frequency, total intensity) tuple.

    Parameter
    --------
    plist: [(float, float)...]
        a list of (frequency, intensity) tuples

    Returns
    -------
    (float, float)
        a tuple of (average frequency, total intensity)
    """
    # TODO: Is this if statement necessary?
    if len(plist) == 1:
        return plist[0]  # nothing to add
    v_total = 0
    i_total = 0
    for v, i in plist:
        v_total += v
        i_total += i
    return v_total / len(plist), i_total


def reduce_peaks(plist_, tolerance=0):
    """
    Takes a list of (x, y) tuples and adds together tuples whose values are
    within a certain tolerance limit.

    Parameters
    ---------
    plist_ : [(float, float)...]
        A list of (x, y) tuples (sorted by x)
    tolerance : float
        tuples that differ in x by <= tolerance are combined using `add_peaks`

    Returns
    -------
    [(float, float)...]
        a list of (x, y) tuples where all x values differ by > `tolerance`
    """
    res = []
    work = []  # an accumulator of peaks to be added
    plist = sorted(plist_)
    for peak in plist:
        if not work:
            work.append(peak)
            continue
        if peak[0] - work[-1][0] <= tolerance:
            work.append(peak)
            continue
        else:
            res.append(add_peaks(work))
            work = [peak]
    if work:  # process any remaining work after for loop
        res.append(add_peaks(work))

    return res


def _normalize(intensities, n=1):
    """
    Scale a list of intensities so that they sum to the total number of
    nuclei.

    Parameters
    ---------
    intensities : [float...]
        A list of intensities.
    n : int
        Number of nuclei.
    """
    factor = n / sum(intensities)
    for index, intensity in enumerate(intensities):
        intensities[index] = intensity * factor


def normalize_spectrum(spectrum, n=1):
    """
    Normalize the intensities in a spectrum so that total intensity equals
    value n (nominally the number of nuclei giving rise to the signal).

    Parameters
    ---------
    spectrum : [(float, float)...]
        a list of (frequency, intensity) tuples.
    n : int or float
        total intensity to normalize to.
    """
    # TODO: refactor to freq, in_ = zip(*spectrum)?
    freq, int_ = [x for x, y in spectrum], [y for x, y in spectrum]
    _normalize(int_, n)
    return list(zip(freq, int_))


def lorentz(v, v0, I, w):
    """
    A lorentz function that takes linewidth at half intensity (w) as a
    parameter.

    When `v` = `v0`, and `w` = 0.5 (Hz), the function returns intensity I.

    Arguments
    ---------
    v : float
        The frequency (x coordinate) at which to evaluate intensity (y
        coordinate).
    v0 : float
        The center of the distribution.
    I : float
        the relative intensity of the signal
    w : float
        the peak width at half maximum intensity

    Returns
    -------
    float
        the intensity (y coordinate) for the Lorentzian distribution
        evaluated at frequency `v`.
    """
    # Adding a height scaling factor so that peak intensities are lowered as
    # they are more broad. If I is the intensity with a default w of 0.5 Hz:
    scaling_factor = 0.5 / w  # i.e. a 1 Hz wide peak will be half as high
    return scaling_factor * I * (
            (0.5 * w) ** 2 / ((0.5 * w) ** 2 + (v - v0) ** 2))

