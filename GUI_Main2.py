import tkinter
import tkinter.messagebox
import customtkinter
from PIL import Image, ImageTk

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Tesis Ila")
        self.geometry(f"{1300}x{700}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure((1,2,3,4,5), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=100, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsw")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Thesis Project: Ilana Villanueva Carrión", font=customtkinter.CTkFont(size=10, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # ADD LOGO IMAGE *
        # button_image = customtkinter.CTkImage(Image.open("images/urbandevelopment.png"), size=(100, 50))
        # image_button = customtkinter.CTkLabel(self,image=button_image, text="")
        # image_button.grid(row=0, column=0)
        
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text='Run', command=self.sidebar_button_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text='Save',command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text='Load',command=self.sidebar_button_event)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
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



        # configure canvas for raster creation or upload
        self.matrix_size = 200
        self.canvas = tkinter.Canvas(self, width=600, height=600, bg='white')
        self.canvas.grid(row=0, column=5)
        self.colors = ["#2C3333", "#1D267D", "#5C469C", "#0E8388", "#CBE4DE"]
        self.selected_color = self.colors[0]
        self.create_grid()
        self.create_color_buttons()
        self.canvas.bind("<Button-1>", self.start_coloring)
        self.canvas.bind("<B1-Motion>", self.color_cell)
        self.canvas.bind("<ButtonRelease-1>", self.stop_coloring)
        self.is_coloring = False


    def create_grid(self):
        cell_size = int(self.canvas['width']) // self.matrix_size
        for row in range(self.matrix_size):
            for col in range(self.matrix_size):
                x1 = col * cell_size
                y1 = row * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill='white', outline='black')

    def create_color_buttons(self):
        # button_frame = tkinter.Frame(self)
        # button_frame.grid(column=1, row=3)
        draw_options_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color='transparent')
        draw_options_frame.grid(row=3, column=5)

        slider_size_draw = customtkinter.CTkSlider(draw_options_frame, from_=0, to=1, number_of_steps=10)
        slider_size_draw.grid(row=3, column=5, padx=(20, 10), pady=(10, 10), sticky="ew")

        i=0
        for color in self.colors:
            i+=50
            color_button = tkinter.Button(draw_options_frame, bg=color,  width=2, command=lambda c=color: self.select_color(c))
            color_button.grid(row=4, column=5, padx=10+i)

    def select_color(self, color):
        self.selected_color = color

    def start_coloring(self, event):
        self.is_coloring = True
        self.color_cell(event)

    def color_cell(self, event):
        if self.is_coloring:
            cell_size = int(self.canvas['width']) // self.matrix_size
            col = event.x // cell_size
            row = event.y // cell_size
            x1 = col * cell_size
            y1 = row * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size

            self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.selected_color, outline='black')

    def stop_coloring(self, event):
        self.is_coloring = False

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")




if __name__ == "__main__":
    app = App()
    app.mainloop()