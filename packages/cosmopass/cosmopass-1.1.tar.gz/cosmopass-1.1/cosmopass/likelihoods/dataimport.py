from numpy import loadtxt, linalg, array
import os
this_dir, this_filename = os.path.split(__file__)
DAT = os.path.join(this_dir, "Data/" )

######### H_data ###############################
dataH = loadtxt(DAT + 'Hdata.dat')
zH = dataH[:, 0]
H_z = dataH[:, 1]
dH = dataH[:, 2]


######## Quasar ################################
dataQ = loadtxt(DAT + 'DL_all_short.txt')
zQ = dataQ[:, 0]
mu_Q = dataQ[:, 1]
dmu_Q = dataQ[:, 2]


######## Pantheon ##############################
correlation = array([[1.0, 0.39, 0.53, 0.37, 0.01], 
               [0.39, 1.0, -0.14, 0.37, -0.08], 
               [0.53, -0.14, 1.0, -0.16, 0.17], 
               [0.37, 0.37, -0.16, 1.0, -0.39], 
               [0.01, -0.08, 0.17, -0.39, 1.0]])
stand_deviation = array([0.023,0.020,0.037,0.063,0.12])
cov_panth = []
for i in range(len(stand_deviation)):
    for j in range(len(stand_deviation)):
        cov_panth = cov_panth + [correlation[i, j]*stand_deviation[i]*stand_deviation[j]]
cov_panth = array(cov_panth)
cov_panth = cov_panth.reshape(5, 5)

sigma_mat_pant = linalg.inv(cov_panth)

########### F sigma 8 ##########################
datafs8 = loadtxt(DAT + 'fs8.dat')
zfs8 = datafs8[:, 0]
fs8 = datafs8[:, 1]
dfs8 = datafs8[:, 2]

############### BAO ###################################################
bao_1_cov = [[0.0150, -0.0358, 0.0071, -0.0100, 0.0032, -0.0036, 0, 0], 
             [-0.0357, 0.5304, -0.0160, 0.1766, -0.0083, 0.0616, 0, 0], 
             [0.0071, -0.0160, 0.0182, -0.0323, 0.0097, -0.0131, 0, 0], 
             [-0.0100, 0.1766, -0.0323, 0.3267, -0.0167, 0.1450, 0, 0], 
             [0.0032, -0.0083, 0.0097, -0.0167, 0.0243, -0.0352, 0, 0], 
             [-0.0036, 0.0616, -0.0131, 0.1450, -0.0352, 0.2684, 0, 0], 
             [0, 0, 0, 0, 0, 0, 0.1358, -0.0296], 
             [0, 0, 0, 0, 0, 0, -0.0296, 0.0492]]

sigma_mat_bao1 = linalg.inv(bao_1_cov)

############## CMB #############################
corr_mat1 = array([[1., 0.47], [0.47, 1.0]])
err_mat1 = array([0.089, 0.0046])
cov_cmb1 = []
for i in range(len(err_mat1)):
    for j in range(len(err_mat1)):
        cov_cmb1 = cov_cmb1 + [corr_mat1[i, j]*err_mat1[i]*err_mat1[j]]
cov_cmb1 = array(cov_cmb1)
cov_cmb1 = cov_cmb1.reshape(2, 2)
sigma_mat_cmb = linalg.inv(cov_cmb1)

############# time delay #######################
data_time_delay = loadtxt(DAT + 'time_delay_data.dat')
zd = data_time_delay[:, 0]
zs = data_time_delay[:, 1]
mud = data_time_delay[:, 2]
sigd = data_time_delay[:, 3]
lad = data_time_delay[:, 4]

############### jla #############################
dataSN = loadtxt(DAT+'jla_mub.txt')
zsn = dataSN[:,0]
mu_sn = dataSN[:,1]

cov_sn = loadtxt(DAT+'jla_mub_covmatrix.dat')
covarray_sn = cov_sn[1:len(cov_sn)]
covmat_sn = covarray_sn.reshape(31,31)
sigma_mat_sn = linalg.inv(covmat_sn)



#if not __name__ == "__main__":
#    print('Importing data')
