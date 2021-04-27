#!/usr/bin/env python

import numpy as np
import scipy.sparse
import scipy.sparse.linalg
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="quantum trajectory free fermion")
    parser.add_argument("-Ns",metavar="Ns",dest="Ns",type=np.int64,default=128,help="set Ns (default: 128)")
    parser.add_argument("-dt",metavar="dt",dest="dt",type=np.float64,default=0.05,help="set dt (default: 0.05)")
    parser.add_argument("-gamma",metavar="gamma",dest="gamma",type=np.float64,default=0.01,help="set gamma (default: 0.01)")
    parser.add_argument("-seed",metavar="seed",dest="seed",type=np.int64,default=12345,help="set seed (default: 12345)")
    return parser.parse_args()

def make_ham(tij,Ns):
#    ham = scipy.sparse.diags([tij[:-1],tij[:-1]],[-1,1],format="csr") ## open BC
    ham = scipy.sparse.diags([tij[:-1],tij[:-1],tij[-1:],tij[-1:]],[-1,1,Ns-1,1-Ns],format="csr") ## periodic BC
    return ham

def make_cdw(Ns,Ne):## Ne=Ns/2, this state is already normalized
    state = np.zeros((Ns,Ne),dtype=np.float64)
    for i in range(Ne):
        state[2*i,i] = 1.0
    return state

def update_state(dt,ham,gamma,ni,Ns,state):
    state = scipy.sparse.linalg.expm_multiply((-1j)*dt*ham,state,start=0.0,stop=1.0,num=2,endpoint=True)[1]
    exp_dw_ngt = np.exp( np.random.normal(0.0,np.sqrt(gamma*dt),Ns) + (2.0*ni-1.0)*gamma*dt )
    mij = scipy.sparse.diags([exp_dw_ngt],[0],format="csr")
    state = mij@state
    state,_ = scipy.linalg.qr(state,mode="economic")## normalization
    return state

def calc_aiaj(state):
    return state@state.conj().T

def calc_ni_from_aiaj(aiaj):
    return np.diag(aiaj).real

def calc_nA_nB_from_ni(ni):
    return np.average(ni[0::2]), np.average(ni[1::2])

def calc_ee(aiaj,size):
    lmd = scipy.linalg.eigvalsh(aiaj[:size,:size])
    omlmd = 1.0 - lmd
    ## ignore zero eigenvalues since l*log(l)=0 if l=0
    ## ignore tiny negative eigenvalues caused by numerical error
    lmd = lmd[lmd>0]
    omlmd = omlmd[omlmd>0]
    ee = - np.sum(lmd * np.log2(lmd)) - np.sum(omlmd * np.log2(omlmd))
    return ee


def main():
    args = parse_args()
    Ns = args.Ns
    dt = args.dt
    gamma = args.gamma
    seed = args.seed

    Ne = Ns//2
    if Ns < 16:
        print("## choose Ns >= 16")
        return -1
    Nstep = int(1.0/dt/gamma * Ns/16 + 1e-10)
    Nmeasure = Nstep//128 if Nstep>=128 else Nstep
    np.random.seed(seed=seed)
    tij = np.ones(Ns)
    ham = make_ham(tij,Ns)
    if Ns*gamma < 1:
        print("## Ns*gamma > 1 is recommended")
    print("# Ns",Ns)
    print("# Ne",Ne)
    print("# gamma",gamma)
    print("# dt",dt)
    print("# Nstep",Nstep)
    print("# Nmeasure",Nmeasure)
    print("# seed",seed)
    list_info = [Ns,Ne,gamma,dt,Nstep,seed]

    list_timeevol = []
    state = make_cdw(Ns,Ne)
    aiaj = calc_aiaj(state)
    ni = calc_ni_from_aiaj(aiaj)
    nA,nB = calc_nA_nB_from_ni(ni)
    ee = calc_ee(aiaj,Ne)
    ee16 = calc_ee(aiaj,Ns//16)
    print("\n")
    print("# time evolution of nA nB ee ee16")
#    print(0,0.0,nA,nB,ee,e16)
    list_timeevol.append([0,0.0,nA,nB,ee,ee16])

    for step in range(1,Nstep+1):
        state = update_state(dt,ham,gamma,ni,Ns,state)
        aiaj = calc_aiaj(state)
        ni = calc_ni_from_aiaj(aiaj)
        if step%Nmeasure == 0:
            nA,nB = calc_nA_nB_from_ni(ni)
            ee = calc_ee(aiaj,Ne)
            ee16 = calc_ee(aiaj,Ns//16)
#            print(step,dt*step,nA,nB,ee,ee16)
            list_timeevol.append([step,dt*step,nA,nB,ee,ee16])

    list_dist_ee = []
    print("\n")
    print("# distance depndence of ee at time=Ns/gamma/16")
    for size in range(1,Ns):
        ee = calc_ee(aiaj,size)
#        print(size,ee)
        list_dist_ee.append([size,ee])

    np.savez_compressed("dat_Ns%d_dt%.6f_gamma%.6f_seed%d.npz"%(Ns,dt,gamma,seed),
        list_info=list_info,\
        list_timeevol=list_timeevol,\
        list_dist_ee=list_dist_ee,\
        )

if __name__ == "__main__":
    main()
