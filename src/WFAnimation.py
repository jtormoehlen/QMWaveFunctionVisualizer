import sys

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation as ani
import WaveFunction as wf
import WFNumeric as wfn
import WFAnalytic as wfa

x = wf.x
dx = wf.dx
t = wfn.t_N

fig = plt.figure(figsize=(6, 4))
ax = plt.subplot(1, 1, 1)
ax.set_xlim(min(x), max(x))
ax.set_ylim(-0.01, 6.E8)
ax.set_xlabel(r'Position $x/$m')
ax.set_ylabel(r'Probability density $|\psi(x,t)|^2/$m$^{-1}$')

an = wfa.psi(x, 0, wfa.psi_x)
psi_an, = ax.plot(x, np.abs(an) ** 2, label='Gauss-Hermite')
norm_an = wf.norm(an)
# an = wfa.psi(x, 0, wfa.psi_alpha)
# psi_an, = ax.plot(x, np.abs(an) ** 2, label='Gauss-Hermite')
# norm_an = wf.norm(an)

rk = wfn.PsiRK().solve()
psi_rk, = ax.plot(x, np.abs(rk.y[:, 0]) ** 2, label='Runge-Kutta')
norm_rk = wf.norm(rk.y[:, 0])

cn = wfn.PsiCN()
psi_cn, = ax.plot(x, np.abs(cn.evolve(0)) ** 2, label='Crank-Nicolson')
norm_cn = wf.norm(cn.evolve(0))

prob_text = ax.text(wf.x_0, 4.5E8, '', fontsize=12)

particle, = ax.plot(wf.x_0, 0., 'ok')


def init():
    ax.plot(x, np.heaviside(wf.V(x), 0.) * 6.E8, '--k')
    return psi_an, psi_rk, psi_cn, prob_text,


def update(i):
    psi2_an = np.abs(wfa.psi(x, t[i], wfa.psi_x)) ** 2 / norm_an
    psi_an.set_ydata(psi2_an)
    # psi2_an = np.abs(wfa.psi(x, t[i], wfa.psi_alpha)) ** 2 / norm_an
    # psi_an.set_ydata(psi2_an)

    psi2_rk = np.abs(rk.y[:, i]) ** 2 / norm_rk
    psi_rk.set_ydata(psi2_rk)

    psi2_cn = np.abs(cn.evolve(i)) ** 2 / norm_cn
    psi_cn.set_ydata(psi2_cn)

    prob_text.set_text(r'$P_{GH}=$' + f'{round(wf.prob(psi2_an), 4)}\n'
                       r'$P_{RK}=$' + f'{round(wf.prob(psi2_rk), 4)}\n'
                       r'$P_{CN}=$' + f'{round(wf.prob(psi2_cn), 4)}')

    particle.set_xdata(wfa.x_t(t[i]))
    return psi_an, psi_rk, psi_cn, prob_text, particle,


plt.legend()
plt.tight_layout()
anim = ani.FuncAnimation(fig, update, init_func=init,
                         frames=len(t), interval=100, blit=True)

wf.param_info()
wfa.info(wfa.psi(x, 2. * wf.t_col(), wfa.psi_x))
wfn.PsiRK().info(rk.y[:, wfn.t_N.size - 1])
cn.info()
if True:
    anim.save('img/barrier.gif', writer='imagemagick',
              fps=10, dpi=100, extra_args=['-layers Optimize'],
              progress_callback=lambda i, n: print(f'Saving frame {i+1} of {n}'))

    sys.exit(0)
else:
    plt.show()
