def plot2d(title, x, y, xlabel, ylabel, colors=['red'], lw=[1], ls=['-.'], xaxis=[0,10], yaxis=[0,10], xtick=range(1,10), ytick=range(1,10)):
    import matplotlib.pyplot as plt
    for i in range(len(y)):
        plt.plot(x, y[i], linewidth=lw[i], color = colors[i], linestyle=ls[i])
    plt.xticks(ticks=xtick)
    plt.yticks(ticks=ytick)
    plt.xlim(xaxis[0], xaxis[1])
    plt.ylim(yaxis[0], yaxis[1])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    
def bar(title, y, xlabel, ylabel, colors=['red','blue'], names = [''], yaxis=[0,4], xtick=range(1,10), ytick=range(1,10), width = 0.7):
    import matplotlib.pyplot as plt
    x = [i*1.5 for i in range(len(y))]
    plt.bar(x,y, color=colors, edgecolor='black', tick_label=names)
    plt.xticks(ticks=xtick)
    plt.yticks(ticks=ytick)
    plt.ylim(yaxis[0], yaxis[1])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.savefig('../images/'+title+'.pdf', format = 'pdf')
    plt.show()

def histogram (title, values, nbins, xlabel, ylabel, colors=['red'], xaxis=[0,5], yaxis=[0,5], xtick=range(1,10), ytick=range(1,10), x =[], lcolors = [], lw = [], ls = []):
    import matplotlib.pyplot as plt
    plt.hist(values, bins = nbins)
    plt.xticks(ticks=xtick)
    plt.yticks(ticks=ytick)
    plt.xlim(xaxis[0], xaxis[1])
    plt.ylim(yaxis[0], yaxis[1])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    
def heatmap (title, values, xlabel, ylabel, colors='bwr',  xtick=range(1,10), ytick=range(1,10)):
    from seaborn import heatmap
    ax = heatmap(values, linewidth=1.0, xticklabels = xtick, yticklabels = ytick, cmap=colors)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)