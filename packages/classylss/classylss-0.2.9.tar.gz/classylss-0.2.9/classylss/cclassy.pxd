# Bunch of declarations from C to python. The idea here is to define only the
# quantities that will be used, for input, output or intermediate manipulation,
# by the python wrapper. For instance, in the precision structure, the only
# item used here is its error message. That is why nothing more is defined from
# this structure. The rest is internal in Class.
# If, for whatever reason, you need an other, existing parameter from Class,
# remember to add it inside this cdef.

DEF _MAX_NUMBER_OF_K_FILES_ = 30
DEF _MAXTITLESTRINGLENGTH_ = 8000
DEF _FILENAMESIZE_ = 256
DEF _LINE_LENGTH_MAX_ = 1024
DEF _ERRORMSGSIZE_ = 2048

cdef extern from "class.h":

    ctypedef char FileArg[40]

    ctypedef char ErrorMsg[_ERRORMSGSIZE_]

    ctypedef char FileName[_FILENAMESIZE_]

    cdef enum linear_or_logarithmic:
        linear
        logarithmic

    cdef enum file_format:
        class_format
        camb_format

    cdef enum possible_gauges:
        newtonian
        synchronous

    cdef struct precision:
        FileName hyrec_Alpha_inf_file;
        FileName hyrec_R_inf_file;
        FileName hyrec_two_photon_tables_file;
        FileName sBBN_file;
        ErrorMsg error_message

    cdef struct background:
        ErrorMsg error_message
        short has_fld
        short has_lambda
        int bg_size
        int index_bg_a
        int index_bg_ang_distance
        int index_bg_lum_distance
        int index_bg_conf_distance
        int index_bg_time
        int index_bg_H
        int index_bg_H_prime
        int index_bg_D
        int index_bg_f
        int index_bg_Omega_r
        int index_bg_Omega_m
        int index_bg_rho_g
        int index_bg_rho_b
        int index_bg_rho_cdm
        int index_bg_rho_fld
        int index_bg_rho_lambda
        int index_bg_w_fld
        int index_bg_rho_ur
        int index_bg_rho_crit
        int index_bg_rho_ncdm1
        int index_bg_p_ncdm1

        int sgnK
        short long_info
        short inter_normal
        double T_cmb
        double * T_ncdm
        double H0
        double h
        double age
        double a_today
        double a_max
        double conformal_age
        int N_ncdm
        double * m_ncdm_in_eV
        double Neff
        double Omega0_b
        double Omega0_g
        double Omega0_cdm
        double Omega0_dcdm
        double Omega0_ur
        double Omega0_ncdm_tot
        double * Omega0_ncdm
        double Omega0_lambda
        double Omega0_fld
        double Omega0_k
        double w0_fld
        double wa_fld
        double cs2_fld
        double K
        int bt_size

    cdef struct thermo:
        ErrorMsg error_message
        int th_size
        int index_th_xe
        int index_th_Tb
        short inter_normal
        double tau_reio
        double z_reio
        double z_rec
        double tau_rec
        double rs_rec
        double ra_rec
        double ds_rec
        double da_rec
        double z_d
        double tau_d
        double ds_d
        double rs_d
        double YHe
        double n_e

        int tt_size

    cdef struct perturbs:
        ErrorMsg error_message
        short has_scalars
        short has_vectors
        short has_tensors

        short has_density_transfers
        short has_velocity_transfers
        short has_metricpotential_transfers

        possible_gauges gauge
        double k_max_for_pk
        double z_max_pk
        int has_pk_matter
        int l_lss_max

        int store_perturbations
        int k_output_values_num
        double k_output_values[_MAX_NUMBER_OF_K_FILES_]
        int index_k_output_values[_MAX_NUMBER_OF_K_FILES_]
        char scalar_titles[_MAXTITLESTRINGLENGTH_]
        char vector_titles[_MAXTITLESTRINGLENGTH_]
        char tensor_titles[_MAXTITLESTRINGLENGTH_]
        int number_of_scalar_titles
        int number_of_vector_titles
        int number_of_tensor_titles


        double * scalar_perturbations_data[_MAX_NUMBER_OF_K_FILES_]
        double * vector_perturbations_data[_MAX_NUMBER_OF_K_FILES_]
        double * tensor_perturbations_data[_MAX_NUMBER_OF_K_FILES_]
        int size_scalar_perturbation_data[_MAX_NUMBER_OF_K_FILES_]
        int size_vector_perturbation_data[_MAX_NUMBER_OF_K_FILES_]
        int size_tensor_perturbation_data[_MAX_NUMBER_OF_K_FILES_]

    cdef struct transfers:
        ErrorMsg error_message

    cdef struct primordial:
        ErrorMsg error_message
        double k_pivot
        double A_s
        double n_s
        double alpha_s
        double beta_s
        double r
        double n_t
        double alpha_t
        double V0
        double V1
        double V2
        double V3
        double V4
        double f_cdi
        double n_cdi
        double c_ad_cdi
        double n_ad_cdi
        double f_nid
        double n_nid
        double c_ad_nid
        double n_ad_nid
        double f_niv
        double n_niv
        double c_ad_niv
        double n_ad_niv
        double phi_min
        double phi_max

        int lnk_size
    cdef struct spectra:
        ErrorMsg error_message
        int has_tt
        int has_te
        int has_ee
        int has_bb
        int has_pp
        int has_tp
        int has_dd
        int has_td
        int has_ll
        int has_dl
        int has_tl
        int l_max_tot
        int ** l_max_ct
        int ln_k_size
        int ct_size
        int * ic_size
        int * ic_ic_size
        int md_size
        int d_size
        int non_diag
        int index_ct_tt
        int index_ct_te
        int index_ct_ee
        int index_ct_bb
        int index_ct_pp
        int index_ct_tp
        int index_ct_dd
        int index_ct_td
        int index_ct_pd
        int index_ct_ll
        int index_ct_dl
        int index_ct_tl
        int * l_size
        int index_md_scalars
        double* ln_k
        double sigma8
        double alpha_II_2_20
        double alpha_RI_2_20
        double alpha_RR_2_20
        double alpha_II_21_200
        double alpha_RI_21_200
        double alpha_RR_21_200
        double alpha_II_201_2500
        double alpha_RI_201_2500
        double alpha_RR_201_2500
        double alpha_II_2_2500
        double alpha_RI_2_2500
        double alpha_RR_2_2500
        double alpha_kp
        double alpha_k1
        double alpha_k2

    cdef struct output:
        ErrorMsg error_message

    cdef struct lensing:
        int has_tt
        int has_ee
        int has_te
        int has_bb
        int has_pp
        int has_tp
        int has_dd
        int has_td
        int has_ll
        int has_dl
        int has_tl
        int index_lt_tt
        int index_lt_te
        int index_lt_ee
        int index_lt_bb
        int index_lt_pp
        int index_lt_tp
        int index_lt_dd
        int index_lt_td
        int index_lt_ll
        int index_lt_dl
        int index_lt_tl
        int * l_max_lt
        int lt_size
        int has_lensed_cls
        int l_lensed_max
        int l_unlensed_max
        ErrorMsg error_message

    cdef struct nonlinear:
        int method
        ErrorMsg error_message

    cdef struct file_content:
        char * filename
        int size
        FileArg * name
        FileArg * value
        short * read

    void parser_free(void*)
    void lensing_free(void*)
    void spectra_free(void*)
    void transfer_free(void*)
    void primordial_free(void*)
    void perturb_free(void*)
    void thermodynamics_free(void*)
    void background_free(void*)
    void nonlinear_free(void*)

    cdef int _FAILURE_
    cdef int _FALSE_
    cdef int _TRUE_

    int input_init(void*, void*, void*, void*, void*, void*, void*, void*, void*,
        void*, void*, char*) nogil
    int background_init(void*,void*) nogil
    int thermodynamics_init(void*,void*,void*) nogil
    int perturb_init(void*,void*,void*,void*) nogil
    int primordial_init(void*,void*,void*) nogil
    int nonlinear_init(void*,void*,void*,void*,void*,void*) nogil
    int transfer_init(void*,void*,void*,void*,void*,void*) nogil
    int spectra_init(void*,void*,void*,void*,void*,void*,void*) nogil
    int lensing_init(void*,void*,void*,void*,void*) nogil

    int background_tau_of_z(void* pba, double z,double* tau) nogil
    int background_at_tau(void* pba, double tau, short return_format, short inter_mode, int * last_index, double *pvecback) nogil
    int background_output_titles(void * pba, char titles[_MAXTITLESTRINGLENGTH_]) nogil
    int background_output_data(void *pba, int number_of_titles, double *data) nogil

    int thermodynamics_at_z(void * pba, void * pth, double z, short inter_mode, int * last_index, double *pvecback, double *pvecthermo) nogil
    int thermodynamics_output_titles(void * pba, void *pth, char titles[_MAXTITLESTRINGLENGTH_]) nogil
    int thermodynamics_output_data(void *pba, void *pth, int number_of_titles, double *data) nogil

    int primordial_output_titles(void * ppt, void *ppm, char titles[_MAXTITLESTRINGLENGTH_]) nogil
    int primordial_output_data(void *ppt, void *ppm, int number_of_titles, double *data) nogil
    int primordial_spectrum_at_k(void * ppm, int index_md, linear_or_logarithmic mode, double k, double * pk) nogil

    int spectra_output_tk_titles(void *pba, void *ppt,  file_format output_format, char titles[_MAXTITLESTRINGLENGTH_]) nogil
    int spectra_output_tk_data(void *pba,void *ppt,void *psp,  file_format output_format, double z, int number_of_titles, double *data) nogil

    int spectra_cl_at_l(void* psp,double l,double * cl,double * * cl_md,double * * cl_md_ic) nogil
    int lensing_cl_at_l(void * ple,int l,double * cl_lensed) nogil
    int spectra_pk_at_z(
        void * pba,
        void * psp,
        int mode,
        double z,
        double * output_tot,
        double * output_ic
        ) nogil

    int spectra_pk_at_k_and_z(
        void* pba,
        void * ppm,
        void * psp,
        double k,
        double z,
        double * pk,
        double * pk_ic) nogil

    int spectra_pk_nl_at_k_and_z(
        void* pba,
        void * ppm,
        void * psp,
        double k,
        double z,
        double * pk) nogil

    int spectra_pk_nl_at_z(
        void * pba,
        void * psp,
        int mode,
        double z,
        double * output_tot) nogil

    int spectra_sigma(
        void * pba,
        void * ppm,
        void * psp,
        double R,
        double z,
        double *sigma) nogil

    int nonlinear_k_nl_at_z(void* pba, void* pnl, double z, double* k_nl) nogil

    int spectra_firstline_and_ic_suffix(void *ppt, int index_ic, char first_line[_LINE_LENGTH_MAX_], FileName ic_suffix) nogil
