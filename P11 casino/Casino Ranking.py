import pandas as pd
import tkinter as tk
from tkinter import PhotoImage

h = 1000
w = 1900

def load_ranking_data_frame():
    ranking_data_frame = pd.read_excel("database.xlsx", 
                       sheet_name="ランキング", 
                       usecols="A:C", 
                       nrows=5, 
                       header=None)
    ranking_data_frame = ranking_data_frame.fillna("")
    ranking_data_list = ranking_data_frame.values.tolist()
    return ranking_data_list

def update_ranking():

    canvas.delete("all")
    
    canvas.create_image(0, 0, image=bg, anchor="nw")
    
    
    ranking_data_frame = load_ranking_data_frame()
    
    num_rows = len(ranking_data_frame) + 1
    num_cols = len(ranking_data_frame[0]) if ranking_data_frame else 3
    cell_width = 800
    cell_height = 120
    table_width = num_cols * cell_width
    table_height = num_rows * cell_height


    start_x = (w - table_width) // 2
    start_y = (h - table_height) // 2

    # Headers
    headers = ['ランク(位)', 'ニックネーム', 'ポイント']
    for col, header in enumerate(headers):
        canvas.create_text(
            start_x + col * cell_width + cell_width // 2, start_y + cell_height // 2,
            text=header, 
            font=('Arial', 30, 'bold'), 
            fill="white", 
            anchor="center"
        )
    

    for row_num, row_data in enumerate(ranking_data_frame, start=1):
        for col_num, cell_data in enumerate(row_data):

            if isinstance(cell_data, float) and cell_data.is_integer():
                cell_data = int(cell_data)
            
            font_size = 40
            font_weight = 'normal'
            font_color = 'white'
    
            if row_num == 1:
                font_size = 100
                font_color = "#E5B80B"
                font_weight = 'bold'
            elif row_num == 2:
                font_size = 70
                font_color = "#AFb1AE"
                font_weight = 'bold'
            elif row_num == 3:
                font_size = 50
                font_color = "#D37731"
                font_weight = 'bold'
    
            canvas.create_text(
                start_x + col_num * cell_width + cell_width // 2, start_y + row_num * cell_height + cell_height // 2,
                text=cell_data, 
                font=('Arial', font_size, font_weight), 
                fill=font_color, 
                anchor="center"
            )


    root.after(5000, update_ranking)


root = tk.Tk()
root.title("カジノランキング")


root.geometry(f"{w}x{h}")

bg = PhotoImage(file="background.png")
ic = PhotoImage(file="icon.png")
root.iconphoto(True, ic)

canvas = tk.Canvas(root, width=w, height=h)
canvas.pack(fill="both", expand=True)


update_ranking()


root.mainloop()
