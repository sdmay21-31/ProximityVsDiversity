import urllib
import base64
import io

import matplotlib
matplotlib.use('agg')
    
from matplotlib import pyplot as plt

def get_plt():
    plt.close()
    return plt


def plot_to_uri(plt):
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf,format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return uri