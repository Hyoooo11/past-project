from table_builder import TableBuilder
 
h_size : int = 0
html : str = "<html>"
title : str = "<title>"
style : str = "<style>"
head : str = "<head>"
h : str = f"<h{h_size}>"
body : str = "<body>"
 
 
html_close : str = "</html>"
title_close : str = "</title>"
style_close : str = "</style>"
head_close : str = "</head>"
h_close : str = f"</h{h_size}>"
body_close : str = "</body>"
 
table_content = []
 
def create_table():
    table_builder = TableBuilder()
 
    while True:
        user_input = input().split('|')
 
        if user_input == ["end"]:
            break
        elif user_input == ["-1"]:
            table_builder.remove_last_row()
            continue
 
        table_builder.add_row(user_input)
 
    return table_builder
 
 
def result():
    print("heres your base html code :")
    print(html)
    print(head)
    print(title)
    print(f"    {title_input}")
    print(title_close)
    print(head_close)
    if background_confirm:
        print(style)
        print("    body{")
        print(f"        background-color : {background_color_choice}")
        print("    }")
        print(style_close)
    print(body)
    if table_confirm:
        print(table_content.build_table())
    print(body_close)
    print(html_close)
 
 
print("website title :")
 
title_input : str = input()
 
print("do you want background color : ")
 
background_confirm_input : str = input()
background_confirm : bool = False
 
if background_confirm_input == "yes":
    background_confirm = True
    print("what color do you want : ")
    background_color_choice : str= input()
 
print("do you want to put a table in your html :")
 
table_confirm_input : str = input()
table_confirm : bool = False
 
if table_confirm_input == "yes":
    table_confirm = True
    print("please insert your table content (separate columns with -> | ): ")
    table_content = create_table()
result()