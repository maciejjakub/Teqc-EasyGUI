from tkinter import *
import tkinter.messagebox
import subprocess
import sys
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import scrolledtext
from tkinter import ttk
import fileinput
import webbrowser
import matplotlib.pyplot as plt
import numpy as np


class Application(Tk):
	
	def __init__(self, master = None):
		super().__init__(master)
		self.master = master
		self.create_widgets()
		self.title('Poland Secret Space Program')
		
	def create_widgets(self):
	
		# MENU
		self.menu = Menu(self)
		self.config(menu=self.menu)
		
		self.subMenu = Menu(self.menu, tearoff = 0)
		self.menu.add_cascade(label='File', menu=self.subMenu)
		self.subMenu.add_command(label='Open file', command=self.wybierzPlik)
		self.subMenu.add_separator()
		self.subMenu.add_command(label='File version check', command=self.czyRinex)
		
		self.aboutMenu = Menu(self.menu, tearoff = 0)
		self.menu.add_cascade(label='About', menu=self.aboutMenu)
		self.aboutMenu.add_command(label='About application', command=self.about_program)
		
		self.helpMenu = Menu(self.menu, tearoff = 0)
		self.menu.add_cascade(label='Help', menu=self.helpMenu)
		self.helpMenu.add_command(label='Help', command=self.help)
		
		
		# ZAKŁADKI
		self.tab_control = ttk.Notebook(self)
		self.tab_edit = ttk.Frame(self.tab_control)
		self.tab_analyze = ttk.Frame(self.tab_control)
		self.tab_draw = ttk.Frame(self.tab_control)
		
		self.tab_control.add(self.tab_edit, text = 'Edit')
		self.tab_control.add(self.tab_analyze, text = 'Analyze')
		self.tab_control.add(self.tab_draw, text = 'Visualize')
		self.tab_control.pack(expand = 1, fill = BOTH, side=TOP)
		
		# EDIT TOOLBAR
		self.toolbar = Frame(self.tab_edit, bg='#749da8')
		
		self.e_text_com =[('Convert into RINEX obs file', self.konwertuj), 
		('Convert into RINEX obs and RINEX nav files', self.convert_with_nav),
		('Merge multiple RINEX files', self.splice_data)]
		
		for i in self.e_text_com:
			self.e_button = Button(self.toolbar, text=i[0], command=i[1])
			self.e_button.pack(side=LEFT, padx=2, pady=2)
		
		
		self.button6 = Button(self.toolbar, text='Clear', command=self.clear)
		self.button6.pack(side=RIGHT, padx=2, pady=2)
		
		self.toolbar.pack(side=TOP, fill=X)
		
		
		# STATUSBAR
		self.statusbar = Label(self, text='Waiting for input...', bd=1, relief=SUNKEN, anchor=W)
		self.statusbar.pack(side=BOTTOM, fill=BOTH)
		
		
		# LEFT EDIT FRAME
		self.left_edit_frame = Frame(self.tab_edit)
		
		# ANTENNA HEIGHT INSERT
		self.left_e_frame1 = Frame(self.left_edit_frame)
		
		self.ins_time_label = Label(self.left_e_frame1, text='Insert start time [hh:mm:ss]')
		self.ins_time_label.pack(side=LEFT, pady = 10)
		self.ins_time_entry = Entry(self.left_e_frame1)
		self.ins_time_entry.pack(side=LEFT, padx=2)
		
		self.left_e_frame1.pack()
		
		self.left_e_frame1 = Frame(self.left_edit_frame)
		
		self.time_per_label = Label(self.left_e_frame1, text='Insert time period\nin minutes')
		self.time_per_label.pack(side=LEFT)
		self.time_per_entry = Entry(self.left_e_frame1)
		self.time_per_entry.pack(side=LEFT, padx=2)
		self.time_per_button = Button(self.left_e_frame1, text='Insert', command=self.time_windowing)
		self.time_per_button.pack(side=LEFT, padx=2)
		
		self.left_e_frame1.pack()
		
		self.left_e_frame1 = Frame(self.left_edit_frame)
		
		self.interval_label = Label(self.left_e_frame1, text='Interval [s]')
		self.interval_label.pack(side=LEFT, pady = 15)
		self.interval_entry = Entry(self.left_e_frame1)
		self.interval_entry.pack(side=LEFT, padx=2)
		self.interval_button = Button(self.left_e_frame1, text='Insert', command=self.decimate_data)
		self.interval_button.pack(side=LEFT, padx=2)
		
		self.left_e_frame1.pack()
		
		
		self.entry2 = Label(self.left_edit_frame, text='------ RINEX header modify ------')
		self.entry2.pack(side=TOP, pady = 10, padx = 10)
		
		# RINEX HEADER MODIFICATION
		
		self.left_e_frame1 = Frame(self.left_edit_frame)
		
		self.antenna_label = Label(self.left_e_frame1, text='Satellite system')
		self.antenna_label.pack(side=LEFT, pady = 5)
		self.satellite_system_entry = ttk.Combobox(self.left_e_frame1, values=('G (GPS)', 'R (GLONASS)', 'S (SBAS)', 'E (Galileo)', 'C (Beidou)', 'J (QZSS)'), width=17)
		self.satellite_system_entry.pack(side=RIGHT, padx=2)
		self.left_e_frame1.pack(fill=X)
		
		self.username_entry = StringVar()
		self.observer_entry = StringVar()
		self.agency_entry = StringVar()
		self.monument_entry = StringVar()
		self.monumentnumber_entry = StringVar()
		self.recievernumber_entry = StringVar()
		self.recievertype_entry = StringVar()
		self.software_entry = StringVar()
		self.antennanumber_entry = StringVar()
		self.antennatype_entry = StringVar()
		
		header_mod_list = [('Username', self.username_entry),
		('Observer', self.observer_entry),
		('Agency name', self.agency_entry),
		('Monument name', self.monument_entry),
		('Monument number', self.monumentnumber_entry),
		('Reciever number', self.recievernumber_entry),
		('Reciever type', self.recievertype_entry),
		('Software version', self.software_entry),
		('Antenna number', self.antennanumber_entry),
		('Antenna type', self.antennatype_entry)]
		
		for i in header_mod_list:
		
			self.left_e_frame1 = Frame(self.left_edit_frame)
			self.left_frame_label = Label(self.left_e_frame1, text=i[0])
			self.left_frame_label.pack(side=LEFT, pady = 5)
			self.left_frame_entry = Entry(self.left_e_frame1, textvariable=i[1])
			self.left_frame_entry.pack(side=RIGHT, padx=2)
			self.left_e_frame1.pack(fill=X)
		
		self.left_e_frame1 = Frame(self.left_edit_frame)
		self_antenna_label = Label(self.left_e_frame1, text='Approximate position X/Y/Z')
		self_antenna_label.pack(side=LEFT, pady = 5)
		self.appposx_entry = Entry(self.left_e_frame1, width=10)
		self.appposx_entry.pack(side=RIGHT, padx=2)
		self.appposy_entry = Entry(self.left_e_frame1, width=10)
		self.appposy_entry.pack(side=RIGHT, padx=2)
		self.appposz_entry = Entry(self.left_e_frame1, width=10)
		self.appposz_entry.pack(side=RIGHT, padx=2)
		self.left_e_frame1.pack(fill=X)
		
		self.left_e_frame1 = Frame(self.left_edit_frame)
		self_antenna_label = Label(self.left_e_frame1, text='Antenna delta H/E/N')
		self_antenna_label.pack(side=LEFT, pady = 5)
		self.antennadh_entry = Entry(self.left_e_frame1, width=10)
		self.antennadh_entry.pack(side=RIGHT, padx=2)
		self.antennade_entry = Entry(self.left_e_frame1, width=10)
		self.antennade_entry.pack(side=RIGHT, padx=2)
		self.antennadn_entry = Entry(self.left_e_frame1, width=10)
		self.antennadn_entry.pack(side=RIGHT, padx=2)
		self.left_e_frame1.pack(fill=X)
		
		self.left_e_frame1 = Frame(self.left_edit_frame)
		self_comment_label = Label(self.left_e_frame1, text='Add comment')
		self_comment_label.pack(side=LEFT, pady = 5)
		self.comment_entry = Entry(self.left_e_frame1, width=40)
		self.comment_entry.pack(side=RIGHT, padx=2)
		self.left_e_frame1.pack(fill=X)
		
		self.left_e_frame1 = Frame(self.left_edit_frame)
		self_antenna_button = Button(self.left_e_frame1, text='Modify', command=self.rinex_header_modify)
		self_antenna_button.pack(pady = 5, fill=X)
		self.left_e_frame1.pack(fill=X)
		
		
		
		self.left_edit_frame.pack(side=LEFT, fill=BOTH, expand=1)

		
		# ANALYZE TOOLBAR
		self.analyze_toolbar = Frame(self.tab_analyze, bg='#c5e0dc')
		
		self.a_text_com =[('Show metadata', self.show_metadata), 
		('Format check', self.format_check),
		('Quality check', self.qC),
		('Summary', self.ile)]
		
		for i in self.a_text_com:
			self.a_button = Button(self.analyze_toolbar, text=i[0], command=i[1])
			self.a_button.pack(side=LEFT, padx=2, pady=2)
		
		self.a_button = Button(self.analyze_toolbar, text='Clear', command=self.a_clear)
		self.a_button.pack(side=RIGHT, padx=2, pady=2)
		
		self.analyze_toolbar.pack(side=TOP, fill=X)
		
		# LEFT ANALYZE FRAME
		self.left_analyze_frame = Frame(self.tab_analyze)
		self.a_label1 = Label(self.left_analyze_frame, text ='Choose satellite systems to analyze', pady=10)
		self.a_label1.pack()
		
		self.gps_check = IntVar()
		self.glonass_check = IntVar()
		self.sbas_check = IntVar()
		self.galileo_check = IntVar()
		self.beidou_check = IntVar()
		self.qzss_check = IntVar()
		
		self.left_checkframe = Frame(self.left_analyze_frame)
		
		self.checklist = [('GPS', self.gps_check),
		('GLONASS', self.glonass_check),
		('SBAS', self.sbas_check),
		('Galileo', self.galileo_check),
		('Beidou', self.beidou_check),
		('QZSS', self.qzss_check)]
		
		for i in self.checklist:
			self.checkbutton = Checkbutton(self.left_checkframe, text=i[0], variable=i[1])
			self.checkbutton.select()
			self.checkbutton.pack(side=LEFT, padx=2, pady=2)
		self.left_checkframe.pack()
		
		self.left_analyze_frame.pack(side=LEFT, fill=BOTH, expand=1)
		
		
		# DRAW
		
		# LEFT DRAW FRAME
		self.left_draw_frame = Frame(self.tab_draw)
		
		self.left_d_frame1 = Frame(self.left_draw_frame)
		self.svn_label = Label(self.left_d_frame1, text='Insert maximum number of SVs to visualize')
		self.svn_label.pack(side=LEFT, pady = 10)
		self.svn_entry = Entry(self.left_d_frame1)
		self.svn_entry.pack(side=LEFT, padx=2)
		self.left_d_frame1.pack()
		
		self.left_d_frame1 = Frame(self.left_draw_frame)
		self.file_label = Label(self.left_d_frame1, text='Choose file for additional visualisation')
		self.file_label.pack(side=LEFT)
		self.file_entry = Button(self.left_d_frame1, text='Choose', command=self.load_drawfile)
		self.file_entry.pack(side=RIGHT, padx=2)
		self.left_d_frame1.pack(pady=30)
		
		self.left_d_frame1 = Frame(self.left_draw_frame)
		self.skyplot_button = Button(self.left_d_frame1, text='Draw skyplot', command=self.draw_skyplot)
		self.skyplot_button.pack(side=LEFT, expand=1, fill=BOTH)
		self.aziele_button = Button(self.left_d_frame1, text='Draw azimuth-elevation plot', command=self.draw_azelplot)
		self.aziele_button.pack(side=LEFT, expand=1, fill=BOTH)
		self.left_d_frame1.pack(fill=X)
		
		self.left_d_frame1 = Frame(self.left_draw_frame)
		self.bandplot_button = Button(self.left_d_frame1, text='Draw bandplot', command=self.draw_bandplot)
		self.bandplot_button.pack(side=LEFT, expand=1, fill=BOTH)
		self.timeelplot_button = Button(self.left_d_frame1, text='Draw time-elevation plot', command=self.draw_timeelplot)
		self.timeelplot_button.pack(side=LEFT, expand=1, fill=BOTH)
		self.left_d_frame1.pack(fill=X)
		
		self.display_map_button = Button(self.left_draw_frame, text='Display position on map', command=self.map_display)
		self.display_map_button.pack(side=TOP, pady=30, fill=X)
		
		self.left_draw_frame.pack(side=LEFT, fill=BOTH, expand=1)
		
		
		#POLE TEKSTOWE EDIT
		self.scrltxt = scrolledtext.ScrolledText(self.tab_edit, width = 100, height = 40, wrap=WORD, bg='beige')
		self.scrltxt.pack(side=RIGHT)
		
		#POLE TEKSTOWE ANALYZE
		self.scrltxt2 = scrolledtext.ScrolledText(self.tab_analyze, width = 100, height = 40, wrap=WORD)
		self.scrltxt2.pack(side=RIGHT)

		#DRAW SCROLLEDTEXT
		self.scrltxt3 = scrolledtext.ScrolledText(self.tab_draw, width = 100, height = 42, wrap=WORD)
		self.scrltxt3.pack(side=RIGHT, anchor=SE)
		
		
	def show_metadata(self):
		try:
			a = subprocess.run('teqc +meta ' + self.filename, capture_output=True, encoding='utf-8')
			self.scrltxt2.insert(INSERT, a.stdout)
		except AttributeError:
			self.attribute_error()
		
	def clear(self):
		self.scrltxt.delete(1.0, END)
	
	def a_clear(self):
		self.scrltxt2.delete(1.0, END)
		
	def d_clear(self):
		self.scrltxt3.delete(1.0, END)
		
	def qC(self):
		try:
			com_list = []
			var_list = [('-G ', self.gps_check.get()),
			('-R ', self.glonass_check.get()),
			('-S ', self.sbas_check.get()),
			('-E ', self.galileo_check.get()),
			('-C ', self.beidou_check.get()),
			('-J ', self.qzss_check.get())]
			
			for i in var_list:
				if not i[1]:
					com_list.append(i[0])
			qc = subprocess.run('teqc +qc +plot ' + ' '.join(com_list) + self.filename, capture_output=True, encoding='utf-8')
			self.scrltxt2.insert(INSERT, qc.stdout)
		except AttributeError:
			self.attribute_error()
			
	def qc_full(self):
		try:
			obs_file = self.filename
			nav_file = self.wybierzPlik()
			com_list = []
			var_list = [('-G ', self.gps_check.get()),
			('-R ', self.glonass_check.get()),
			('-S ', self.sbas_check.get()),
			('-E ', self.galileo_check.get()),
			('-C ', self.beidou_check.get()),
			('-J ', self.qzss_check.get())]
			
			for i in var_list:
				if not i[1]:
					com_list.append(i[0])
					
			qc_f = subprocess.run('teqc +qc +plot -nav ' + ' '.join(com_list) + nav_file + ' ' + obs_file, capture_output=True, encoding='utf-8')
			self.scrltxt2.insert(INSERT, qc_f.stderr)
			self.scrltxt2.insert(INSERT, qc_f.stdout)
		except AttributeError:
			self.attribute_error()
			
	def czyRinex(self):
		try:
			b = subprocess.run('teqc +v ' + self.filename, capture_output=True, encoding='utf-8')
			self.scrltxt.insert(INSERT, b.stderr)
		except AttributeError:
			self.attribute_error()
		
	def attribute_error(self):
		print('wykryto błąd!')
		tkinter.messagebox.showerror('Warning', 'Please open file first')
		
	def wybierzPlik(self):
		self.filename = askopenfilename()
		self.filename = self.filename.replace('/', '\\')
		print(self.filename)
		check = subprocess.run('teqc ' + self.filename, capture_output=True, encoding='utf-8')
		while check.stdout == '':
			if self.filename == '':
				break
			else:
				self.scrltxt.insert(INSERT, check.stderr)
				tkinter.messagebox.showerror('Warning', 'File not selected or selected in incorrect format')
				self.filename = askopenfilename()
				check = subprocess.run('teqc ' + self.filename, capture_output=True, encoding='utf-8')
		if self.filename != '':
			self.statusbar["text"] = 'File: ' + self.filename.split('\\')[-1] + ' successfully opened.'
			
		print(self.filename)
		return(self.filename)
		
	def konwertuj(self):
		try:
			self.saved_filename = asksaveasfilename()
			print('teqc ' + self.filename + ' > ' + self.saved_filename)
			conv = subprocess.run('teqc ' + self.filename + ' > ' + self.saved_filename, capture_output=True, encoding='utf-8', shell = True)
			print(conv.stderr)
			self.scrltxt.insert(INSERT, conv.stdout)
			self.scrltxt.insert(INSERT, 'Conversion ended with success.\n')
			self.filename = self.saved_filename
			self.statusbar["text"] = 'File: ' + self.filename.split('\\')[-1] + ' successfully opened.'
		except AttributeError:
			self.attribute_error()
		except FileNotFoundError:
			self.attribute_error()
			
	def convert_with_nav(self):
		try:
			input_file = self.filename
			obs_file = asksaveasfilename(title = "Select observation file name")
			nav_file = asksaveasfilename(title = "Select navigation file name")
			subprocess.run('teqc +nav ' + nav_file + ' ' + input_file + ' > ' + obs_file, capture_output=True, encoding='utf-8', shell = True)
			self.scrltxt.insert(INSERT, 'Conversion ended with success.\n')
			self.filename = obs_file
			self.statusbar["text"] = 'File: ' + self.filename.split('\\')[-1] + ' successfully opened.'
		except AttributeError:
			self.attribute_error()
		
	def format_check(self):
		try:
			format_check = subprocess.run('teqc +mdf ' + self.filename, capture_output=True, encoding='utf-8')
			self.scrltxt2.insert(INSERT, format_check.stdout)
			print(format_check.stdout.split()[-1])
		except AttributeError:
			self.attribute_error()
		except UnboundLocalError:
			self.attribute_error()
		return(format_check.stdout)
			
	def about_program(self):
		tkinter.messagebox.showinfo('About', 'An application for satellite data edit and analyze based on existing open-source application teqc and plotting script teqcplot.py.\nDeveloped by Maciej Miliszewski\nWarsaw University of Technology\nPoland')
	
	def help(self):
		tkinter.messagebox.showinfo('Help', 'For help with usage of application please check file readme.txt in source folder')
	
	def rinex_header_modify(self):
		try:
			self.saved_filename = asksaveasfilename()
			com_list = []
			sat_list = {'-G', '-R', '-E', '-C', '-S', '-J'}
			var_list = [('-O.s ', self.satellite_system_entry.get()),
			('-O.r ', self.username_entry.get()),
			('-O.o ', self.observer_entry.get()),
			('-O.ag ', self.agency_entry.get()),
			('-O.mo ', self.monument_entry.get()),
			('-O.mn ', self.monumentnumber_entry.get()),
			('-O.rn ', self.recievernumber_entry.get()),
			('-O.rt ', self.recievertype_entry.get()),
			('-O.rv ', self.software_entry.get()),
			('-O.an ', self.antennanumber_entry.get()),
			('-O.at ', self.antennatype_entry.get()),
			('-O.px[WGS84xyz,m] ', self.appposx_entry.get(), self.appposy_entry.get(), self.appposz_entry.get()),
			('-O.pe[hEN,m] ', self.antennadh_entry.get(), self.antennade_entry.get(), self.antennadn_entry.get()),
			('-O.c ', self.comment_entry.get())]
			
			if not self.filename:
				raise AttributeError
				
			for i in var_list:
				if i[1]:
					if i[0] == '-O.s ':
						com_list.append(i[0] + '"{}"'.format(i[1]))
						sat_list.remove('-' + i[1].split()[0])
						com_list.append(' '.join(sat_list))
					elif i[0] == '-O.px[WGS84xyz,m] ' or i[0] == '-O.pe[hEN,m] ':
						com_list.append(i[0] + ' '.join(i[1:4]))
					else:
						com_list.append(i[0] + '"{}"'.format(i[1]))

			subprocess.run('teqc ' + ' '.join(com_list) + ' ' + self.filename + ' > ' + self.saved_filename, capture_output=True, encoding='utf-8', shell = True)
			print('teqc ' + ' '.join(com_list) + ' ' + self.filename + ' > ' + self.saved_filename)
			self.scrltxt.insert(INSERT, 'Header modification ended with success.\n')
		except AttributeError:
			self.attribute_error()
	
	def compare(self):
		try:
			file1 = self.filename
			file2 = self.wybierzPlik()
			compare_variable = subprocess.run('diff ' + file1 + ' ' + file2, capture_output=True, encoding='utf-8', shell = True)
			self.scrltxt2.insert(INSERT, compare_variable.stderr)
			self.scrltxt2.insert(INSERT, compare_variable.stdout)
		except AttributeError:
			self.attribute_error()
		
	def decimate_data(self):
		try:
			if len(self.interval_entry.get()) > 0 and type(int(self.interval_entry.get())): 
				self.saved_filename = asksaveasfilename()
				subprocess.run('teqc -O.dec ' + str(int(self.interval_entry.get())) + ' ' + self.filename + ' > ' + self.saved_filename, capture_output=True, encoding='utf-8', shell = True)
				self.scrltxt.insert(INSERT, 'Decimation ended with success.\n')
		except AttributeError:
			self.attribute_error()
		except ValueError:
			self.scrltxt.insert(INSERT, 'Cannot decimate data. Inserted value has to be an integer number.\n')
		
	def time_windowing(self):
		try:
			self.saved_filename = asksaveasfilename()
			com_list = []
			var_list = [('-st ', self.ins_time_entry.get()),
			('-dm ', self.time_per_entry.get())]
			
			if not self.filename:
				raise AttributeError
				
			for i in var_list:
				if i[1]:
					com_list.append(i[0] + i[1])

			subprocess.run('teqc ' + ' '.join(com_list) + ' ' + self.filename + ' > ' + self.saved_filename, capture_output=True, encoding='utf-8', shell = True)
			self.scrltxt.insert(INSERT, 'Time windowing ended with success.\n')
		except AttributeError:
			self.attribute_error()
		except ValueError:
			self.scrltxt.insert(INSERT, 'Cannot decimate data. Inserted value has to be an integer number.\n')
		
		
	def splice_data(self):
		try:
			filename_list = [self.filename]
			while(len(self.filename) > 0):
				self.filename = askopenfilename()
				filename_list.append(self.filename)
			self.statusbar["text"] = 'File: ' + self.filename.split('\\')[-1] + ' opened successfully'
			tkinter.messagebox.showinfo('', 'Choose output filename now.')
			saved = asksaveasfilename()
			subprocess.run('teqc ' + ' '.join(filename_list) + ' > ' + saved, encoding='utf-8', shell=True)
			self.scrltxt.insert(INSERT, 'Splicing ended with success.\n')
		except AttributeError:
			self.attribute_error()

	def ile(self):
		try:
			com_list = []
			var_list = [('-G ', self.gps_check.get()),
			('-R ', self.glonass_check.get()),
			('-S ', self.sbas_check.get()),
			('-E ', self.galileo_check.get()),
			('-C ', self.beidou_check.get()),
			('-J ', self.qzss_check.get())]
			
			for i in var_list:
				if not i[1]:
					com_list.append(i[0])
					
			ile = subprocess.run('teqc -O.sum . ' + ' '.join(com_list) + self.filename, encoding='utf-8', capture_output = True, shell=True)
			self.scrltxt2.insert(INSERT, ile.stdout)
		except AttributeError:
			self.attribute_error()

	def map_display(self):
		try:
			file = self.filename[:-1] + 'S'
			map_var = 0
			for i in fileinput.input(files = file):
				if 'antenna WGS 84 (geo)  :  ' in i and float(i.split()[7]) < 180:
					webbrowser.open('http://www.google.com/maps/place/{},{}'.format(i.split()[5], i.split()[7]))
					map_var = 1
				elif 'antenna WGS 84 (geo)  :  ' in i and float(i.split()[7]) > 180:
					webbrowser.open('http://www.google.com/maps/place/{},{}'.format(i.split()[5], i.split()[10]))
					map_var = 1
			if not map_var:
				self.scrltxt3.insert(INSERT, 'Cannot display map, unable to find coordinates in quality check report file.\n')
		except FileNotFoundError:
			self.scrltxt3.insert(INSERT, 'Cannot display map, unable to find quality check report file.\n')
		except AttributeError:
			self.attribute_error()
			
	def load_drawfile(self):
		self.drawfile = askopenfilename()
		
	def draw_skyplot(self):
		try:
			elevation_file = self.filename[:-3] + 'ele'
			azimuth_file = self.filename[:-3] + 'azi'
			print(self.svn_entry.get())
			if int(self.svn_entry.get()):
				draw = subprocess.run('teqcplot.py +skyplot +tcl=' + self.svn_entry.get() + ' ' + azimuth_file + ' ' + elevation_file + ' ' + self.drawfile, capture_output=True, encoding='utf-8', shell = True)
				self.scrltxt3.insert(INSERT, draw.stdout)
		except FileNotFoundError:
			self.scrltxt3.insert(INSERT, 'Cannot draw plot. Do full quality check first.\n')
		except ValueError:
			self.scrltxt3.insert(INSERT, 'Cannot draw plot. SVs quantity has to be a number.\n')
		except AttributeError:
			self.attribute_error()

	def draw_bandplot(self):
		try:
			elevation_file = self.filename[:-3] + 'ele'
			azimuth_file = self.filename[:-3] + 'azi'
			print(self.svn_entry.get())
			if int(self.svn_entry.get()):
				draw = subprocess.run('teqcplot.py +bandplot +tcl=' + self.svn_entry.get() + ' ' + azimuth_file + ' ' + elevation_file + ' ' + self.drawfile, capture_output=True, encoding='utf-8', shell = True)
				self.scrltxt3.insert(INSERT, draw.stdout)
		except FileNotFoundError:
			self.scrltxt3.insert(INSERT, 'Cannot draw plot. Do full quality check first.\n')
		except ValueError:
			self.scrltxt3.insert(INSERT, 'Cannot draw plot. SVs quantity has to be a number.\n')
		except AttributeError:
			self.attribute_error()

	def draw_azelplot(self):
		try:
			elevation_file = self.filename[:-3] + 'ele'
			azimuth_file = self.filename[:-3] + 'azi'
			print(self.svn_entry.get())
			if int(self.svn_entry.get()):
				draw = subprocess.run('teqcplot.py +azelplot +tcl=' + self.svn_entry.get() + ' ' + azimuth_file + ' ' + elevation_file + ' ' + self.drawfile, capture_output=True, encoding='utf-8', shell = True)
				self.scrltxt3.insert(INSERT, draw.stdout)
		except FileNotFoundError:
			self.scrltxt3.insert(INSERT, 'Cannot draw plot. Do full quality check first.\n')
		except ValueError:
			self.scrltxt3.insert(INSERT, 'Cannot draw plot. SVs quantity has to be a number.\n')
		except AttributeError:
			self.attribute_error()
		
	def draw_timeelplot(self):
		try:
			elevation_file = self.filename[:-3] + 'ele'
			azimuth_file = self.filename[:-3] + 'azi'
			print(self.svn_entry.get())
			if int(self.svn_entry.get()):
				draw = subprocess.run('teqcplot.py +timeelplot +tcl=' + self.svn_entry.get() + ' ' + azimuth_file + ' ' + elevation_file + ' ' + self.drawfile, capture_output=True, encoding='utf-8', shell = True)
				self.scrltxt3.insert(INSERT, draw.stdout)
		except FileNotFoundError:
			self.scrltxt3.insert(INSERT, 'Cannot draw plot. Do full quality check first.\n')
		except ValueError:
			self.scrltxt3.insert(INSERT, 'Cannot draw plot. SVs quantity has to be a number.\n')
		except AttributeError:
			self.attribute_error()
		
	
			
if __name__ == "__main__":		
	print('Starting...')		
	app = Application()
	app.mainloop()
	print('Done!')