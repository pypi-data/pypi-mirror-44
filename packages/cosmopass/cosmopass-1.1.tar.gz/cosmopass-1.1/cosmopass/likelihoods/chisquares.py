from cosmopass.likelihoods.dataimport import *
from sys import path
import numpy as np
from cosmopass.equations.fluids import *
from cosmopass.equations.scalar_all_eqn import *
Params = {'LCDM':"Om0,rd,h,Or0,sigma8",
          'w0waCDM':"Om0,rd,w0,wa,h,Or0,sigma8",
          'wCDM':"Om0,rd,w,h,Or0,sigma8",
          'GCG':"Om0,rd,As,alpha,h,Or0,sigma8",
          'BA':"Om0,rd,w0,wa,h,Or0,sigma8",
          'JBP':"Om0,rd,w0,wa,h,Or0,sigma8",
          'SCPL':"Om0,rd,w0,wa,h,Or0,sigma8",
          'scalarpow':"Ophi_i,rd,li,n,Orad_i,h,sigma8",
          'scalarexp':"Ophi_i,rd,li,Orad_i,h,sigma8",
          'tachyonpow':"Ophi_i,rd,li,n,Orad_i,h,sigma8",
          'tachyonexp':"Ophi_i,rd,li,Orad_i,h,sigma8",
          'galileonpow':"Ophi_i,rd,epsilon_i,li,n,Orad_i,h,sigma8",
          'galileonexp':"Ophi_i,rd,epsilon_i,li,Orad_i,h,sigma8"
           }


class model():
    """
    h,qso,panth,bao,masers,fs8,cmb,td,jla
    """
    def __init__(self,model_name,chi_list=None):
        self.model_name = model_name
        self.Params = Params[model_name] + ' [QSO:+ m,delta]'
        self.chi_list = chi_list
        

    def chi_h(self,*args):
        H_th = np.vectorize(globals()['%s'%self.model_name](*args).hubble_z)
        return np.sum((H_z-H_th(zH))**2./dH**2)

    def chi_qso(self,*args):
        m = args[-2]
        delta = args[-1]
        ld = np.vectorize(globals()['%s'%self.model_name](*args[:-2]).luminosity_distance_z)
        x = m + 5.0*np.log10(ld(zQ))+25.
        return np.sum((mu_Q - x)**2./(dmu_Q**2. + delta**2))

    def chi_panth(self,*args):
        mod = globals()['%s'%self.model_name](*args)
        yy1 = [mod.hubble_normalized_z(0.07)-0.997, mod.hubble_normalized_z(0.20)-1.111, 
               mod.hubble_normalized_z(0.35)-1.128, mod.hubble_normalized_z(0.55)-1.364, 
               mod.hubble_normalized_z(0.90)-1.52]
        return np.dot(yy1, np.dot(sigma_mat_pant, yy1))

    def chi_bao(self,*args):
        mod = globals()['%s'%self.model_name](*args)
        xx1 = [mod.Dm_rd(0.38)/(1.0+0.38)-7.42, mod.Dh_rd(.38)-24.97, 
               mod.Dm_rd(0.51)/(1.0+0.51)-8.85, mod.Dh_rd(.51)-22.31,
               mod.Dm_rd(0.61)/(1.0+0.61)-9.69, mod.Dh_rd(.61)-20.49, 
               mod.Dm_rd(2.4)/(1.0+2.4)-10.76, mod.Dh_rd(2.4)-8.94]
        bao1 = np.dot(xx1, np.dot(sigma_mat_bao1, xx1))

        bao2 = ((mod.Dv_rd(0.106)-2.98)/.13)**2 + ((mod.Dv_rd(0.15)-4.47)/.17)**2+ \
                ((mod.Dv_rd(1.52)-26.1)/1.1)**2
        return bao1 + bao2
    
    def chi_masers(self,*args):
        mod = globals()['%s'%self.model_name](*args)
        return ((mod.comoving_distance_z(0.0116)/(1+0.0116)-49.6)/5.1)**2 + \
                ((mod.comoving_distance_z(0.0340)/(1.0+0.0340)-144)/19)**2+ \
                ((mod.comoving_distance_z(0.0277)/(1.0+0.0277)-126.3)/11.6)**2

    def chi_fs8(self,*args):
        fs8_th = globals()['%s'%self.model_name](*args).fsigma8z(zfs8)
        return np.sum((fs8-fs8_th)**2./dfs8**2)

    def chi_cmb(self,*args):
        mod = globals()['%s'%self.model_name](*args)
        vec = np.array([mod.acoustic_length()-301.462,
                        mod.cmb_shift_parameter()-1.7493])
        return np.dot(vec, np.dot(sigma_mat_cmb, vec))
    
    def chi_td(self,*args):
        td_th = globals()['%s'%self.model_name](*args).time_delay_distance(zd, zs)
        return np.sum(-2*np.log(1/(np.sqrt(2*np.pi)*(td_th-lad)*sigd))+((np.log(td_th-lad)-mud)**2/sigd**2))
    
    def chi_jla(self, *args):
        ld = np.vectorize(globals()['%s'%self.model_name](*args).luminosity_distance_z)
        x = 5.0*np.log10(ld(zsn))+25.-mu_sn
        return np.dot(x,np.dot(sigma_mat_sn,x))
    
    def chi_sq(self, *args):
        chisq = 0
        combination = self.chi_list
        if 'qso' in combination:
            chisq = chisq + self.chi_qso(*args)
            args = args[:-2]
        if 'h' in combination:
            chisq = chisq + self.chi_h(*args)
        if 'panth' in combination:
            chisq = chisq + self.chi_panth(*args)
        if 'bao' in combination:
            chisq = chisq + self.chi_bao(*args)
        if 'masers' in combination:
            chisq = chisq + self.chi_masers(*args)
        if 'fs8' in combination:
            chisq = chisq + self.chi_fs8(*args)
        if 'cmb' in combination:
            chisq = chisq + self.chi_cmb(*args)
        if 'td' in combination:
            chisq = chisq + self.chi_td(*args)
        if 'jla' in combination:
            chisq = chisq + self.chi_jla(*args)
        return chisq


#if not __name__ == '__main__':
#    print("Importing Likelihoods")
#else:
#    M = model('LCDM')
#    print(M.chi_panth(.3,147,.7,5,.8))

