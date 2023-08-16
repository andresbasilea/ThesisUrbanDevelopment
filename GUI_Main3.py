import tkinter
import tkinter.messagebox
import customtkinter
from PIL import Image, ImageTk
import numpy as np
from tkinter.filedialog import askopenfilename, asksaveasfilename
from datetime import datetime
from random import randint

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


        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=100, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsw")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Thesis Project:", font=customtkinter.CTkFont(size=14, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Ilana Villanueva Carrión", font=customtkinter.CTkFont(size=14, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(70, 10))
        
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text='Run')
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
        self.tabview.add("Weights")
        
        # tabview cell % tab
        self.tabview.tab("Cell %").grid_columnconfigure((0,1,2,3,4,5,6), weight=1)  # configure grid of individual tabs
        self.cell_perc_initial_label = customtkinter.CTkLabel(self.tabview.tab("Cell %"), text="Initial Cells %", anchor="w", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.cell_perc_initial_label.grid(row=0, column=0, columnspan=2)
        self.cell_perc_end_label = customtkinter.CTkLabel(self.tabview.tab("Cell %"), text="End Cells %", anchor="e", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.cell_perc_end_label.grid(row=0, column=4, columnspan=2)
        self.update_percentage_button = customtkinter.CTkButton(self.tabview.tab("Cell %"), text='Update Percentages', command=self.update_percentage_values)
        self.update_percentage_button.grid(row=8, column=2, columnspan=2, padx=20, pady=10)
        self.land_categories = ['Industrial', 'Commercial', 'Residential', 'Green', 'Vacant']
        self.ind_initial_val = np.count_nonzero(self.matrix_array==1) / self.total_number_cells
        self.com_initial_val = np.count_nonzero(self.matrix_array==2) / self.total_number_cells
        self.res_initial_val = np.count_nonzero(self.matrix_array==3) / self.total_number_cells
        self.gre_initial_val = np.count_nonzero(self.matrix_array==4) / self.total_number_cells
        self.vac_initial_val = np.count_nonzero(self.matrix_array==5) / self.total_number_cells
        self.cell_perc_initial_value = [self.ind_initial_val, self.com_initial_val, self.res_initial_val, self.gre_initial_val, self.vac_initial_val]
        self.cell_perc_end_value = [ 0.0,0.0,0.0,0.0,0.0]
        for row in range(1,6):
            label = customtkinter.CTkLabel(self.tabview.tab("Cell %"), text=self.land_categories[row-1], fg_color="transparent")
            label.grid(row=row, column=0)
            label = customtkinter.CTkLabel(self.tabview.tab("Cell %"), text=self.cell_perc_initial_value[row-1], fg_color="transparent")
            label.grid(row=row, column=1)

        for row in range(1,6):
            label = customtkinter.CTkLabel(self.tabview.tab("Cell %"), text=self.land_categories[row-1], fg_color="transparent")
            label.grid(row=row, column=4)
            label = customtkinter.CTkLabel(self.tabview.tab("Cell %"), text=self.cell_perc_end_value[row-1], fg_color="transparent")
            label.grid(row=row, column=5)

        # tabview parameters tab
        self.tabview.tab("Parameters").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Parameters").grid_rowconfigure((0,1,2,3,4,5), weight=1)

        self.slider_interactions = customtkinter.CTkSlider(self.tabview.tab("Parameters"), from_=1, to=40, number_of_steps=39, command=self.set_label_parameter_interactions)
        self.slider_interactions.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.slider_interactions_value = str(int(self.slider_interactions.get()))
        self.interactions_parameter = customtkinter.CTkLabel(self.tabview.tab("Parameters"), text="Number of Interactions: " + self.slider_interactions_value , fg_color="transparent")
        self.interactions_parameter.grid(row=0, column=0)

        self.slider_perturbation = customtkinter.CTkSlider(self.tabview.tab("Parameters"), from_=0, to=1, number_of_steps=100, command=self.set_label_parameter_perturbation)
        self.slider_perturbation.grid(row=3, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.slider_perturbation_value = str(self.slider_perturbation.get())
        self.perturbation_parameter = customtkinter.CTkLabel(self.tabview.tab("Parameters"), text="Perturbation: " + self.slider_perturbation_value, fg_color="transparent")
        self.perturbation_parameter.grid(row=2, column=0)

        self.slider_radius = customtkinter.CTkSlider(self.tabview.tab("Parameters"), from_=1, to=10, number_of_steps=10, command=self.set_label_parameter_radius)
        self.slider_radius.grid(row=5, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.slider_radius.set(8)
        self.slider_radius_value = str(int(self.slider_radius.get()))
        self.radius_parameter = customtkinter.CTkLabel(self.tabview.tab("Parameters"), text="Moore Neighborhood (Radius): " + self.slider_radius_value, fg_color="transparent")
        self.radius_parameter.grid(row=4, column=0)







        self.tabview.tab("Weights").grid_columnconfigure(0, weight=1)



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
        self.clear_draw_button = customtkinter.CTkButton(self.draw_options_frame, text='Clear', command=self.create_grid)
        self.clear_draw_button.grid(row=7, column=5, columnspan=5, padx=20, pady=10)
        

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

            # print(col, row, x1/12, y1/12, x2,y2)
            canvas_matrix_size = self.canvas_width/self.matrix_size
            x_pos = int(x1/canvas_matrix_size)
            y_pos = int(y1/canvas_matrix_size)
            self.matrix_array[x_pos][y_pos] = self.colors_mapping[self.selected_color]
            
            # Transpose
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.selected_color, outline='black')

            
            

    def stop_coloring(self, event):
        self.is_coloring = False
    
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
        self.grid_size_label.configure(text = "Grid Size: " + value)
        self.matrix_size = int(value)
        self.total_number_cells = self.matrix_size*self.matrix_size
        self.canvas.destroy()
        # configure canvas for raster creation or upload
        self.canvas_width = 600 + int(value)
        self.canvas = tkinter.Canvas(self, width=self.canvas_width, height=self.canvas_width, bg='white')
        self.canvas.grid(row=0, column=5, rowspan=3)
        # self.create_grid()
        self.canvas.bind("<Button-1>", self.start_coloring)
        self.canvas.bind("<B1-Motion>", self.color_cell)
        self.canvas.bind("<ButtonRelease-1>", self.stop_coloring)
        self.is_coloring = False
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



if __name__ == "__main__":
    app = App()
    app.mainloop()