import streamlit as st

import numpy as np
import matplotlib.pyplot as plt
import forallpeople as u
u.environment('structural')

def dim_params_plot(b0,t0,b1,t1):
    """Plot the dimensional variables beta, 
    2*gamma and tau, showing the acceptable range in green highlighted area"""
    # Create Plot
    fig, ax = plt.subplots(ncols=3,figsize=(9,3))

    #Plot max and min lines
    ax[0].plot([0,500],[0,500], label=r'$\beta=1$', color='red') #max line
    ax[0].plot([0,500],[0.,0.35 * 500.], label=r'$\beta=0.35$', color='yellow') #min line
    ax[1].plot([0,20],[0,35 * 20],label=r'$2\cdot \gamma = 35$', color='red')
    ax[1].plot([0,20],[0,10 * 20],label=r'$2\cdot \gamma = 10$', color='yellow')
    ax[2].plot([0,20],[0,20],label=r'$\tau=1.0$', color='red')
    ax[2].plot([0,20],[0,0.25*20],label=r'$\tau=0.25$', color='yellow')

    #Plot single points for each of graph
    ax[0].plot(b0,b1,'ro',c="black")
    ax[1].plot(t0,b0,'ro',c="black")
    ax[2].plot(t0,t1,'ro',c="black")

    #Annotate single points for each graph with beta,gamma,tau values
    ax[0].annotate(text=b1/b0,xy=(b0,b1),xytext=(b0-75,b1+25),fontsize=8)
    ax[1].annotate(text=b0/t0,xy=(t0,b0),xytext=(t0-2,b0+25),fontsize=8)
    ax[2].annotate(text=t1/t0,xy=(t0,t1),xytext=(t0-2,t1+2),fontsize=8)

    #Create shaded region of acceptable values
    ax[0].fill_between([0,500],[0,500],[0,0.35 * 500], facecolor='green', alpha=0.5)
    ax[1].fill_between([0,20],[0,35 * 20],[0,10 * 20], facecolor='green', alpha=0.5)
    ax[2].fill_between([0,20],[0,20],[0,0.25*20], facecolor='green', alpha=0.5)

    #Set graph titles with allowable range
    ax[0].set_title(r'$0.35 \leq \beta(=\frac{b_1}{b_0}) \leq 1.0$',fontsize=10)
    ax[1].set_title(r'$10 \leq 2\gamma(=\frac{b_0}{t_0}) \leq 35$',fontsize=10)
    ax[2].set_title(r'$0.25 \leq \tau(=\frac{t_1}{t_0}) \leq 1.0$',fontsize=10)

    #Label axes
    ax[0].set_xlabel('b0')
    ax[0].set_ylabel('b1')
    ax[1].set_xlabel('t0')
    ax[1].set_ylabel('b0')
    ax[2].set_xlabel('t0')
    ax[2].set_ylabel('t1')

    #Turn on legends and grid for each graph
    [ax[i].legend(loc='upper left') for i in range(3)]
    [ax[i].grid() for i in range(3)]

    return fig, ax

def bar_chart(sigma_chord1P,
                sigma_chord2P,
                sigma_chordM_ip,
                sigma_chordM_op,
                sigma_brace_1P,
                sigma_braceM_op,
                sigma_max):
    """Generate a bar chart showing the total stresses on the brace and chord,
    and compare these to the max allowable stress"""
    fig, ax = plt.subplots()
    members = ['chord','brace']
    sigma_1P = [sigma_chord1P,sigma_brace_1P]
    sigma_2P = [sigma_chord2P,0]
    sigma_M_ip = [sigma_chordM_ip,0]
    sigma_M_op = [sigma_chordM_op,sigma_braceM_op]
    y_pos = np.arange(len(members))
    # horizontal line indicating the threshold
    ax.plot([sigma_max, sigma_max],[-0.5, 1.5], "k--",label="$\sigma_{MAX}$")

    #Add stacked elements
    sigma_1and2 = np.add(sigma_1P, sigma_2P).tolist()
    sigma_1to3 = np.add(np.add(sigma_1P, sigma_2P), sigma_M_ip).tolist()


    ax.barh(y_pos,sigma_1P,left=0,label=r"$\sigma_{ax}$ - Balanced LC")
    ax.barh(y_pos,sigma_2P,left=sigma_1P,label=r"$\sigma_{ax}$ - Unbalanced LC")
    ax.barh(y_pos,sigma_M_ip,left=sigma_1and2,label=r"$\sigma_{Mip}$ - Unbalanced LC")
    ax.barh(y_pos,sigma_M_op,left=sigma_1to3,label=r"$\sigma_{Mop}$")
    plt.yticks(y_pos, members)
    ax.set_ylabel("Members")
    ax.set_xlabel("Stresses (MPa)")
    ax.legend(loc="best")
    ax.set_title("Member Stresses")
    ax.set_xlim(left=0)
    ax.plot([])

    return fig, ax