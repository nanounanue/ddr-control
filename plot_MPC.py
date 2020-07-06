from matplotlib import animation
import matplotlib.pyplot as plt
import numpy as np

def plot_mpc(x_ref, u_ref, x_mpc, u_mpc, phi_mpc):
    
    kmax = len(x_mpc)
    iteraciones = np.arange(kmax)
    
    fig, axs = plt.subplots(4, 2, figsize=(16,16))
    
    #Errores en x
    axs[0,0].axhline(0, ls='--', color='r', alpha=0.9)
    axs[0,0].plot(iteraciones, x_mpc[:,0] - x_ref[:kmax,0], label=r"$e_x$", alpha=0.7)
    axs[0,0].plot(iteraciones, x_mpc[:,1] - x_ref[:kmax,1], label=r"$e_y$", alpha=0.7)
    axs[0,0].plot(iteraciones, x_mpc[:,2] - x_ref[:kmax,2], label=r"$e_\theta$", alpha=0.7)
    axs[0,0].grid(color='gray', linestyle='--')
    axs[0,0].legend(fontsize=15)
    axs[0,0].set_title(r"Error en $x$", fontsize=19)
    
    #Errores en u
    axs[0,1].axhline(0, ls='--', color='r', alpha=0.9)
    axs[0,1].plot(iteraciones, u_mpc[:,0] - u_ref[:kmax,0], label=r"$e_v$", alpha=0.7)
    axs[0,1].plot(iteraciones, u_mpc[:,1] - u_ref[:kmax,1], label=r"$e_\omega$", alpha=0.7)
    axs[0,1].grid(color='gray', linestyle='--')
    axs[0,1].legend(fontsize=15)
    axs[0,1].set_title(r"Error en $u$", fontsize=19)
    
    #Estados x
    axs[1,0].plot(iteraciones, x_mpc[:,0], 'g', label=r"$x_{mpc}$", alpha=0.6)
    axs[1,0].plot(iteraciones, x_ref[:kmax,0], '-.g', label=r"$x_{ref}$", alpha=0.7)
    axs[1,0].grid(color='gray', linestyle='--')
    axs[1,0].legend(fontsize=15)
    axs[1,0].set_title(r"$x$", fontsize=19)
    
    axs[2,0].plot(iteraciones, x_mpc[:,1], 'b', label=r"$y_{mpc}$", alpha=0.6)
    axs[2,0].plot(iteraciones, x_ref[:kmax,1], '-.b', label=r"$y_{ref}$", alpha=0.7)
    axs[2,0].grid(color='gray', linestyle='--')
    axs[2,0].legend(fontsize=15)
    axs[2,0].set_title(r"$y$", fontsize=19)
    
    axs[3,0].plot(iteraciones, x_mpc[:,2], 'r', label=r"$\theta_{mpc}$", alpha=0.6)
    axs[3,0].plot(iteraciones, x_ref[:kmax,2], '-.', color='r', label=r"$\theta_{ref}$", alpha=0.7)
    axs[3,0].grid(color='gray', linestyle='--')
    axs[3,0].legend(fontsize=15)
    axs[3,0].set_title(r"$\theta$", fontsize=19)
    
    #Entradas u
    axs[1,1].plot(iteraciones, u_mpc[:,0], 'purple', label=r"$v_{mpc}$", alpha=0.6)
    axs[1,1].plot(iteraciones, u_ref[:kmax,0], '-.', color='purple', label=r"$v_{ref}$", alpha=0.7)
    axs[1,1].grid(color='gray', linestyle='--')
    axs[1,1].legend(fontsize=15)
    axs[1,1].set_title(r"$v$", fontsize=19)
    
    axs[2,1].plot(iteraciones, u_mpc[:,1], 'darkorange', label=r"$\omega_{mpc}$", alpha=0.6)
    axs[2,1].plot(iteraciones, u_ref[:kmax,1], '-.', color='darkorange', label=r"$\omega_{ref}$", alpha=0.7)
    axs[2,1].grid(color='gray', linestyle='--')
    axs[2,1].legend(fontsize=15)
    axs[2,1].set_title(r"$\omega$", fontsize=19)
    
    #Función Phi
    axs[3,1].plot(iteraciones[:-1], phi_mpc, 'g', label=r"$\phi(k)$")
    axs[3,1].grid(color='gray', linestyle='--')
    axs[3,1].legend(fontsize=15)
    axs[3,1].set_title(r"$\phi(k)$", fontsize=19)
    
    #fig.show()

def animacion_trayectoria(x_r, solMPC, predMPC, N, nt, T, filename):
    
    fig, ax = plt.subplots(1, figsize=(8,8))
    ax.set_xlim((-6,6))
    ax.set_ylim((-6,6))
    ax.set_axis_off()
    ax.set_aspect('equal')

    trayectoria, = ax.plot([], [], 'g', alpha=0.7, lw=5)
    prediccion, = ax.plot([], [], 'r', alpha=0.7, lw=3)

    #initialization function: plot the background of each frame
    def init():
        ax.plot(x_r[:nt-N+1, 0], x_r[:nt-N+1, 1], '--b', alpha=0.1)
        prediccion.set_data([], [])
        return trayectoria, prediccion, 

    # animation function.  This is called sequentially
    def animate(i):
        trayectoria.set_data(solMPC[:i, 0], solMPC[:i, 1])
        prediccion.set_data(predMPC[i][3*np.arange(N)], predMPC[i][3*np.arange(N) + 1])
        return trayectoria, prediccion, 

    # call the animator.  blit=True means only re-draw the parts that have changed.
    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                   frames=nt-N+1, interval=int(T*1000), blit=True)
    #ani = animation.FuncAnimation(fig, animate, frames=nt-N+1)
    # save the animation as an mp4.  This requires ffmpeg or mencoder to be
    # installed.  The extra_args ensure that the x264 codec is used, so that
    # the video can be embedded in html5.  You may need to adjust this for
    # your system: for more information, see
    # http://matplotlib.sourceforge.net/api/animation_api.html
    anim.save('MPC/'+filename, fps=int(1/T), extra_args=['-vcodec', 'libx264'])
    
    return anim