import matplotlib.pyplot as plt
import sys, time
import numpy as np
import os
from scipy import interpolate
from matplotlib.pyplot import cm
plt.style.use('classic')
path ="/home/ml/kkheta2/sowo_a2ocdelib/serverbackup/multipleruns"
plt.ion()
fig = plt.figure()
plt.show(block=False)
refresh_rate = 5.0


def handle_close(evt):
  sys.exit()


def errorfill(x, y, yerr, color=None, alpha_fill=0.3, ax=None):
    ax = ax if ax is not None else plt.gca()
    if color is None:
        color = ax._get_lines.color_cycle.next()
    if np.isscalar(yerr) or len(yerr) == len(y):
        ymin = y - yerr
        ymax = y + yerr
    elif len(yerr) == 2:
        ymin, ymax = yerr
    ax.plot(x, y, color=color)
    ax.fill_between(x, ymax, ymin, color=color, alpha=alpha_fill)

colors = ["blue", "red", "green", "black", "violet", "crimson", "dimgrey", "magenta", "deepskyblue", "teal", "lime"]
friendly_colors = ['#377eb8', '#f781bf', '#4daf4a', '#a65628', '#984ea3',
                  '#ff7f00', '#999999', '#e41a1c', '#dede00']

show_term = "--term" in sys.argv

data = []
indices = []
data_std = []

plt.clf()
weight_moves = False
for i in range(len(sys.argv[1:])):
    if "--" in sys.argv[i+1]:
        continue
    data_y = []
    data_y_std = []
    indice_x = []
    filenames = []
    filename = sys.argv[i+1]
    runs = 2
    parts = filename.split('/')
    for run in range(1,runs+1):
        name = 'models_run'+ str(run)
        parts[-3] = name
        filename = ('/').join(parts)
        if ".csv" not in filename: filename += "/data.csv"
        filenames.append(filename)  # List of all runs for each parameter

    minimum_x = []
    maximum_x = []
    interpolators = []
    for run_filename in filenames:
        d = []
        e = []
        f = open(run_filename, "rb")
        for j, line in enumerate(f):
            if not line.split(",")[0].isdigit(): continue
            if weight_moves or ("," in line):
                d.append(float(line.split(",")[1]))
                e.append(int(line.split(",")[0]))
                weight_moves = True
            else:
                d.append(int(line))
                weight_moves = False
        f.close()
        data_y.append(d) #All 5 runs are now stored in data.
        indice_x.append(e)


    minimum_x = [min(indice_x[i]) for i in range(runs)]
    maximum_x = [max(indice_x[i]) for i in range(runs)]

    end_point = np.max(maximum_x)
    #---------------------------Averaging across runs and interpolating values before that-------------------------------------
    ys = np.zeros((runs,end_point+1))
    x = np.linspace(0,end_point+1,end_point+1)
    for run in range(runs):
        #print("Run # ", run)
        for i in range(len(indice_x[run])-1):
            ys[run,indice_x[run][i]:indice_x[run][i+1]] = data_y[run][i]
        ys[run, indice_x[run][i+1]:] = data_y[run][i+1]
    y_mean = np.mean(ys, 0)
    y_std = np.std(ys, 0)

    idxs = sorted(np.random.choice(range(end_point+1), 10000, replace=False))
    data.append(y_mean[idxs])
    data_std.append(y_std[idxs])
    #indices.append(x)
    indices.append(idxs)

while True:
  try:
    a = int(max([len(each) for each in data])/250)+1
    if weight_moves:
      a = int(float(max([i[-1] for i in indices]))/250)
    d2 = []
    all_p = []
    i = -1
    color_count = 0
    for i in range(len(data)):
      if weight_moves:
        frame_interval = a
        new_matrix = []
        one_row = []
        counter = 0
        count = 0
        new_matrix_std = []
        one_row_std = []
        counter_std = 0
        count_std = 0
        while count < len(data[i]):
          if indices[i][count] > (counter+1)*frame_interval:
            if len(one_row) == 0:
              if len(new_matrix) == 0:
                one_row = [data[i][count]]
              else:
                one_row = [new_matrix[-1]]
            new_matrix.append(np.mean(one_row))
            one_row = []
            counter += 1
          else:
            one_row.append(data[i][count])
            count += 1
        while count_std < len(data_std[i]):
          if indices[i][count_std] > (counter_std+1)*frame_interval:
            if len(one_row_std) == 0:
              if len(new_matrix_std) == 0:
                  one_row_std = [data_std[i][count_std]]
              else:
                  one_row_std = [new_matrix_std[-1]]
            new_matrix_std.append(np.mean(one_row_std))
            one_row_std = []
            counter_std += 1
          else:
            one_row_std.append(data_std[i][count_std])
            count_std += 1
        p, = plt.plot(np.array(range(len(new_matrix))) * frame_interval, np.array(new_matrix), linewidth=3, color=friendly_colors[color_count])
        #import pdb;pdb.set_trace()
        p = plt.fill_between(np.array(range(len(new_matrix))) * frame_interval, np.array(new_matrix)-np.array(new_matrix_std), np.array(new_matrix)+np.array(new_matrix_std), facecolor=friendly_colors[color_count], alpha=0.2)
        color_count += 1
      else:
        #p, = plt.plot(np.array(data[i][:-(len(data[i])%a)]).reshape(((len(data[i])-(len(data[i])%a))/a,a)).mean(axis=1).flatten(), linewidth=2, color=next(colors))
	p, = plt.plot(np.array(data[i][:-(len(data[i])%a)]).reshape(((len(data[i])-(len(data[i])%a))/a,a)).mean(axis=1).flatten(), linewidth=3, color=friendly_colors[color_count])
        color_count += 1
      all_p.append(p)
    legends = []
    legendsforpaper = []

    for dd in sys.argv[1:]:
      if "--" not in dd:
        legend = dd.split("/")[-1]
        tempname = legend.split("_MC0.99_")[-1]
        psivalue = float((tempname.split("_")[0]).split("C")[1])
        optvalue = (tempname.split("_")[1]).split("OPT")[1]
        epsvalue = float((tempname.split("_")[2]).split("EPS")[1])
	if psivalue!=0:
		tname = " ( Safe-A2OC )"
	else:
		tname = " ( A2OC )"
        #tempname1 = "$\psi$={:4.2f}, $\epsilon$={:4.2f}".format(psivalue, epsvalue) + tname
	tempname1 = "$\psi$={:4.2f}".format(psivalue) + tname
        legendsforpaper.append(tempname1)
    #plt.legend(all_p, legends, prop={'size': 10}, loc='upper left', handletextpad=0.1, fancybox=True, framealpha=0.5)
    plt.legend(all_p, legendsforpaper, prop={'size': 10}, loc='upper left', handletextpad=0.1, fancybox=True, framealpha=0.5)
    plt.xlabel("Frames", fontsize=14)
    plt.ylabel("Score", fontsize=14)
    fig.canvas.mpl_connect('close_event', handle_close)
    plt.draw()
    plt.savefig((os.path.join(path,"Enduro_4options_learningcurve_sowo_less"+ ".png")), dpi=200, facecolor='w', edgecolor='w',
            orientation='portrait', papertype=None, format=None,
            transparent=True, bbox_inches='tight', pad_inches=0,
            frameon=None, figsize=(5, 5))
    plt.pause(refresh_rate)
  except Exception, e:
    print e
    time.sleep(2)
    pass
