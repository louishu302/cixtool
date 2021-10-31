import os
import sys
from tkinter import *
import tkinter.font as font
from tkinter import messagebox
import tool
#/*
# Layer1- Labelframe to outline overall stuffs
# Entry:  accept single-line text strings from a user; note: entry.get() return string 
# Text:   accept multiple lines of text that can be edited
# Label:  display multiples lines of text that cannot be modified
# Button: start operations
# Color:  white/black/red/green/blue/cyan/yellow/magenta/pink
# font.Font(family="Helvetica", size = 20, weight ="bold/normal",
# slant ="italic/roman", underline="1/0", overstrike="1/0")
#relief = FLAT/RAISED/SUNKEN/GROOVE/RIDGE
#Anchor = NW/N/NE/w/CENTER/E/SW/S/SE
# geometry(WxH+x+y); widget.pack(expand=true,fill=NONE/X/Y/BOTH,side=TOP/BOTTOM/LEFT/RIGHT)
# widget.grid(row=1, rowspan=1,column=0,columnspan=1,ipadx/ipady=n,padx/pady=n,sticky='NESWNENWSESW')
# widget.place(anchor=NESWNENWSESW,bordermode=INSIDE/OUTSIDE,height/width=npixels,x/y=npixels)
#*/

#/*
#   unified var_lst usage definition:
#     var_lst[0..99] For Log usage,     local parameter: cru_idx_log to walk through list
#     var_lst[100..199] For DFD usage,  local parameter: cur_idx_dfd to walk through list
#     var_lst[200..899] For SPI usage,  local parameter: cur_idx_spi to walk through list
#*/
class TOOL_GUI():
    def __init__(self, init_window_name, var_lst):
        self.init_window_name = init_window_name
        self.var_lst = var_lst
        for r in range(5):
            for c in range(256): 
                self.var_lst.append(c)        
        self.cur_idx_log_g = (0)               # const value
        self.cur_idx_dfd_g = (100)             # const value
        self.cur_idx_spi_g = (200)             # const value
        self.cur_idx_hbm_g = (900)             # const value
        self.myFont = font.Font(family="Helvetica", size = 15, weight ="bold",\
           slant ="roman", underline= 0, overstrike= 0)
        # For test Only
        for i in range(148):
            self.var_lst[900+i] = 0x11223344 + i

    def donothing(self):
        filewin = Toplevel(self.init_window_name)
        button = Button(filewin,text="Do nothing currently^<^")

    def spi_frame(self):
        cur_idx_spi = self.cur_idx_spi_g   #200

        spi_top = Toplevel(bg="khaki", width= 1024, height = 800)
        spi_top.title("SPI Flash")
        spi_top.geometry("1024x800+10+10")
        spi_labelframe_read = LabelFrame(spi_top, text="SPI Reading Area",\
         labelanchor = N, relief=RAISED, width= 800, height= 600)
        spi_labelframe_read.pack(expand = 1, fill = BOTH, side = LEFT)

        spi_addr_label = Label(spi_labelframe_read, text = "Start Address")
        spi_addr_label.grid(row = 10, rowspan = 1, column = 1, columnspan = 3, sticky = 'W')

        self.spi_addr_read = Entry(spi_labelframe_read, width = 20)
        self.spi_addr_read.grid(row = 10, rowspan = 1, column = 3, columnspan = 20)        
        
        addr_c = ("0x00","0x01","0x02","0x03","0x04","0x05","0x06","0x07","0x08","0x09","0x0A","0x0B","0x0C","0x0D","0x0E","0x0F")
        addr_r = ("0x00","0x10","0x20","0x30","0x40","0x50","0x60","0x70","0x80","0x90","0xA0","0xB0","0xC0","0xD0","0xE0","0xF0")
        for c1 in range(16):
            Label(spi_labelframe_read, text = addr_c[c1], pady=2).grid(row = 15, column = c1 + 1)
            Label(spi_labelframe_read, text = addr_r[c1], pady=2).grid(row = 16 + c1, column = 0)

        for r in range(16):
            for c in range(16):
                w = Button(spi_labelframe_read, text=f"0x{self.var_lst[cur_idx_spi + r*16 + c + 1]:X}", padx=2, relief = SUNKEN)
                w.grid(row=r + 16, column=c + 1)

        def spi_read():
            self.var_lst[self.cur_idx_spi_g] = self.spi_addr_read.get()                   #Note: Entry.get() return string
            addr_int = IntVar()
            addr_int = int(self.var_lst[self.cur_idx_spi_g] , base = 16)
            print("read_base_address=0x",addr_int)
            # call c function to update read data to self.var_lst[self.cur_idx_spi_g + 1: 256]
            data_dw = IntVar()
            for it in range(0x0, 0x40, 0x1):
                data_dw = tool.spird(addr_int + it)
                bytes_val = data_dw.to_bytes(4, "little")
                for byte in range(4):
                    self.var_lst[self.cur_idx_spi_g + 1 + byte + it] = bytes_val[byte] 
            for r in range(16):
               for c in range(16):
                   w = Button(spi_labelframe_read, text=f"0x{self.var_lst[cur_idx_spi + r*16 + c + 1]:X}", padx=2, relief = SUNKEN)
                   w.grid(row=r + 16, column=c + 1)
        
        spi_read_btn = Button(spi_labelframe_read, command = spi_read, height = 1,\
            justify = CENTER, relief = RAISED, width = 10, wraplength =0 )
        spi_read_btn.grid(row = 100, rowspan = 2, column = 1, columnspan = 20,sticky = 'S')
        spi_read_btn.flash()
        spi_read_btn['font'] = self.myFont
        spi_read_btn['text'] = "Start"

        spi_labelframe_write = LabelFrame(spi_top, text="SPI Writting Area",\
         labelanchor = N, relief=RAISED, width= 640, height= 480)
        spi_labelframe_write.pack(expand = 1, fill = BOTH, side = RIGHT)

        spi_addr_label_w = Label(spi_labelframe_write, text = "Start Address")
        spi_addr_label_w.grid(row = 10, rowspan = 1, column = 1, columnspan = 3, sticky = 'W')

        self.spi_addr_write = Entry(spi_labelframe_write, width = 20)
        self.spi_addr_write.grid(row = 10, rowspan = 1, column = 3, columnspan = 20)
        
        cur_idx_spi = cur_idx_spi + 16*16 + 3

        for c in range(16):
            Label(spi_labelframe_write, text = addr_c[c], pady=4).grid(row = 15, column = c + 1)
            Label(spi_labelframe_write, text = addr_r[c], pady=4).grid(row = 16 + c, column = 0)

        self.spi_w = []
        for r in range(16):
            for c in range(16):
                w = Entry(spi_labelframe_write, width=4).grid(row=r + 16, column=c + 1)
                self.spi_w.append(w)

        spi_write_btn = Button(spi_labelframe_write, command = self.spi_write, height = 1,\
            justify = CENTER, relief = RAISED, width = 10, wraplength =0 )
        spi_write_btn.grid(row = 100, rowspan = 2, column = 1, columnspan = 20,sticky = 'S')
        spi_write_btn.flash()
        spi_write_btn['font'] = self.myFont
        spi_write_btn['text'] = "Start"
   


    def spi_write(self):
        self.var_lst[self.cur_idx_spi_g + 16 * 16 + 2] = self.spi_addr_write.get()
        print("write_base_address=",self.var_lst[self.cur_idx_spi_g + 16 * 16 + 2])
        for i in range(256):
            self.var_lst[self.cur_idx_spi_g + i] = self.spi_w[i].get()
            print("spi_write_data @" + str(self.cur_idx_spi_g + i),self.var_lst[self.cur_idx_spi_g + i])

    def log_man(self):
        log_top = Toplevel(bg="khaki", width= 1024, height = 800)
        log_top.title("System Logging")
        log_top.geometry("1024x800+10+10")
        log_labelframe = LabelFrame(log_top, text="Logman Running...",\
         labelanchor = N, relief=RAISED, width= 800, height= 600)
        log_labelframe.pack(expand = 1, fill = BOTH, side = LEFT)

        log_label = Label(log_labelframe, text="Configuration List")
        log_label.grid(row = 10, rowspan = 1, column = 1, columnspan = 3, sticky = 'W')
        self.log_entry = []
        string = ["1","2","3","4","5"]
        data   = [1,2,3,4,5]
        for i in range(5):
            wl = Entry(log_labelframe, width = 20, textvariable= data[i])
            wl.grid(row = 10 + i, rowspan = 1, column = 10, columnspan = 3, sticky = 'NE')
            self.log_entry.append(wl)

        log_btn = Button(log_labelframe, command = self.log_read, height = 1, justify = CENTER, relief = RAISED, width = 10, wraplength =0 )
        log_btn.grid(row = 100, rowspan = 2, column = 1, columnspan = 20,sticky = 'S')
        log_btn.flash()
        log_btn['font'] = self.myFont
        log_btn['text'] = "Start"

    def log_read(self):
        for i in range(5):
            self.var_lst[500 + i] = self.log_entry[i].get()
            print("log reading " + str(i), self.var_lst[500 + i])

    def debug_bus(self):
        # dfd_data_collection unified to list self.dfd_data[i]
        self.dfd_data = []
        cur_idx_dfd = self.cur_idx_dfd_g         #100
        self.dbs_top = Toplevel(bg="khaki", width= 1024, height = 800)
        self.dbs_top.title("Design For Debug Widget")
        self.dbs_top.geometry("1024x800+10+10")
        dbs_labelframe = LabelFrame(self.dbs_top, text="Debug Bus Configuration Table",\
         labelanchor = N, relief=RAISED, width= 800, height= 600)
        dbs_labelframe.pack(expand = 1, fill = BOTH, side = LEFT)

        self.chk_val = [IntVar(),IntVar(),IntVar(),IntVar(),IntVar(),IntVar()]    #For 6 chk-box
        self.wbe_cluster = []
        font_label_name = ("DBUS mode selection","DBUS multi-block selection","DBUS Input Entry")
        for i in range(3):
            wl = Label(dbs_labelframe, text = font_label_name[i])
            wl.grid(row = 10 + i * 5, rowspan = 1, column = 1, columnspan = 3, sticky = 'NW')
            wl['font']= self.myFont
        radio_name = ("DBUS synchoronous mode(dbg data onto dfd tracer)", \
                      "DBUS asynchoronous mode(dbg data onto pkg pins)",  \
                      "DBUS single block mode**************************", \
                      "DBUS multiple block mode************************")
        for i in range(2):
            wrd = Radiobutton(dbs_labelframe, text= radio_name[i],variable = self.chk_val[0], value = i, anchor = 'nw')
            wrd.grid(row = 11 + i, rowspan = 1, column = 1, columnspan = 30)
            wr = Radiobutton(dbs_labelframe, text= radio_name[i + 2],variable = self.chk_val[1], value = i, anchor = 'w',justify=LEFT)
            wr.grid(row =16 + i, rowspan = 1, column = 1, columnspan = 30)
        self.dbus_label_name = ("DBUS Partition ID Input(1~530)", "DBUS Mux ID Input(variable)",\
                      "DBUS Block1 ID Input(enable)", "DBUS Byte1 Sel Input(0~3)", \
                      "DBUS Block2 ID Input(enable)", "DBUS Byte2 Sel Input(0~3)", \
                      "DBUS Block3 ID Input(enable)", "DBUS Byte3 Sel Input(0~3)", \
                      "DBUS Controller Enable")
        
        for i in range(9):
            wl = Label(dbs_labelframe, text = self.dbus_label_name[i])
            wl.grid(row = 21 + i, rowspan = 1, column = 1, columnspan = 3, sticky = 'SW')
        sbar = Scrollbar(dbs_labelframe, orient=VERTICAL, width = 20)
        sbar.grid(row = 21, column = 18, ipady = 200)
        lbox = Listbox(dbs_labelframe, yscrollcommand = sbar.set, bd = 1,height=25)
        lbox.grid(row = 21, column = 10, sticky = 'SW')
        for sel in range(531):
            lbox.insert(END, self.partition_lst[sel])
        sbar.config(command = lbox.yview)        
        self.wbe_cluster.append(lbox)
        wb = Entry(dbs_labelframe,width = 20)
        wb.grid(row = 21 + 1, rowspan = 1, column = 10, columnspan = 3, sticky = 'SW')
        self.wbe_cluster.append(wb)
        for i in range(4):
            chk = Checkbutton(dbs_labelframe,variable = self.chk_val[2 + i] ,width = 17)
            chk.grid(row = 23 + i * 2, rowspan = 1, column = 10, columnspan = 3, sticky = 'SW')
        for i in range(3,8,2):
            we = Entry(dbs_labelframe,width = 20)
            we.grid(row = 21 + i, rowspan = 1, column = 10, columnspan = 3, sticky = 'SW')
            self.wbe_cluster.append(we)
     
        dbus_btn = Button(dbs_labelframe, command = self.dbus_go, height = 1, justify = CENTER, relief = RAISED, width = 10, wraplength =0 )
        dbus_btn.grid(row = 140, rowspan = 2, column = 1, columnspan = 20,sticky = 'S')
        dbus_btn.flash()
        dbus_btn['font'] = self.myFont
        dbus_btn['text'] = "DBUS_GO"
        # Dummy self.dfd_data for stackholder
        for i in range(11):
            self.dfd_data.append("dummy")
        self.tracer_cfg()         # calling tracer widget 
        
    def dbus_go(self):
        self.var_lst[self.cur_idx_dfd_g]     = self.chk_val[0].get()
        self.var_lst[self.cur_idx_dfd_g + 1] = self.chk_val[1].get()
        print("dbus_mode=",self.var_lst[self.cur_idx_dfd_g])
        print("multi_blk=",self.var_lst[self.cur_idx_dfd_g + 1])
        self.var_lst[self.cur_idx_dfd_g + 2] = self.wbe_cluster[0].curselection()
        self.var_lst[self.cur_idx_dfd_g + 3] = self.wbe_cluster[1].get()
        for i in range(3):
            self.var_lst[self.cur_idx_dfd_g + 2 + 3 + i * 2] = self.wbe_cluster[i+2].get()
        for i in range(4):
            self.var_lst[self.cur_idx_dfd_g + 4 + i * 2] = self.chk_val[2 + i].get()
        for i in range(9):
            print(self.dbus_label_name[i],self.var_lst[self.cur_idx_dfd_g + 2 +i])

    def tracer_cfg(self):
        #data struct collection
        tracer_labelframe = LabelFrame(self.dbs_top, text="DFD Tracer Configuration Table",\
         labelanchor = N, relief=RAISED, width= 800, height= 600)
        tracer_labelframe.pack(expand = 1, fill = BOTH, side = RIGHT)
        # Frame_top : Tracer Control Zone; Observations;  Frame_right: DRB
        self.frame_top = Frame(tracer_labelframe)
        self.frame_top.grid(row = 10, column = 1, sticky='NW')
        self.frame_right = Frame(tracer_labelframe)
        self.frame_right.grid(row = 10, column = 70, sticky='NE')
        self.tracer_ctrl()              # In order to call function for data_stack in order properly
        # self.drb_ctrl()
        # self.obs_ctrl()

    def tracer_ctrl(self):

        tr_ctrl_zone = Label(self.frame_top, text = "Tracer Control Zone")
        tr_ctrl_zone.grid(row = 10, rowspan = 1, column = 1, columnspan = 3, sticky = 'NW')
        tr_ctrl_zone['font'] = self.myFont
        self.label_name_tr = ("Trace_store_space_full_stop", "Trace_store_start", \
                      "Store_To_Cache", "Disable_Tcs_Writes","General_Counter0_Increments",\
                       "General_Counter1_Increments", "Disable absolute time counter",     \
                       "Store_On_Change", "Observation0 enable", "Observation1 enable",    \
                       "Observation2 enable","Observation3 enable","Debug Bus comparator sel0",\
                       "Debug Bus comparator mode0","Debug Bus comparator sel1",\
                       "Debug Bus comparator mode1","Debug trace On")
        
        for i in range(9):
            tmp_data = IntVar()
            self.dfd_data.append(tmp_data)
            wb = Checkbutton(self.frame_top,variable = tmp_data ,width = 27,text=self.label_name_tr[i],anchor="w",justify="left") 
            wb.grid(row = 11 + i, column=1, sticky='W')
            if (i == 8):
                wb['command']=self.obs_ctrl
            
        for i in range(8):
            tmp_data = IntVar()
            self.dfd_data.append(tmp_data)
            wb = Checkbutton(self.frame_top,variable = tmp_data ,width = 27,text=self.label_name_tr[i+9],anchor="w",justify="left") 
            wb.grid(row = 11 + i, column = 2,sticky='W')
            if (i<=2):
                wb['command']=self.obs_ctrl
            
        self.drb_ctrl()

    def drb_ctrl(self):
        #param_loc =(row, rowspan, column, columnspan, sticky,additional columnspan)
        param_loc = (10,1,70,1,'W',2)
        text_name = (
        "DRB2CHUB Enable","General Counter0(RO)","General Counter1(RO)","Clock Counter(RO)",
        "DRB Read Data(RO)","DRB Pack mode(0~2)","HBM Address","General Counter0 Data match",
        "General Counter1 Data match","Clk Cntr Data match","DBUS0 Data match","DBUS1 Data match",
        "DBUS bit sel0(0~23)","DBUS bit sel1(0~23)","DBUS bit sel2(0~23)","DBUS bit sel3(0~23)")
        def drb_read():
            #update 4 Read-only data
            #TODO- C Function return updated value 
            for btn in range(4):
                self.var_lst[self.cur_idx_hbm_g + btn + 29] = 0xdeadbeaf    #For Test Only
                wb = Button(self.frame_right, text=str(hex(self.var_lst[self.cur_idx_hbm_g + btn + 29])), relief = SUNKEN,bd=1)
                wb.grid(row=param_loc[0] + 2 + btn, column=param_loc[2] + 1)

        trace_btn = Button(self.frame_right, command = drb_read, height = 1, justify = CENTER, relief = RAISED, width = 10, wraplength =0 )
        trace_btn.grid(row = param_loc[0], rowspan = param_loc[1], column = param_loc[2], columnspan = param_loc[3],sticky = 'N')
        trace_btn.flash()
        trace_btn['font'] = self.myFont
        trace_btn['text'] = "DRB_READ"

        tmp_data = IntVar()
        wb = Checkbutton(self.frame_right,variable = tmp_data ,width = 27,text=text_name[0],anchor="w",justify="left") 
        wb.grid(row = param_loc[0] + 1, column=param_loc[2], sticky=param_loc[4])
        self.dfd_data.append(tmp_data)

        for btn in range(1,5,1):
            wl=Label(self.frame_right,text=text_name[btn])
            wl.grid(row=param_loc[0] + 1 + btn,column=param_loc[2],columnspan=param_loc[3],sticky=param_loc[4])
            wb = Button(self.frame_right, text="init_value", relief = SUNKEN,bd=1)
            wb.grid(row=param_loc[0] + 1 + btn, column=param_loc[2] + 1)
            self.dfd_data.append(wb)

        for i in range(5,16,1):
            wl=Label(self.frame_right,text=text_name[i])
            wl.grid(row=param_loc[0] + i + 1,column=param_loc[2],columnspan=param_loc[3],sticky=param_loc[4])
            wb = Entry(self.frame_right,width = 20)
            wb.grid(row = param_loc[0] + i + 1, column = param_loc[2]+param_loc[1])
            self.dfd_data.append(wb)

        wl=Label(self.frame_right,text="DBUS bit mode sel0")
        wl.grid(row=param_loc[0] + 19,column=param_loc[2],columnspan=param_loc[3],sticky=param_loc[4])
        lbox = Listbox(self.frame_right, bd = 1,height=4)
        lbox.grid(row = param_loc[0] + 19, column = param_loc[2]+param_loc[1])
        for sel in range(4):
            lbox.insert(END,self.dbus_bitTrig_mode[sel])
        self.dfd_data.append(lbox)

        for i in range(1,4,1):
            wl=Label(self.frame_right,text="DBUS bit mode"+str(i)+"(0~3)")
            wl.grid(row=param_loc[0] + 19 + i,column=param_loc[2],columnspan=param_loc[3],sticky=param_loc[4])
            wb = Entry(self.frame_right,width = 20)
            wb.grid(row = param_loc[0] + 19 + i, column = param_loc[2]+param_loc[1],sticky=param_loc[4])
            self.dfd_data.append(wb)

        wl=Label(self.frame_right,text="DBUS trig sel0")
        wl.grid(row=param_loc[0] + 23,column=param_loc[2],columnspan=param_loc[3],sticky=param_loc[4])
        sbar = Scrollbar(self.frame_right, orient=VERTICAL, width = 20, bd = 1)
        sbar.grid(row = param_loc[0] + 23, column = param_loc[2]+param_loc[1]+param_loc[5], ipady = 15,sticky=param_loc[4])
        lbox = Listbox(self.frame_right, yscrollcommand = sbar.set, bd = 1,height=5)
        lbox.grid(row = param_loc[0] + 23, column = param_loc[2]+param_loc[1])
        self.dfd_data.append(lbox)
        for sel in range(13):
            lbox.insert(END,self.dbustrig_lst[sel])
        sbar.config(command = lbox.yview)

        for i in range(1,12,1):
            wl=Label(self.frame_right,text="DBUS trig sel"+str(i)+"(0~0xC)")
            wl.grid(row=param_loc[0]+24+i,column=param_loc[2],columnspan=param_loc[3],sticky=param_loc[4])
            wb = Entry(self.frame_right,width = 20)
            wb.grid(row = param_loc[0]+24+i, column = param_loc[2]+param_loc[1],sticky=param_loc[4])
            self.dfd_data.append(wb)

        self.obs_ctrl()

    def obs_ctrl(self):
        self.obs_chk = [
            "Observation0 Control Zone*******",30,1,1,3,'W',
            "Observation1 Control Zone*******",30,1,5,3,'W',
            "Observation2 Control Zone*******",60,1,1,3,'W',
            "Observation3 Control Zone*******",60,1,5,3,'W'
        ]
        obs_active = []
        for obs in range(4):
            obs_active.append(self.dfd_data[19 + obs].get())
            print("obs enable bit",self.dfd_data[19 + obs].get())

        for i in range(0,24,6):

            if (i==0):
                special_span = 1
                if (obs_active[0] == 1):
                    special_state = NORMAL
                else:
                    special_state = DISABLED
            elif (i==12):
                special_span = 1
                if (obs_active[2] ==1):
                    special_state = NORMAL
                else:
                    special_state = DISABLED          
            elif (i==6):
                special_span = 2
                if (obs_active[1] ==1):
                    special_state = NORMAL
                else:
                    special_state = DISABLED
            elif (i==18):
                special_span = 2
                if (obs_active[3] ==1):
                    special_state = NORMAL
                else:
                    special_state = DISABLED

            wb=Label(self.frame_top,text=self.obs_chk[i],font=self.myFont)
            wb.grid(row=self.obs_chk[i+1],rowspan=self.obs_chk[i+2],column=self.obs_chk[i+3],columnspan=self.obs_chk[i+4],sticky=self.obs_chk[i+5])
            #Main Trigger Scrollbar
            wl=Label(self.frame_top,text="Main Trigger Selection A")
            wl.grid(row=self.obs_chk[i+1]+1,column=self.obs_chk[i+3],sticky='W')
            sbar = Scrollbar(self.frame_top, orient=VERTICAL, width = 20, bd = 1)
            sbar.grid(row = self.obs_chk[i+1] + 1, column = self.obs_chk[i+3]+special_span, ipady = 15,sticky='W')
            lbox = Listbox(self.frame_top, yscrollcommand = sbar.set, bd = 1,height=4)
            lbox.grid(row = self.obs_chk[i+1] + 1, column = self.obs_chk[i+3]+1)
            lbox['state'] = special_state
            self.dfd_data.append(lbox)

            for sel in range(22):
                lbox.insert(END,self.maintrig_lst[sel])
            sbar.config(command = lbox.yview)        

            wl=Label(self.frame_top,text="Main Trigger Selection B")
            wl.grid(row=self.obs_chk[i+1]+2,column=self.obs_chk[i+3],columnspan=self.obs_chk[i+4],sticky='W')
            wb = Entry(self.frame_top,width = 20)
            wb.grid(row = self.obs_chk[i+1]+2, column = self.obs_chk[i+3]+1)
            wb['state'] = special_state
            self.dfd_data.append(wb)

            wl=Label(self.frame_top,text="Main Trigger Selection C")
            wl.grid(row=self.obs_chk[i+1]+3,column=self.obs_chk[i+3],columnspan=self.obs_chk[i+4],sticky='W')
            wb = Entry(self.frame_top,width = 20)
            wb.grid(row = self.obs_chk[i+1]+3, column = self.obs_chk[i+3]+1)
            wb['state'] = special_state
            self.dfd_data.append(wb)

            wl=Label(self.frame_top,text="Permutation Selection")
            wl.grid(row=self.obs_chk[i+1]+4,column=self.obs_chk[i+3],columnspan=self.obs_chk[i+4],sticky='W')
            sbar = Scrollbar(self.frame_top, orient=VERTICAL, width = 20, bd = 1)
            sbar.grid(row = self.obs_chk[i+1] + 4, column = self.obs_chk[i+3]+special_span, ipady = 15,sticky='W')
            lbox = Listbox(self.frame_top, yscrollcommand = sbar.set, bd = 1,height=4)
            lbox.grid(row = self.obs_chk[i+1] + 4, column = self.obs_chk[i+3]+1)
            lbox['state'] = special_state
            self.dfd_data.append(lbox)
            for sel in range(17):
                lbox.insert(END,self.permutation_lst[sel])
            sbar.config(command = lbox.yview)

            wl=Label(self.frame_top,text="Action0 Selection")
            wl.grid(row=self.obs_chk[i+1]+5,column=self.obs_chk[i+3],columnspan=self.obs_chk[i+4],sticky='W')
            sbar = Scrollbar(self.frame_top, orient=VERTICAL, width = 20, bd = 1)
            sbar.grid(row = self.obs_chk[i+1] + 5, column = self.obs_chk[i+3]+special_span, ipady = 15,sticky='W')
            lbox = Listbox(self.frame_top, yscrollcommand = sbar.set, bd = 1,height=4)
            lbox.grid(row = self.obs_chk[i+1] + 5, column = self.obs_chk[i+3]+1)
            lbox['state'] = special_state
            self.dfd_data.append(lbox)
            for sel in range(15):
                lbox.insert(END,self.action_lst[sel])
            sbar.config(command = lbox.yview)

            wl=Label(self.frame_top,text="Action1 Selection")
            wl.grid(row=self.obs_chk[i+1]+6,column=self.obs_chk[i+3],columnspan=self.obs_chk[i+4],sticky='W')
            wb = Entry(self.frame_top,width = 20)
            wb.grid(row = self.obs_chk[i+1]+6, column = self.obs_chk[i+3]+1)
            wb['state'] = special_state
            self.dfd_data.append(wb)

        trace_btn = Button(self.frame_top, command = self.trace_go, height = 1, justify = CENTER, relief = RAISED, width = 10, wraplength =0 )
        trace_btn.grid(row = 140, rowspan = 2, column = 1, columnspan = 20,sticky = 'S')
        trace_btn.flash()
        trace_btn['font'] = self.myFont
        trace_btn['text'] = "TRACE_GO"


 

    def trace_go(self):
        #Get control zone data
        for i in range(17):
            self.var_lst[self.cur_idx_dfd_g + 11 +i] = self.dfd_data[11 + i].get()
            print(self.label_name_tr[i], self.var_lst[self.cur_idx_dfd_g + 11 +i] )
        #Get DRB zone data
        self.var_lst[self.cur_idx_dfd_g + 28] = self.dfd_data[28].get()
        self.var_lst[self.cur_idx_dfd_g + 44] = self.dfd_data[44].curselection()
        self.var_lst[self.cur_idx_dfd_g + 48] = self.dfd_data[48].curselection()
        for i in range(33,44,1):
            self.var_lst[self.cur_idx_dfd_g + i] = self.dfd_data[i].get()
        for bit in range(45,48,1):
            self.var_lst[self.cur_idx_dfd_g + i] = self.dfd_data[i].get()
        for bus in range(49,60,1):
            self.var_lst[self.cur_idx_dfd_g + i] = self.dfd_data[i].get()
        #Get OBS zone data
        for obs in range(4):
            self.var_lst[self.cur_idx_dfd_g + 60 + obs * 6] = self.dfd_data[60 + obs * 6].curselection()
            self.var_lst[self.cur_idx_dfd_g + 61 + obs * 6] = self.dfd_data[61 + obs * 6].get()
            self.var_lst[self.cur_idx_dfd_g + 62 + obs * 6] = self.dfd_data[62 + obs * 6].get()
            self.var_lst[self.cur_idx_dfd_g + 63 + obs * 6] = self.dfd_data[63 + obs * 6].curselection()
            self.var_lst[self.cur_idx_dfd_g + 64 + obs * 6] = self.dfd_data[64 + obs * 6].curselection()
            self.var_lst[self.cur_idx_dfd_g + 65 + obs * 6] = self.dfd_data[65 + obs * 6].get()

    def hbm_frame(self):
        #collect data
        self.hbm_data = []
        addr_c = ("0x00","0x04","0x08","0x0C")
        addr_r = ("0x00","0x10","0x20","0x30","0x40","0x50","0x60","0x70","0x80", \
        "0x90","0xA0","0xB0","0xC0","0xD0","0xE0","0xF0")

        hbm_top = Toplevel(bg="khaki", width= 1024, height = 800)
        hbm_top.title("Device Memory Zone")
        hbm_top.geometry("1024x800+10+10")

        frame_top  = Frame(hbm_top)
        frame_top.pack(expand = 1, fill = BOTH, side = TOP)
        frame_left  = Frame(hbm_top)
        frame_left.pack(expand = 1, fill = BOTH, side = LEFT)
        frame_right = Frame(hbm_top)
        frame_right.pack(expand = 1, fill = BOTH, side = RIGHT)
        
        #HBM Request
        for dev in range(8):
            self.var_lst[self.cur_idx_hbm_g + dev + 8] = dev
        for dev in range(8):
            wb = Label(frame_top, text = "Request PA Size at Device"+str(dev)+"(unit:Byte)")
            wb.grid(row = 10 + dev, column = 1, padx =20)
            we = Entry(frame_top, width = 20)
            we.grid(row = 10 + dev, column = 8, padx =20)        
            self.hbm_data.append(we)

            wt = Label(frame_top, text = "Response Base Address ")
            wt.grid(row = 10 + dev, column = 120, padx =20)
            def button_click(x=dev):
                # get devicex request PA size and clear
                # TODO!!!-10/27: C function interface to respond physical address soon
                self.var_lst[self.cur_idx_hbm_g + x] = self.hbm_data[x].get()
                # self.var_lst[self.cur_idx_hbm_g + dev + 8] = C_RETURN 
                self.var_lst[self.cur_idx_hbm_g + x + 8] = 0xdeadbeaf    # For Test Only
                print("click dev",x)                                     # For Test Only
                print("dev text",str(hex(self.var_lst[self.cur_idx_hbm_g + x + 8])))  # For Test Only
                wl = Label(frame_top, text=str(hex(self.var_lst[self.cur_idx_hbm_g + x + 8])),relief=SUNKEN)
                wl.grid(row = 10 + x, column = 160)

            wb = Button(frame_top, text = "click me", padx=20,command=button_click)
            wb.grid(row = 10 + dev, column = 160)
        for dummy in range(8):
            self.hbm_data.append(dummy)      #For stackholder
        
        # HBM Read/Write   
        read_write = [frame_left,frame_right]
        t_n = ("DeviceID Selection(0~7)","Start Address(64bit)","READ_GO","WRITE_GO")
        for fop in read_write:
            for i in range(2):
                wb = Label(fop, text = t_n[i])
                wb.grid(row = 10 + i, rowspan = 1, column = 1, columnspan = 3, sticky = 'W')
                we = Entry(fop, width = 20)
                we.grid(row = 10 + i, rowspan = 1, column = 3, columnspan = 20)        
                self.hbm_data.append(we)

            for c in range(4):
                wb = Label(fop, text = addr_c[c])
                wb.grid(row = 15, column = c + 1)
            for r in range(16):            
                wb =Label(fop, text = addr_r[r])
                wb.grid(row = 16 + r, column = 0)

            def hbm_read():
                self.var_lst[self.cur_idx_hbm_g + 16] = self.hbm_data[16]
                self.var_lst[self.cur_idx_hbm_g + 17] = self.hbm_data[17]
                #TODO- C Function return updated value 
                for r in range(16):
                    for c in range(4):
                        self.var_lst[self.cur_idx_hbm_g + r*4 + c + 18] = 0xdeadbeaf    #For Test Only
                        wb = Button(frame_left, text=str(hex(self.var_lst[self.cur_idx_hbm_g + r*4 + c + 18])), relief = SUNKEN,bd=1)
                        wb.grid(row=r + 16, column=c + 1)

            hbm_btn = Button(fop, height = 1, justify = CENTER, width = 10, wraplength =0 )
            hbm_btn.grid(row = 100, rowspan = 2, column = 5, sticky = 'S')
            hbm_btn.flash()
            hbm_btn['font'] = self.myFont
            if (fop == frame_left):            
                hbm_btn['text']    = t_n[2]
                hbm_btn['command'] = hbm_read
                for r in range(16):
                    for c in range(4):
                        wb = Button(fop, text=str(hex(self.var_lst[self.cur_idx_hbm_g + r*4 + c + 18])), relief = SUNKEN,bd=1)
                        wb.grid(row=r + 16, column=c + 1)
                        self.hbm_data.append(wb)            # For stackholder
            else:
                hbm_btn['text']    = t_n[3]
                hbm_btn['command'] = self.hbm_write 
                for r in range(16):
                    for c in range(4):
                        w = Entry(fop, width=20)
                        w.grid(row=r + 16, column=c + 1)
                        self.hbm_data.append(w)

    def hbm_write(self):
        self.var_lst[self.cur_idx_hbm_g + 82] = self.hbm_data[82]
        self.var_lst[self.cur_idx_hbm_g + 83] = self.hbm_data[83]
        for i in range(64):
            self.var_lst[self.cur_idx_hbm_g+84+i] = self.hbm_data[84+i].get()

    def help_index(self):
        b = 0

    def help_about(self):
        messagebox.showinfo("About","This is a powerful Validation Tool")
        messagebox.showwarning()
        messagebox.showerror()
        messagebox.askquestion()
        messagebox.askokcancel()
        messagebox.askyesno()
        messagebox.askretrycancel()

    def set_init_window(self):
        self.init_window_name.title("CIXTool-version 1.0.0-10/18/2021")
        self.init_window_name.geometry("1024x800+10+10")
      
        self.init_window_name.attributes("-alpha",0.9)
        menubar = Menu(self.init_window_name)

        filemenu = Menu(menubar,tearoff=0)
        filemenu.add_command(label="New",command=self.donothing)
        filemenu.add_command(label="Open",command=self.donothing)
        filemenu.add_command(label="Save",command=self.donothing)
        filemenu.add_command(label="Save as...",command=self.donothing)
        filemenu.add_command(label="Load Configure",command=self.donothing)
        filemenu.add_command(label="Close",command=self.donothing)
        filemenu.add_separator()
        filemenu.add_command(label="Exit",command=self.init_window_name.quit)

        menubar.add_cascade(label="File",menu=filemenu)        
        editmenu = Menu(menubar,tearoff=0)        
        editmenu.add_command(label="Log CFG", command = self.log_man)
        editmenu.add_separator()
        editmenu.add_command(label="DBUS CFG", command = self.debug_bus)
        editmenu.add_separator()
        editmenu.add_command(label="SPI_RW", command = self.spi_frame)
        editmenu.add_separator()
        editmenu.add_command(label="HBM_RW", command = self.hbm_frame)
        menubar.add_cascade(label="Edit",menu=editmenu)
 
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Index",command=self.help_index)
        helpmenu.add_command(label="About...",command=self.help_about)
        menubar.add_cascade(label="Help",menu=helpmenu)

        self.init_window_name.config(menu=menubar)

        usage_label_frame = LabelFrame(self.init_window_name, text="CIXTool Usages",\
         labelanchor = N, relief=RAISED, width= 640, height= 480)
        usage_label_frame.pack(expand = 1, fill = BOTH, side = TOP)
        usage_text = Text(usage_label_frame,width = 80, height = 10)
        usage_text['font'] = self.myFont
        # usage_text['bg'] = "DeepSkyBlue"
        usage_text['bg'] = "Black"
        usage_text['fg'] = "White"
        usage_text.insert(1.0,
        "Here is a powerful tool's user manual in brielf!\n\n \
         Mainly 3 features:\n                       \
         System Logging\n                           \
         Design For Debug configure\n               \
         SPI Flash Read/Write\n                     \
         HBM Read/Write operations\n")
        usage_text.insert(END, "If any bug, pls report to xxxx")
        usage_text.pack(expand = 1, fill = BOTH, side= TOP)

        self.partition_lst = (
            "0  Reserved for future ",
            "1  wonderful models", 
            "2  wonderful models", 
            "3  wonderful models", 
            "4  wonderful models", 
            "5  wonderful models", 
            "6  wonderful models", 
            "7  wonderful models", 
            "8  wonderful models", 
            "9  wonderful models", 
            "10 wonderful models", 
            "11 wonderful models", 
            "12 wonderful models", 
            "13 wonderful models", 
            "14 wonderful models", 
            "15 wonderful models", 
            "16 wonderful models", 
            "17 wonderful models", 
            "18 wonderful models",  
            "19 wonderful models", 
            "20 wonderful models", 
            "21 wonderful models", 
            "22 wonderful models", 
            "23 wonderful models", 
            "24 wonderful models", 
            "25 wonderful models", 
            "26 wonderful models", 
            "27 wonderful models", 
            "28 wonderful models", 
            "29 wonderful models", 
            "30 wonderful models",
            "31 wonderful models",
            "32 wonderful models",
            "33 wonderful models",
            "34 wonderful models",
            "35 wonderful models",
            "36 wonderful models",
            "37 wonderful models",
            "38 wonderful models",
            "39 wonderful models",
            "40 wonderful models",
            "41 wonderful models",
            "42 wonderful models",
            "43 wonderful models",
            "44 wonderful models",
            "45 wonderful models",
            "46 wonderful models",
            "47 wonderful models",
            "48 wonderful models",
            "49 wonderful models",
            "50 wonderful models",
            "51 wonderful models",
            "52 wonderful models",
            "53 wonderful models",
            "54 wonderful models",
            "55 wonderful models",
            "56 wonderful models",
            "57 wonderful models",
            "58 wonderful models",
            "59 wonderful models",
            "60 wonderful models",
            "61 wonderful models",
            "62 wonderful models",
            "63 wonderful models",
            "64 wonderful models",
            "65 wonderful models",
            "66 wonderful models",
            "67 wonderful models",
            "68 wonderful models",
            "69 wonderful models",
            "70 wonderful models",
            "71 wonderful models",
            "72 wonderful models",
            "73 wonderful models",
            "74 wonderful models",
            "75 wonderful models",
            "76 wonderful models",
            "77 wonderful models",
            "78 wonderful models",
            "79 wonderful models",
            "80 wonderful models",
            "81 wonderful models",
            "82 wonderful models",
            "83 wonderful models",
            "84 wonderful models",
            "85 wonderful models",
            "86 wonderful models",
            "87 wonderful models",
            "88 wonderful models",
            "89 wonderful models",
            "90 wonderful models",
            "91 wonderful models",
            "92 wonderful models",
            "93 wonderful models",
            "94 wonderful models",
            "95 wonderful models",
            "96 wonderful models",
            "97 wonderful models",
            "98 wonderful models",
            "99 wonderful models",
            "100 wonderful models",
            "101 wonderful models",
            "102 wonderful models",
            "103 wonderful models",
            "104 wonderful models",
            "105 wonderful models",
            "106 wonderful models", 
            "107 wonderful models", 
            "108 wonderful models", 
            "109 wonderful models", 
            "110 wonderful models", 
            "111 wonderful models", 
            "112 wonderful models", 
            "113 wonderful models", 
            "114 wonderful models", 
            "115 wonderful models", 
            "116 wonderful models", 
            "117 wonderful models", 
            "118 wonderful models", 
            "119 wonderful models", 
            "120 wonderful models", 
            "121 wonderful models", 
            "122 wonderful models", 
            "123 wonderful models", 
            "124 wonderful models", 
            "125 wonderful models", 
            "126 wonderful models", 
            "127 wonderful models", 
            "128 wonderful models", 
            "129 wonderful models", 
            "130 wonderful models", 
            "131 wonderful models", 
            "132 wonderful models", 
            "133 wonderful models", 
            "134 wonderful models", 
            "135 wonderful models", 
            "136 wonderful models", 
            "137 wonderful models", 
            "138 wonderful models", 
            "139 wonderful models", 
            "140 wonderful models", 
            "141 wonderful models", 
            "142 wonderful models", 
            "143 wonderful models", 
            "144 wonderful models", 
            "145 wonderful models", 
            "146 wonderful models", 
            "147 wonderful models", 
            "148 wonderful models", 
            "149 wonderful models", 
            "150 wonderful models", 
            "151 wonderful models", 
            "152 wonderful models", 
            "153 wonderful models", 
            "154 wonderful models", 
            "155 wonderful models", 
            "156 wonderful models", 
            "157 wonderful models", 
            "158 wonderful models", 
            "159 wonderful models", 
            "160 wonderful models", 
            "161 wonderful models", 
            "162 wonderful models", 
            "163 wonderful models", 
            "164 wonderful models", 
            "165 wonderful models", 
            "166 wonderful models", 
            "167 wonderful models", 
            "168 wonderful models", 
            "169 wonderful models", 
            "170 wonderful models", 
            "171 wonderful models", 
            "172 wonderful models", 
            "173 wonderful models", 
            "174 wonderful models", 
            "175 wonderful models", 
            "176 wonderful models", 
            "177 wonderful models", 
            "178 wonderful models", 
            "179 wonderful models", 
            "180 wonderful models", 
            "181 wonderful models", 
            "182 wonderful models", 
            "183 wonderful models", 
            "184 wonderful models", 
            "185 wonderful models", 
            "186 wonderful models", 
            "187 wonderful models", 
            "188 wonderful models", 
            "189 wonderful models", 
            "190 wonderful models", 
            "191 wonderful models", 
            "192 wonderful models", 
            "193 wonderful models", 
            "194 wonderful models", 
            "195 wonderful models", 
            "196 wonderful models", 
            "197 wonderful models", 
            "198 wonderful models", 
            "199 wonderful models", 
            "200 wonderful models", 
            "201 wonderful models", 
            "202 wonderful models", 
            "203 wonderful models", 
            "204 wonderful models", 
            "205 wonderful models", 
            "206 wonderful models", 
            "207 wonderful models", 
            "208 wonderful models", 
            "209 wonderful models", 
            "210 wonderful models", 
            "211 wonderful models", 
            "212 wonderful models", 
            "213 wonderful models", 
            "214 wonderful models", 
            "215 wonderful models", 
            "216 wonderful models", 
            "217 wonderful models", 
            "218 wonderful models", 
            "219 wonderful models", 
            "220 wonderful models", 
            "221 wonderful models", 
            "222 wonderful models", 
            "223 wonderful models", 
            "224 wonderful models", 
            "225 wonderful models", 
            "226 wonderful models", 
            "227 wonderful models", 
            "228 wonderful models", 
            "229 wonderful models", 
            "230 wonderful models", 
            "231 wonderful models", 
            "232 wonderful models", 
            "233 wonderful models", 
            "234 wonderful models", 
            "235 wonderful models", 
            "236 wonderful models", 
            "237 wonderful models", 
            "238 wonderful models", 
            "239 wonderful models", 
            "240 wonderful models", 
            "241 wonderful models", 
            "242 wonderful models", 
            "243 wonderful models", 
            "244 wonderful models", 
            "245 wonderful models", 
            "246 wonderful models", 
            "247 wonderful models", 
            "248 wonderful models", 
            "249 wonderful models", 
            "250 wonderful models", 
            "251 wonderful models", 
            "252 wonderful models", 
            "253 wonderful models", 
            "254 wonderful models", 
            "255 wonderful models", 
            "256 wonderful models", 
            "257 wonderful models", 
            "258 wonderful models", 
            "259 wonderful models", 
            "260 wonderful models", 
            "261 wonderful models", 
            "262 wonderful models", 
            "263 wonderful models", 
            "264 wonderful models", 
            "265 wonderful models", 
            "266 wonderful models", 
            "267 wonderful models", 
            "268 wonderful models", 
            "269 wonderful models", 
            "270 wonderful models", 
            "271 wonderful models", 
            "272 wonderful models", 
            "273 wonderful models", 
            "274 wonderful models", 
            "275 wonderful models", 
            "276 wonderful models", 
            "277 wonderful models", 
            "278 wonderful models", 
            "279 wonderful models", 
            "280 wonderful models", 
            "281 wonderful models", 
            "282 wonderful models", 
            "283 wonderful models", 
            "284 wonderful models", 
            "285 wonderful models", 
            "286 wonderful models", 
            "287 wonderful models", 
            "288 wonderful models", 
            "289 wonderful models", 
            "290 wonderful models", 
            "291 wonderful models", 
            "292 wonderful models", 
            "293 wonderful models", 
            "294 wonderful models", 
            "295 wonderful models", 
            "296 wonderful models", 
            "297 wonderful models", 
            "298 wonderful models", 
            "299 wonderful models", 
            "300 wonderful models", 
            "301 wonderful models", 
            "302 wonderful models", 
            "303 wonderful models", 
            "304 wonderful models", 
            "305 wonderful models", 
            "306 wonderful models", 
            "307 wonderful models", 
            "308 wonderful models", 
            "309 wonderful models", 
            "310 wonderful models", 
            "311 wonderful models", 
            "312 wonderful models", 
            "313 wonderful models", 
            "314 wonderful models", 
            "315 wonderful models", 
            "316 wonderful models", 
            "317 wonderful models", 
            "318 wonderful models", 
            "319 wonderful models", 
            "320 wonderful models", 
            "321 wonderful models", 
            "322 wonderful models", 
            "323 wonderful models", 
            "324 wonderful models", 
            "325 wonderful models", 
            "326 wonderful models", 
            "327 wonderful models", 
            "328 wonderful models", 
            "329 wonderful models", 
            "330 wonderful models", 
            "331 wonderful models", 
            "332 wonderful models", 
            "333 wonderful models", 
            "334 wonderful models", 
            "335 wonderful models", 
            "336 wonderful models", 
            "337 wonderful models", 
            "338 wonderful models", 
            "339 wonderful models", 
            "340 wonderful models", 
            "341 wonderful models", 
            "342 wonderful models", 
            "343 wonderful models", 
            "344 wonderful models", 
            "345 wonderful models", 
            "346 wonderful models", 
            "347 wonderful models", 
            "348 wonderful models", 
            "349 wonderful models", 
            "350 wonderful models", 
            "351 wonderful models", 
            "352 wonderful models", 
            "353 wonderful models", 
            "354 wonderful models", 
            "355 wonderful models", 
            "356 wonderful models", 
            "357 wonderful models", 
            "358 wonderful models", 
            "359 wonderful models", 
            "360 wonderful models", 
            "361 wonderful models", 
            "362 wonderful models", 
            "363 wonderful models", 
            "364 wonderful models", 
            "365 wonderful models", 
            "366 wonderful models", 
            "367 wonderful models", 
            "368 wonderful models", 
            "369 wonderful models", 
            "370 wonderful models", 
            "371 wonderful models", 
            "372 wonderful models", 
            "373 wonderful models", 
            "374 wonderful models", 
            "375 wonderful models", 
            "376 wonderful models", 
            "377 wonderful models", 
            "378 wonderful models", 
            "379 wonderful models", 
            "380 wonderful models", 
            "381 wonderful models", 
            "382 wonderful models", 
            "383 wonderful models", 
            "384 wonderful models", 
            "385 wonderful models", 
            "386 wonderful models", 
            "387 wonderful models", 
            "388 wonderful models", 
            "389 wonderful models", 
            "390 wonderful models", 
            "391 wonderful models", 
            "392 wonderful models", 
            "393 wonderful models", 
            "394 wonderful models", 
            "395 wonderful models", 
            "396 wonderful models", 
            "397 wonderful models", 
            "398 wonderful models", 
            "399 wonderful models", 
            "400 wonderful models", 
            "401 wonderful models", 
            "402 wonderful models", 
            "403 wonderful models", 
            "404 wonderful models", 
            "405 wonderful models", 
            "406 wonderful models", 
            "407 wonderful models", 
            "408 wonderful models", 
            "409 wonderful models", 
            "410 wonderful models", 
            "411 wonderful models", 
            "412 wonderful models", 
            "413 wonderful models", 
            "414 wonderful models", 
            "415 wonderful models", 
            "416 wonderful models", 
            "417 wonderful models", 
            "418 wonderful models", 
            "419 wonderful models", 
            "420 wonderful models", 
            "421 wonderful models", 
            "422 wonderful models", 
            "423 wonderful models", 
            "424 wonderful models", 
            "425 wonderful models", 
            "426 wonderful models", 
            "427 wonderful models", 
            "428 wonderful models", 
            "429 wonderful models", 
            "430 wonderful models", 
            "431 wonderful models", 
            "432 wonderful models", 
            "433 wonderful models", 
            "434 wonderful models", 
            "435 wonderful models", 
            "436 wonderful models", 
            "437 wonderful models", 
            "438 wonderful models", 
            "439 wonderful models", 
            "440 wonderful models", 
            "441 wonderful models", 
            "442 wonderful models", 
            "443 wonderful models", 
            "444 wonderful models", 
            "445 wonderful models", 
            "446 wonderful models", 
            "447 wonderful models", 
            "448 wonderful models", 
            "449 wonderful models", 
            "450 wonderful models", 
            "451 wonderful models", 
            "452 wonderful models", 
            "453 wonderful models", 
            "454 wonderful models", 
            "455 wonderful models", 
            "456 wonderful models", 
            "457 wonderful models", 
            "458 wonderful models", 
            "459 wonderful models", 
            "460 wonderful models", 
            "461 wonderful models", 
            "462 wonderful models", 
            "463 wonderful models", 
            "464 wonderful models", 
            "465 wonderful models", 
            "466 wonderful models", 
            "467 wonderful models", 
            "468 wonderful models", 
            "469 wonderful models", 
            "470 wonderful models", 
            "471 wonderful models", 
            "472 wonderful models", 
            "473 wonderful models", 
            "474 wonderful models", 
            "475 wonderful models", 
            "476 wonderful models", 
            "477 wonderful models", 
            "478 wonderful models", 
            "479 wonderful models", 
            "480 wonderful models", 
            "481 wonderful models", 
            "482 wonderful models", 
            "483 wonderful models", 
            "484 wonderful models", 
            "485 wonderful models", 
            "486 wonderful models", 
            "487 wonderful models", 
            "488 wonderful models", 
            "489 wonderful models", 
            "490 wonderful models", 
            "491 wonderful models", 
            "492 wonderful models", 
            "493 wonderful models", 
            "494 wonderful models", 
            "495 wonderful models", 
            "496 wonderful models", 
            "497 wonderful models", 
            "498 wonderful models", 
            "499 wonderful models", 
            "500 wonderful models", 
            "501 wonderful models", 
            "502 wonderful models", 
            "503 wonderful models", 
            "504 wonderful models", 
            "505 wonderful models", 
            "506 wonderful models", 
            "507 wonderful models", 
            "508 wonderful models", 
            "509 wonderful models", 
            "510 wonderful models", 
            "511 wonderful models", 
            "512 wonderful models", 
            "513 wonderful models", 
            "514 wonderful models", 
            "515 wonderful models", 
            "516 wonderful models", 
            "517 wonderful models", 
            "518 wonderful models", 
            "519 wonderful models", 
            "520 wonderful models", 
            "521 wonderful models", 
            "522 wonderful models", 
            "523 wonderful models", 
            "524 wonderful models", 
            "525 wonderful models", 
            "526 wonderful models", 
            "527 wonderful models", 
            "528 wonderful models", 
            "529 wonderful models", 
            "530 wonderful models") 
            
        self.action_lst = (
            "0x0   GenCntTogInc[0]",
            "0x1   GenCntTogInc[1]",
            "0x2   GenCnt[0] Reset",
            "0x3   GenCnt[1] Reset",
            "0x4   ClkCntReset",
            "0x5   StopClk",
            "0x6   TraceStoreCurrent",
            "0x7   TraceStoreStart",
            "0x8   TraceStoreStop",
            "0x9   TimeStore",
            "0xA   ClrTraceIndex",
            "0xB   Goto TrigObs1",
            "0xC   Goto TrigObs3",
            "0xD   Snapshot GenCnt0&GenCnt1",
            "0xE   PPUGDBBreakInReq (TBD)"
        )

        self.permutation_lst = (
           "0x80    ABC       ",
           "0xC0    BC        ",
           "0xA0    AC        ",
           "0x88    AB        ",
           "0xAA    A         ",
           "0xCC    B         ",
           "0xF0    C         ",
           "0xEE    A|B       ",
           "0xFC    B|C       ",
           "0xFA    A|C       ",
           "0x66    A XOR B   ",
           "0x5A    A XOR C   ",
           "0x3C    B XOR C   ",
           "0x72    A~B|~AC   ",
           "0x52    A~BC|~AC  ",
           "0x2E    A~B|B~C   ",
           "0x3A    A~C|~BC   "
        )

        self.maintrig_lst = (
            "0x00    TrigGenCnt[0]",
            "0x01    TrigGenCnt[1]",
            "0x02    TrigEqCnt10",
            "0x03    TrigClkCnt",
            "0x04    TRUE",
            "0x05    TrigDBUS[0]",
            "0x06    TrigDBUS[1]",
            "0x07    TrigDBUS[2]",
            "0x08    TrigDBUS[3]",
            "0x09    TrigDBUS[4]",
            "0x0A    TrigDBUS[5]",
            "0x0B    TrigDBUS[6]",
            "0x0C    TrigDBUS[7]",
            "0x0D    TrigDBUS[8]",
            "0x0E    TrigDBUS[9]",
            "0x0F    TrigDBUS[10]",
            "0x10    TrigDBUS[11]",
            "0x11    DbgWrEn",
            "0x12    TrigPerfMon[0]",
            "0x13    TrigPerfMon[1]",
            "0x14    DrbFullTrig",
            "0x15    DebugBusValid"
        )

        self.dbustrig_lst = (
            "0x00    Change",	        
            "0x01    CmprTrigEq0L",	
            "0x02    CmprTrigEq0U",	
            "0x03    CmprTrigEq0",	    
            "0x04    CmprTrigGt0",	    
            "0x05    CmprTrigEq1L",	
            "0x06    CmprTrigEq1U",	
            "0x07    CmprTrigEq1",	    
            "0x08    CmprTrigGt1",	    
            "0x09    BusBitTrig0",	    
            "0x0A    BusBitTrig1",	    
            "0x0B    BusBitTrig2",	    
            "0x0C    BusBitTrig3"  
        )

        self.dbus_bitTrig_mode = (
            "0x0   Level",
            "0x1   AnyEdge",
            "0x2   PosEdge",
            "0x3   NegEdge"
        )