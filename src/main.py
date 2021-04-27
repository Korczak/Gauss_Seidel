#!/usr/bin/env python
# coding: utf-8

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
from tkinter import ttk
import tkinter.font

import urllib
import json

import pandas as pd
import numpy as np

from matplotlib import pyplot as plt

from gauss_seidel_alg import GaussSeidel

np.set_printoptions(precision=2)
gaussSeidel = GaussSeidel(); 
fig = Figure()
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
		self.functionInput = tk.Entry(inputFrame, textvariable = tk.StringVar(inputFrame, value = "x1 + x2^2"))
		self.functionInput.grid(row = 1, column = 1, pady=5, sticky='ew')
		startPointLabel = tk.Label(inputFrame, text="Poczatkowy punkt = ").grid(row = 2, column = 0, pady=5)
		self.startPointInput = tk.Entry(inputFrame, textvariable = tk.StringVar(inputFrame, value = "1.5; 2"))
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
		self.textView = tk.Text(outputFrame, height = 20)
		self.textView.grid(row = 2, pady=5, columnspan = 2)
		

		self.textResult = tk.StringVar()
		self.textResult.set("Wynik: ")
		self.resultLabel = tk.Label(outputFrame, textvariable=self.textResult)
		self.resultLabel.grid(row = 3, pady=5, columnspan = 2)

		self.showGraphButton = tk.Button(outputFrame, text="Pokaz warstwice", command=lambda: controller.show_frame(PageGraph), state=tk.DISABLED)
		self.showGraphButton.grid(row = 4, pady=5, columnspan = 2)
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

		self.showGraphButton['state'] = tk.NORMAL
		self.set_text(self.textView, gaussSeidel.get_iteration_text())
		self.textResult.set("Wynik: {}, X = {}".format(round(gaussSeidel.get_current_res(), 3), np.around(gaussSeidel.get_current_X(), 3)))
		try:
			controller.get_frame(PageGraph).drawGraph()
		except Exception as e:
			print("Graph not exists")

	def set_text(self, text, value):
	    text.delete('1.0', tk.END)
	    text.insert(tk.END, value)


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
		global gaussSeidel
		global fig
		fig.clear()
		ax = fig.add_subplot(111)
		ax = gaussSeidel.generatePlot(ax)
		self.canvas.draw_idle()


app = TimoGui()
app.geometry("720x600")
app.mainloop()
