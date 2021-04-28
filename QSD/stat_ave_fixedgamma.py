#!/usr/bin/env python

import glob
import re
import numpy as np
import matplotlib.pyplot as plt

def main():
    Nss = [16,32,64,128,256,512,1024,2048]
    gamma = 0.1
    dt = 0.05

    dat_ee_sizedep = []

    for Ns in Nss:
        list_info = []
        list_timeevol = []
        list_dist_ee = []
        list_f = glob.glob("dat_Ns%d_dt%.6f_gamma%.6f_seed*.npz"%(Ns,dt,gamma))
        for f in list_f:
            npz = np.load(f)
            list_info.append(npz["list_info"])
            list_timeevol.append(npz["list_timeevol"])
            list_dist_ee.append(npz["list_dist_ee"])

        Nsmp = len(list_f)
        dat_timeevol = np.array(list_timeevol)
        dat_ave_timeevol = np.average(dat_timeevol,axis=0)
        dat_err_timeevol = np.sqrt(np.var(dat_timeevol,axis=0)/Nsmp)
        dat_dist_ee = np.array(list_dist_ee)
        dat_ave_dist_ee = np.average(dat_dist_ee,axis=0)
        dat_err_dist_ee = np.sqrt(np.var(dat_dist_ee,axis=0)/Nsmp)

        print("Nsmp",Nsmp)
#        print(len(dat_ave_dist_ee[:,1]))
#        print(dat_ave_dist_ee[:,1])
#        print(dat_ave_dist_ee[Ns//2-2,1])
#        print(dat_ave_dist_ee[Ns//2-1,1])## middle
#        print(dat_ave_dist_ee[Ns//2,1])

        dat_ee_sizedep.append([Ns,dat_ave_dist_ee[Ns//2-1,1],dat_err_dist_ee[Ns//2-1,1]])

        fig = plt.figure(figsize=(4,3))
        cmap = plt.get_cmap("tab10")
        plt.xlabel(r"$\mathrm{time}\times\gamma/\lambda\times 16/N_{\mathrm{s}}$")
        plt.ylabel(r"$\overline{S_{[0,N_{\mathrm{s}}/2]}}/N_{\mathrm{s}}$")
        plt.plot(dat_ave_timeevol[:,1]*gamma*16/Ns,dat_ave_timeevol[:,4]/Ns,color=cmap(0))
        plt.fill_between(dat_ave_timeevol[:,1]*gamma*16/Ns,\
            dat_ave_timeevol[:,4]/Ns-dat_err_timeevol[:,4]/Ns,\
            dat_ave_timeevol[:,4]/Ns+dat_err_timeevol[:,4]/Ns,\
            alpha=0.5,edgecolor=cmap(0),facecolor=cmap(0))
        plt.tight_layout()
        plt.xlim(0,1)
        plt.ylim(0,)
        fig.savefig("fig_timeevol_ee_Ns%d_dt%.6f_gamma%.6f.pdf"%(Ns,dt,gamma))
        plt.close()

        fig = plt.figure(figsize=(4,3))
        cmap = plt.get_cmap("tab10")
        plt.xlabel(r"$\mathrm{time}\times\gamma/\lambda\times 16/N_{\mathrm{s}}$")
        plt.ylabel(r"$\overline{S_{[0,N_{\mathrm{s}}/16]}}/N_{\mathrm{s}}$")
        plt.plot(dat_ave_timeevol[:,1]*gamma*16/Ns,dat_ave_timeevol[:,5]/Ns,color=cmap(0))
        plt.fill_between(dat_ave_timeevol[:,1]*gamma*16/Ns,\
            dat_ave_timeevol[:,5]/Ns-dat_err_timeevol[:,5]/Ns,\
            dat_ave_timeevol[:,5]/Ns+dat_err_timeevol[:,5]/Ns,\
            alpha=0.5,edgecolor=cmap(0),facecolor=cmap(0))
        plt.tight_layout()
        plt.xlim(0,1)
        plt.ylim(0,)
        fig.savefig("fig_timeevol_ee16_Ns%d_dt%.6f_gamma%.6f.pdf"%(Ns,dt,gamma))
        plt.close()

        fig = plt.figure(figsize=(4,3))
        cmap = plt.get_cmap("tab10")
        plt.xlabel(r"$r/N_{\mathrm{s}}$")
        plt.ylabel(r"$\overline{S}/N_{\mathrm{s}}$")
        plt.plot(dat_ave_dist_ee[:,0]/Ns,dat_ave_dist_ee[:,1]/Ns,color=cmap(0))
        plt.fill_between(dat_ave_dist_ee[:,0]/Ns,\
            dat_ave_dist_ee[:,1]/Ns-dat_err_dist_ee[:,1]/Ns,\
            dat_ave_dist_ee[:,1]/Ns+dat_err_dist_ee[:,1]/Ns,\
            alpha=0.5,edgecolor=cmap(0),facecolor=cmap(0))
        plt.tight_layout()
        plt.xlim(0,1)
        plt.ylim(0,)
        fig.savefig("fig_dist_ee_Ns%d_dt%.6f_gamma%.6f.pdf"%(Ns,dt,gamma))
        plt.close()

    dat_ee_sizedep = np.array(dat_ee_sizedep)
    print(dat_ee_sizedep)

    fig = plt.figure(figsize=(4,3))
    cmap = plt.get_cmap("tab10")
    plt.xlabel(r"$N_{\mathrm{s}}$")
    plt.ylabel(r"$\overline{S_{[0,N_{\mathrm{s}}/2]}}}$")
    plt.errorbar(dat_ee_sizedep[:,0],dat_ee_sizedep[:,1],dat_ee_sizedep[:,2],
        marker="o",markersize=4,capsize=4,color=cmap(0))
    plt.tight_layout()
    plt.xscale("log")
#    plt.xlim(,)
#    plt.ylim(,)
    fig.savefig("fig_sizedep_ee_dt%.6f_gamma%.6f.pdf"%(dt,gamma))
    fig.savefig("fig_sizedep_ee_dt%.6f_gamma%.6f.png"%(dt,gamma))
    plt.close()

if __name__ == "__main__":
    main()
