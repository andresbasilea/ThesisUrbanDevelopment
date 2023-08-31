import tkinter
import tkinter.messagebox
import customtkinter
from PIL import Image, ImageTk
import numpy as np
from tkinter.filedialog import askopenfilename, asksaveasfilename
from datetime import datetime
from random import randint
from CA_Utils import CA_Utils
from pathlib import Path
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd
import time
import traceback

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Tesis Ila")
        self.geometry(f"{1600}x{900}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure((1,2,3,4,5), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)


        # GENERAL GRID PARAMETERS
        self.matrix_size = 100
        self.cell_size = 0
        self.matrix_array_size = np.empty((self.matrix_size, self.matrix_size))
        self.matrix_array = np.zeros_like(self.matrix_array_size)
        self.total_number_cells = self.matrix_size*self.matrix_size
        self.weights_matrix = None


        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=100, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsw")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Thesis Project:", font=customtkinter.CTkFont(size=14, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Ilana Villanueva Carrión", font=customtkinter.CTkFont(size=14, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(70, 10))
        
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text='Run', command=self.run_simulation)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text='Save', command=self.save_matrix_array)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text='Load', command=self.load_matrix_array)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        
        self.combobox_grid_size = customtkinter.CTkComboBox(self.sidebar_frame,
                                                    values=["10", "50", "100", "200"], command=self.change_grid_size)
        self.combobox_grid_size.set("100")
        self.combobox_grid_size.grid(row=4, column=0, padx=20, pady=(100, 10))
        self.grid_size_label = customtkinter.CTkLabel(self.sidebar_frame, text="Grid Size: {}".format(self.matrix_size), anchor="w")
        self.grid_size_label.grid(row=4, column=0, padx=20, pady=(10, 0))

        self.random_fill_button = customtkinter.CTkButton(self.sidebar_frame, text='Random Fill', command=self.random_fill)
        self.random_fill_button.grid(row=4, column=0, padx=20,pady=(200, 10))

        self.load_weights_button = customtkinter.CTkButton(self.sidebar_frame, text='Load Weights', command=self.load_weights)
        self.load_weights_button.grid(row=4, column=0, padx=20,pady=(280, 10))

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))


        # create tabview frame
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=1, columnspan=3, rowspan=3,padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("Cell %")
        self.tabview.add("Parameters")
        #self.tabview.add("Weights")
        self.tabview.add("Graphs")
        
        # tabview cell % tab
        self.tabview.tab("Cell %").grid_columnconfigure((0,1,2,3,4,5,6), weight=1)  # configure grid of individual tabs
        self.cell_perc_initial_label = customtkinter.CTkLabel(self.tabview.tab("Cell %"), text="Initial Cells %", anchor="w", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.cell_perc_initial_label.grid(row=0, column=0, columnspan=2)
        self.cell_perc_end_label = customtkinter.CTkLabel(self.tabview.tab("Cell %"), text="End Cells %", anchor="e", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.cell_perc_end_label.grid(row=0, column=4, columnspan=2)
        self.update_percentage_button = customtkinter.CTkButton(self.tabview.tab("Cell %"), text='Update Percentages', command=self.update_percentage_values)
        self.update_percentage_button.grid(row=8, column=2, columnspan=2, padx=20, pady=10)
        self.land_categories = ['Industrial', 'Commercial', 'Residential', 'Green', 'Vacant']
        self.ind_initial_val = np.count_nonzero(self.matrix_array==1) / self.total_number_cells *100
        self.com_initial_val = np.count_nonzero(self.matrix_array==2) / self.total_number_cells *100
        self.res_initial_val = np.count_nonzero(self.matrix_array==3) / self.total_number_cells *100
        self.gre_initial_val = np.count_nonzero(self.matrix_array==4) / self.total_number_cells *100
        self.vac_initial_val = np.count_nonzero(self.matrix_array==5) / self.total_number_cells *100
        self.cell_perc_initial_value = [self.ind_initial_val, self.com_initial_val, self.res_initial_val, self.gre_initial_val, self.vac_initial_val]

        
        self.ind_final_val = (np.count_nonzero(self.matrix_array==1) / self.total_number_cells) *100
        self.com_final_val = (np.count_nonzero(self.matrix_array==2) / self.total_number_cells) *100
        self.res_final_val = (np.count_nonzero(self.matrix_array==3) / self.total_number_cells) *100
        self.gre_final_val = (np.count_nonzero(self.matrix_array==4) / self.total_number_cells) *100
        self.vac_final_val = (np.count_nonzero(self.matrix_array==5) / self.total_number_cells) *100
        self.cell_perc_final_value = [self.ind_final_val, self.com_final_val, self.res_final_val, self.gre_final_val, self.vac_final_val]
        self.cell_perc_final_value = [0.0,0.0,0.0,0.0,0.0]

        for row in range(1,6):
            label = customtkinter.CTkLabel(self.tabview.tab("Cell %"), text=self.land_categories[row-1], fg_color="transparent")
            label.grid(row=row, column=0)
            label = customtkinter.CTkLabel(self.tabview.tab("Cell %"), text=self.cell_perc_initial_value[row-1], fg_color="transparent")
            label.grid(row=row, column=1)

        for row in range(1,6):
            label_final = customtkinter.CTkLabel(self.tabview.tab("Cell %"), text=self.land_categories[row-1], fg_color="transparent")
            label_final.grid(row=row, column=4)
            label_final = customtkinter.CTkLabel(self.tabview.tab("Cell %"), text=self.cell_perc_final_value[row-1], fg_color="transparent")
            label_final.grid(row=row, column=5)

        # tabview parameters tab
        self.tabview.tab("Parameters").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Parameters").grid_rowconfigure((0,1,2,3,4,5), weight=1)

        self.slider_interactions = customtkinter.CTkSlider(self.tabview.tab("Parameters"), from_=1, to=40, number_of_steps=39, command=self.set_label_parameter_interactions)
        self.slider_interactions.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.slider_interactions_value = str(int(self.slider_interactions.get()))
        self.interactions_parameter = customtkinter.CTkLabel(self.tabview.tab("Parameters"), text="Number of Interactions: " + self.slider_interactions_value , fg_color="transparent")
        self.interactions_parameter.grid(row=0, column=0)

        self.slider_perturbation = customtkinter.CTkSlider(self.tabview.tab("Parameters"), from_=0, to=5, number_of_steps=100,state='disabled', command=self.set_label_parameter_perturbation)
        self.slider_perturbation.grid(row=3, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.slider_perturbation_value = str(self.slider_perturbation.get())
        self.perturbation_parameter = customtkinter.CTkLabel(self.tabview.tab("Parameters"), text="Perturbation: " + self.slider_perturbation_value, fg_color="transparent")
        self.slider_perturbation.set(2.5)
        self.perturbation_parameter.grid(row=2, column=0)

        self.slider_radius = customtkinter.CTkSlider(self.tabview.tab("Parameters"), from_=1, to=10, number_of_steps=10, state='disabled', command=self.set_label_parameter_radius)
        self.slider_radius.grid(row=5, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.slider_radius.set(6)
        self.slider_radius_value = str(int(self.slider_radius.get()))
        self.radius_parameter = customtkinter.CTkLabel(self.tabview.tab("Parameters"), text="Moore Neighborhood (Radius): " + self.slider_radius_value, fg_color="transparent")
        self.radius_parameter.grid(row=4, column=0)



        # WEIGHTS

        #self.weights_file = read_weights.read_excel_weights("pesos.xlsx")

        # self.tabview.tab("Weights").grid_columnconfigure(0, weight=1)
        # self.root = self.tabview.tab("Weights")
        # self.table_rows = 127
        # self.table_columns = 19
        # self.column_headings = [ 
        #     "1", "1.4", "2", "2.2", "2.8", "3", "3.2", "3.6", "4", "4.1", 
        #     "4.2", "4.5", "5", "5.1", "5.4", "5.7", "5.8", "6.0", "6.1-8"
        # ]
        # self.row_headings = [ "A-A",

        #     "V-C", "V-I", "V-R", "V-G", "V-V", "I-C", "I-I", "I-R", "I-G", 
        #     "C-C", "C-I", "C-R", "C-G", "R-C", "R-I", "R-R", "R-G", 
        #     "A-C", "A-I", "A-R", "A-A",

        #     "V-C", "V-I", "V-R", "V-G", "V-V", "I-C", "I-I", "I-R", "I-G", 
        #     "C-C", "C-I", "C-R", "C-G", "R-C", "R-I", "R-R", "R-G", 
        #     "A-C", "A-I", "A-R", "A-A",

        #     "V-C", "V-I", "V-R", "V-G", "V-V", "I-C", "I-I", "I-R", "I-G", 
        #     "C-C", "C-I", "C-R", "C-G", "R-C", "R-I", "R-R", "R-G", 
        #     "A-C", "A-I", "A-R", "A-A",

        #     "V-C", "V-I", "V-R", "V-G", "V-V", "I-C", "I-I", "I-R", "I-G", 
        #     "C-C", "C-I", "C-R", "C-G", "R-C", "R-I", "R-R", "R-G", 
        #     "A-C", "A-I", "A-R", "A-A",

        #     "V-C", "V-I", "V-R", "V-G", "V-V", "I-C", "I-I", "I-R", "I-G", 
        #     "C-C", "C-I", "C-R", "C-G", "R-C", "R-I", "R-R", "R-G", 
        #     "A-C", "A-I", "A-R", "A-A",

        #     "V-C", "V-I", "V-R", "V-G", "V-V", "I-C", "I-I", "I-R", "I-G", 
        #     "C-C", "C-I", "C-R", "C-G", "R-C", "R-I", "R-R", "R-G", 
        #     "A-C", "A-I", "A-R", "A-A"
        # ]

        # self.table_data = np.zeros((self.table_rows, self.table_columns), dtype=int)

        # my_file = Path("weights_file.npy")
        # if my_file.is_file():
        #     self.table_data = np.load("weights_file.npy")

        # self.table_frame = customtkinter.CTkScrollableFrame(self.root)
        # #self.table_frame.grid(column=0, columnspan=30)
        # self.entry_widgets = []

        # for i, row_heading in enumerate(self.row_headings):
        #     row_label = customtkinter.CTkLabel(self.table_frame, text=row_heading, width=3, anchor="w") # faster to load with tkinter than customtkinter
        #     row_label.grid(row=i+2, column=0)
            
        #     row_entries = []
        #     for j, col_heading in enumerate(self.column_headings):
        #         if i == 0:  # Add column headings to the first row
        #             col_label = customtkinter.CTkLabel(self.table_frame, text=col_heading, width=3) # faster to load with tkinter than customtkinter
        #             col_label.grid(row=1, column=j+1)
                
        #         entry = tkinter.Entry(self.table_frame, width=2)  # faster to load with tkinter than customtkinter
        #         entry.insert(-1, self.table_data[i,j])
        #         entry.grid(row=i+2, column=j+1)
        #         row_entries.append(entry)
        #     self.entry_widgets.append(row_entries)

        # self.save_button = customtkinter.CTkButton(self.root, text="Save", command=self.save_table_data)
        # self.save_button.grid(row=50, column=0)

        # self.table_frame.grid()





        # GRAPHS

        self.tabview.tab("Graphs").grid_columnconfigure(0, weight=1)
        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.root = self.tabview.tab("Graphs")
        self.plot = self.figure.add_subplot(111)
        self.plot.set_xlabel('Time Interval')
        self.plot.set_ylabel('Percentage of Green Areas')
        self.plot.set_title('Change in Percentage of Green Areas over Time')
        self.canvas_graphs = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas_widget = self.canvas_graphs.get_tk_widget()
        self.canvas_widget.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        self.update_button = customtkinter.CTkButton(self.root, text="Update Plot", command=self.update_plot)
        self.update_button.pack(side=tkinter.BOTTOM, pady=10)

        self.time_intervals = [1, 2]
        self.data_points = [self.gre_initial_val, self.gre_final_val+10]
        #self.update_plot()






        # configure canvas for raster creation or upload
        self.canvas_width = 700
        self.canvas = tkinter.Canvas(self, width=self.canvas_width, height=self.canvas_width, bg='white')
        self.canvas.grid(row=0, column=5, rowspan=3)
        #self.colors = ["#2C3333", "#1D267D", "#5C469C", "#0E8388", "#CBE4DE"]
        self.colors = ['rebeccapurple', 'crimson', 'darkorange', 'darkcyan','black']
        self.colors_mapping = {'white':0,'rebeccapurple':1, 'crimson':2, 'darkorange':3,'darkcyan':4,'black':5}
        self.selected_color = self.colors[0]
        self.draw_options_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color='transparent')
        self.draw_options_frame.grid(row=3, column=5)
        self.create_grid()
        self.create_color_buttons()
        self.canvas.bind("<Button-1>", self.start_coloring)
        self.canvas.bind("<B1-Motion>", self.color_cell)
        self.canvas.bind("<ButtonRelease-1>", self.stop_coloring)
        self.is_coloring = False
        
        # Polygon
        self.canvas.bind("<Button-3>", self.start_drawing)
        self.canvas.bind("<B3-Motion>", self.draw_polygon)
        self.canvas.bind("<Button-2>", self.stop_drawing) 
        self.current_polygon = []
        self.is_drawing = False
        self.list_of_polygon_points = []
        self.pixels_inside = None

        self.clear_draw_button = customtkinter.CTkButton(self.draw_options_frame, text='Clear', command=self.create_grid)
        self.clear_draw_button.grid(row=7, column=5, columnspan=5, padx=20, pady=10)
        self.undo_draw_button = customtkinter.CTkButton(self.draw_options_frame, text='Undo', command=self.undo_polygon)
        self.undo_draw_button.grid(row=7, column=0, padx=110, pady=10)
        

        #self.slider_size_draw = 1
        # self.slider_size_draw = customtkinter.CTkSlider(self.draw_options_frame, from_=1, to=5, number_of_steps=4)
        # self.slider_size_draw.grid(row=3, column=5, columnspan=5, padx=(20, 10), pady=(10, 10), sticky="ew")


    def create_grid(self):
        #print(self.matrix_array)
        self.cell_size = int(self.canvas['width']) // self.matrix_size
        for row in range(self.matrix_size):
            for col in range(self.matrix_size):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill='white', outline='black')
        self.matrix_array = np.zeros((self.matrix_size,self.matrix_size))


    def create_color_buttons(self):
        i=0
        for color in self.colors:
            i+=1
            color_button = tkinter.Button(self.draw_options_frame, bg=color,  width=2, command=lambda c=color: self.select_color(c))
            color_button.grid(row=3, column=4+i)

    def select_color(self, color):
        self.selected_color = color

    def start_coloring(self, event):
        self.is_coloring = True
        self.color_cell(event)

    def color_cell(self, event):
        if self.is_coloring:
            #self.cell_size = int(int(self.canvas['width']) * self.slider_size_draw.get() )// self.matrix_size
            self.cell_size = int(int(self.canvas['width']))// self.matrix_size
            col = event.x // self.cell_size
            row = event.y // self.cell_size
            x1 = col * self.cell_size
            y1 = row * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size

            #print(col, row, x1/12, y1/12, x2,y2)
            canvas_matrix_size = self.canvas_width/self.matrix_size
            x_pos = int(x1/canvas_matrix_size)
            y_pos = int(y1/canvas_matrix_size)
            self.matrix_array[x_pos][y_pos] = self.colors_mapping[self.selected_color]
            
            # Transpose
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.selected_color, outline='black')


    def stop_coloring(self, event):
        self.is_coloring = False
    


    # Polygon draw
    def start_drawing(self, event):
        #print('drawing true')
        self.is_drawing = True
        self.draw_polygon(event)
        
        #self.current_polygon = [event.x, event.y]
        #self.list_of_polygon_points.append(self.current_polygon[0], self.current_polygon[1])
        

    def draw_polygon(self, event):
        if self.is_drawing:
            x, y = event.x, event.y
            self.list_of_polygon_points.append(x)
            self.list_of_polygon_points.append(y)
            #print("x: ",y,"y: ",y)
            self.current_polygon.append(self.canvas.create_oval(
                [x-2,y-2,x+2,y+2],
                outline=self.selected_color, fill=self.selected_color, width=2
            ))

            #print(self.current_polygon)
            #self.current_polygon.pack()


    def stop_drawing(self, event):
        #print("stop drawing")
        if self.is_drawing:
            self.is_drawing = False
            self.fill_cells_under_polygon()
            self.canvas.delete(self.current_polygon)
            self.current_polygon.clear()
            self.list_of_polygon_points.clear()
        self.is_drawing = False
        #print(self.is_drawing)

    def fill_cells_under_polygon(self):
        self.pixels_inside = self.get_pixels_inside_polygon(self.list_of_polygon_points, self.matrix_size,self.matrix_size)

        for (x,y) in self.pixels_inside:
            self.cell_size = int(int(self.canvas['width']))// self.matrix_size
            col = x // self.cell_size
            row = y // self.cell_size
            x1 = col * self.cell_size
            y1 = row * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size

            canvas_matrix_size = self.canvas_width/self.matrix_size
            x_pos = int(x1/canvas_matrix_size)
            y_pos = int(y1/canvas_matrix_size)
            self.matrix_array[x_pos][y_pos] = self.colors_mapping[self.selected_color]
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.selected_color, outline='black')

    def undo_polygon(self):
        for (x,y) in self.pixels_inside:
            self.cell_size = int(int(self.canvas['width']))// self.matrix_size
            col = x // self.cell_size
            row = y // self.cell_size
            x1 = col * self.cell_size
            y1 = row * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size

            canvas_matrix_size = self.canvas_width/self.matrix_size
            x_pos = int(x1/canvas_matrix_size)
            y_pos = int(y1/canvas_matrix_size)
            self.matrix_array[x_pos][y_pos] = self.colors_mapping['white']
            self.canvas.create_rectangle(x1, y1, x2, y2, fill='white', outline='black')
        self.update_percentage_values()

    def is_point_inside_polygon(self,x, y, polygon_coords):
        n = len(polygon_coords)
        inside = False
        p1x, p1y = polygon_coords[0], polygon_coords[1]
        for i in range(0, n + 2, 2):
            p2x, p2y = polygon_coords[i % n], polygon_coords[(i + 1) % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            x_intersection = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                            if p1x == p2x or x <= x_intersection:
                                inside = not inside
            p1x, p1y = p2x, p2y
        return inside

    def get_pixels_inside_polygon(self,polygon_item, canvas_width, canvas_height):
        polygon_coords = polygon_item
        #print(polygon_coords)
        min_x, max_x = min(polygon_coords[::2]), max(polygon_coords[::2])
        min_y, max_y = min(polygon_coords[1::2]), max(polygon_coords[1::2])

        pixels_inside = []
        for x in range(int(min_x), int(max_x) + 1):
            for y in range(int(min_y), int(max_y) + 1):
                if self.is_point_inside_polygon(x, y, polygon_coords):
                    pixels_inside.append((x, y))

        return pixels_inside




        # Graph

    def update_plot(self):
        # Clear the previous plot and update with new data

        # self.canvas_graphs.destroy()
        self.canvas_widget.destroy()
        self.canvas_graphs = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas_widget = self.canvas_graphs.get_tk_widget()
        self.canvas_widget.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        self.plot.clear()
        self.data_points = [self.gre_initial_val, self.gre_final_val]
        # for i in range(len(self.time_intervals)):
        #     plt.annotate(self.data_points[i], (self.time_intervals[i], self.data_points[i] + 0.2))
        self.plot.plot(self.time_intervals, self.data_points, marker='p', color='darkcyan')



        self.plot.set_xlabel('Time Interval')
        self.plot.set_ylabel('Percentage of Green Areas')
        self.plot.set_title('Change in Percentage of Green Areas over Time')
        #self.canvas.draw()



    def save_matrix_array(self):
        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y--%H:%M:%S")
        with open('modelo_{date}.npy'.format(date=dt_string), 'wb') as f:
            np.save(f, self.matrix_array)

    def load_matrix_array(self):
        filename = askopenfilename()
        if filename:
            self.matrix_array = np.load(filename)
            self.matrix_size = self.matrix_array.shape[0]
        self.change_grid_size(str(self.matrix_size))
        if filename:    # Load again because create_grid erases the matrix_array 
            self.matrix_array = np.load(filename)
        for x in range(self.matrix_size):
            for y in range(self.matrix_size):
                #print(x,y,x+self.cell_size,y+self.cell_size)
                x1 = x*self.cell_size
                y1 = y*self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.canvas.create_rectangle(x1,y1,x2,y2, fill=list(self.colors_mapping.keys())[list(self.colors_mapping.values()).index(int(self.matrix_array[x][y]))], outline='black')
        self.update_percentage_values()

    def update_percentage_values(self):
        self.ind_initial_val = (np.count_nonzero(self.matrix_array==1) / self.total_number_cells) *100
        self.com_initial_val = (np.count_nonzero(self.matrix_array==2) / self.total_number_cells) *100
        self.res_initial_val = (np.count_nonzero(self.matrix_array==3) / self.total_number_cells) *100
        self.gre_initial_val = (np.count_nonzero(self.matrix_array==4) / self.total_number_cells) *100
        self.vac_initial_val = (np.count_nonzero(self.matrix_array==5) / self.total_number_cells) *100
        self.cell_perc_initial_value = [self.ind_initial_val, self.com_initial_val, self.res_initial_val, self.gre_initial_val, self.vac_initial_val]


        for row in range(1,6):
            label = customtkinter.CTkLabel(self.tabview.tab("Cell %"), text=self.land_categories[row-1], fg_color="transparent")
            label.grid(row=row, column=0)
            label = customtkinter.CTkLabel(self.tabview.tab("Cell %"), text=" " + str(self.cell_perc_initial_value[row-1])[0:4] + " ", fg_color="transparent")
            label.grid(row=row, column=1)


    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def set_label_parameter_interactions(self, value):
        self.interactions_parameter.configure(text = "Number of Interactions: " + str(int(value)))
    def set_label_parameter_perturbation(self, value):
        self.perturbation_parameter.configure(text = "Perturbation: " + str(value)[0:4])
    def set_label_parameter_radius(self, value):
        self.radius_parameter.configure(text = "Moore Neighborhood (Radius): " + str(int(value)))

    def change_grid_size(self, value):
        #self.cell_size = int(self.canvas['width']) // self.matrix_size
        self.grid_size_label.configure(text = "Grid Size: " + value)
        self.matrix_size = int(value)
        self.total_number_cells = self.matrix_size*self.matrix_size
        self.canvas.destroy()
        
        self.canvas_width = 600 + int(value)
        self.canvas = tkinter.Canvas(self, width=self.canvas_width, height=self.canvas_width, bg='white')
        self.canvas.grid(row=0, column=5, rowspan=3)
        # self.create_grid()
        self.canvas.bind("<Button-1>", self.start_coloring)
        self.canvas.bind("<B1-Motion>", self.color_cell)
        self.canvas.bind("<ButtonRelease-1>", self.stop_coloring)
        self.is_coloring = False

        #Polygon creator initial states
        self.canvas.bind("<Button-3>", self.start_drawing)
        self.canvas.bind("<B3-Motion>", self.draw_polygon)
        self.canvas.bind("<Button-2>", self.stop_drawing) 
        self.current_polygon = []
        self.is_drawing = False
        self.list_of_polygon_points = []

        self.create_grid()

    def random_fill(self):
        for x in range(self.matrix_size):
            for y in range(self.matrix_size):
                #print(x,y,x+self.cell_size,y+self.cell_size)
                x1 = x*self.cell_size
                y1 = y*self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                color = randint(1,5)
                canvas_matrix_size = self.canvas_width/self.matrix_size
                x_pos = int(x1/canvas_matrix_size)
                y_pos = int(y1/canvas_matrix_size)
                self.matrix_array[x_pos][y_pos] = color
                self.canvas.create_rectangle(x1,y1,x2,y2, fill=list(self.colors_mapping.keys())[list(self.colors_mapping.values()).index(color)], outline='black')


    def save_table_data(self):
        self.table_data = np.zeros((self.table_rows, self.table_columns), dtype=int)
        for i in range(self.table_rows):
            for j in range(self.table_columns):
                entry = self.entry_widgets[i][j]
                value = entry.get()
                try:
                    self.table_data[i, j] = float(value)
                except ValueError:
                    pass

        print("Saved data to NumPy array:\n", self.table_data)

        with open('table_data.npy','wb') as f:
            np.save(f, self.table_data)




    def run_simulation(self):
        utils = CA_Utils()
        ##for _ in range(int(self.slider_interactions_value)):
        #self.matrix_array = utils.update_array(self.matrix_array)
        
        changed_state_matrix = None

        try:
            if self.weights_matrix.any():
                
                for iteration_num in range(int(self.slider_interactions.get())):
                    changed_state_matrix = utils.white_transition(self.matrix_array, self.weights_matrix)
                    
                    print("\n\n\n##########\n\n","iteration: ", iteration_num+1,  "changed_state_matrix: ", changed_state_matrix)

                    for x in range(self.matrix_size):
                        for y in range(self.matrix_size):
                            #print(x,y,x+self.cell_size,y+self.cell_size)
                            x1 = x*self.cell_size
                            y1 = y*self.cell_size
                            x2 = x1 + self.cell_size
                            y2 = y1 + self.cell_size
                            self.canvas.create_rectangle(x1,y1,x2,y2, fill=list(self.colors_mapping.keys())[list(self.colors_mapping.values()).index(int(changed_state_matrix[x][y]))], outline='black')
                    #self.update_percentage_values()


                    self.ind_final_val = (np.count_nonzero(changed_state_matrix==1) / self.total_number_cells) *100
                    self.com_final_val = (np.count_nonzero(changed_state_matrix==2) / self.total_number_cells) *100
                    self.res_final_val = (np.count_nonzero(changed_state_matrix==3) / self.total_number_cells) *100
                    self.gre_final_val = (np.count_nonzero(changed_state_matrix==4) / self.total_number_cells) *100
                    self.vac_final_val = (np.count_nonzero(changed_state_matrix==5) / self.total_number_cells) *100
                    self.cell_perc_final_value = [self.ind_final_val, self.com_final_val, self.res_final_val, self.gre_final_val, self.vac_final_val]

                    for row in range(1,6):
                        label_final = customtkinter.CTkLabel(self.tabview.tab("Cell %"), text=self.land_categories[row-1], fg_color="transparent")
                        label_final.grid(row=row, column=4)
                        label_final = customtkinter.CTkLabel(self.tabview.tab("Cell %"), text= " " + str(self.cell_perc_final_value[row-1])[0:4] + "  ", fg_color="transparent")
                        label_final.grid(row=row, column=5)

                    # time.sleep(1)
                    self.matrix_array = changed_state_matrix
        except Exception as error: print("Error (either missing weights file or something else): ", error, "\n\n", traceback.format_exc())

        




    def load_weights(self):

        filename = askopenfilename()
        if filename:
            weights_file = pd.read_excel(filename)

            print(weights_file)

            weights_file = weights_file.dropna()
            weights_file.drop(columns=weights_file.columns[0], axis=1, inplace=True)

            weights_file_np = weights_file.to_numpy()
            print(weights_file_np)
            print(weights_file_np.shape)
            self.weights_matrix = weights_file_np






            

        



if __name__ == "__main__":
    app = App()
    app.mainloop()