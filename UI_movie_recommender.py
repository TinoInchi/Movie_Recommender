import customtkinter as ctk
from Rec_Logic import *


class ComboBoxManager(ctk.CTkComboBox):
    # Makes comboboxes with the needed value
    def __init__(self, frame, list_values):
        super().__init__(master=frame)
        self.list_values = list_values
        if len(self.list_values) > 100:
            pass
        else:
            self.configure(values=self.list_values)
        self.set('')
        self.bind("<KeyRelease>", self.update_options)
        self.bind("<BackSpace>", self.update_options)
    
    # Updates the choice in dropbox movie after manual typing
    def update_options(self, event):
        self.current_input = self.get()
        filtered_options = [option for option in self.list_values if self.current_input.lower() in option.lower()]
        if len(filtered_options) <100:
            self.configure(values=filtered_options)
        self.event_generate('<Down>')


class MovieRecommenderApp(ctk.CTk):
    def __init__(self, list_of_all_genres,movie_titles, movies, reviews):
        super().__init__()
        # set appearance
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme('dark-blue')

        # define lists and df from main
        self.list_of_all_genres = list_of_all_genres
        self.movies = movies
        self.reviews = reviews
        self.movie_titles = movie_titles

        # set display geometry and title
        self.title("Movie Recommender")
        self.state('zoomed') 
        self.width = 1100
        self.height = 580
        self.geometry(f"{self.width}x{self.height}")

        # set grid
        self.grid_columnconfigure(0,weight=0)
        self.grid_columnconfigure(1,weight=1)
        self.grid_rowconfigure((0,1,2),weight=1)

        # Sidebar Frame
        self.sidebar_frame = ctk.CTkFrame(self, width=250, fg_color='grey15', corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.label_sidebar = ctk.CTkLabel(self.sidebar_frame, text='MovieRe', font=ctk.CTkFont(size=25, weight="bold"),anchor='center')
        self.label_sidebar.grid(row=0, column=0, padx = 55, pady = 40)

        self.button_menu_sidebar = ctk.CTkButton(self.sidebar_frame, text="Menu", corner_radius = 0, height = 40, state='disabled')
        self.button_menu_sidebar.grid(row=1, column = 0, pady = 0, sticky = 'ew')
        self.button_movie_info_sidebar = ctk.CTkButton(self.sidebar_frame, text="Movie Infos", corner_radius = 0, height = 40, state='disabled')
        self.button_movie_info_sidebar.grid(row=2, column = 0, pady = 0, sticky = 'ew')

        # Main Frame

        # Frame definition
        self.main_menu_frame = ctk.CTkFrame(self, width=self.width-250,corner_radius=0)
        self.main_menu_frame.grid(row=0, column=1, rowspan=3, sticky='nsew')
        self.main_menu_frame.grid_rowconfigure(6, weight=1)
        self.main_menu_frame.grid_columnconfigure(2, weight=1)

        # Text lable
        self.text_title = "Find the Movie you watched in the Title section and choose a genre, if any.\n"\
            +"Start typing the movie into movie slot and it will show you the available movies.\n"\
            +"Click on submit and it will show you some recommendation!"
        self.title_label = ctk.CTkLabel(self.main_menu_frame, text=self.text_title, font=ctk.CTkFont(size=15), anchor='center',justify='left')
        self.title_label.grid(row=0, column=0, columnspan=3, padx = 50, pady = 40, sticky='ew')

        # text labels for the dropdown boxes (movie)
        self.label1 = ctk.CTkLabel(self.main_menu_frame, text="Movie Title",font=ctk.CTkFont(size=15, weight="bold"))
        self.label1.grid(row = 1, column = 0, padx = 40 ,sticky='w')

        # text labels for the dropdown boxes (genre)
        self.label2 = ctk.CTkLabel(self.main_menu_frame, text="Genre",font=ctk.CTkFont(size=15, weight="bold"))
        self.label2.grid(row = 1, column = 1, padx = 10 ,sticky='w')

        # Makes dropdown option with the class comboboxmanager
        self.dropdown1 = ComboBoxManager(self.main_menu_frame, self.movie_titles)
        self.dropdown1.grid(row=2, column=0, padx=40, pady=5, sticky='w')

        self.dropdown2 = ComboBoxManager(self.main_menu_frame, self.list_of_all_genres)
        self.dropdown2.grid(row=2, column=1, padx=10, pady=5, sticky='w')

        # Submit button
        self.submit_btn = ctk.CTkButton(self.main_menu_frame, text="Submit", command=self.process_input)
        self.submit_btn.grid(row = 3, column = 0, padx = 40, pady = 10 ,sticky='w')

        # Clear button
        self.clear_btn = ctk.CTkButton(self.main_menu_frame, text="Clear", command=self.clear_selection)
        self.clear_btn.grid(row = 4, column = 0, padx = 40, pady = 0,sticky='w')

        # Frame for result table
        self.result_frame = ctk.CTkFrame(self, width=self.width-250,corner_radius=0)
        self.result_frame.grid(row=2, column=1, sticky='nsew')
        self.result_frame.grid_rowconfigure(0, weight=1)

        # Label for displaying results
        self.output_table_title = ctk.CTkLabel(self.result_frame, text="", font=ctk.CTkFont(size=15, weight="bold"),justify='left')
        self.output_table_title.grid(row = 0, column = 0, padx = 20 ,sticky='w')
        self.output_table_year = ctk.CTkLabel(self.result_frame, text="", font=ctk.CTkFont(size=15, weight="bold"),justify='left')
        self.output_table_year.grid(row = 0, column = 1, padx = 5,sticky='w')
        self.output_table_genre = ctk.CTkLabel(self.result_frame, text="", font=ctk.CTkFont(size=15, weight="bold"),justify='left')
        self.output_table_genre.grid(row = 0, column = 2, padx = 5 ,sticky='w')
    
    # Event Function after pressing clear button -> clear the entries
    def clear_selection(self):
        self.dropdown1.set('')
        self.dropdown2.set('')
        self.output_table_title.configure(text='')
        self.output_table_year.configure(text='')
        self.output_table_genre.configure(text='')

    # Event function after pressing submit button -> calculates results and displays them
    def process_input(self):
        title = self.dropdown1.get()
        genre = self.dropdown2.get()

        # Error Handling
        if title not in self.movies['title'].to_list():
            text_na = 'The movie cannot be found in the data set.\n'\
                + 'Please put only available options'
            self.output_table_title.configure(text = text_na)
        elif genre not in self.list_of_all_genres:
            text_na = 'The genre cannot be found in the data set.\n'\
                + 'Please put only available options'
            self.output_table_title.configure(text = text_na)
        elif genre not in self.movies[self.movies['title'] == title]['split_genre'].to_list()[0]:
            text_na = 'The movie does not contain this genre.\n'\
                + 'Please chose another genre'
            self.output_table_title.configure(text = text_na)

        else:
            result = check_genre_with_rec(title, genre, self.movies, self.reviews)
            result_text = f"{'Title':<35}\n\n"
            result_year = f"{'Year':<10}\n\n"
            result_genre = f"{'Genre':<80}\n\n"
            for count in range(len(result.index)):
                result_text += f"{result.iloc[count,0]:<35}\n"
                result_year += f"{result.iloc[count,1]:<10}\n"
                result_genre += f"{result.iloc[count,2]:<80}\n"
            self.output_table_title.configure(text=result_text)
            self.output_table_year.configure(text=result_year)
            self.output_table_genre.configure(text=result_genre)
