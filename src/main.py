#!/usr/bin/env python
# coding: utf-8

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from mpl_toolkits.mplot3d import Axes3D
import tkinter as tk
from tkinter import ttk
import tkinter.font

import urllib
import json

import pandas as pd
import numpy as np

from matplotlib.figure import Figure
from gauss_seidel_alg import GaussSeidel

np.set_printoptions(precision=2)
gaussSeidel = GaussSeidel(); 
fig = Figure(figsize=(5, 4), dpi=100)
LARGE_FONT= ("Verdana", 12)
DEFAULT_FONT = ("Times New Roman", 12)

style.use("ggplot")
	
class TimoGui(tk.Tk):

	def __init__(self, *args, **kwargs):
		
		tk.Tk.__init__(self, *args, **kwargs)

		tk.Tk.wm_title(self, "Optymalizacja metoda Gaussa-Seidela")
		
		
		self.container = tk.Frame(self)
		self.container.pack(side="top", fill="both", expand = True)
		self.container.grid_rowconfigure(0, weight=1)
		self.container.grid_columnconfigure(0, weight=1)

		self.frames = {}

		self.show_frame(PageStart)


	def show_frame(self, cont):
		if(cont not in self.frames):
			frame = cont(self.container, self)
			self.frames[cont] = frame			
			frame.grid(row=0, column=0, sticky="nsew")

		frame = self.frames[cont]
		frame.tkraise()

	def get_frame(self, cont):
		return self.frames[cont]

class PageStart(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		inputFrame = tk.Frame(self)
		defaultFont = tk.font.nametofont("TkDefaultFont")
		defaultFont.configure(family = "Times New Roman", size = 10)

		label = tk.Label(self, text="", font=LARGE_FONT).grid(row=1, column = 0, pady=5)
		#label.pack(pady=10,padx=10)

		functionLabel = tk.Label(inputFrame, text="F(x) = ").grid(row = 1, column = 0, pady=5)
		self.functionInput = tk.Entry(inputFrame, textvariable = tk.StringVar(inputFrame, value = "x1 + x2^2 + x3"))
		self.functionInput.grid(row = 1, column = 1, pady=5, sticky='ew')
		startPointLabel = tk.Label(inputFrame, text="Poczatkowy punkt = ").grid(row = 2, column = 0, pady=5)
		self.startPointInput = tk.Entry(inputFrame, textvariable = tk.StringVar(inputFrame, value = "1.5; 2; 3"))
		self.startPointInput.grid(row = 2, column = 1, pady=5, sticky='ew')
		epsLabel = tk.Label(inputFrame, text="Epsilon = ").grid(row = 3, column = 0, pady=5)
		self.epsInput = tk.Entry(inputFrame, textvariable = tk.StringVar(inputFrame, value = "0.0001"))
		self.epsInput.grid(row = 3, column = 1, pady=5, sticky='ew')
		sectionRangeLabel = tk.Label(inputFrame, text="Przedzial = ").grid(row = 4, column = 0, pady=5)
		self.sectionRangeInput = tk.Entry(inputFrame, textvariable = tk.StringVar(inputFrame, value = "10"))
		self.sectionRangeInput.grid(row = 4, column = 1, pady=5, sticky='ew')
		maxIterLabel = tk.Label(inputFrame, text="Maksymalna ilosc iteracji = ").grid(row = 5, column = 0, pady=5)
		self.maxIterInput = tk.Entry(inputFrame, textvariable = tk.StringVar(inputFrame, value = "30"))
		self.maxIterInput.grid(row = 5, column = 1, pady=5, sticky='ew')
		self.evaluateButton = tk.Button(inputFrame, text="Oblicz", command=lambda: self.onResult(controller))
		self.evaluateButton.grid(row = 6, column = 0, columnspan=2, pady=5, sticky='ew')


		outputFrame = tk.Frame(self)
		iterationLabel = tk.Label(outputFrame, text="Iteracje").grid(row = 1, pady=5, columnspan = 2)
		
		self.treeView = ttk.Treeview(outputFrame, columns=5, show='headings')
		self.treeView['columns']=('Pozycja', 'Wartość funkcji', 'Kryterium 1', 'Kryterium 2', 'Kryterium 3')
		self.treeView.grid(row = 2, pady=5, columnspan = 2)
		self.treeView.column('#0', width=0, stretch=tk.NO)
		self.treeView.column('Pozycja', anchor=tk.CENTER, width=250, stretch=tk.YES)
		self.treeView.column('Wartość funkcji', anchor=tk.CENTER, width=150, stretch=tk.YES)
		self.treeView.column('Kryterium 1', anchor=tk.CENTER, width=100, stretch=tk.YES)
		self.treeView.column('Kryterium 2', anchor=tk.CENTER, width=100, stretch=tk.YES)
		self.treeView.column('Kryterium 3', anchor=tk.CENTER, width=100, stretch=tk.YES)

		self.treeView.heading('Pozycja', text='Pozycja', anchor=tk.CENTER)
		self.treeView.heading('Wartość funkcji', text='Wartość funkcji', anchor=tk.CENTER)
		self.treeView.heading('Kryterium 1', text='Kryterium 1', anchor=tk.CENTER)
		self.treeView.heading('Kryterium 2', text='Kryterium 2', anchor=tk.CENTER)
		self.treeView.heading('Kryterium 3', text='Kryterium 3', anchor=tk.CENTER)

		self.endingText = tk.StringVar()
		self.endingLabel = tk.Label(outputFrame, textvariable=self.endingText)
		self.endingLabel.grid(row = 3, pady=5, columnspan = 2)

		self.textResult = tk.StringVar()
		self.textResult.set("Wynik: ")
		self.resultLabel = tk.Label(outputFrame, textvariable=self.textResult)
		self.resultLabel.grid(row = 4, pady=5, columnspan = 2)


		self.showGraphButton = tk.Button(outputFrame, text="Pokaz warstwice", command=lambda: controller.show_frame(PageGraph), state=tk.DISABLED)
		self.showGraphButton.grid(row = 5, pady=5, columnspan = 2)
		#showGraphButton.config(state = "disabled")

		inputFrame.grid(row=4, column=0, sticky="NESW", padx = 5)
		inputFrame.grid_columnconfigure(0, weight=1)
		inputFrame.grid_columnconfigure(1, weight=9)
		outputFrame.grid(row=5, column=0, sticky="NESW", padx = 5)
		outputFrame.grid_rowconfigure(0, weight=1)
		outputFrame.grid_rowconfigure(1, weight=5)		
		outputFrame.grid_rowconfigure(2, weight=1)
		outputFrame.grid_rowconfigure(3, weight=1)
		outputFrame.grid_rowconfigure(4, weight=1)
		outputFrame.grid_rowconfigure(5, weight=1)
		outputFrame.grid_columnconfigure(1, weight=1)
		self.grid_columnconfigure(0, weight=1)

	def onResult(self, controller):
		global gaussSeidel
		gaussSeidel.calculate(
			self.functionInput.get(), 
			self.startPointInput.get(), 
			self.epsInput.get(), 
			self.sectionRangeInput.get(),
			self.maxIterInput.get()
			)

		canPlot = gaussSeidel.canPlotLevelSets()
		if(canPlot):
			self.showGraphButton['state'] = tk.NORMAL
		else:
			self.showGraphButton['state'] = tk.DISABLED
		self.treeView.delete(*self.treeView.get_children())
		for result in gaussSeidel.get_result_table_data():
			self.treeView.insert('', tk.END, values=result)

		self.endingText.set(gaussSeidel.get_ending_text())

		self.textResult.set("Wynik: {}, X = {}".format(round(gaussSeidel.get_current_res(), 3), np.around(gaussSeidel.get_current_X(), 3)))

		try:
			controller.get_frame(PageGraph).drawGraph()
		except Exception as e:
			print("Graph not exists")
		
	def set_text(self, text, value):
	    text.delete('1.0', tk.END)
	    text.insert(tk.END, value)

	def set_table(self):
		pass


class PageGraph(tk.Frame):

	def __init__(self, parent, controller):
		global fig
		tk.Frame.__init__(self, parent)

		button1 = ttk.Button(self, text="Powrot", command=lambda: controller.show_frame(PageStart))
		
		self.canvas = FigureCanvasTkAgg(fig, self)
		self.drawGraph()
		button1.pack(side=tk.BOTTOM, fill='x')		
		toolbar = NavigationToolbar2Tk(self.canvas, self).update()
		self.canvas.get_tk_widget().pack(side=tk.BOTTOM, expand=True)
		
		self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
		self.canvas.draw()


	def drawGraph(self):
		print('Draw graph')
		global gaussSeidel
		global fig
		fig.clear()
		if(gaussSeidel.is2D()):
			ax = fig.add_subplot(111)
			ax = gaussSeidel.generatePlot(ax)
		else:
			#ax = Axes3D(fig)
			ax = fig.add_subplot(111, projection="3d")
			#ax = plt.axes(projection="3d")
			ax = gaussSeidel.generatePlot(ax)
		self.canvas.draw_idle()


app = TimoGui()
app.geometry("720x600")
app.mainloop()

