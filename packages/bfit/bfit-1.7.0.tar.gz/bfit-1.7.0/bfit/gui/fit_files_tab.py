# fit_files tab for bfit
# Derek Fujimoto
# Dec 2017

from tkinter import *
from tkinter import ttk, messagebox, filedialog
from functools import partial
from bfit.gui.zahersCalculator import current2field
from bfit.gui.show_param_popup import show_param_popup
from bdata import bdata
from bfit import logger_name

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import datetime, os, traceback
import logging


# =========================================================================== #
# =========================================================================== #
class fit_files(object):
    """
        Data fields:
            annotation:     stringvar: name of quantity for annotating parameters 
            chi_threshold:  if chi > thres, set color to red
            draw_components:list of titles for labels, options to export, draw.
            file_tabs:      fitinputtab object
            fitter:         fitting object from self.bfit.routine_mod
            fit_function_title: title of fit function to use
            fit_function_title_box: spinbox for fit function names
            fit_input:      fitting input values = (fn_name,ncomp,data_list)
            mode:           what type of run is this. 
            n_component:    number of fitting components (IntVar)
            runframe:       frame for displaying fit results and inputs
            runmode_label:  display run mode 
            set_as_group:   BooleanVar() if true, set fit parfor whole group
            xaxis:          StringVar() for parameter to draw on x axis
            yaxis:          StringVar() for parameter to draw on y axis
            xaxis_combobox: box for choosing x axis draw parameter
            yaxis_combobox: box for choosing y axis draw parameter
    """ 
    
    default_fit_functions = {'20':('Exp','Str Exp'),'2h':('Exp','Str Exp'),
            '1f':('Lorentzian','Gaussian'),'1n':('Lorentzian','Gaussian')}
    mode = ""
    chi_threshold = 1.5 # threshold for red highlight on bad fits 
    n_fitx_pts = 500    # number of points to draw in fitted curves
    
    # ======================================================================= #
    def __init__(self,fit_data_tab,bfit):
        
        # get logger
        self.logger = logging.getLogger(logger_name)
        self.logger.debug('Initializing')
        
        # initialize
        self.file_tabs = None
        self.bfit = bfit
        self.fit_output = {}
        self.fitter = self.bfit.routine_mod.fitter()
        self.draw_components = bfit.draw_components
            
        # make top level frames
        mid_fit_frame = ttk.Frame(fit_data_tab,pad=5)   # notebook
        right_frame = ttk.Labelframe(fit_data_tab,
            text='Fit Results and Run Conditions',pad=5)     # draw fit results
        
        mid_fit_frame.grid(column=0,row=1,sticky=(N,W,E))
        right_frame.grid(column=1,row=1,columnspan=2,rowspan=2,sticky=(N,E,W))
        
        fit_data_tab.grid_columnconfigure(0,weight=1)   # fitting space
        fit_data_tab.grid_columnconfigure(1,weight=10)  # par select space
        
        # TOP FRAME 
        
        # fit function select 
        fn_select_frame_border = ttk.Labelframe(fit_data_tab,text='Fit Function')
        fn_select_frame = ttk.Frame(fn_select_frame_border)
        self.fit_function_title = StringVar()
        self.fit_function_title.set("")
        self.fit_function_title_box = ttk.Combobox(fn_select_frame, 
                textvariable=self.fit_function_title,state='readonly')
        self.fit_function_title.trace('w', self.populate_param)
        
        # number of components in fit spinbox
        self.n_component = IntVar()
        self.n_component.set(1)
        n_component_box = Spinbox(fn_select_frame,from_=1,to=20, 
                textvariable=self.n_component,width=5,command=self.populate_param)
        
        # fit and residual button
        fit_button = ttk.Button(fn_select_frame,text='Fit',command=self.do_fit,\
                                pad=1)
        residual_button = ttk.Button(fn_select_frame,text=' Draw Residual ',
                        command=self.do_draw_residual,pad=1)
                                
        # set as group checkbox
        self.set_as_group = BooleanVar()
        set_group_check = ttk.Checkbutton(fn_select_frame,
                text='Set Parameters for Group',\
                variable=self.set_as_group,onvalue=True,offvalue=False)
        self.set_as_group.set(True)
        
        # run mode 
        fit_runmode_label_frame = ttk.Labelframe(fit_data_tab,pad=(10,5,10,5),
                text='Run Mode',)
        self.fit_runmode_label = ttk.Label(fit_runmode_label_frame,text="",
                font='bold',justify=CENTER)
        
        # fitting routine
        fit_routine_label_frame = ttk.Labelframe(fit_data_tab,pad=(10,5,10,5),
                text='Fitting Routine',)
        self.fit_routine_label = ttk.Label(fit_routine_label_frame,text="",
                font='bold',justify=CENTER)
                
        # GRIDDING
            
        # top frame gridding
        fn_select_frame_border.grid(column=0,row=0,sticky=(W,E))
        fn_select_frame.grid(column=0,row=0,sticky=(W))
        
        c = 0
        self.fit_function_title_box.grid(column=c,row=0); c+=1
        ttk.Label(fn_select_frame,text="Number of Components:").grid(column=c,
                row=0,sticky=(E),padx=5,pady=5); c+=1
        n_component_box.grid(column=c,row=0,padx=5,pady=5); c+=1
        fit_button.grid(column=c,row=0,padx=1,pady=1); c+=1
        residual_button.grid(column=c,row=0,padx=1,pady=1); c+=1
        set_group_check.grid(column=c,row=0,padx=1,pady=1); c+=1
        
        # run mode gridding
        fit_runmode_label_frame.grid(column=1,row=0,sticky=(E,W))
        self.fit_runmode_label.grid(column=0,row=0,sticky=(E,W))
        
        # routine label gridding
        fit_routine_label_frame.grid(column=2,row=0,sticky=(E,W))
        self.fit_routine_label.grid(column=0,row=0,sticky=(E,W))
        
        # MID FRAME        
        self.runframe = ttk.Labelframe(mid_fit_frame,
                    text='Set Initial Parameters',pad=5) 
        self.runframe.grid(column=0,row=0,sticky=(N,E,W))
        
        # RIGHT FRAME
        
        # draw and export buttons
        button_frame = ttk.Frame(right_frame)
        draw_button = ttk.Button(button_frame,text='Draw',command=self.draw_param)
        export_button = ttk.Button(button_frame,text='Export',command=self.export)
        show_button = ttk.Button(button_frame,text='Show All',command=self.show_all_results)
        
        # menus for x and y values
        ttk.Label(right_frame,text="x axis:").grid(column=0,row=1)
        ttk.Label(right_frame,text="y axis:").grid(column=0,row=2)
        ttk.Label(right_frame,text="Annotation:").grid(column=0,row=3)
        
        self.xaxis = StringVar()
        self.yaxis = StringVar()
        self.annotation = StringVar()
        
        self.xaxis.set('')
        self.yaxis.set('')
        self.annotation.set('')
        
        self.xaxis_combobox = ttk.Combobox(right_frame,textvariable=self.xaxis,
                                      state='readonly',width=15)
        self.yaxis_combobox = ttk.Combobox(right_frame,textvariable=self.yaxis,
                                      state='readonly',width=15)
        self.annotation_combobox = ttk.Combobox(right_frame,
                                      textvariable=self.annotation,
                                      state='readonly',width=15)
        
        # gridding
        button_frame.grid(column=0,row=0,columnspan=2)
        draw_button.grid(column=0,row=0,padx=5,pady=5)
        export_button.grid(column=1,row=0,padx=5,pady=5)
        show_button.grid(column=2,row=0,padx=5,pady=5)
        
        self.xaxis_combobox.grid(column=1,row=1,pady=5)
        self.yaxis_combobox.grid(column=1,row=2,pady=5)
        self.annotation_combobox.grid(column=1,row=3,pady=5)
        
        # resizing
        
        # fn select
        fn_select_frame_border.grid_columnconfigure(0,weight=1)
        fn_select_frame.grid_columnconfigure(1,weight=1)
        
        # fitting frame
        fit_data_tab.grid_rowconfigure(1,weight=1)  #fitting area
        mid_fit_frame.grid_columnconfigure(0,weight=1)
        mid_fit_frame.grid_rowconfigure(0,weight=1)
        
        # right frame
        for i in range(2):
            right_frame.grid_columnconfigure(i,weight=1)
        
    # ======================================================================= #
    def populate(self,*args):
        """
            Make tabs for setting fit input parameters. 
        """
        
        # get data
        dl = self.bfit.fetch_files.data_lines
        self.logger.debug('Populating data.')
        
        # get run mode by looking at one of the data dictionary keys
        for key_zero in self.bfit.data.keys(): break
            
        # delete everything in the initial parameters frame 
        for child in self.runframe.winfo_children():
            child.destroy()
        
        # create fit function combobox options
        try:               
            if self.mode != self.bfit.data[key_zero].mode:
                
                # set run mode 
                self.mode = self.bfit.data[key_zero].mode 
                self.fit_runmode_label['text'] = \
                        self.bfit.fetch_files.runmode_relabel[self.mode]
                
                # set routine
                self.fit_routine_label['text'] = self.fitter.__name__
                
                # set run functions        
                fn_titles = self.fitter.function_names[self.mode]
                self.fit_function_title_box['values'] = fn_titles
                if self.fit_function_title.get() == '':
                    self.fit_function_title.set(fn_titles[0])
                    
        except UnboundLocalError:
            self.fit_function_title_box['values'] = ()
            self.fit_function_title.set("")
            self.fit_runmode_label['text'] = ""
            self.mode = ""
                    
        # make fitinputtab objects
        self.file_tabs = fitinputtab(self.bfit,self.runframe)
        self.file_tabs.create()
        
        # populate the list of parameters 
        self.file_tabs.populate_param()
        self.populate_param()        
   
    # ======================================================================= #
    def populate_param(self,*args):
        """Populate the list of parameters"""
        
        self.logger.debug('Populating fit parameters')
        
        # populate axis comboboxes
        lst = self.draw_components.copy()
        lst.sort()
        
        try:
            parlst = [p for p in self.fitter.gen_param_names(
                                                self.fit_function_title.get(),
                                                self.n_component.get())]
        except KeyError:
            self.xaxis_combobox['values'] = []
            self.yaxis_combobox['values'] = []
            self.annotation_combobox['values'] = []
            return
            
        parlst.sort()
        
        self.xaxis_combobox['values'] = ['']+parlst+lst
        self.yaxis_combobox['values'] = ['']+parlst+lst
        self.annotation_combobox['values'] = ['']+parlst+lst
            
    # ======================================================================= #
    def do_fit(self,*args):
                
        # fitter
        fitter = self.fitter
        
        # get fitter inputs
        fn_name = self.fit_function_title.get()
        ncomp = self.n_component.get()
        
        self.logger.info('Fitting with "%s" with %d components',fn_name,ncomp)
        
        # build data list
        data_list = []
        tab = self.file_tabs
        collist = tab.collist
        runlist = tab.runlist
        
        self.logger.debug('Contains runs %s',runlist)
                
        for r in runlist:
            
            # bdata object
            bdfit = self.bfit.data[r]
            bdataobj = bdfit.bd
            
            # pdict
            pdict = {}
            for parname in tab.parentry.keys():
                
                # get entry values
                pline = tab.parentry[parname]
                line = []
                for col in collist:
                    
                    # get number entries
                    if col in ['p0','blo','bhi']:
                        try:
                            line.append(float(pline[col][0].get()))
                        except ValueError as errmsg:
                            self.logger.exception("Bad input.")
                            messagebox.showerror("Error",str(errmsg))
                    
                    # get "Fixed" entry
                    elif col in ['fixed']:
                        line.append(pline[col][0].get())
                
                    # get "Shared" entry
                    elif col in ['shared']:
                        line.append(pline[col][0].get())
                
                # make dict
                pdict[parname] = line
                
            # doptions
            doptions = {}
            doptions['rebin'] = bdfit.rebin.get()
            
            if self.mode == '1f':
                dline = self.bfit.fetch_files.data_lines[r]
                doptions['omit'] = dline.bin_remove.get()
                if doptions['omit'] == dline.bin_remove_starter_line: 
                    doptions['omit'] = ''
                
            elif self.mode == '20':
                pass
                
            elif self.mode == '2h':
                pass
                
            elif self.mode == '2e':
                self.logger.error('2e fitting not implemented')
                raise RuntimeError('2e fitting not implemented')
            
            else:
                self.logger.error('Fitting mode not recognized')
                raise RuntimeError('Fitting mode not recognized')
            
            # make data list
            data_list.append([bdataobj,pdict,doptions])
        
        # call fitter with error message, potentially
        self.fit_input = (fn_name,ncomp,data_list)
        
        # make fitting status window
        fit_status_window = Toplevel(self.bfit.root)
        fit_status_window.lift()
        fit_status_window.resizable(FALSE,FALSE)
        ttk.Label(fit_status_window,text="Please Wait",pad=20).grid(column=0,
                                                    row=0,sticky=(N,S,E,W))
        fit_status_window.update_idletasks()
        self.bfit.root.update_idletasks()
        
        width = fit_status_window.winfo_reqwidth()
        height = fit_status_window.winfo_reqheight()
        
        rt_x = self.bfit.root.winfo_x()
        rt_y = self.bfit.root.winfo_y()
        rt_w = self.bfit.root.winfo_width()
        rt_h = self.bfit.root.winfo_height()
        
        x = rt_x + rt_w/2 - (width/2)
        y = rt_y + rt_h/3 - (width/2)
        
        fit_status_window.geometry('{}x{}+{}+{}'.format(width, height, int(x), int(y)))
        fit_status_window.update_idletasks()
        
        # do fit then kill window
        for d in data_list:
            self.logger.info('Fitting run %d (%d): %s',d[0].run,d[0].year,d[1:])
            
        try:
            # fit_output keyed as {run:[key/par/cov/chi/fnpointer]}
            fit_output = fitter(fn_name=fn_name,ncomp=ncomp,
                                     data_list=data_list,
                                     hist_select=self.bfit.hist_select)
        except Exception as errmsg:
            self.logger.exception('Fitting error')
            fit_status_window.destroy()
            messagebox.showerror("Error",str(errmsg))
            raise errmsg
        else:
            fit_status_window.destroy()
        
        # set output results
        for run in fit_output.keys():
            self.bfit.data[run].set_fitresult(fit_output[run])
            
        # display run results
        self.file_tabs.set_display()
        self.file_tabs.set_run_color()
        
        # enable draw buttons on fetch files tab
        for r in runlist:
            dline = self.bfit.fetch_files.data_lines[r]
            
            dline.draw_fit_checkbox['state'] = 'normal'
            dline.draw_res_checkbox['state'] = 'normal'
            dline.check_fit.set(True)
        
        # draw fit results
        self.bfit.fetch_files.draw_all(ignore_check=False)
        style = self.bfit.draw_style.get()
        
        if style in ['redraw','new']:
            self.bfit.draw_style.set('stack')
        
        self.bfit.draw_style.set(style)
            
    # ======================================================================= #
    def do_draw_residual(self,*args):
        """Draw the residual of the actively selected run."""
        
        # get fitinputtab
        tab = self.file_tabs
        
        # get run number
        run = int(tab.runbox.get(tab.selected))
        rebin = self.bfit.fetch_files.data_lines[run].rebin.get()
        
        # draw
        self.draw_residual(run=run,rebin=rebin)
    
    # ======================================================================= #
    def do_scrollbar(self,event):
        """Change selection based on scrolling"""
        runbox = self.file_tabs.runbox
        
        cur = runbox.index(ACTIVE)
        runbox.selection_clear(cur)
        
        # move selection
        if event.num == 4:
            cur -= 1
        elif event.num == 5:
            cur += 1
    
        # check bounds
        if cur < 0:     cur = 0
        else:           cur = min(cur,runbox.size()-1)
        
        # set selection 
        runbox.select_set(cur)
        runbox.activate(cur)
        runbox.see(cur)
        runbox.event_generate("<<ListboxSelect>>")

    # ======================================================================= #
    def draw_residual(self,run,rebin=1,**drawargs):
        """Draw fitting residuals for a single run"""
        
        self.logger.info('Drawing residual for run %d, rebin %d, '+\
                         'standardized: %s, %s',run,rebin,
                         self.bfit.draw_standardized_res.get(),drawargs)
        
        # Settings
        xlabel_dict={'20':"Time (s)",
                     '2h':"Time (s)",
                     '2e':'Frequency (MHz)',
                     '1f':'Frequency (MHz)',
                     '1n':'Voltage (V)'}
        
        # get draw setting 
        draw_style = self.bfit.draw_style
        plt.ion()
        
        # get data and fit results
        data = self.bfit.data[run]
        fit_par = [data.fitpar['res'][p] for p in data.parnames]
        fn = data.fitfn
        data = data.bd
        
        # default label value
        if 'label' not in drawargs.keys():
            label = str(data.run)
        else:
            label = drawargs.pop('label',None)
            
        # set drawing style arguments
        for k in self.bfit.style:
            if k not in drawargs.keys():
                drawargs[k] = self.bfit.style[k]
        
        # make new window
        if draw_style.get() == 'new':
            plt.figure()
            ax = plt.gca()
            
        # get index of label in run and delete that run
        elif draw_style.get() == 'stack':
            ax = plt.gca()
            try:
                idx = [ell.get_label() for ell in ax.containers].index(label)
            except ValueError as err:
                pass
            else:
                del ax.lines[idx]              # clear lines 
                del ax.collections[idx]        # clear errorbar object 
                del ax.containers[idx]         # clear errorbar object
        
        # delete all runs
        elif draw_style.get() == 'redraw':
            ax = plt.gca()
            del ax.lines[:]              # clear lines 
            del ax.collections[:]        # clear errorbar object 
            del ax.containers[:]         # clear errorbar object
            
        ax.get_xaxis().get_major_formatter().set_useOffset(False)
        
        # get draw style
        style = self.bfit.draw_style.get()

        # get residuals
        x,a,da = data.asym('c',rebin=rebin)
        res = a - fn(x,*fit_par)
            
        # set x axis
        if   data.mode == '1f': x *= self.bfit.freq_unit_conv
        elif data.mode == '1n': x *= self.bfit.volt_unit_conv    

        # draw 
        if self.bfit.draw_standardized_res.get():
            plt.errorbar(x,res/da,np.zeros(len(x)),label=label,**drawargs)
            
            # draw fill
            ax = plt.gca()
            lim = ax.get_xlim()
            for i in range(1,4):
                ax.fill_between(lim,-1*i,i,color='k',alpha=0.1)
            plt.xlim(lim)
            plt.ylabel(r'Standardized Residual ($\sigma$)')
        else:
            plt.errorbar(x,res,da,label=label,**drawargs)
            plt.ylabel('Residual')
        
        # draw pulse marker
        if '2' in data.mode: plt.axvline(data.get_pulse_s(),ls='--',color='k')
            
        
        # plot elementsplt.ylabel('Residual')
        plt.xlabel(xlabel_dict[self.mode])
        plt.axhline(0,color='k',linestyle='-',zorder=20)
        
        # show
        plt.tight_layout()
        plt.legend()
        
    # ======================================================================= #
    def draw_fit(self,run,**drawargs):
        """Draw fit for a single run"""
        
        self.logger.info('Drawing fit for run %d. %s',run,drawargs)
        
        # Settings
        xlabel_dict={'20':"Time (s)",
                     '2h':"Time (s)",
                     '2e':'Frequency (MHz)',
                     '1f':'Frequency (MHz)',
                     '1n':'Voltage (V)'}
                     
        # get data and fit results
        data = self.bfit.data[run]
        fit_par = [data.fitpar['res'][p] for p in data.parnames]
        fn = data.fitfn
        data = data.bd
        
        # get draw style
        style = self.bfit.draw_style.get()
        
        # label reset
        if 'label' not in drawargs.keys():
            drawargs['label'] = self.bfit.data[run].label.get()
        drawargs['label'] += ' (fit)'
        label = drawargs['label']
        
        # set drawing style
        if style == 'new':
            plt.figure()
        if style == 'stack':
            
            ax = plt.gca()
            try:
                idx = [ell.get_label() for ell in ax.lines].index(label)
            except ValueError as err:
                pass
            else:
                del ax.lines[idx]              # clear lines 
                
        elif style == 'redraw':
            ylim = ax.get_ylim()
            xlim = ax.get_xlim()
            plt.clf()
            plt.ylim(*ylim)
            plt.xlim(*xlim)
            
        # set drawing style arguments
        for k in self.bfit.style:
            if k not in drawargs.keys() \
                    and 'marker' not in k \
                    and k not in ['elinewidth','capsize']:
                drawargs[k] = self.bfit.style[k]
        
        # linestyle reset
        if drawargs['linestyle'] == 'None': 
            drawargs['linestyle'] = '-'
        
        # draw
        t,a,da = data.asym('c')
        fitx = np.arange(self.n_fitx_pts)/float(self.n_fitx_pts)*\
                                                    (max(t)-min(t))+min(t)
        
        if   data.mode == '1f': fitxx = fitx*self.bfit.freq_unit_conv
        elif data.mode == '1n': fitxx = fitx*self.bfit.volt_unit_conv
        else:                   fitxx = fitx
    
        plt.plot(fitxx,fn(fitx,*fit_par),zorder=10,**drawargs)
        
        # plot elements
        plt.ylabel('Asymmetry')
        plt.xlabel(xlabel_dict[self.mode])
        
        # show
        plt.tight_layout()
        plt.legend()
        
    # ======================================================================= #
    def draw_param(self,*args):
        
        # make sure plot shows
        plt.ion()
        
        # get draw components
        xdraw = self.xaxis.get()
        ydraw = self.yaxis.get()
        ann = self.annotation.get()
        
        self.logger.info('Draw fit paramters "%s" vs "%s" with annotation "%s"',
                          ydraw,xdraw,ann)
        
        # get plottable data
        try:
            xvals, xerrs = self.get_values(xdraw)
            yvals, yerrs = self.get_values(ydraw)
        except UnboundLocalError as err:
            self.logger.error('Bad input parameter selection')
            messagebox.showerror("Error",'Select two input parameters')
            raise err
        except (KeyError,AttributeError) as err:
            self.logger.error('Parameter "%s or "%s" not found for drawing',
                              xdraw,ydraw)
            messagebox.showerror("Error",
                    'Drawing parameter "%s" or "%s" not found' % (xdraw,ydraw))
            raise err
            
        # get annotation
        if ann != '':
            try:
                ann, _ = self.get_values(ann)
            except UnboundLocalError:
                ann = None
            except (KeyError,AttributeError) as err:
                self.logger.error('Bad input annotation value "%s"',ann)
                messagebox.showerror("Error",
                        'Annotation "%s" not found' % (ann))
                raise err
        
        # fix annotation values (blank to none)
        else:
            ann = None
        
        # fix annotation values (round floats)
        if ann is not None: 
            number_string = '%.'+'%df' % self.bfit.rounding
            for i,a in enumerate(ann):
                if type(a) in [float,np.float64]:
                    ann[i] = number_string % np.around(a,self.bfit.rounding)
            
        # get draw style
        style = self.bfit.draw_style.get()
        
        if style == 'new':
            plt.figure()
        elif style == 'redraw':
            plt.clf()
        plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
        plt.gca().get_yaxis().get_major_formatter().set_useOffset(False)
        
        # draw
        if type(xvals[0]) == str:
            plt.xticks(np.arange(len(xvals)))
            plt.gca().set_xticklabels(xvals)
            xvals = np.arange(len(xvals))
        
        if type(yvals[0]) == str:
            plt.yticks(np.arange(len(yvals)))
            plt.gca().set_yticklabels(yvals)
            yvals = np.arange(len(yvals))
        
        f = plt.errorbar(xvals,yvals,xerr=xerrs,yerr=yerrs,fmt='.')
        self._annotate(xvals,yvals,ann,color=f[0].get_color())
        
        # plot elements
        plt.xlabel(xdraw)
        plt.ylabel(ydraw)
        plt.tight_layout()
        
    # ======================================================================= #
    def export(self,savetofile=True):
        
        # get values and errors
        val = {}
        
        for v in self.xaxis_combobox['values']:
            if v == '': continue
            
            try:
                v2 = self.get_values(v) 
            except Exception: 
                traceback.print_exc()
            else:
                val[v] = v2[0]
                val['Error '+v] = v2[1]
        
        # make data frame for output
        df = pd.DataFrame(val)
        df.set_index('Run Number',inplace=True)
        
        # drop completely empty columns
        bad_cols = [c for c in df.columns if all(df[c].isna())]
        for c in bad_cols:
            df.drop(c,axis='columns',inplace=True)
        
        if savetofile:
            
            # get file name
            filename = filedialog.asksaveasfilename()
            self.logger.info('Exporting parameters to "%s"',filename)
            
            # check extension 
            if os.path.splitext(filename)[1] == '':
                filename += '.csv'
            df.to_csv(filename)
            self.logger.debug('Export success')
        else:
            self.logger.info('Returned exported parameters')
            return df
        
    # ======================================================================= #
    def show_all_results(self):
        """Make a window to display table of fit results"""
        
        # get fit results
        df = self.export(savetofile=False)
        show_param_popup(df)
        
    # ======================================================================= #
    def get_values(self,select):
        """ Get plottable values"""
        data = self.bfit.data
        runs = list(data.keys())
        runs.sort()
    
        self.logger.debug('Fetching parameter %s',select)
    
        # Data file options
        if select == 'Temperature (K)':
            val = [data[r].temperature.mean for r in runs]
            err = [data[r].temperature.std for r in runs]
        
        elif select == 'B0 Field (T)':
            val = [data[r].field for r in runs]
            err = [data[r].field_std for r in runs]
        
        elif select == 'RF Level DAC':
            try:
                val = [data[r].camp.rf_dac.mean for r in runs]
                err = [data[r].camp.rf_dac.std for r in runs]
            except AttributeError:
                pass
        
        elif select == 'Platform Bias (kV)':
            try:
                val = [data[r].bias for r in runs]
                err = [data[r].bias_std for r in runs]
            except AttributeError:
                pass
                
        elif select == 'Impl. Energy (keV)':
            val =  [data[r].bd.beam_kev() for r in runs]
            err =  [data[r].bd.beam_kev(get_error=True) for r in runs]
        
        elif select == 'Run Duration (s)':
            val = [data[r].bd.duration for r in runs]
            err = [np.nan for r in runs]
        
        elif select == 'Run Number':
            val = [data[r].run for r in runs]
            err = [np.nan for r in runs]
        
        elif select == 'Sample':
            val = [data[r].bd.sample for r in runs]
            err = [np.nan for r in runs]
            
        elif select == 'Start Time':
            val = [data[r].bd.start_date for r in runs]
            err = [np.nan for r in runs]
        
        elif select == 'Title':
            val = [data[r].bd.title for r in runs]
            err = [np.nan for r in runs]
        
        # fitted parameter options
        elif select in self.fitter.gen_param_names(self.fit_function_title.get(),
                                                   self.n_component.get()):
            val = []
            err = []
            
            for r in runs:
                try:
                    val.append(self.bfit.data[r].fitpar['res'][select])
                    err.append(self.bfit.data[r].fitpar['dres'][select])
                except KeyError:
                    val.append(np.nan)
                    err.append(np.nan)
    
        try:
            return (val,err)
        except UnboundLocalError:
            self.logger.warning('Parameter selection "%s" not found' % select)
            raise AttributeError('Selection "%s" not found' % select)
        
    # =========================================================================== #
    def _annotate(self,x,y,ptlabels,color='k'):
        """Add annotation"""
        
        # base case
        if ptlabels is None: return
        
        # do annotation
        for label,xcoord,ycoord in zip(ptlabels,x,y):        
            if type(label) != type(None):
                plt.annotate(label,
                             xy=(xcoord,ycoord),
                             xytext=(-3, 20),
                             textcoords='offset points', 
                             ha='right', 
                             va='bottom',
                             bbox=dict(boxstyle='round,pad=0.1',
                                       fc=color, 
                                       alpha=0.1),
                             arrowprops=dict(arrowstyle = '->', 
                                             connectionstyle='arc3,rad=0'),
                            fontsize='xx-small',
                            )    
                            
# =========================================================================== #
# =========================================================================== #
class fitinputtab(object):
    """
        Instance variables 
        
            bfit        pointer to top class
            data        pointer to bfit.data
            parent      pointer to parent object (frame)
            parlabels   label objects, saved for later destruction
            parentry    [parname][colname] of ttk.Entry objects saved for 
                            retrieval and destruction
            runbox      listbox with run numbers: select which result to display
            run_label   label for showing which run is selected
            runlist     list of run numbers to fit
            selected    index of selected run in runbox (int)
            fitframe    mainframe for this tab. 
    """
    
    n_runs_max = 5      # number of runs before scrollbar appears
    collist = ['p0','blo','bhi','res','dres','chi','fixed','shared']
    selected = 0        # index of selected run 
    
    # ======================================================================= #
    def __init__(self,bfit,parent):
        """
            Inputs:
                bfit: top level pointer
                parent      pointer to parent object (frame)
        """
        
        # get logger
        self.logger = logging.getLogger(logger_name)
        self.logger.debug('Initalizing fit tab')
        
        # initialize
        self.bfit = bfit
        self.parent = parent
        self.parlabels = []
        self.parentry = {}
        
    # ======================================================================= #
    def create(self):
        """Create graphics for this object"""
        
        self.logger.debug('Creating graphics for fit input')
        
        fitframe = self.parent
        
        # get list of runs
        dl = self.bfit.fetch_files.data_lines
        self.runlist = [dl[k].run for k in dl.keys() 
                if dl[k].check_state.get()]
        
        # Display run info label 
        ttk.Label(fitframe,text="Run Numbers").grid(column=0,row=1,padx=5)

        # List box for run viewing
        rlist = StringVar(value=tuple(map(str,self.runlist)))
        self.runbox = Listbox(fitframe,height=min(len(self.runlist),self.n_runs_max),
                                width=10,listvariable=rlist,justify=CENTER,
                                selectmode=BROWSE)
        self.runbox.activate(0)
        self.runbox.bind('<<ListboxSelect>>',self.set_display)
        self.runbox.grid(column=0,row=2,rowspan=self.n_runs_max)
        
        sbar = ttk.Scrollbar(fitframe,orient=VERTICAL,command=self.runbox.yview)
        self.runbox.configure(yscrollcommand=sbar.set)
        sbar.grid(column=1,row=2,sticky=(N,S),rowspan=self.n_runs_max)
        
        # label for displyaing run number
        self.run_label = ttk.Label(fitframe,text='',font='bold')
        
        # Parameter input labels
        c = 2
        ttk.Label(fitframe,text='Parameter').grid(      column=c,row=1,padx=5); c+=1
        ttk.Label(fitframe,text='Initial Value').grid(  column=c,row=1,padx=5); c+=1
        ttk.Label(fitframe,text='Low Bound').grid(      column=c,row=1,padx=5); c+=1
        ttk.Label(fitframe,text='High Bound').grid(     column=c,row=1,padx=5); c+=1
        ttk.Label(fitframe,text='Result').grid(         column=c,row=1,padx=5); c+=1
        ttk.Label(fitframe,text='Result Error').grid(   column=c,row=1,padx=5); c+=1
        ttk.Label(fitframe,text='ChiSq').grid(          column=c,row=1,padx=5); c+=1
        ttk.Label(fitframe,text='Fixed').grid(          column=c,row=1,padx=5); c+=1
        ttk.Label(fitframe,text='Shared').grid(         column=c,row=1,padx=5); c+=1
        
        # grid the run_label
        self.run_label.grid(column=0,row=0,padx=5,pady=5,columnspan=c-1)
        
        # resizing
        for i in (4,5):
            fitframe.grid_columnconfigure(i,weight=1000)      # bounds
        for i in (1,2,3):
            fitframe.grid_columnconfigure(c-i,weight=10)  # fixed,share,chi
        
        fitframe.grid_columnconfigure(0,weight=1)           # run select
        
        fitframe.grid_rowconfigure(0,weight=1)              # run title
        
        for i in range(2,50):
            fitframe.grid_rowconfigure(i,weight=1)
        self.parent.grid_rowconfigure(1,weight=1)
        
        # save
        self.fitframe = fitframe
        
    # ======================================================================= #
    def get_new_parameters(self,runlist):
        """
            Fetch initial parameters from fitter, set to data.    
            
            runlist: list of run numbers to set new parameters for. 
        """
        
        self.logger.debug('Fetching new parameters')
        
        # get pointer to fit files object
        fit_files = self.bfit.fit_files
        fitter = fit_files.fitter
        ncomp = fit_files.n_component.get()
        fn_title = fit_files.fit_function_title.get()
        
        # get list of parameter names
        plist = fitter.gen_param_names(fn_title,ncomp)
        for run in runlist:
            
            # get init values
            values = fitter.gen_init_par(fn_title,ncomp,self.bfit.data[run].bd)
            
            # set to data
            self.bfit.data[run].set_fitpar(values)
        
        return plist
        
    # ======================================================================= #
    def get_selected_run(self):
        """Get the run number of the selected run"""
        
        try:
            self.selected = self.runbox.curselection()[0]
        except IndexError:
            self.selected = 0 
            
        self.logger.debug("Selected combobx[%d] (run %d)",
                          self.selected,self.runlist[self.selected])
            
        return self.runlist[self.selected]
        
    # ======================================================================= #
    def populate_param(self):
        """Populate the list of parameters"""
        
        # get list of parameters and initial values
        try:
            plist = self.get_new_parameters(self.runlist)
        except KeyError:
            return
        finally:
            for label in self.parlabels:
                label.destroy()
            for k in self.parentry.keys():
                for p in self.parentry[k]:
                    self.parentry[k][p][1].destroy()
        
        self.logger.debug('Populating parameter list with %s',plist)
        
        # make parameter input fields ---------------------------------------
        
        # labels
        c = 2
        
        self.parlabels = []     # track all labels and inputs
        for i,p in enumerate(plist):
            self.parlabels.append(ttk.Label(self.fitframe,text=p,justify=LEFT))
            self.parlabels[-1].grid(column=c,row=2+i,padx=5,sticky=E)
        
        # get data of selected run
        run = self.get_selected_run()
        fitdat = self.bfit.data[run]
        
        # input values: initial parameters
        r = 1
        for p in plist:         # iterate parameter names
            c = 2   # gridding column         
            r += 1  # gridding row         
            self.parentry[p] = {}
            for i in range(3):
                c += 1
                
                value = StringVar()
                entry = ttk.Entry(self.fitframe,textvariable=value,width=10)
                entry.insert(0,str(fitdat.fitpar[self.collist[i]][p]))
                entry.grid(column=c,row=r,padx=5,sticky=E)
                self.parentry[p][self.collist[i]] = (value,entry)
            
            # do results
            c += 1
            par_val = StringVar()
            par = ttk.Entry(self.fitframe,textvariable=par_val,width=15)
            par['state'] = 'readonly'
            par['foreground'] = 'black'
            
            dpar_val = StringVar()
            dpar = ttk.Entry(self.fitframe,textvariable=dpar_val,width=10)
            dpar['state'] = 'readonly'
            dpar['foreground'] = 'black'
                                     
            par. grid(column=c,row=r,padx=5,sticky=E); c += 1
            dpar.grid(column=c,row=r,padx=5,sticky=E); c += 1

            # do chi only once
            if r == 2:
                chi_val = StringVar()
                chi = ttk.Entry(self.fitframe,textvariable=chi_val,width=7)
                chi['state'] = 'readonly'
                chi['foreground'] = 'black'
                
                chi.grid(column=c,row=r,padx=5,sticky=E,rowspan=len(plist)); 
            c += 1
            
            # save ttk.Entry objects in dictionary [parname][colname]
            self.parentry[p][self.collist[3]] = (par_val,par)
            self.parentry[p][self.collist[4]] = (dpar_val,dpar)
            self.parentry[p][self.collist[5]] = (chi_val,chi)
            
            # do fixed box
            value = BooleanVar()
            entry = ttk.Checkbutton(self.fitframe,text='',\
                                     variable=value,onvalue=True,offvalue=False)
            entry.grid(column=c,row=r,padx=5,sticky=E); c += 1
            self.parentry[p][self.collist[6]] = (value,entry)
            
            # do shared box
            value = BooleanVar()
            entry = ttk.Checkbutton(self.fitframe,text='',\
                                     variable=value,onvalue=True,offvalue=False)
            entry.grid(column=c,row=r,padx=5,sticky=E); c += 1
            self.parentry[p][self.collist[7]] = (value,entry)
        
        # set parameters
        self.set_display()
        
    # ======================================================================= #
    def set_display(self,*args):
        """Set initial parameters and fit results in display to that of selected run"""
        
        # INITIAL PARAMETERS
        
        # get data that is currently there
        run = self.runlist[self.selected]
        fitdat_old = self.bfit.data[run]
        
        self.logger.debug('Setting display for run %d',run)
        
        # set as group 
        if self.bfit.fit_files.set_as_group.get():
            fitdat_list = [self.bfit.data[r] for r in self.runlist]
        else:
            fitdat_list = [fitdat_old]
        
        # get run number of new selected run
        run = self.get_selected_run()
        fitdat_new = self.bfit.data[run]
    
        # set label for run slection 
        self.run_label['text'] = '[ %d ]' % (run)
    
        for p in self.parentry.keys():  # parentry = [parname][colname][value,entry]
            for i in range(3):          # iterate input columns
                col = self.collist[i]   # column title
        
                # get new initial parameter
                if len(fitdat_new.fitpar[col].keys()) == 0:
                    self.get_new_parameters([run])
                newpar = float(self.parentry[p][col][0].get())
                    
                # check data of old entry: True if change data of all runs
                change_par = fitdat_old.fitpar[col][p] != newpar
                
                # set parameters of all data
                if change_par: 
                    for d in fitdat_list:
                        d.fitpar[col][p] = newpar
                
                # set only selected run
                else:
                    fitdat_old.fitpar[col][p] = newpar
                    
                # set values of new data
                self.parentry[p][col][0].set(
                            ("%"+".%df" % self.bfit.rounding) % \
                            fitdat_new.fitpar[col][p])
                
            # get fixed status of old data then set to new
            try:
                newpar = self.parentry[p]['fixed'][0].get()
                change_par = fitdat_old.fitpar['fixed'][p] != newpar
            except KeyError:
                pass
            else:
                if change_par:
                    for d in fitdat_list:   
                        d.fitpar['fixed'][p] = newpar
                else:
                    fitdat_old.fitpar['fixed'][p] = newpar
            
            try:
                self.parentry[p]['fixed'][0].set(fitdat_new.fitpar['fixed'][p])
            except KeyError:
                fitdat_new.fitpar['fixed'][p] = False
                self.parentry[p]['fixed'][0].set(False)
    
            # get and set shared status 
            try:
                newpar = self.parentry[p]['shared'][0].get()
                change_par = fitdat_old.fitpar['shared'][p] != newpar
            except KeyError:
                pass
            else:
                if change_par:
                    for d in [self.bfit.data[r] for r in self.runlist]:   # shared is always shared
                        d.fitpar['shared'][p] = newpar
                else:
                    fitdat_old.fitpar['shared'][p] = newpar
            
            try:
                self.parentry[p]['shared'][0].set(fitdat_new.fitpar['shared'][p])
            except KeyError:
                fitdat_new.fitpar['shared'][p] = False
                self.parentry[p]['shared'][0].set(False)
            
        # FIT RESULTS    
        
        # Set up variables
        displays = self.parentry
        
        try:
            data = self.bfit.data[run]
        except KeyError:
            return
            
        try:
            chi = data.chi
        except AttributeError:
            return 
        
        # display
        for parname in data.fitpar['res'].keys():
            disp = displays[parname]
            showstr = "%"+".%df" % self.bfit.rounding
            disp['res'][0].set(showstr % data.fitpar['res'][parname])
            disp['dres'][0].set(showstr % data.fitpar['dres'][parname])
            disp['chi'][0].set(showstr % chi)
         
    # ======================================================================= #
    def set_run_color(self):
        """On fit, set the color of the line in the run number select."""

        runlist = map(int,self.runbox.get(0,self.runbox.size()))
        
        for i,r in enumerate(runlist):
            if self.bfit.data[r].chi > self.bfit.fit_files.chi_threshold:
                self.runbox.itemconfig(i, {'bg':'red'})
            else:
                self.runbox.itemconfig(i, {'bg':'white'})

    # ======================================================================= #
    # ~ def update(self):
        # ~ """Update tab with new data"""
        
        # ~ self.logger.debug('Updating fit tab')
        
        # ~ # get list of runs
        # ~ dl = self.bfit.fetch_files.data_lines
        # ~ self.runlist = [dl[k].run for k in dl.keys() 
                # ~ if dl[k].check_state.get()]
        
        # ~ # List box for run viewing
        # ~ rlist = StringVar(value=tuple(map(str,self.runlist)))
        # ~ self.runbox.config(height=min(len(self.runlist),self.n_runs_max))
        # ~ self.runbox.config(listvariable=rlist)
        # ~ self.runbox.activate(0)
        # ~ self.runbox.event_generate('<<ListboxSelect>>')
        
