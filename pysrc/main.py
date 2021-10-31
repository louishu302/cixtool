import os
import sys
from toolgui import *
from tkinter import *


# main function calls method gui_start() to start gui
def gui_start(var_lst):
    init_window = Tk()
    tool = TOOL_GUI(init_window, var_lst)
    tool.set_init_window()
    init_window.mainloop()

if __name__ == '__main__':
    var_lst = []
    gui_start(var_lst)
    #Write Data to file 
    # path = '/home/cixlab/emu/'
    # testfile = path + 'collection_data.csv'
    # fp = open(testfile, mode='w+',buffering=-1,encoding=None,errors=None,newline=None,
        #   closefd=True,opener=None)
    # spi_dict = {"read_bar":var_lst[200]}
    # for offset in range(1,257,1):
        # spi_dict.update({"read_offset"+str(offset):var_lst[200+offset]})
    # spi_dict.update({"write_bar":var_lst[457]})
    # for offset in range(1,257,1):
        # spi_dict.update({"write_offset"+str(offset):var_lst[457+offset]})
    # 
    # for key in range(len(spi_dict)):
        # fp.write(spi_dict.items())
# 
    # fp.close()
    
# method list
# fp.close()
# fp.flush()
# fp.next()        : return next line in file
# fp.read([size])  : if no size then read all
# fp.readline([size]):  read line from file
# fp.readlines([sizeint]) : read all lines
# fp.seek(offset[,whence]) : set file current position 
# fp.tell()                : return current position
# fp.truncate([size])      : capture certain texts 
# fp.write(str)            : write string to file
# fp.writelines(sequence)  : write sequence string list to file  

#/* 
# main() function mainly used to start GUI window; and collect user input data */
#/*
#   unified var_lst usage definition:
#     var_lst[0..99]     For Log usage,  local parameter: cru_idx_log to walk through list
#     var_lst[100..199]  For DFD usage,  local parameter: cur_idx_dfd to walk through list
#     var_lst[200..899]  For SPI usage,  local parameter: cur_idx_spi to walk through list
#     var_lst[900..1099] For HBM usage,  local parameter: cur_idx_hbm to walk through list
#*/
# Note: data structure collection here, need convery to C interface
#/* SPI data structure
#   BaseAddr_rd: self.var_lst[cur_idx_spi]             #200
#   Data_rd    : self.var_lst[cur_idx_spi + 1..256]    #201~456
#   BaseAddr_wr: self.var_lst[cur_idx_spi + 257]       #457
#   Data_wr    : self.var_lst[cur_idx_spi + 458..713]  #458~713
#*/

# DFD data structure 
# Segment 1 - For debug_bus(self)
# sync_sel_var                     : self.var_lst[cur_idx_dfd + 0]         #100
# single_blk_var                   : self.var_lst[cur_idx_dfd + 1]
# partition_id_var                 : self.var_lst[cur_idx_dfd + 2]
# mux_id_var                       : self.var_lst[cur_idx_dfd + 3]
# blk1_id_var                      : self.var_lst[cur_idx_dfd + 4]
# byte_sel1_var                    : self.var_lst[cur_idx_dfd + 5]
# blk2_id_var                      : self.var_lst[cur_idx_dfd + 6]
# byte_sel2_var                    : self.var_lst[cur_idx_dfd + 7]
# blk3_id_var                      : self.var_lst[cur_idx_dfd + 8]
# byte_sel3_var                    : self.var_lst[cur_idx_dfd + 9]
# cntrl_en_var                     : self.var_lst[cur_idx_dfd + 10]
###################################################################
# Segment 2 - For tracer_ctrl(self)
# trace_store_var                  : self.var_lst[cur_idx_dfd + 11]
# trace_start_var                  : self.var_lst[cur_idx_dfd + 12]
# trace_cache_var                  : self.var_lst[cur_idx_dfd + 13]
# trace_disTsc_var                 : self.var_lst[cur_idx_dfd + 14]
# trace_cnt0_var                   : self.var_lst[cur_idx_dfd + 15]
# trace_cnt1_var                   : self.var_lst[cur_idx_dfd + 16]
# trace_disTcnt_var                : self.var_lst[cur_idx_dfd + 17]
# trace_stOnChg_var                : self.var_lst[cur_idx_dfd + 18]
# trace_obs0_var                   : self.var_lst[cur_idx_dfd + 19]
# trace_obs1_var                   : self.var_lst[cur_idx_dfd + 20]
# trace_obs2_var                   : self.var_lst[cur_idx_dfd + 21]
# trace_obs3_var                   : self.var_lst[cur_idx_dfd + 22]
# dbs_cmpsel0_var                  : self.var_lst[cur_idx_dfd + 23]
# dbs_cmpmod0_var                  : self.var_lst[cur_idx_dfd + 24]
# dbs_cmpsel1_var                  : self.var_lst[cur_idx_dfd + 25]
# dbs_cmpmod1_var                  : self.var_lst[cur_idx_dfd + 26]
# trace_dbgOn_var                  : self.var_lst[cur_idx_dfd + 27]
###################################################################
# DRB2CHUB Enable                   : self.var_lst[cur_idx_dfd + 28]
# General Counter0(RO)              : self.var_lst[cur_idx_dfd + 29]
# General Counter1(RO)              : self.var_lst[cur_idx_dfd + 30]
# Clock Counter(RO)                 : self.var_lst[cur_idx_dfd + 31]
# DRB Read Data(RO)                 : self.var_lst[cur_idx_dfd + 32]
# DRB Pack mode(0~2)                : self.var_lst[cur_idx_dfd + 33]
# HBM Address                       : self.var_lst[cur_idx_dfd + 34]
# General Counter0 Data match       : self.var_lst[cur_idx_dfd + 35]
# General Counter1 Data match       : self.var_lst[cur_idx_dfd + 36]
# Clk Cntr Data match               : self.var_lst[cur_idx_dfd + 37]
# DBUS0 Data match                  : self.var_lst[cur_idx_dfd + 38]
# DBUS1 Data match                  : self.var_lst[cur_idx_dfd + 39]
# DBUS bit select0                  : self.var_lst[cur_idx_dfd + 40]
# DBUS bit select1                  : self.var_lst[cur_idx_dfd + 41]
# DBUS bit select2                  : self.var_lst[cur_idx_dfd + 42]
# DBUS bit select3                  : self.var_lst[cur_idx_dfd + 43]
# DBUS bit mode sel0                : self.var_lst[cur_idx_dfd + 44]
# DBUS bit mode sel1                : self.var_lst[cur_idx_dfd + 45]
# DBUS bit mode sel2                : self.var_lst[cur_idx_dfd + 46]
# DBUS bit mode sel3                : self.var_lst[cur_idx_dfd + 47]
# DBUS trig sel0                    : self.var_lst[cur_idx_dfd + 48]
# DBUS trig sel1                    : self.var_lst[cur_idx_dfd + 49]
# DBUS trig sel2                    : self.var_lst[cur_idx_dfd + 50]
# DBUS trig sel3                    : self.var_lst[cur_idx_dfd + 51]
# DBUS trig sel4                    : self.var_lst[cur_idx_dfd + 52]
# DBUS trig sel5                    : self.var_lst[cur_idx_dfd + 53]
# DBUS trig sel6                    : self.var_lst[cur_idx_dfd + 54]
# DBUS trig sel7                    : self.var_lst[cur_idx_dfd + 55]
# DBUS trig sel8                    : self.var_lst[cur_idx_dfd + 56]
# DBUS trig sel9                    : self.var_lst[cur_idx_dfd + 57]
# DBUS trig sel10                   : self.var_lst[cur_idx_dfd + 58]
# DBUS trig sel11                   : self.var_lst[cur_idx_dfd + 59]
###################################################################
# OBS0_Main Trigger Selection A     : self.var_lst[cur_idx_dfd + 60]
# OBS0_Main Trigger Selection B     : self.var_lst[cur_idx_dfd + 61]
# OBS0_Main Trigger Selection C     : self.var_lst[cur_idx_dfd + 62]
# OBS0_Permutation Selection        : self.var_lst[cur_idx_dfd + 63]
# OBS0_Action0 Selection            : self.var_lst[cur_idx_dfd + 64]
# OBS0_Action1 Selection            : self.var_lst[cur_idx_dfd + 65]
# OBS1_Main Trigger Selection A     : self.var_lst[cur_idx_dfd + 66]
# OBS1_Main Trigger Selection B     : self.var_lst[cur_idx_dfd + 67]
# OBS1_Main Trigger Selection C     : self.var_lst[cur_idx_dfd + 68]
# OBS1_Permutation Selection        : self.var_lst[cur_idx_dfd + 69]
# OBS1_Action0 Selection            : self.var_lst[cur_idx_dfd + 70]
# OBS1_Action1 Selection            : self.var_lst[cur_idx_dfd + 71]
# OBS2_Main Trigger Selection A     : self.var_lst[cur_idx_dfd + 72]
# OBS2_Main Trigger Selection B     : self.var_lst[cur_idx_dfd + 73]
# OBS2_Main Trigger Selection C     : self.var_lst[cur_idx_dfd + 74]
# OBS2_Permutation Selection        : self.var_lst[cur_idx_dfd + 75]
# OBS2_Action0 Selection            : self.var_lst[cur_idx_dfd + 76]
# OBS2_Action1 Selection            : self.var_lst[cur_idx_dfd + 77]
# OBS3_Main Trigger Selection A     : self.var_lst[cur_idx_dfd + 78]
# OBS3_Main Trigger Selection B     : self.var_lst[cur_idx_dfd + 79]
# OBS3_Main Trigger Selection C     : self.var_lst[cur_idx_dfd + 80]
# OBS3_Permutation Selection        : self.var_lst[cur_idx_dfd + 81]
# OBS3_Action0 Selection            : self.var_lst[cur_idx_dfd + 82]
# OBS3_Action1 Selection            : self.var_lst[cur_idx_dfd + 83]

# HBM data structure 
# Device0 Request PA Size                   : self.var_lst[cur_idx_hbm + 0]         #900
# Device1 Request PA Size                   : self.var_lst[cur_idx_hbm + 1]
# Device2 Request PA Size                   : self.var_lst[cur_idx_hbm + 2]
# Device3 Request PA Size                   : self.var_lst[cur_idx_hbm + 3]
# Device4 Request PA Size                   : self.var_lst[cur_idx_hbm + 4]
# Device5 Request PA Size                   : self.var_lst[cur_idx_hbm + 5]
# Device6 Request PA Size                   : self.var_lst[cur_idx_hbm + 6]
# Device7 Request PA Size                   : self.var_lst[cur_idx_hbm + 7]
# Device0 Response PA Base Address          : self.var_lst[cur_idx_hbm + 8]         
# Device1 Response PA Base Address          : self.var_lst[cur_idx_hbm + 9]
# Device2 Response PA Base Address          : self.var_lst[cur_idx_hbm + 10]
# Device3 Response PA Base Address          : self.var_lst[cur_idx_hbm + 11]
# Device4 Response PA Base Address          : self.var_lst[cur_idx_hbm + 12]
# Device5 Response PA Base Address          : self.var_lst[cur_idx_hbm + 13]
# Device6 Response PA Base Address          : self.var_lst[cur_idx_hbm + 14]
# Device7 Response PA Base Address          : self.var_lst[cur_idx_hbm + 15]
# Reading Device ID selection               : self.var_lst[cur_idx_hbm + 16]
# Reading Device Start Address              : self.var_lst[cur_idx_hbm + 17]
# Reading Data DWord Index0                 : self.var_lst[cur_idx_hbm + 18]
# Reading Data DWord Index1                 : self.var_lst[cur_idx_hbm + 19]
# Reading Data DWord Index2                 : self.var_lst[cur_idx_hbm + 20]
#   .......................                    ....................
# Reading Data DWord Index63                : self.var_lst[cur_idx_hbm + 81]
# Writting Device ID selection              : self.var_lst[cur_idx_hbm + 82]
# Writting Device Start Address             : self.var_lst[cur_idx_hbm + 83]
# Writting Data DWord Index0                : self.var_lst[cur_idx_hbm + 84]
# Writting Data DWord Index1                : self.var_lst[cur_idx_hbm + 85]
# Writting Data DWord Index2                : self.var_lst[cur_idx_hbm + 86]
#   .......................                    ....................
# Writting Data DWord Index63               : self.var_lst[cur_idx_hbm + 147]







































































































