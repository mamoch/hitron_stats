# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pylab as plt
from matplotlib.dates import strpdate2num, AutoDateLocator, AutoDateFormatter
import ConfigParser

cfgPars  = ConfigParser.RawConfigParser()
cfgPars.read('hitron.cfg')

downFile = cfgPars.get('Stat files', 'downFile')
upFile = cfgPars.get('Stat files', 'upFile')

dataDown = np.loadtxt(downFile, \
                      converters={0: strpdate2num('%Y-%m-%dT%H:%M:%S')})
dataUp = np.loadtxt(upFile, \
                    converters={0: strpdate2num('%Y-%m-%dT%H:%M:%S')})

##################################################
# plot function
def plot_data(upDown, col, ylabel, title):
    if upDown == 'down':
        data = dataDown
        number = 8
    elif upDown == 'up':
        data = dataUp
        number = 4
    fig = plt.figure()
    ax = fig.add_axes([0.13, 0.13, 0.68, 0.8])
    
    for i in np.arange(number):
        ind = np.where(data[:, 1] == i+1)[0]
        ax.plot(data[ind, 0], data[ind, col], marker='.', label='Port '+str(i+1))
    
    autoDL = AutoDateLocator()
    autoDF = AutoDateFormatter(autoDL)
    
    ax.xaxis.set_major_locator(autoDL)
    ax.xaxis.set_major_formatter(autoDF)
    
    fig.autofmt_xdate()
    ax.set_ylabel(ylabel)
    ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0)
    ax.set_title(title)
##################################################

##################################################
# save function
def save_plot(name):
    plt.savefig('hitron_stats_'+name+'.pdf')
    #plt.savefig('hitron_stats_'+name+'.png', dpi=300)
#################################################

plot_data('down', 3, 'frequency (MHz)', 'Downstream: frequency')
save_plot('downFrq')
plot_data('down', 6, u'signal strenth (dBμV)', 'Downstream: signal strength')
save_plot('downSigStr')
plot_data('down', 7, 'SNR (dB)', 'Downstream: signal-to-noise ratio')
save_plot('downSNR')

plot_data('up', 3, 'frequency (MHz)', 'Upstream: frequency')
save_plot('upFrq')
plot_data('up', 6, u'signal strenth (dBμV)', 'Upstream: signal strength')
save_plot('upSigStr')

plt.show()
