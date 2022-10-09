from math import e
from numpy import trapz

def equation8(alpha, gamma_e, t_0, G_ee, G_ei, G_ese, G_esre, G_srs, omega_min = 0, omega_max = 650, G_es = 1, G_sn = 1, phi_n = 1):
    '''
    Description:
        Equation 8 from Robinson2002.

    Inputs:
        alpha
        gamma_e
        t_0
        G_ee
        G_ei
        G_ese
        G_esre
        G_srs
        omega_min = 0 (default)
        omega_max = 650 (default)
        G_es = 1 (default)
        G_sn = 1 (default)
        phi_n = 1 (default)

    Outputs:
        phi_e: Y-axis values for the equation
        stability_x: X-axis values for the stability 
        stability_y: Y-axis values for the stability
    '''
    omega = [i for i in range(omega_min, omega_max+1)]
    comp_omega = [complex(imag=omega[i]) for i in omega]
    beta = 4*alpha

    # Equation L (eq 11.)
    L = [((1-comp_omega[i]/alpha)**(-1))*((1-comp_omega[i]/beta)**(-1)) for i in omega]

    # Equation q^2r^2_e (eq 9.)
    q2r2e_p1 = [((1-comp_omega[i]/gamma_e)**2) for i in omega] # Only real numbers because of squared
    q2r2e_p2 = [(L[i]/(1-G_ei*L[i])) for i in omega]
    q2r2e_p3 = [(G_ee + ((((G_ese+G_esre*L[i])*L[i])/(1-G_srs*(L[i]**2)))*e**(comp_omega[i]*t_0))) for i in omega]
    q2r2e_full = [(q2r2e_p1[i] - q2r2e_p2[i]*q2r2e_p3[i]) for i in omega]

    # Equation Phi_e (eq 8.)
    phi_e_p1 = [(G_es*L[i])/(1-G_ei*L[i]) for i in omega]
    phi_e_p2 = [((G_sn*L[i]*e**(comp_omega[i]*t_0/2))/(1-G_srs*L[i]**2)) for i in omega]
    phi_e_p3 = [(phi_e_p1[i] * phi_e_p2[i] * phi_n/(q2r2e_full[i])) for i in omega]
    phi_e = [abs(phi_e_p3[i])**2 for i in omega]

    stability_x = [q2r2e_full[i].real for i in omega]
    stability_y = [q2r2e_full[i].imag for i in omega]

    return phi_e, stability_x, stability_y

def calc_area(y, x, xlims, dx=None):
    '''
    Description:
        Given a set of points, calculate the area between the xlimits.
        Not very accurate for few integer values of x.

    Inputs:
        y:      the set of y coordinates (array)
        x:      the set of x coordinates (array)
        xlims:  lower and upper x limits (array)
        dx:     distance between x points. Default = None
    
    Output:
        area under the curve that makes up the points between the x-axis limits
    
    Example:
        area = calc_area(y=[0,1,4,9,16], x=[0,1,2,3,4], xlims=[1,3])
    '''

    # Array to store Y-axis points that fall between the x-axis limits
    new_y = []

    # Get the upper and lower limits
    lower_limit = xlims[0]
    upper_limit = xlims[1]

    # For each value in y that is between the x limits, store the points in the new_y array
    for index, yval in enumerate(y):
        if lower_limit <= x[index] < upper_limit:
            new_y.append(yval)

    # Calculate the area of the points that fall between the x-axis limits       
    area = trapz(new_y, dx=dx)
    return area