# Lindblad dynamics free fermion chain

- types of trajectory dynamics
  - quantum state diffusion (QSD)
  - "raw" quantum state diffusion mimicking a non-unitary circuit evolution (QSDc)
  - quantum jump evolution (QJ)

- examples
  - QSD: See Fig.4 in https://doi.org/10.21468/SciPostPhys.7.2.024<br>
    (our gamma/lambda=1 corresponds to their gamma=0.5)
    - time evolution of entanglement entropy<br>
      ![time evolution](./QSD/dat_example/Ns512/fig_timeevol_ee_Ns512_dt0.050000_gamma_all.png)
    - distance dependence of entanglement entropy<br>
      ![distance dependence](./QSD/dat_example/Ns512/fig_dist_ee_Ns512_dt0.050000_gamma_all.png)
    - data collapse of entanglement entropy<br>
      ![data collapse](./QSD/dat_example/Ns512/fig_collapse_ee_Ns512_dt0.050000_gamma_all.png)
  - QSD: See Fig.1(c) in https://arxiv.org/abs/2005.09722<br>
    - size dependence of entanglement entropy at gamma/lambda=0.1<br>
      ![data collapse](./QSD/dat_example/gamma0.1/fig_sizedep_ee_dt0.050000_gamma0.100000.png)
    - size dependence of entanglement entropy at gamma/lambda=0.25<br>
      ![data collapse](./QSD/dat_example/gamma0.25/fig_sizedep_ee_dt0.050000_gamma0.250000.png)

- References
  - https://doi.org/10.21468/SciPostPhys.7.2.024 (hopping: lambda=1/2)
  - https://doi.org/10.1103/PhysRevLett.126.170602 (https://arxiv.org/abs/2005.09722) (hopping: lambda=1)
  - https://arxiv.org/abs/2104.09118 (long-range hopping)
  - (hopping: lambda=1 in our notation)
