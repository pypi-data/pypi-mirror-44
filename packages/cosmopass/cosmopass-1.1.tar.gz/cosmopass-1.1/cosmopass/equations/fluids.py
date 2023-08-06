import numpy as np
from scipy.integrate import odeint
from scipy import interpolate
from scipy.integrate import quad
from scipy.interpolate import splrep, splev, UnivariateSpline
from scipy.misc import derivative
from scipy.optimize import fsolve
import cosmopass.equations.transfer_func as tf
######################################


class LCDM(object):
    def __init__(self,Om0,rd,h,Or0,sigma8):
        self.Om0 = float(Om0)
        self.rd = float(rd)
        self.Ob0 = float(0.045)
        self.Or0 = float(Or0*1e-5)
        self.ns = float(0.96)
        self.h = float(h)
        self.sigma_8 = float(sigma8)

    def hubble_normalized_z(self,z):
        return np.sqrt(self.Om0*(1.+z)**3. + self.Or0*(1+z)**4 + (1.-self.Om0-self.Or0))

    def inverse_hubble_normalized_z(self,z):
        """
        Inverse of the normalized hubble parameter: 1/h(z)
        where h(z) = H(z)/H0
        Input:
          z: redshift
        Output:
          1/h(z): inverse of normalized hubble parameter
        """
        return 1./self.hubble_normalized_z(z)

    def hubble_normalized_a(self,a):
        """
        Calculates normalized Hubble parameter h(a) = H(a)/H0
        where:
          H(a) is the Hubble parameter at redshift z
          H0 is the current value of Hubble parameter
        Input:
          a: scale factor of the Universe
        Output:
          h(a): normalized hubble parameter
        """
        return self.hubble_normalized_z(1./a-1)

    def hubble_prime_normalized_a(self,a):
        """
        Derivative of dimensionless hubble parameter w.r.t. a
        """
        return derivative(self.hubble_normalized_a,a,dx=1e-6)
    def hubble_z(self,z):
        return 100*(self.h)*(self.hubble_normalized_z(z))

    def D_H(self):
        """
        Hubble distance in units of MPc (David Hogg arxiv: astro-ph/9905116v4)
        """
        return 2997.98/self.h

    def comoving_distance_z(self,z1):
        """
        Line of sight comoving distance as a function of redshift z
        as described in David Hogg paper
        in units of MPc
        """
        return self.D_H()*quad(self.inverse_hubble_normalized_z,0,z1)[0]

    #angular diameter distance in units of MPc
    def angular_diameter_distance_z(self,z):
        """
        Angular diameter distance as function of redshift z
        in units of MPc
        """
        d_c = self.comoving_distance_z(z)/(1.+z)
        return d_c

    #luminosity distance in units of MPc
    def luminosity_distance_z(self,z):
        """
        Luminosity distance in as function of redshift z
        in units of MPc
        """
        d_l = self.comoving_distance_z(z)*(1.+z)
        return d_l

    def time_delay_distance(self,zd,zs):
        """
        Time delay distance used in strong lensing cosmography
        (See Suyu et. al., Astrophys. J. 766, 70, 2013; arxiv:1208.6010)
        zs = redshift at which the source is placed
        zd = redshift at which the deflector (or lens) is present        
        """
        D_ds = self.D_H()/(1+zs)*quad(self.invhub,zd,zs)[0]
        return (1+zd)*self.ang_dis_z(zd)*self.ang_dis_z(zs)/D_ds


    def time_delay_distance_z(self,zd,zs):
        """
        Time delay distance used in strong lensing cosmography
        (See Suyu et. al., Astrophys. J. 766, 70, 2013; arxiv:1208.6010)
        zs = redshift at which the source is placed
        zd = redshift at which the deflector (or lens) is present        
        """
        D_ds = self.D_H()/(1+zs)*quad(self.inverse_hubble_normalized_z,zd,zs)[0]
        return (1+zd)*self.angular_diameter_distance_z(zd)*self.angular_diameter_distance_z(zs)/D_ds

    def time_delay_distance(self,zd,zs):
        return np.vectorize(self.time_delay_distance_z)(zd,zs)    


    def z_decoupling(self):
        """
        Gives the redshit of the decoupling era
        """
        g1 = 0.0783*(self.Ob0*self.h**2)**(-0.238)/(1+39.5*(self.Ob0*self.h**2)**(0.763))
        g2 = 0.560/(1+21.1*(self.Ob0*self.h**2)**1.81)
        return 1048*(1.+0.00124*(self.Ob0*self.h**2)**(-0.738))*(1+g1*(self.Om0*self.h**2)**g2)

    def z_drag_epoch(self):
        """
        Gives the redshit of baryon drag epoch
        Eisenstein and Hu; arxiv:astro-ph/9709112
        """
        b1 = 0.313*(self.Om0*self.h**2)**(-0.419)*(1+0.607*(self.Om0*self.h**2)**0.674)
        b2 = 0.238*(self.Om0*self.h**2)**0.223
        return 1291.*(self.Om0*self.h**2)**0.251*(1+b1*(self.Om0*self.h**2)**b2)/(1+0.659*(self.Om0*self.h**2)**0.828)


    def sound_horizon(self,z):
        """
        Gives the sound horizon at redshift z
        """
        if z<self.z_decoupling():
            raise ValueError('Redshift should be greater than decoupling redshift')
        R1 = 31500*(self.Ob0*self.h**2)*(2.728/2.7)**(-4)*1/(1.+z)
        def integrand1(a):
            return 1/(np.sqrt(3*(1+R1))*self.hubble_normalized_a(a)*a**2)
        return self.D_H()*quad(integrand1,0,1./(1+z))[0]



    def sound_drag(self,z):
        """
        Gives the sound horizon at drag epoch
        """
        R2=3.0*self.Ob0/(4.0*self.Or0)
        def integrand2(a):
            return 1/(self.hubble_normalized_a(a)*a**2*(np.sqrt(1.0+R2*a)))
        return (self.D_H()/np.sqrt(3.0))*quad(integrand2,0,1./(1+z))[0]    


    def d_v(self,z):
        
        return (self.D_H()*z*(self.comoving_distance_z(z)**2)/self.hubble_normalized_z(z))**(1./3.)


    def bao_d_n(self,z):

        return self.rd/self.d_v(z)    
        
    def Dv_rd(self,z):
        return 1/self.bao_d_n(z)


    def Dm_rd(self,z):
        return self.comoving_distance_z(z)/self.rd


     
    def Dh_rd(self,z):
        return self.D_H()/(self.rd * self.hubble_normalized_z(z))
        

    def cmb_shift_parameter(self):
        """
        CMB Shift parameter at decoupling redshift 
        (see Shafer and Huterer, arxiv:1312.1688v2)
        Output:
          R (shift parameter)
        """
        return np.sqrt(self.Omega_m_z(0.))*(1+self.z_decoupling())*self.angular_diameter_distance_z(self.z_decoupling())/self.D_H()

    def acoustic_length(self):
        """
        It calculates acoustis length scale at decoupling redshift
        """
        z_star = self.z_decoupling()
        return np.pi*self.angular_diameter_distance_z(z_star)*(1+z_star)/self.sound_horizon(z_star)


    def t_H(self):
        """
        Hubble time in units of Billion years
        """
        return 9.78/self.h

    def lookback_time_z(self,z):
        """
        Lookback time as a function of redshift z
        in units of billion years
        """
        def integrand(z1):
            return self.inverse_hubble_normalized_z(z1)/(1.+z1)
        lt = quad(integrand,0,z)[0]
        return self.t_H()*lt

    def Omega_m_a(self,a):
        return self.Om0*a**(-3)/self.hubble_normalized_a(a)**2.

    def Omega_m_z(self,z):
        return self.Omega_m_a(1./(1.+z))

    a11 = np.linspace(1./31,1,1000)

    def deriv(self,y,a):
        return [ y[1], -(3./a + self.hubble_prime_normalized_a(a)/self.hubble_normalized_a(a))*y[1] + 1.5*self.Omega_m_a(a)*y[0]/(a**2.)]

    def sol1(self):
        yinit = (1./31,1.)
        return odeint(self.deriv,yinit,self.a11)

    def D_p(self,a):
            yn11=self.sol1()[:,0]
            ynn11=UnivariateSpline(self.a11,yn11,k=3,s=0)
            return ynn11(a)

    def D_plus_a(self,a):
        return self.D_p(a)/self.D_p(1.0)

    def D_plus_z(self,z):
        """
        Normalized solution for the growing mode as a function of redshift
        """
        return self.D_plus_a(1./(1.+z))

    def growth_rate_a(self,a):
        d = self.sol1()[:,:]
        d1 = d[:,0]
        dp = d[:,1]
        gr1 = UnivariateSpline(self.a11,self.a11*dp/d1,k=3,s=0)
        return gr1(a)

    def growth_rate_z(self,z):
        """
        Growth Rate f = D log(Dplus)/ D Log(a) as a function of redshift
        """
        return self.growth_rate_a(1./(1.+z))

    def fsigma8z(self,z):
        """
        fsigma_{8} as a function of redshift
        """
        return self.growth_rate_z(z)*self.D_plus_z(z)*self.sigma_8
    
    # Defining window function

    def Wf(self,k):
        """
        Window function
        """
        return 3.*(np.sin(k*8.) - (k*8.)*np.cos(k*8.))/(k*8.)**3.

    def integrand_bbks(self,k):
        return k**(self.ns + 2.)*tf.Tbbks(k,self.Om0,self.Ob0,self.h)**2.*(self.Wf(k))**2.

    def integrand_wh(self,k):
        return k**(self.ns + 2.)*tf.Twh(k,self.Om0,self.Ob0,self.h)**2.*(self.Wf(k))**2.

    def A0bbks(self):
        return (2.0*np.pi**2*self.sigma_8**2.)/(quad(self.integrand_bbks,0,np.inf)[0])

    def A0wh(self):
        return (2.0*np.pi**2*self.sigma_8**2.)/(quad(self.integrand_wh,0,np.inf)[0])

    def Pk_bbks(self,k,z):
        """
        Matter Power Spectra Pk in units if h^{-3}Mpc^{3} as a function of k in units of [h Mpc^{-1}]
        and z;
        Transfer function is taken to be BBKS
        Ref: Bardeen et. al., Astrophys. J., 304, 15 (1986)
        """
        return self.A0bbks()*k**self.ns*tf.Tbbks(k,self.Om0,self.Ob0,self.h)**2.*self.D_plus_z(z)**2.

    def Pk_wh(self,k,z):
        """
        Matter Power Spectra Pk in units if h^{-3}Mpc^{3} as a function of k in units of [h Mpc^{-1}]
        and z;
        Transfer function is taken to be Eisenstein & Hu 
        Ref: Eisenstein and Hu, Astrophys. J., 496, 605 (1998)
        """
        return self.A0wh()*k**self.ns*tf.Twh(k,self.Om0,self.Ob0,self.h)**2.*self.D_plus_z(z)**2.

    def DPk_bbks(self,k,z):
        """
        Dimensionless Matter Power Spectra Pk  as a function of k in 
        units of [h Mpc^{-1}] and z;
        Transfer function is taken to be BBKS 
        Ref: Bardeen et. al., Astrophys. J., 304, 15 (1986)
        """
        return k**3.*self.Pk_bbks(k,z)/(2.0*np.pi**2.)

    def DPk_wh(self,k,z):
        """
        Dimensionless Matter Power Spectra Pk  as a function of k in 
        units of [h Mpc^{-1}] and z;
        Transfer function is taken to be Eisenstein & Hu 
        Ref: Eisenstein and Hu, Astrophys. J., 496, 605 (1998)
        """
        return k**3.*self.Pk_wh(k,z)/(2.0*np.pi**2.)

class wCDM(LCDM):
    """
    A Class to calculate cosmological observables for a model with CDM and dark energy
    for which equation of state w is constant but not equal to -1. See hubble_normalized_z function 
    for details.  

    parameters are:
    Om0 : present day density parameter for total matter (baryonic + dark)
    Ob0 : present day density parameter for baryons (or visible matter)
    w : equation of state for "dark energy"
    ns : spectral index for primordial power spectrum
    h : dimensionless parameter related to Hubble constant H0 = 100*h km s^-1 MPc^-1
    sigma_8 : r.m.s. mass fluctuation on 8h^-1 MPc scale
    """
    def __init__(self,Om0,rd,w,h,Or0,sigma8):
        self.Om0 = float(Om0)
        self.rd = float(rd)
        self.w = float(w)
        self.Ob0 = float(0.045)
        self.Or0 = float(Or0*1e-5)
        self.ns = float(0.96)
        self.h = float(h)
        self.sigma_8 = float(sigma8)
    
    def hubble_normalized_z(self,z):
        return np.sqrt(self.Om0*(1.+z)**3. + self.Or0*(1+z)**4 + (1.-self.Om0-self.Or0)*(1.+z)**(3*(1+self.w)))

class w0waCDM(LCDM):
    """
    A Class to calculate cosmological observables for a model with CDM and dark energy
    for which equation of state w is parametrized as:
    w(a) = w0 + wa*(1-a)
    where 'a' is the scale factor and w0,wa are constants in Taylor expansion of 
    variable equation of state w(a)

    parameters are:
    Om0 : present day density parameter for total matter (baryonic + dark)
    w0 and wa: coefficients of Taylor expansion of equation of state w(a) near a=1
    Ob0 : present day density parameter for baryons (or visible matter)
    ns : spectral index for primordial power spectrum
    h : dimensionless parameter related to Hubble constant H0 = 100*h km s^-1 MPc^-1
    sigma_8 : r.m.s. mass fluctuation on 8h^-1 MPc scale
    """
    def __init__(self,Om0,rd,w0,wa,h,Or0,sigma8):
        self.Om0 = float(Om0)
        self.rd = float(rd)
        self.w0 = float(w0)
        self.wa = float(wa)
        self.Ob0 = float(0.045)
        self.Or0 = float(Or0*1e-5)
        self.ns = float(0.96)
        self.h = float(h)
        self.sigma_8 = float(sigma8)
    def hubble_normalized_z(self,z):
        return np.sqrt(self.Om0*(1.+z)**3. + self.Or0*(1+z)**4 + (1.-self.Om0-self.Or0)*(1.+z)**(3*(1+self.w0+self.wa))*np.exp(-3.*self.wa*(z/(1.+z))))


class SCPL(LCDM):

    def __init__(self,Om0,rd,w0,wa,h,Or0,sigma8):
        self.Om0 = float(Om0)
        self.rd = float(rd) 
        self.w0 = float(w0)
        self.wa = float(wa)
        self.Ob0 = float(0.045)
        self.Or0 = float(Or0*1e-5)
        self.ns = float(0.96)
        self.h = float(h)
        self.sigma_8 = float(sigma8)

    def hubble_normalized_z(self,z):
        newadd = np.exp(-self.wa*(7.7785714 + 3.*((-((1.+z)**-7.)/7.) + ((7.*(1.+z)**-6.)/6.) - ((21.*(1.+z)**-5.)/5.) + ((35.*(1.+z)**-4.)/4.) - ((35.*(1.+z)**-3.)/3.) + ((21.*(1.+z)**-2.)/2.) - (7*(1.+z)**-1.) - np.log(1.+z))))
        return np.sqrt(self.Om0*(1.+z)**3. + self.Or0*(1.+z)**4. + (1.-self.Om0-self.Or0)*(1.+z)**(3.*(1.+self.w0))*newadd)


class GCG(LCDM):
    """
    A Class to calculate cosmological observables for a model with CDM and dark energy
    for which equation of state is parametrized as that by GCG $p= -A/rho^{alpha}$:
    w(z) = -As/(As+(1-As)*(1+z)**(3*(1+alpha)))
    where 'z' is the redshift and As,alpha are model parameters.

    parameters are:
    Om0 : present day density parameter for total matter (baryonic + dark)
    As and alpha: parameters involved in eqn. of state for GCG (ref())
    Ob0 : present day density parameter for baryons (or visible matter)
    ns : spectral index for primordial power spectrum
    h : dimensionless parameter related to Hubble constant H0 = 100*h km s^-1 MPc^-1
    sigma_8 : r.m.s. mass fluctuation on 8h^-1 MPc scale
    """
    def __init__(self,Om0,rd,As,alpha,h,Or0,sigma8):
        self.Om0 = float(Om0)
        self.rd = float(rd)
        self.As = float(As)
        self.alpha = float(alpha)
        self.h = float(h)
        self.Ob0 = float(0.045)
        self.Or0 = float(Or0*1e-5)
        self.ns = float(0.96)
        self.sigma_8 = float(sigma8)
    
    def hubble_normalized_z(self,z):
        return np.sqrt(self.Om0*(1.+z)**3. + self.Or0*(1+z)**4 + (1.-self.Om0-self.Or0)*(self.As+(1-self.As)*(1+z)**(3*(1+self.alpha)))**(1/(1+self.alpha)))

class BA(LCDM):

    def __init__(self,Om0,rd,w0,wa,h,Or0,sigma8):
        self.Om0 = float(Om0)
        self.rd = float(rd)
        self.w0 = float(w0)
        self.wa = float(wa)
        self.Ob0 = float(0.045)
        self.Or0 = float(Or0*1e-5)
        self.ns = float(0.96)
        self.h = float(h)
        self.sigma_8 = float(sigma8)

    def hubble_normalized_z(self,z):
        return np.sqrt(self.Om0*(1.+z)**3. + self.Or0*(1.+z)**4. + (1.-self.Om0-self.Or0)*(1.+z)**(3.*(1.+self.w0))*((1+z**2.)**(.65*self.wa)))


class JBP(LCDM):

    def __init__(self,Om0,rd,w0,wa,h,Or0,sigma8):
        self.Om0 = float(Om0)
        self.rd = float(rd) 
        self.w0 = float(w0)
        self.wa = float(wa)
        self.Ob0 = float(0.045)
        self.Or0 = float(Or0*1e-5)
        self.ns = float(0.96)
        self.h = float(h)
        self.sigma_8 = float(sigma8)

    def hubble_normalized_z(self,z):
        
        return np.sqrt(self.Om0*(1.+z)**3. + self.Or0*(1.+z)**4. + (1.-self.Om0-self.Or0)*(1.+z)**(3.*(1.+self.w0))*np.exp(1.5*self.wa*(z**2/(z**2+2.*z+1))))

