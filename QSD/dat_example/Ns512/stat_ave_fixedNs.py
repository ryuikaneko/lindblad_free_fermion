#!/usr/bin/env python

import glob
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcol
import matplotlib.cm as cm

def main():
    Ns = 512
#    gammas = [1.0,0.4,0.2,0.1,0.04,0.02,0.01]
    gammas = [0.01,0.02,0.04,0.1,0.2,0.4,1.0]
    dt = 0.05

    dat_ee_gdep = []
    dat_te_gdep = []

    for gamma in gammas:
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

        dat_ee_gdep.append([gamma,dat_ave_dist_ee[:,0],dat_ave_dist_ee[:,1],dat_err_dist_ee[:,1]])
        dat_te_gdep.append([gamma,dat_ave_timeevol[:,1],dat_ave_timeevol[:,4],dat_err_timeevol[:,4]])

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

#    print(dat_ee_gdep[0][0])
#    print(dat_ee_gdep[0][1])
#    print(dat_ee_gdep[0][2])
#    print(dat_ee_gdep[0][3])

    ## https://stackoverflow.com/questions/25748183/python-making-color-bar-that-runs-from-red-to-blue
    cm1 = mcol.LinearSegmentedColormap.from_list("MyCmapName",["r","b"])
    cnorm = mcol.Normalize(vmin=0,vmax=len(gammas))
    cpick = cm.ScalarMappable(norm=cnorm,cmap=cm1)
    cpick.set_array([])

    fig = plt.figure(figsize=(4,3))
    cmap = plt.get_cmap("tab10")
    plt.xlabel(r"$r/N_{\mathrm{s}}$")
    plt.ylabel(r"$\overline{S}/N_{\mathrm{s}}$")
    for i,gamma in enumerate(gammas):
        plt.plot(dat_ee_gdep[i][1]/Ns,dat_ee_gdep[i][2]/Ns,
            color=cpick.to_rgba(i),label=r"$\gamma/\lambda=%.3f$"%(gamma))
        plt.fill_between(dat_ee_gdep[i][1]/Ns,
            dat_ee_gdep[i][2]/Ns-dat_ee_gdep[i][3]/Ns,
            dat_ee_gdep[i][2]/Ns+dat_ee_gdep[i][3]/Ns,
            alpha=0.5,edgecolor=cpick.to_rgba(i),facecolor=cpick.to_rgba(i))
    plt.legend(bbox_to_anchor=(1,1),loc="upper right",borderaxespad=0.5)
    plt.tight_layout()
    plt.xlim(0,1)
    plt.ylim(0,)
    fig.savefig("fig_dist_ee_Ns%d_dt%.6f_gamma_all.pdf"%(Ns,dt))
    fig.savefig("fig_dist_ee_Ns%d_dt%.6f_gamma_all.png"%(Ns,dt))
    plt.close()

    fig = plt.figure(figsize=(4,3))
    plt.xlabel(r"$r\gamma/\lambda$")
    plt.ylabel(r"$\overline{S_{[0,r]}}/r$")
    for i,gamma in enumerate(gammas):
        ## show data for r=0, 2, 4, ..., Ns/8
        plt.plot(dat_ee_gdep[i][1][:Ns//8+1:2]*gamma,
            dat_ee_gdep[i][2][:Ns//8+1:2]/dat_ee_gdep[i][1][:Ns//8+1:2],
            ls="None",mfc="None",marker="o",ms="4",
            color=cpick.to_rgba(i),label=r"$\gamma/\lambda=%.3f$"%(gamma))
    plt.legend(bbox_to_anchor=(0,0),loc="lower left",borderaxespad=0.5)
    plt.tight_layout()
    plt.xscale("log")
    plt.ylim(0,1)
    fig.savefig("fig_collapse_ee_Ns%d_dt%.6f_gamma_all.pdf"%(Ns,dt))
    fig.savefig("fig_collapse_ee_Ns%d_dt%.6f_gamma_all.png"%(Ns,dt))
    plt.close()

    fig = plt.figure(figsize=(4,3))
    plt.xlabel(r"$\mathrm{time}/N_{\mathrm{s}}\times\gamma/\lambda$")
    plt.ylabel(r"$\overline{S}/N_{\mathrm{s}}$")
    for i,gamma in enumerate(gammas):
        plt.plot(dat_te_gdep[i][1]/Ns*gamma,dat_te_gdep[i][2]/Ns,
            color=cpick.to_rgba(i),label=r"$\gamma/\lambda=%.3f$"%(gamma))
        plt.fill_between(dat_te_gdep[i][1]/Ns*gamma,\
            dat_te_gdep[i][2]/Ns-dat_te_gdep[i][3]/Ns,\
            dat_te_gdep[i][2]/Ns+dat_te_gdep[i][3]/Ns,\
            alpha=0.5,edgecolor=cpick.to_rgba(i),facecolor=cpick.to_rgba(i))
    plt.legend(bbox_to_anchor=(1,0),loc="lower right",borderaxespad=0.5)
    plt.tight_layout()
    plt.xlim(0,)
    plt.ylim(0,)
    fig.savefig("fig_timeevol_ee_Ns%d_dt%.6f_gamma_all.pdf"%(Ns,dt))
    fig.savefig("fig_timeevol_ee_Ns%d_dt%.6f_gamma_all.png"%(Ns,dt))
    plt.close()

if __name__ == "__main__":
    main()
