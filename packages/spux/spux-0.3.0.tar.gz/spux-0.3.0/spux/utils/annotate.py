
import pandas, numpy

# annotate array with the given labels
def annotate (data, labels, time):
    """Annotate array with the given labels."""

    if not isinstance (data, numpy.ndarray):
        data = numpy.array (data)
    shape = (1, len (labels))
    if data.shape != shape:
        data = data.reshape (shape)
    prediction = pandas.DataFrame (data, columns=labels, index=[time]) .iloc [0]
    return prediction
