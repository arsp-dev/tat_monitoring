

entero = ["phs", "eae", "o78", "o2k", "o1k", "mmo", "eaa", "hal", "ein", "cro", "esa", "yok", "yre", "yer", "yru", "yro", "yes", "yep", "ymo", "ykr", "yin", "yfr", "yen", "ybe", "yal", "trb", "tgu", "tat", "tpt", "se-", "sru", "sqv", "spc", "spc", "spl", "so2", "so1", "sod", "sma", "slq", "sgr", "sfo", "sfi", "sem", "kte", "rao", "kpl", "kor", "rah", "raq", "psu", "pst", "prv", "prg", "pre", "phe", "pal", "pvu", "pr-", "pre", "ppe", "pmy", "pmi", "pal", "ple", "psh", "pan", "eag", "mor", "msb", "mmo", "mmo", "mwi", "moe", "cgr", "lem", "lri", "lgr", "lec", "lad", "yre", "yok", "klu", "kcr", "kas", "kpl", "kte", "kl-", "krn", "krn", "kpn", "koz", "kpn", "kpl", "koz", "kox", "kor", "eae", "cgr", "kor", "haf", "hal", "gne", "ewi", "ear", "evu", "esc", "ehe", "efe", "eet", "eep", "eei", "eeh", 788, "o26", "2k2", 157, "of4", 149, 145, 111, 103, "1k1", "k99", "ead", "eco", "ebl", "lad", "erw", "ect", "ece", "eal", "ecg", "en-", "esa", "enp", "ein", "ehm", "egg", "edi", "ecl", "ecg", "eas", "ea2", "ea1", "eam", "eag", "eae", "eta", "edw", "eic", "eho", "cyo", "cwe", "ci-", "csk", "cdi", "ci9", "c11", "c10", "cfr", "cfa", "cdl", "cdi", "cbk", "cml", "ce5", "cnt", "ce3", "ced", "cnt", "cle", "cda", "tgu", "kas", "ehm", "lgr", "mwi", "yre", "lad", "eas", "cda", "ehe", "efe", "evu", "tpt", "bua", "bud", "baq"]
sal_shi = ["snd", "shi", "sn1", "dxx", "sd1", "d09", "d08", "d07", "d06", "d05", "d04", "d03", "d02", "d15", "d14", "d13", "d12", "d11", "d10", "d01", "sha", "bxx", "b09", "b08", "b07", "b06", "b05", "b04", "b03", "b02", "b18", "b17", "b16", "b15", "b14", "b13", "b12", "b11", "b10", "b01", "shc", "s02", "s01", "shd", "fvy", "fvx", 479, "fxx", "f06", "f5b", "f5a", "f05", "f4c", "f4b", "f4a", "f04", "f3b", "f3a", "f03", "f2b", "f2a", "f02", "f1b", "f1a", "f01", "shb", "sat"]
non_ent = ["aug", "asd", "ano", "ano", "aby", "aro", "apt", "apa", "ac-", "alw", "aju", "ajo", "aha", "abx", "alw", "aca", "aba", "aan"]
pce = ['pce']
pae = ['pae']
pma = ['pma']
def select_panel(org_name : str) -> tuple:
    ## abx from disk and mic should be aligned in the list
    if org_name in entero:
        disk_abx = ['amc_nd20','amc_nd20_ris','amx_nd30','amx_nd30_ris','czo_nd30','czo_nd30_ris','ctx_nd30','ctx_nd30_ris','cro_nd30','cro_nd30_ris',
                    'cip_nd5','cip_nd5_ris','gen_nd10','gen_nd10_ris','lvx_nd5','lvx_nd5_ris','tzp_nd100','tzp_nd100_ris',
                    'sxt_nd1_2','sxt_nd1_2_ris','amk_nd30','amk_nd30_ris','fep_nd30','fep_nd30_ris','fox_nd30','fox_nd30_ris',
                    'cxm_nd30','cxm_nd30_ris','etp_nd10','etp_nd10_ris','ipm_nd10','ipm_nd10_ris','mem_nd10','mem_nd10_ris', 'tcy_nd30','tcy_nd30_ris',
                    'tob_nd10', 'tob_nd10_ris','fdc_nd','fdc_nd_ris','cza_nd30','cza_nd30_ris','imr_nd10','imr_nd10_ris','mev_nd20','mev_nd20_ris',
                    'plz_nd','plz_nd_ris','atm_nd30','atm_nd30_ris','caz_nd30','caz_nd30_ris','czt_nd30','czt_nd30_ris','col_nd10','col_nd10_ris',
                    'pol_nd300','pol_nd300_ris','nit_nd300','nit_nd300_ris'
                    ]
        mic_abx = ['amc_nm','amc_nm_ris','amx_nm','amx_nm_ris','czo_nm','czo_nm_ris','ctx_nm','ctx_nm_ris','cro_nm','cro_nm_ris','cip_nm','cip_nm_ris',
                   'gen_nm','gen_nm_ris','lvx_nm','lvx_nm_ris','tzp_nm','tzp_nm_ris','sxt_nm','sxt_nm_ris','amk_nm','amk_nm_ris','fep_nm','fep_nm_ris',
                   'fox_nm','fox_nm_ris','cxm_nm','cxm_nm_ris','etp_nm','etp_nm_ris','ipm_nm','ipm_nm_ris','mem_nm','mem_nm_ris','tcy_nm','tcy_nm_ris',
                   'tob_nm','tob_nm_ris','fdc_nm','fdc_nm_ris','cza_nm','cza_nm_ris','imr_nm','imr_nm_ris','mev_nm','mev_nm_ris','plz_nm','plz_nm_ris',
                   'atm_nm','atm_nm_ris','caz_nm','caz_nm_ris','czt_nm','czt_nm_ris','col_nm','col_nm_ris','pol_nm','pol_nm_ris','nit_nm','nit_nm_ris']
        return disk_abx, mic_abx
    
    if org_name in sal_shi:
        disk_abx = ['amp_nd10','amp_nd10_ris','ctx_nd30','ctx_nd30_ris','cro_nd30','cro_nd30_ris','cip_nd5','cip_nd5_ris','lvx_nd5','lvx_nd5_ris',
                    'sxt_nd1_2','sxt_nd1_2_ris','azm_nd15','azm_nd15_ris','etp_nd10','etp_nd10_ris','ipm_nd10','ipm_nd10_ris','mem_nd10','mem_nd10_ris',
                    'tcy_nd30','tcy_nd30_ris','chl_nd30','chl_nd30_ris','col_nd10','col_nd10_ris'
                    ]
        mic_abx = ['amp_nm','amp_nm_ris','ctx_nm','ctx_nm_ris','cro_nm','cro_nm_ris','cip_nm','cip_nm_ris','lvx_nm','lvx_nm_ris','sxt_nm','sxt_nm_ris',
                   'azm_nm','azm_nm_ris','etp_nm','etp_nm_ris','ipm_nm','ipm_nm_ris','mem_nm','mem_nm_ris','tcy_nm','tcy_nm_ris','chl_nm','chl_nm_ris',
                   'col_nm','col_nm_ris']

        return disk_abx, mic_abx
    
    if org_name in non_ent:
        disk_abx = ['sam_nd10','sam_nd10_ris','fep_nd30','fep_nd30_ris','caz_nd30','caz_nd30_ris','cip_nd5','cip_nd5_ris','lvx_nd5','lvx_nd5_ris','gen_nd10','gen_nd10',
                    'tob_nd10','tob_nd10_ris','amk_nd30','amk_nd30_ris','ipm_nd10','ipm_nd10_ris','mem_nd10','mem_nd10_ris','mno_nd30','mno_nd30_ris','tzp_nd100','tzp_nd100_ris',
                    'fdc_nd','fdc_nd_ris','sxt_nd1_2','sxt_nd1_2_ris','ctx_nd30','ctx_nd30_ris','cro_nd30','cro_nd30_ris','col_nd10','col_nd10_ris','pol_nd300','pol_nd300_ris',
                    'tcy_nd30','tcy_nd30_ris']
        mic_abx = ['sam_nm','sam_nm_ris','fep_nm','fep_nm_ris','caz_nm','caz_nm_ris','cip_nm','cip_nm_ris','lvx_nm','lvx_nm_ris','gen_nm','gen_nm_ris',
                   'tob_nm','tob_nm_ris','amk_nm','amk_nm_ris','ipm_nm','ipm_nm_ris','mem_nm','mem_nm_ris','mno_nm','mno_nm_ris','tzp_nm','tzp_nm_ris',
                   'fdc_nm','fdc_nm_ris','sxt_nm','sxt_nm_ris','ctx_nm','ctx_nm_ris','cro_nm','cro_nm_ris','col_nm','col_nm_ris','pol_nm','pol_nm_ris',
                   'tcy_nm','tcy_nm_ris']
        return disk_abx, mic_abx
    

    if org_name in pce:
        disk_abx = ['caz_nd30','caz_nd30_ris','lvx_nd5','lvx_nd5_ris','mem_nd10','mem_nd10_ris','mno_nd30','mno_nd30_ris','sxt_nd1_2','sxt_nd1_2_ris','chl_nd30','chl_nd30_ris']
        mic_abx = ['caz_nm','caz_nm_ris','lvx_nm','lvx_nm_ris','mem_nm','mem_nm_ris','mno_nm','mno_nm_ris','sxt_nm','sxt_nm_ris','chl_nm','chl_nm_ris']
        return disk_abx, mic_abx
    

    if org_name in pae:
        disk_abx = ['fep_nd30','fep_nd30_ris','caz_nd30','caz_nd30_ris','cip_nd5','cip_nd5_ris','lvx_nd5','lvx_nd5_ris','tzp_nd100','tzp_nd100_ris','tob_nd10','tob_nd10_ris',
                    'ipm_nd10','ipm_nd10_ris','mem_nd10','mem_nd10_ris','fdc_nd','fdc_nd_ris','cza_nd30','cza_nd30_ris','czt_nd30','czt_nd30_ris','imr_nd10','imr_nd10_ris',
                    'atm_nd30','atm_nd30_ris','col_nd10','col_nd10_ris','pol_nd300','pol_nd300_ris','amk_nd30','amk_nd30_ris']
        mic_abx = ['fep_nm','fep_nm_ris','caz_nm','caz_nm_ris','cip_nm','cip_nm_ris','lvx_nm','lvx_nm_ris','tzp_nm','tzp_nm_ris','tob_nm','tob_nm_ris',
                   'ipm_nm','ipm_nm_ris','mem_nm','mem_nm_ris','fdc_nm','fdc_nm_ris','cza_nm','cza_nm_ris','czt_nm','czt_nm_ris','imr_nm','imr_nm_ris',
                   'atm_nm','atm_nm_ris','col_nm','col_nm_ris','pol_nm','pol_nm_ris','amk_nm','amk_nm_ris']
        return disk_abx, mic_abx
    

    if org_name in pma:
        disk_abx = ['lvx_nd5','lvx_nd5_ris','mno_nd30','mno_nd30_ris','sxt_nd1_2','sxt_nd1_2_ris','fdc_nd','fdc_nd_ris','chl_nd30','chl_nd30_ris']
        mic_abx = ['lvx_nm','lvx_nm_ris','mno_nm','mno_nm_ris','sxt_nm','sxt_nm_ris','fdc_nm','fdc_nm_ris','chl_nm','chl_nm_ris']
        return disk_abx, mic_abx