import tkinter as tk
from PIL import Image, ImageTk
import random

# ゲーム設定
charsize = 70
startx = 150
starty = 200
h = 750
w = 550
floorcollision = h - 5

jump_strength = -18

point = 0
leaderboard = []

# tkinter ウィンドウ
win = tk.Tk()
win.title("Meow Meow Rocket")

# キャラと背景と障害物の画像を呼び出し
char_img_original = Image.open("meowrocket.png")
char_img_original = char_img_original.resize((charsize, charsize))
char_img = ImageTk.PhotoImage(char_img_original)

backimg1 = tk.PhotoImage(file="spacebackground.png")
backimg2 = tk.PhotoImage(file="spacebackground.png")

obstacle1 = Image.open("obstacle1.png")
obstacle1 = obstacle1.resize((70,750))
obstacle2 = Image.open("obstacle2.png")
obstacle2 = obstacle2.resize((70,750))
obstacle3 = Image.open("obstacle3.png")
obstacle3 = obstacle3.resize((70,750))

obstacle1_img = ImageTk.PhotoImage(obstacle1)
obstacle2_img = ImageTk.PhotoImage(obstacle2)
obstacle3_img = ImageTk.PhotoImage(obstacle3)
# Canvasはgameという名前を使います
game = tk.Canvas(win, width=w, height=h)
game.pack()

# 地面
back1 = game.create_image(0, int(h / 2), image=backimg1, anchor='w')
back2 = game.create_image(w, int(h / 2), image=backimg2, anchor='w')

ground = game.create_rectangle(0, floorcollision, w, h, fill="", outline="")

# 背景を後ろに移動
game.tag_lower(back1)
game.tag_lower(back2)

# ゲームオーバーフラグ
game_over = False

class Character:
    def __init__(self, canvas):
        
        self.x = startx
        self.y = starty
        self.width = charsize
        self.height = charsize
        self.canvas = canvas
        self.velocity = 0
        self.gravity = 1.5
        self.jump_strength = -21
        self.char_img_original = char_img_original
        self.char_img = char_img
        
        self.char = canvas.create_image(self.x + int(self.width / 2), 
                                        self.y + int(self.height / 2), 
                                        image=self.char_img)
        # キャラヒットボックス
        self.charcollision = canvas.create_oval(self.x, 
                                                self.y, 
                                                self.x + self.width, 
                                                self.y + self.height, 
                                                fill="", 
                                                outline="")

    def move(self):
        self.velocity += self.gravity  # 重力

        # キャラ向き更新
        max_tilt = 40  # 最大向き角度
        tilt_angle = max(-max_tilt, min(max_tilt, -self.velocity * 2))  # 速度に合わせた角度設定
        rotated_img = self.char_img_original.rotate(tilt_angle, resample=Image.BICUBIC)
        
        self.char_img = ImageTk.PhotoImage(rotated_img)

        # キャラ向きのイメージも更新します
        self.canvas.itemconfig(self.char, image=self.char_img)

        # キャラの動き
        self.canvas.move(self.charcollision, 0, self.velocity)
        self.canvas.move(self.char, 0, self.velocity)

    def jump(self):
        self.velocity = self.jump_strength  # ジャンプの速度をリセットする

    def check_ground_collision(self, ground_coords):
        charcollision_coords = self.canvas.coords(self.charcollision) 
        
        # 地面当たりチェック
        if (charcollision_coords[2] > ground_coords[0] and
            charcollision_coords[0] < ground_coords[2] and
            charcollision_coords[3] > ground_coords[1] and
            charcollision_coords[1] < ground_coords[3]):
            return True  # 当たりフラグ

        return False

    def stop_at_ground(self, floor):
        # 下以下にいかないように
        coords = self.canvas.coords(self.charcollision)
        if coords[3] >= floor:
            self.canvas.coords(self.charcollision, 
                               coords[0], 
                               floor - self.height, 
                               coords[2], floor)
            self.velocity = 0  # 地面に当たったら止まり

    def check_obstacle_collision(self, obstacles):
        # 障害物座標チェック
        charcollision_coords = self.canvas.coords(self.charcollision)
        
        for obstacle in obstacles:
            # 障害物座標呼び出し
            top_coords = self.canvas.coords(obstacle.top)
            bottom_coords = self.canvas.coords(obstacle.bottom)
            
            # 下の障害物の当たりチェック
            if (charcollision_coords[2] > bottom_coords[0] and
                charcollision_coords[0] < bottom_coords[2] and
                charcollision_coords[3] > bottom_coords[1] and
                charcollision_coords[1] < bottom_coords[3]):
                return True  # 当たりフラグ

            # 上の障害物の当たりチェック
            if (charcollision_coords[2] > top_coords[0] and
                charcollision_coords[0] < top_coords[2] and
                charcollision_coords[3] > top_coords[1] and
                charcollision_coords[1] < top_coords[3]):
                return True  # 当たりフラグ

        return False

# キャラクターインスタンスの作成
character = Character(game)

# キャラクターを動かす関数
def move_charcollision():
    if game_over:
        return  # ゲームが終了したらループを止める

    global velocity

    # キャラクターを動かし、重力を適用
    character.move()

    # 地面の衝突チェックと地面で止まる
    ground_coords = game.coords(ground)
    if character.check_ground_collision(ground_coords):
        game_over_function()  # ゲームオーバー関数を呼ぶ
        return

    # 障害物の衝突チェック
    if character.check_obstacle_collision(obstacles):
        game_over_function()  # ゲームオーバー関数を呼ぶ
        return

    # 必要なら地面で止める
    character.stop_at_ground(floorcollision)

    # この関数を再度呼んでループを維持
    win.after(20, move_charcollision)

# 背景を動かす関数
def move_background():
    if game_over:
        return
    
    game.move(back1, -1, 0)
    game.move(back2, -1, 0)

    # 現在のback1とback2の位置を取得
    back1_x = game.coords(back1)[0]
    back2_x = game.coords(back2)[0]

    # back1が画面外に出たら、その位置をback2の後ろに移動
    if back1_x <= -w:
        game.coords(back1, back2_x + w, int(h / 2))

    # back2が画面外に出たら、その位置をback1の後ろに移動
    if back2_x <= -w:
        game.coords(back2, back1_x + w, int(h / 2))

    # この関数を再度呼んでループを維持
    win.after(20, move_background)

# スペースキーでジャンプ
def jump(event):
    if not game_over:
        character.jump()
 
class Obstacle():
    def __init__(self, canvas, x):
        randh = random.randint(100, 450)  # 下側の障害物の高さをランダムに設定
        randobs = random.randint(1, 3)
        self.gap = 250  # 上下の障害物の間の隙間
        self.x = x
        self.y = h - randh  # 下側の障害物の位置
        self.canvas = canvas
        
        # 使用する画像をランダムに選択
        if randobs == 1:
            self.top_image = obstacle1_img
            self.bottom_image = obstacle1_img
        elif randobs == 2:
            self.top_image = obstacle2_img
            self.bottom_image = obstacle2_img
        else:
            self.top_image = obstacle3_img
            self.bottom_image = obstacle3_img
        
        # 上下の障害物の画像を作成
        self.top_image_id = self.canvas.create_image(self.x, 0, image=self.top_image)
        self.bottom_image_id = self.canvas.create_image(self.x, self.y+375, 
                                                        image=self.bottom_image)
        
        # 上下の障害物の当たり判定ボックスを作成
        self.top = self.canvas.create_rectangle(self.x, 0, self.x + 50, self.y - self.gap, 
                                                fill="", 
                                                outline="")
        self.bottom = self.canvas.create_rectangle(self.x, self.y, self.x + 50, self.y + h, 
                                                   fill="", 
                                                   outline="")
        self.passed = False
        
    def move_left(self):
        self.x -= 1
        self.update_position()

    def update_position(self):
        # 画像と当たり判定ボックスの位置を更新
        self.canvas.coords(self.top_image_id, self.x, self.y-375-self.gap)
        self.canvas.coords(self.bottom_image_id, self.x, self.y+375)
        
        self.canvas.coords(self.top, self.x, 0, self.x + 50, self.y - self.gap)
        self.canvas.coords(self.bottom, self.x, self.y, self.x + 50, self.y + h)

    def delete(self):
        # 画像と当たり判定ボックスを削除
        self.canvas.delete(self.top_image_id)
        self.canvas.delete(self.bottom_image_id)
        self.canvas.delete(self.top)
        self.canvas.delete(self.bottom)


obstacles = []


def create():#障害物作る
    if game_over:
        return  # ゲームオーバーの時は障害物の作成を止める

    new_obstacle = Obstacle(game, w)
    obstacles.append(new_obstacle)
    game.after(3250, create)

def obstacles_mover_deleter():
    if game_over:
        return  # ゲームオーバーの時は障害物の移動を止める

    # 障害物を移動し、必要なら削除
    for obstacle in obstacles[:]:
        obstacle.move_left()

        if obstacle.x <= -50:
            obstacle.delete()
            obstacles.remove(obstacle)
    if obstacles:  # 障害物が残っている場合は次の更新をスケジュール
        game.after(10, obstacles_mover_deleter)  # 10ms後に繰り返し更新
    
# スコアテキストアイテムIDを保持する変数
score_text_id = None

def point_system(): #ポイントシステム
    global point
    global leaderboard
    global score_text_id  # グローバル変数でスコアテキストIDを参照

    # ゲームオーバーでない場合のみポイントシステムを実行
    if game_over:
        leaderboard.append(point)  # 現在のポイントをリーダーボードに追加
        if score_text_id:
            game.delete(score_text_id)  # ゲームオーバー時にスコアテキストを削除
        
        return

    # 現在のキャラクターの位置を取得（キャラクターの中心）
    char_coords = game.coords(character.char)
    char_x = char_coords[0] # キャラクターのX座標
    char_y = char_coords[1] # キャラクターのY座標
    
    # 障害物が通過したかチェック
    for obstacle in obstacles[:]:
        # 障害物のX座標を取得
        obstacle_x = game.coords(obstacle.bottom)[0]  # 障害物の左端

        # キャラクターが障害物を通過した場合（キャラクターのX座標が障害物のX座標より大きい）
        if char_x > obstacle_x and not obstacle.passed:
            if char_y < 0:
                game_over_function()
            point += 1  # スコアを増加
            obstacle.passed = True  # 障害物を通過したことをマーク
            
    # 古いスコアテキストがあれば削除
    if score_text_id:
        game.delete(score_text_id)

    # 新しいスコアテキストを作成
    score_text_id = game.create_text(w / 2, h / 6, 
                                     text=f"{point}", 
                                     font=("arial", 40), 
                                     fill="#FFFFFF")
    
    # 20ms後にスコアを更新するため、関数を再度呼ぶ
    game.after(20, point_system)
    
def gamestart(event=None):
    def delete(event=None):
        game.delete(gametitle, presstostart)
        main()
        win.bind("<space>", jump)
    # Canvasにテキストを表示
    gametitle = game.create_text(w/2, h/2.5, 
                            text="Meow Meow Rocket", 
                            font=("Arial", 40),
                            fill="#FFFFFF")
    presstostart = game.create_text(w/2, h-200, 
                             text="space to start", 
                             font=("Arial", 30),
                             fill="#FFFFFF")

    # スペースキーを押すとテキストを削除
    win.bind('<space>', delete)
    

def main():
    create()
    obstacles_mover_deleter()
    point_system()
    move_charcollision()
    move_background()

# ゲームオーバーのロジック
def game_over_function(event=None):
    
    def delete2(event=None):
        
        global point, game_over, obstacles, character

        # ポイントとゲームオーバーフラグをリセット
        point = 0
        game_over = False

        # ゲームオーバーテキストを削除
        game.delete(highs, restarttext, gameover1, gameover2)
        
        # 背景位置をリセット
        game.coords(back1, 0, int(h / 2))
        game.coords(back2, w, int(h / 2))

        # キャラクター位置をリセットし、現在のキャラクターを削除
        game.delete(character.char, character.charcollision)
        character = Character(game)  # 新しいキャラクターインスタンスを作成

        # 障害物を削除
        for obstacle in obstacles:
            obstacle.delete()
        obstacles.clear()

        # ゲームを再スタート
        main()
        win.bind("<space>", jump) #キー
        
        
    global game_over
    global leaderboard
    global point
    
    game_over = True
    
    leaderboard.append(point)
    
    highscore = max(leaderboard)
    
    highs = game.create_text(w / 2, h / 2, 
                             text=f"High score : {highscore}", 
                             font=("arial", 40), 
                             fill="#FFFFFF")
    
    game.delete(character.charcollision)
    
    restarttext = game.create_text(w/2, h-200, 
                             text="space to restart", 
                             font=("Arial", 30),
                             fill="#FFFFFF")

    gameover1 = game.create_text(w / 2, h / 6, 
                                     text="Game Over!", 
                                     font=("arial", 40), 
                                     fill="#FFFFFF")
    gameover2 = game.create_text(w / 2, h / 6 + 50, 
                                 text=f"Score: {point}", 
                                 font=("arial", 40), 
                                 fill="#FFFFFF")
    #ゲームオーバー1秒待つ
    win.after(3250, lambda: win.bind('<space>', delete2))
    
    
gamestart()


win.mainloop()
