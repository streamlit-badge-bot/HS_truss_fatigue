import streamlit as st
import functions as fnc
import validation as vld
import pandas as pd
import forallpeople as u
u.environment('structural')

#Create Title Markdown
st.title("CIDECT-8 Fatigue - K-joint Trusses")
st.markdown("The purpose of this worksheet is to determine the allowable stresses at the K-Joints of the trusses.\n\
    The CIDECT 8 design guide is adopted. It can be downloaded at: https://www.cidect.org/design-guides/")

#Create section picker in streamlit sidebar
chord_type = st.sidebar.radio("Choose Type of Chord:",("SHS","RHS"))
b0,h0,t0,A_chord,Ix_chord,Iy_chord = vld.hs_lookup(chord_type,"chord")
brace_type = st.sidebar.radio("Choose Type of Brace:",("SHS","RHS"))
b1,h1,t1,A_brace,Ix_brace,Iy_brace = vld.hs_lookup(brace_type,"brace")

#Create Truss geometry input in streamlit sidebar
st.sidebar.markdown('## Truss Geometry:')
e = st.sidebar.slider('Eccentricity',-400,400,-100,step=5,format='%f') / 1000
chordspacing = st.sidebar.slider('Chord spacing (mm)',100,4000,2000,step=50,format='%i') / 1000
L_chord = st.sidebar.slider('Length of Chord (mm)',100,30000,2000,step=100,format='%i') / 1000
div_chord = st.sidebar.slider('Chord divisions',1,20,10,step=1,format='%i')

#Calculate Dimensional parameters beta, gamma and tau, check compliant
st.write('## Dimensional Parameters')
dim_params_latex, dim_params = fnc.dim_params(b0=b0*u.m,t0=t0*u.m,b1=b1*u.m,t1=t1*u.m)
st.latex(dim_params_latex)
beta, twogamma, tau = dim_params

#Plot dimension parameters
fig,ax = fnc.dim_params_plot(b0*1000,t0*1000,b1*1000,t1*1000)
st.pyplot(fig)

#Calculate overlap
st.write('## Calculate overlap')
st.image(r"data/overlap_calculation.png")
overlap_latex, overlap_outputs = fnc.overlap(L_chord*u.m,chordspacing*u.m,div_chord,e*u.m,h0*u.m,h1*u.m)
Ov,theta = overlap_outputs
st.latex(overlap_latex)

#Calculate SCF values
st.write("""## SCF Calculations

The follow calculations determine the Stress Concentration Factors (SCF) for each:
- LC1 chord -> $SCF_{ch,ax}$
- LC1 brace -> $SCF_{b,ax}$
- LC2 chord -> $SCF_{ch,ch}$""")

st.latex("SCF_{chax}")
SCF_chax_latex, SCF_chax = fnc.SCF_chax(beta,twogamma,tau,Ov,theta)
st.latex(SCF_chax_latex)

st.latex("SCF_{bax}")
SCF_bax_latex, SCF_bax = fnc.SCF_bax(beta,twogamma,tau,Ov,theta)
st.latex(SCF_bax_latex)

st.latex("SCF_{chch}")
SCF_chch_latex,SCF_chch = fnc.SCF_chch(beta)
st.latex(SCF_chch_latex)
