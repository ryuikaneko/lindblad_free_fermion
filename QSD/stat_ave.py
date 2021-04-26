#!/usr/bin/env python

import glob
import re
import numpy as np
import matplotlib.pyplot as plt

def main():
    list_info = []
    list_timeevol = []
    list_dist_ee = []
    list_f = glob.glob("dat_*.npz")
    for f in list_f:
        npz = np.load(f)
        list_info.append(npz["list_info"])
        list_timeevol.append(npz["list_timeevol"])
        list_dist_ee.append(npz["list_dist_ee"])
#    print(list_info)
#    print(list_timeevol)
#    print(list_dist_ee)

    Ns = 64
    gamma = 0.01
    dt = 0.05
    mask = [\
        np.abs(list_info[i][0]-Ns)<1e-10 and \
        np.abs(list_info[i][2]-gamma)<1e-10 and \
        np.abs(list_info[i][3]-dt)<1e-10 \
        for i in range(len(list_info))]
#    print(mask)
    Nsmp = np.sum(mask)
#    print(Nsmp)
    dat_timeevol = np.array(list_timeevol)[mask]
    dat_dist_ee = np.array(list_dist_ee)[mask]
#    print(dat_timeevol)
#    print(dat_dist_ee)

    dat_ave_timeevol = np.average(dat_timeevol,axis=0)
    dat_err_timeevol = np.sqrt(np.var(dat_timeevol,axis=0)/Nsmp)
#    print(dat_ave_timeevol)
#    print(dat_err_timeevol)

    dat_ave_dist_ee = np.average(dat_dist_ee,axis=0)
    dat_err_dist_ee = np.sqrt(np.var(dat_dist_ee,axis=0)/Nsmp)
#    print(dat_ave_dist_ee)
#    print(dat_err_dist_ee)

    fig = plt.figure(figsize=(4,3))
    cmap = plt.get_cmap("tab10")
    plt.xlabel(r"$\mathrm{time}/(2N_{\mathrm{s}})$")
    plt.ylabel(r"$\bar{S}/N_{\mathrm{s}}$")
    plt.plot(dat_ave_timeevol[:,1]/Ns,dat_ave_timeevol[:,4]/Ns,color=cmap(0))
    plt.fill_between(dat_ave_timeevol[:,1]/Ns,\
        dat_ave_timeevol[:,4]/Ns-dat_err_timeevol[:,4]/Ns,\
        dat_ave_timeevol[:,4]/Ns+dat_err_timeevol[:,4]/Ns,\
        alpha=0.5,edgecolor=cmap(0),facecolor=cmap(0))
    plt.tight_layout()
    plt.xlim(0,1)
    plt.ylim(0,)
    fig.savefig("fig_timeevol_ee.pdf")
    plt.close()

    fig = plt.figure(figsize=(4,3))
    cmap = plt.get_cmap("tab10")
    plt.xlabel(r"$r/N_{\mathrm{s}}$")
    plt.ylabel(r"$\bar{S}/N_{\mathrm{s}}$")
    plt.plot(dat_ave_dist_ee[:,0]/Ns,dat_ave_dist_ee[:,1]/Ns,color=cmap(0))
    plt.fill_between(dat_ave_dist_ee[:,0]/Ns,\
        dat_ave_dist_ee[:,1]/Ns-dat_err_dist_ee[:,1]/Ns,\
        dat_ave_dist_ee[:,1]/Ns+dat_err_dist_ee[:,1]/Ns,\
        alpha=0.5,edgecolor=cmap(0),facecolor=cmap(0))
    plt.tight_layout()
    plt.xlim(0,1)
    plt.ylim(0,)
    fig.savefig("fig_dist_ee.pdf")
    plt.close()

if __name__ == "__main__":
    main()
