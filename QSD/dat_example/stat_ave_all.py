#!/usr/bin/env python

import glob
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcol
import matplotlib.cm as cm

def main():
    list_info = []
    list_timeevol = []
    list_dist_ee = []
    list_f = glob.glob("../*/dat_*.npz")
    for f in list_f:
        npz = np.load(f)
        list_info.append(npz["list_info"])
        list_timeevol.append(npz["list_timeevol"])
        list_dist_ee.append(npz["list_dist_ee"])

    Ns = 512
    dt = 0.05
    gammas = [0.002,0.02,0.04,0.1,0.2,0.4,1.0]

    list_all_ee_ave = []
    list_all_ee_err = []
    list_all_te_ave = []
    list_all_te_err = []
    for gamma in gammas:
        mask = [\
            np.abs(list_info[i][0]-Ns)<1e-10 and \
            np.abs(list_info[i][2]-gamma)<1e-10 and \
            np.abs(list_info[i][3]-dt)<1e-10 \
            for i in range(len(list_info))]
        Nsmp = np.sum(mask)
        dat_timeevol = np.array(list_timeevol,dtype=object)[mask]
        dat_dist_ee = np.array(list_dist_ee,dtype=object)[mask]
        dat_ave_timeevol = np.average(dat_timeevol,axis=0)
        dat_err_timeevol = np.sqrt(np.var(dat_timeevol,axis=0)/Nsmp)
        dat_ave_dist_ee = np.average(dat_dist_ee,axis=0)
        dat_err_dist_ee = np.sqrt(np.var(dat_dist_ee,axis=0)/Nsmp)
        list_all_ee_ave.append(dat_ave_dist_ee)
        list_all_ee_err.append(dat_err_dist_ee)
        list_all_te_ave.append(dat_ave_timeevol)
        list_all_te_err.append(dat_err_timeevol)

        fig = plt.figure(figsize=(4,3))
        cmap = plt.get_cmap("tab10")
        plt.xlabel(r"$\mathrm{time}/N_{\mathrm{s}}$")
        plt.ylabel(r"$\overline{S}/N_{\mathrm{s}}$")
        plt.plot(dat_ave_timeevol[:,1]/Ns,dat_ave_timeevol[:,4]/Ns,color=cmap(0))
        plt.fill_between(dat_ave_timeevol[:,1]/Ns,\
            dat_ave_timeevol[:,4]/Ns-dat_err_timeevol[:,4]/Ns,\
            dat_ave_timeevol[:,4]/Ns+dat_err_timeevol[:,4]/Ns,\
            alpha=0.5,edgecolor=cmap(0),facecolor=cmap(0))
        plt.tight_layout()
        plt.xlim(0,2)
        plt.ylim(0,)
        fig.savefig("fig_timeevol_ee_Ns%d_gamma%.6f.pdf"%(Ns,gamma))
        plt.close()

#        fig = plt.figure(figsize=(4,3))
#        cmap = plt.get_cmap("tab10")
#        plt.xlabel(r"$r/N_{\mathrm{s}}$")
#        plt.ylabel(r"$\overline{S}/N_{\mathrm{s}}$")
#        plt.plot(dat_ave_dist_ee[:,0]/Ns,dat_ave_dist_ee[:,1]/Ns,color=cmap(0))
#        plt.fill_between(dat_ave_dist_ee[:,0]/Ns,\
#            dat_ave_dist_ee[:,1]/Ns-dat_err_dist_ee[:,1]/Ns,\
#            dat_ave_dist_ee[:,1]/Ns+dat_err_dist_ee[:,1]/Ns,\
#            alpha=0.5,edgecolor=cmap(0),facecolor=cmap(0))
#        plt.tight_layout()
#        plt.xlim(0,1)
#        plt.ylim(0,)
#        fig.savefig("fig_dist_ee_Ns%d_gamma%.6f.pdf"%(Ns,gamma))
#        plt.close()

    for i,gamma in enumerate(gammas):
        np.savetxt("dat_ee_ave_Ns%d_gamma%.6f"%(Ns,gamma),list_all_ee_ave[i])
        np.savetxt("dat_ee_err_Ns%d_gamma%.6f"%(Ns,gamma),list_all_ee_err[i])

    ## https://stackoverflow.com/questions/25748183/python-making-color-bar-that-runs-from-red-to-blue
    cm1 = mcol.LinearSegmentedColormap.from_list("MyCmapName",["r","b"])
    cnorm = mcol.Normalize(vmin=0,vmax=len(gammas))
    cpick = cm.ScalarMappable(norm=cnorm,cmap=cm1)
    cpick.set_array([])

    fig = plt.figure(figsize=(4,3))
    plt.xlabel(r"$r/N_{\mathrm{s}}$")
    plt.ylabel(r"$\overline{S}/N_{\mathrm{s}}$")
    for i,gamma in enumerate(gammas):
        plt.plot(list_all_ee_ave[i][:,0]/Ns,list_all_ee_ave[i][:,1]/Ns,
            color=cpick.to_rgba(i),label=r"$\gamma/\lambda=%.3f$"%(gamma))
        plt.fill_between(list_all_ee_ave[i][:,0]/Ns,\
            list_all_ee_ave[i][:,1]/Ns-list_all_ee_err[i][:,1]/Ns,\
            list_all_ee_ave[i][:,1]/Ns+list_all_ee_err[i][:,1]/Ns,\
            alpha=0.5,edgecolor=cpick.to_rgba(i),facecolor=cpick.to_rgba(i))
    plt.legend(bbox_to_anchor=(1,1),loc="upper right",borderaxespad=0.5)
    plt.tight_layout()
    plt.xlim(0,1)
    plt.ylim(0,)
    fig.savefig("fig_dist_ee_Ns%d_gamma_all.pdf"%(Ns))
    fig.savefig("fig_dist_ee_Ns%d_gamma_all.png"%(Ns))
    plt.close()

    fig = plt.figure(figsize=(4,3))
    plt.xlabel(r"$r\gamma/\lambda$")
    plt.ylabel(r"$\overline{S_{[0,r]}}/r$")
    for i,gamma in enumerate(gammas):
        ## show data for r=0, 2, 4, ..., Ns/8
        plt.plot(list_all_ee_ave[i][:Ns//8+1:2,0]*gamma,list_all_ee_ave[i][:Ns//8+1:2,1]/list_all_ee_ave[i][:Ns//8+1:2,0],
            ls="None",mfc="None",marker="o",ms="4",
            color=cpick.to_rgba(i),label=r"$\gamma/\lambda=%.3f$"%(gamma))
    plt.legend(bbox_to_anchor=(0,0),loc="lower left",borderaxespad=0.5)
    plt.tight_layout()
    plt.xscale("log")
    plt.ylim(0,1)
    fig.savefig("fig_collapse_ee_Ns%d_gamma_all.pdf"%(Ns))
    fig.savefig("fig_collapse_ee_Ns%d_gamma_all.png"%(Ns))
    plt.close()

    fig = plt.figure(figsize=(4,3))
    cmap = plt.get_cmap("tab10")
    plt.xlabel(r"$\mathrm{time}/N_{\mathrm{s}}$")
    plt.ylabel(r"$\overline{S}/N_{\mathrm{s}}$")
    for i,gamma in enumerate(gammas):
        plt.plot(list_all_te_ave[i][:,1]/Ns,list_all_te_ave[i][:,4]/Ns,
            color=cpick.to_rgba(i),label=r"$\gamma/\lambda=%.3f$"%(gamma))
        plt.fill_between(list_all_te_ave[i][:,1]/Ns,\
            list_all_te_ave[i][:,4]/Ns-list_all_te_err[i][:,4]/Ns,\
            list_all_te_ave[i][:,4]/Ns+list_all_te_err[i][:,4]/Ns,\
            alpha=0.5,edgecolor=cpick.to_rgba(i),facecolor=cpick.to_rgba(i))
    plt.legend(bbox_to_anchor=(1,0),loc="lower right",borderaxespad=0.5)
    plt.tight_layout()
    plt.xlim(0,2)
    plt.ylim(0,)
    fig.savefig("fig_timeevol_ee_Ns%d_gamma_all.pdf"%(Ns))
    fig.savefig("fig_timeevol_ee_Ns%d_gamma_all.png"%(Ns))
    plt.close()

if __name__ == "__main__":
    main()
