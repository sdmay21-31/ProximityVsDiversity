import urllib
import base64
import io
import matplotlib

matplotlib.use('agg') #noq
plt = matplotlib.pyplot


def plot_to_uri(plt):
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf,format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return uri