from time import *
import os
import random
from typing import *
import sys

# プレイヤーの基礎ステータス
PLAYER_HP = 20
# スタミナが12ではAIでクリアすることが難しかったため、15に設定いたしました
PLAYER_STAMINA = 15
PLAYER_ATTACK = 3

# プレイヤーのステータスの定数
HP = 0
STAMINA = 1
ATTACK = 2
WEAPON = 3
GOLD = 4
SCORE = 5

# 部屋の種類
TREASUREROOM = "T"
WEAPONROOM = "W"
GOLDROOM = "G"
EVENTROOM = "E"
SHOPROOM = "!"
KEYROOM = "K"
BOSSKEYROOM = "B"
MONSTERROOM = "M"
STARTROOM = "S"

BOSS_ROOM_POSITION = (3, 6) #追加

MEDICINE_RECOVER_HP = 1   # HP回復薬.
MEDICINE_RECOVER_STAMINA = 2   # スタミナ回復薬.
YELLOW_WEAPON = 3   # 黄色武器.
PINK_WEAPON = 4   # ピンク色武器.

#追加 スコア用の定数
HP_SCORE = 300
STAMINA_SCORE = 1200
GOLD_SCORE = 600
ENEMY_SCORE = 2000
WIN_SCORE = 10000
TREASURE_SCORE = 5000

# print()用のカラーコード
COLOR_DICT = {"Black" : "\033[30m", "Red" : "\033[31m", "Green" : "\033[32m", "Yellow" : "\033[33m", "Blue" : "\033[34m", "Magenta" : "\033[35m", "Cyan" : "\033[36m", "White" : "\033[37m"}
END = "\033[0m"

#人工知能に用いる定数を定義
DUNGEON_MAP = [[0, 3], [1, 2], [1, 4], [2, 1], [2, 3], [2, 5], [3, 0], [3, 2], [3, 4], [3, 6], [4, 1], [4, 3], [4, 5], [5, 2], [5, 4], [6, 3]]
IMPORTANT_ROOMS = [BOSSKEYROOM,TREASUREROOM, EVENTROOM, SHOPROOM, KEYROOM]
#ボス部屋に行く条件の重要な部屋数　マップ1では6、マップ2，3では5になるが、マップ1でも5こ回れば、ボスにも勝てるので5個に設定
IMPORTANT_ROOM_NUM = 5

DIR_DICT = {(-1, 1):"1", (1, 1):"2", (-1, -1):"8", (1, -1):"9"}

class Weapon:
    def __init__(self, name: str = "", attack: int = 0, color: str = ""):
        """
        武器の情報を持つクラス.\n
        Args: 
            name (str) : 武器の名前.\n
            attack (int) : 武器の攻撃力.\n
            color (str) : 武器の色.
            
        Vars: 
            name (str) : 武器の名前を保持.\n
            attack (int) : 武器の攻撃力を保持.\n
            color (str) : 武器の色を保持.
        """
        self.name: str = name
        self.attack: int = attack
        self.color: str = color


class Player:
    def __init__(self):
        """
        プレイヤーの情報を持つクラス.\n
        Vars: 
            hp (int) : プレイヤーの現在のhpを保持.\n
            stamina (int) : プレイヤーの現在のスタミナを保持.\n
            attack (int) : プレイヤーの現在の攻撃力を保持.\n
            weapon (Weapon) : プレイヤーが現在持っている武器を保持.\n
            now_loc (tuple[int, int]) : プレイヤーが現在いる位置を保持.\n
            before_loc (tuple[int, int]) : プレイヤーが前回いた位置を保持.\n
            gold (int) : プレイヤーの現在のゴールドを保持.\n
            score (int) : プレイヤーの現在のスコアを保持.\n
            key_exist (bool) : プレイヤーの鍵の所持状態を保持.\n
            boss_key_exist (bool) : プレイヤーのボス鍵の所持状態を保持.\n
            win_check (bool) : プレイヤーの勝利条件の達成状態を保持.\n
            lose_check (bool) : プレイヤーの敗北条件の達成状態を保持.\n
            win_enemy_num (int) : プレイヤーが倒した敵の数を保持.\n
            get_trasure_num (int) : プレイヤー宝箱を開けた数を保持.
        """
        self.hp: int = PLAYER_HP
        self.stamina: int = PLAYER_STAMINA
        self.attack: int = PLAYER_ATTACK
        self.weapon: Weapon = Weapon("未所持", 0)
        self.now_loc: tuple[int, int] = (3, 0)
        self.before_loc: Union[bool, tuple[int, int]] = None
        self.gold: int = 0
        self.score: int = 0
        self.key_exist: bool = False
        self.boss_key_exist: bool = False
        self.win_check: bool = False
        self.lose_check: bool = False
        self.win_enemy_num: int = 0
        self.get_trasure_num: int = 0

    def add(self, typ: int = 0, change_rate: int = 0):
        """
        プレイヤーのステータスを変化させる.
        Args:
        - typ : 変化させるステータス.
        - change_rate : 変化させる変化量.
        
        Examples:
        >>> player.add(HP, 10)
        player.hp += 10
        """
        if (typ == HP):
            self.hp += change_rate
        elif (typ == STAMINA):
            self.stamina += change_rate
        elif (typ == GOLD):
            self.gold += change_rate
            if (self.gold <= 0):
                self.gold = 0
        elif (typ == SCORE):
            self.score += change_rate
            if (self.score <= 0):
                self.score = 0
             
    def weapon_set(self, weapon: Weapon = None):
        """
        プレイヤーの武器をセットする.
        Args:
        - weapon : 獲得した武器.
        
        Examples:
        >>> player.set(Weapon("ピンク色武器", 6))
        """
        if (weapon != None):
            if (self.weapon.attack < weapon.attack):
                self.weapon = weapon
                print(f"{weapon.name}を装備した")
                self.attack = PLAYER_ATTACK + weapon.attack
            else:
                print(f"{weapon.name}は今持っている武器より弱いので装備しなかった")
        
    def player_show(self) -> None:
        """
        プレイヤーのステータスを表示する.
        """
        key_info, boss_key_info = "", ""
        if self.key_exist == True:
            key_info  ="鍵 : あり"
        else:
            key_info = "鍵 : なし"
        if self.boss_key_exist == True:
            boss_key_info = "ボス鍵 : あり"
        else:
            boss_key_info = "ボス鍵 : なし"

        player_info = "プレイヤーのステータス : "  + f"[HP : {self.hp}] [スタミナ : {self.stamina}] [ATK : {self.attack}] [GOLD : {self.gold}] [武器 : {self.weapon.name}] " + f"[{key_info}] [{boss_key_info}]"
        print("-" * 150)    
        print(player_info)
        print("-" * 150)
        
    def calculate_score(self) -> None:
        """
        プレイヤーのスコアを計算する.
        """
        score = self.hp*HP_SCORE + self.stamina*STAMINA_SCORE + self.gold*GOLD_SCORE + self.win_enemy_num*ENEMY_SCORE + self.get_trasure_num*TREASURE_SCORE
        if (self.win_check):
            score += WIN_SCORE

        self.score = score
        print("\n----------スコア------------")
        print(f"HP          : {self.hp:>3} × {HP_SCORE:>4} = {self.hp*HP_SCORE:>5}")
        print(f"スタミナ    : {self.stamina:>3} × {STAMINA_SCORE:>4} = {self.stamina*STAMINA_SCORE:>5}")
        print(f"ゴールド    : {self.gold:>3} × {GOLD_SCORE:>4} = {self.gold*GOLD_SCORE:>5}")
        print(f"倒した敵の数: {self.win_enemy_num:>3} × {ENEMY_SCORE:>4} = {self.win_enemy_num*ENEMY_SCORE:>5}")
        print(f"獲得した宝箱: {self.get_trasure_num:>3} × {TREASURE_SCORE:>4} = {self.get_trasure_num*TREASURE_SCORE:>5}")
        if (self.win_check):
            print(f"ゲームクリア:              {WIN_SCORE}")
        print("----------スコア------------\n")
        print(f"あなたのスコアは{self.score}です\n")

   
class Monster:
    def __init__(self, id: int = 0, name: str = "", hp: int = 0, attack: int = 0, boss_check: bool = False, color: str = ""):
        """
        敵の情報を持つクラス.\n
        Args: 
            id (str) : モンスターのid.\n
            name (str) : モンスターの名前.\n
            hp (int) : モンスターのHP.\n
            attack (int) : モンスターの攻撃力.\n
            boss_check (bool) : モンスターがボスであるかどうか.\n
            color (str) : モンスターの色.
        
        Vars: 
            id (str) : モンスターのidを保持.\n
            name (str) : モンスターの名前を保持.\n
            hp (int) : モンスターのHPを保持.\n
            attack (int) : モンスターの攻撃力を保持.\n
            boss_check (bool) : モンスターがボスであるかどうか.\n
            init_hp (int) : モンスターの初期HPを保持.\n
            color (str) : モンスターの色を保持.
        """
        self.id: int = id
        self.name: str = name
        self.hp: int = hp
        self.attack: int = attack
        self.boss_check: bool = boss_check
        self.init_hp: int = hp
        self.color: str = color
    

class StartRoom:
    """
    スタート位置の情報を保持する.
    """
    def __init__(self):
        self.id: str = STARTROOM

    def process(self, player: Player = None, ai = None):
        pass

    
class TreasureRoom:
    def __init__(self, gold: int = 0, weapon: Weapon = None):
        """
        宝箱の部屋の情報を持つクラス.\n
        Args: 
            gold (int) : 宝箱の中身のゴールドの数.\n
            weapon (Weapon) : 宝箱の中身の武器.        
        Vars:
            id (str) : 宝箱部屋のidを保持.\n
            gold (int) : 宝箱の中身のゴールドの数を保持.\n
            weapon (Weapon) : 宝箱の中身の武器を保持.\n
            process_done (bool) : processが行われたかの情報を保持.
        """
        self.id: str = TREASUREROOM
        self.gold: int = gold
        self.weapon: Weapon = weapon
        self.process_done: bool = False
        
    def process(self, player: Player, ai = None) -> None:
        """
        宝箱の部屋の処理を行う.
        Args: 
            player (Player) : 部屋に到達したプレイヤー.
        """
        if (self.process_done == False):
            print("宝箱を見つけた！")
            if player.key_exist == True:
                print("\r" + "宝箱を開けますか？ y/n : ", end="")
                #人工知能　yを入力する
                witch = ai.input_y()
                    
                while(True):
                    if witch == "y":
                        print("鍵を使用し宝箱を開けた！")
                        #人工知能　宝箱を取ったことを格納する、これでショップにも行けるようになる
                        ai.get_treasure = True
                        player.key_exist = False
                        player.add(GOLD, self.gold)
                        player.get_trasure_num += 1 #追加
                        player.weapon_set(self.weapon)
                        self.process_done = True
                        break

                    elif witch == "n":
                        print("宝箱を開けなかった...")
                        break
                    else:
                        # sys.stdout.write("\033[0K\033[0A%s" % witch)
                        # sys.stdout.flush()
                        print("\r" + "もう一度入力してください y/n : ", end="")
                        witch = input().rstrip("")
                        
            else:
                print("しかし鍵が無かった")
        else:
            print("宝箱は既に取得されている.")


class WeaponRoom:
    def __init__(self, weapon: Weapon = None):
        """
        武器の部屋の情報を持つクラス.\n
        Args: 
            weapon (Weapon) : 部屋に落ちている武器.
        Vars: 
            id (str) : 部屋のidを保持.\n
            weapon (Weapon) : 部屋に落ちている武器を保持.\n
            process_done (bool) : processが行われたかの情報を保持.
        """
        self.id: str = WEAPONROOM
        self.weapon: Weapon = weapon
        self.process_done: bool = False
        
    def process(self, player: Player, ai = None) -> None:
        """
        武器の部屋の処理を行う.
        Args: 
            player (Player) : 部屋に到達したプレイヤー.
        """
        if (self.process_done == False):
            print("武器が落ちている！")
            print(f"{self.weapon.name}を手に入れた!")
            player.weapon_set(self.weapon)
            self.process_done = True
        else:
            print("武器は既に取得された")


class GoldRoom:
    def __init__(self, gold: int = 0):
        """
        ゴールドの部屋の情報を持つクラス.\n
        Args:
            gold (int) : 部屋に落ちているゴールドの数.
        Vars: 
            id (str) : 部屋のidを保持.\n
            gold (int) : 部屋に落ちているゴールドの数を保持.\n
            process_done (bool) : processが行われたかの情報を保持.
        """
        self.id: str = GOLDROOM
        self.gold: int = gold
        self.process_done: bool = False
        
    def process(self, player: Player, ai = None) -> None:
        """
        ゴールドの部屋の処理を行う.
        Args: 
            player (Player) : 部屋に到達したプレイヤー.
        """
        if (self.process_done == False):
            print(f"{self.gold}ゴールドが落ちてた！")
            player.add(GOLD, self.gold)
            self.process_done = True
        else:
            print("既にゴールドは取得された")


class EventRoom:
    def __init__(self):
        """
        イベントの部屋の情報を持つクラス.\n
        Vars:
            id (str) : 部屋のidを保持.\n
            event (int) : どのイベントを発生させるかの情報を保持.\n
            process_done (bool) : processが行われたかの情報を保持.
        """
        self.id: str = EVENTROOM
        self.event: int = 0
        self.process_done: bool = False
        
    def process(self, player: Player, ai = None) -> None:
        """
        イベントの部屋の処理を行う.
        Args: 
            player (Player) : 部屋に到達したプレイヤー.
        """
        if (self.process_done == False):
            print("イベントマス")
            self.event = random.randint(1, 3)
            if (self.event == 1):
                print("泉を発見! 水を飲んで、プレイヤーのhpが10回復した!")
                player.add(HP, 10)
            elif (self.event == 2):
                print("安全な場所を発見! 少し休んで、プレイヤーのスタミナが3回復した!")
                player.add(STAMINA, 3)
            else:
                print("鍵のついていない宝箱を発見！ 中には5Gが入っていた!")
                player.add(GOLD, 5)
            self.process_done = True
        else:
            print("既にイベントマスは使われました.")
     
        
class ShopRoom:
    
    def __init__(self):
        """
        ショップの部屋の情報を持つクラス.\n
        Vars:
            id (str) : 部屋のidを保持.\n
            shop_goods (dict[int:int]) : ショップの商品とその価格の対応関係を保持.\n
            shop_goods_name (dict[int:str]) : ショップの商品とその名前の対応関係を保持.\n
            shpp_log (dict[int:int]) : ショップの商品とその購入回数の対応関係を保持.
        """
        self.id: str = SHOPROOM
        self.shop_goods: dict[int:int] = {MEDICINE_RECOVER_HP : 5, MEDICINE_RECOVER_STAMINA : 5, YELLOW_WEAPON : 4, PINK_WEAPON : 6}   # {ショップの商品 : 価格}
        self.shop_goods_name: dict[int:str] = {MEDICINE_RECOVER_HP : "HP回復薬", MEDICINE_RECOVER_STAMINA : "スタミナ回復薬", YELLOW_WEAPON : "黄色武器", PINK_WEAPON : "ピンク色武器"}   # {ショップの商品 : 商品名}
        self.shop_log: dict[str:int] =  {"HP回復薬" : 0, "スタミナ回復薬" : 0, "黄色武器" : 0, "ピンク色武器" : 0}   # {ショップの商品 : 購入回数}
        
    def process(self, player: Player, ai = None) -> None:
        """
        ショップの部屋の処理を行う.
        Args: 
            player (Player) : 部屋に到達したプレイヤー.
        """ 
        print("いらっしゃい！ 薬や武器を売っているよ！\n")
        print(f"[HP : {player.hp}] [スタミナ : {player.stamina}] [武器 : {player.weapon.name}] [ゴールド : {player.gold}]")
        
        print("\n各武器のステータス.")
        print("水色武器 -> ATK : 1")
        print("青色武器 -> ATK : 3")
        print("緑色武器 -> ATK : 4")
        print("紫色武器 -> ATK : 5")
        print("黄色武器 -> ATK : 5")
        print("赤色武器 -> ATK : 6")
        print("桃色武器 -> ATK : 6")
        print("オレンジ色武器 -> ATK : 7\n")
        
        for (goods, price) in self.shop_goods.items():
            goods_name = self.shop_goods_name[goods]
            print(f"{goods_name} : {price}G ({goods}キーで購入)")
        print()
        
        print("\r" + "購入したい物をキーで選んでください (qキーで退出) : ", end="")
        #人工知能　aiを購入モードにする
        ai.is_buy = True
        #人工知能　aiに何を買うかを決定させる
        user_select = ai.act().rstrip("")
            
        while (True):
            player_gold = player.gold
            
            if (len(user_select) != 0):   # 入力されている場合.
                if (user_select == "q"):
                    print("ショップを退出しました.")
                    ai.is_buy = False
                    break
                
                elif (user_select == str(MEDICINE_RECOVER_HP)):
                    goods_price = self.shop_goods[MEDICINE_RECOVER_HP]
                    goods_name = self.shop_goods_name[MEDICINE_RECOVER_HP]
                    if (player_gold < goods_price):
                        print("お金が足りません.")
                        print("\n")
                    else:
                        print(f"{goods_name}を購入しました.")
                        print("\n")
                        player.add(HP, 10)
                        player.add(GOLD, -goods_price)
                        self.shop_log[goods_name] += 1

                elif (user_select == str(MEDICINE_RECOVER_STAMINA)):
                    goods_price = self.shop_goods[MEDICINE_RECOVER_STAMINA]
                    goods_name = self.shop_goods_name[MEDICINE_RECOVER_STAMINA]
                    
                    if (player_gold < goods_price):
                        print("お金が足りません.")
                        print("\n")
                    else:
                        print(f"{goods_name}を購入しました.")
                        print("\n")
                        player.add(STAMINA, 3)
                        player.add(GOLD, -goods_price)
                        self.shop_log[goods_name] += 1
                
                elif (user_select == str(YELLOW_WEAPON)):
                    goods_price = self.shop_goods[YELLOW_WEAPON]
                    goods_name = self.shop_goods_name[YELLOW_WEAPON]
                    
                    if (player_gold < goods_price):
                        print("お金が足りません.")
                        print("\n")
                    elif (self.shop_log[goods_name] >= 1):
                        print("既に購入されています.")
                        print("\n")
                    else:
                        print(f"{goods_name}を購入しました.")
                        print("")
                        player.weapon_set(Weapon(goods_name, 5))
                        player.add(GOLD, -goods_price)
                        self.shop_log[goods_name] += 1
                
                elif (user_select == str(PINK_WEAPON)):
                    goods_price = self.shop_goods[PINK_WEAPON]
                    goods_name = self.shop_goods_name[PINK_WEAPON]
                    
                    if (player_gold < goods_price):
                        print("お金が足りません.")
                        print("\n")
                    elif (self.shop_log[goods_name] >= 1):
                        print("既に購入されています.")
                        print("\n")
                    else:
                        print(f"{goods_name}を購入しました.")
                        print("")
                        player.weapon_set(Weapon(goods_name, 6))
                        player.add(GOLD, -goods_price)
                        self.shop_log[goods_name] += 1
           
                user_select = ""        
           
            else:
                # sys.stdout.write("\033[0K\033[Aa%s" % user_select)
                # sys.stdout.flush()
                print("\r" + f"購入したい物をキーで選んでください. [[HP : {player.hp}] [スタミナ : {player.stamina}] [武器 : {player.weapon.name}] [ゴールド : {player.gold}]] (qキーで退出) : ", end="")
                user_select = ai.act().rstrip("")
            
        
class KeyRoom:
    def __init__(self):
        """
        鍵の部屋の情報を持つクラス.\n
        Vars:
            id (str) : 部屋のidを保持.\n
            key (bool) : 部屋に落ちている鍵が存在するかの情報を保持.\n
            process_done (bool) : processが行われたかの情報を保持.
        """
        self.id: str = KEYROOM
        self.key: bool = True
        self.process_done: bool = False
        
    def process(self, player: Player, ai = None) -> None:
        """
        鍵の部屋の処理を行う.
        Args: 
            player (Player) : 部屋に到達したプレイヤー.
        """
        if (self.process_done == False):
            print("宝箱のカギを発見した.")
            player.key_exist = True
            self.process_done = True
        else:
            print("既にカギは取得されました")
        
        
class BossKeyRoom:
    def __init__(self):
        """
        ボス鍵の部屋の情報を持つクラス.\n
        Vars:
            id (str) : 部屋のidを保持.\n
            boss_key (bool) : 部屋に落ちているボス鍵が存在するかの情報を保持.\n
            process_done (bool) : processが行われたかの情報を保持.
        """
        self.id: str = BOSSKEYROOM
        self.boss_key: bool = True
        self.process_done: bool = False
        
    def process(self, player: Player, ai = None) -> None:
        """
        ボス鍵の部屋の処理を行う.
        Args: 
            player (Player) : 部屋に到達したプレイヤー.
        """
        if (self.process_done == False):
            print("ボス部屋のカギを発見した.")
            player.boss_key_exist = True
            self.process_done = True
        else:
            print("既にボス鍵は取得されました")
        
        
class MonsterRoom:
    def __init__(self, monster: Monster = Monster()):
        """
        敵がいる部屋の情報を持つクラス.\n
        Args:
            monster (Monster) : 部屋にいる敵の情報.
        Vars:
            id (str) : 部屋のidを保持.\n
            monster (Monster) : 部屋にいる敵の情報を保持.\n
            process_done (bool) : processが行われたかの情報を保持.
        """
        self.id: str = MONSTERROOM
        self.monster: Monster = monster
        self.process_done: bool = False
        
    def process(self, player: Player, ai = None) -> None:
        """
        敵の部屋の処理を行う.
        Args: 
            player (Player) : 部屋に到達したプレイヤー.
        """
        all_damage = 0
        if (self.process_done == False):
            
            print(f"{self.monster.name}との戦闘が開始されます.")
            while (True):
                self.monster.hp -= player.attack
                
                if (self.monster.hp < 0):
                    self.monster.hp = 0
            
                if (self.monster.hp == 0):
                    print("プレイヤーが勝利")
                    print("受けたダメージ : ", all_damage, " 現在HP : ", player.hp)
                    player.win_enemy_num += 1 #追加
                    self.process_done = True
                    if (self.monster.boss_check == True):
                        player.win_check = True
                    break
                
                player.add(HP, -self.monster.attack)
                all_damage += self.monster.attack
                if (player.hp < 0):
                    player.hp = 0
                    
                if (player.hp == 0):
                    print("プレイヤーは敗北")
                    player.lose_check = True
                    print(f"{self.monster.name}の残りHP : {self.monster.hp}")
                    break
        
    
class Room:
    UPPER_RIGHT_ROOM = "1"   # 右上
    LOWER_RIGHT_ROOM = "2"   # 右下
    UPPER_LEFT_ROOM = "8"   # 左上
    LOWER_LEFT_ROOM = "9"   # 左下
    
    def __init__(self, room_info: list[Union[TreasureRoom, WeaponRoom, GoldRoom, EventRoom, ShopRoom, KeyRoom, BossKeyRoom, MonsterRoom]] = [], room_pos: tuple[int, int] = (3, 0)):
        """
        部屋の情報を持つクラス.\n
        Args:
            room_info (list[Union[TreasureRoom, WeaponRoom, GoldRoom, EventRoom, ShopRoom, KeyRoom, BossKeyRoom, MonsterRoom]]) : その部屋が持っている情報.\n
            room_pos (tuple[int, int]) : その部屋の位置.
        Vars: 
            room_info (str) : 部屋の情報を保持.\n
            room_pos (tuple[int, int]) : 部屋の位置(y, x)を保持.\n
            event_exist_dic (dict[int:bool]) : あるイベントが存在するかを保持.\n
            room_event_info (list[Union[TreasureRoom, WeaponRoom, GoldRoom, EventRoom, ShopRoom, KeyRoom, BossKeyRoom, MonsterRoom]]) : その部屋が持っている情報を保持.\n
            room_hide (bool) : 部屋が隠されているかの情報を保持.\n
            reached (bool) : 部屋に到達したことがあるかの情報を保持.\n
            next_room_info (dict[int:tuple[int,int]]) : その部屋において、次に進むことができる部屋の情報を保持.\n
            before_room_info (dict[int:tuple[int,int]]) : その部屋において、前に進むことができる部屋の情報を保持.
        """
        self.room_info: str = ""
        self.room_pos: tuple[int, int] = room_pos
        self.event_exist_dic: dict[int:bool] = {TREASUREROOM : False, WEAPONROOM : False, GOLDROOM : False, EVENTROOM : False, SHOPROOM : False, KEYROOM : False, BOSSKEYROOM : False, MONSTERROOM : False}
        self.room_event_info: list[Union[TreasureRoom, WeaponRoom, GoldRoom, EventRoom, ShopRoom, KeyRoom, BossKeyRoom, MonsterRoom]] = room_info
        self.room_hide: bool = True
        self.reached = False
        self.next_room_info: dict[int:tuple[int, int]] = {Room.UPPER_RIGHT_ROOM : None, Room.LOWER_RIGHT_ROOM : None}
        self.before_room_info: dict[int:tuple[int, int]] = {Room.UPPER_LEFT_ROOM : None, Room.LOWER_LEFT_ROOM : None}
        self.room_info_make()
        
    def room_info_make(self) -> None:
        """
        部屋の情報から部屋の情報を作る.
        """
        room_len = len(self.room_event_info)
        for i, room_event in enumerate(self.room_event_info, 1):
            self.event_exist_dic[room_event.id] = True
            if (i == room_len):
                self.room_info += room_event.id
            else:
                self.room_info += room_event.id + "-"
    
    def next_room_make(self, dungeon_map: list[list[int]]) -> None:
        """
        次に移動することができる部屋(next_room_info)を作る.
        """
        room_x_pos = self.room_pos[1]
        room_y_pos = self.room_pos[0]
        try:
            x, y = room_x_pos+1, room_y_pos-1   # 右上の部屋.
            if ((x < 0) or (y < 0)):
                pass
            elif (type(dungeon_map[x][y]) == Room):
                self.next_room_info[Room.UPPER_RIGHT_ROOM] = (y, x)
        except:
            pass
        
        try:
            x, y = room_x_pos+1, room_y_pos+1   # 右下の部屋.
            if ((x < 0) or (y < 0)):
                pass
            elif (type(dungeon_map[x][y]) == Room):
                self.next_room_info[Room.LOWER_RIGHT_ROOM] = (y, x)
        except:
            pass
        
    def before_room_make(self, dungeon_map: list[list[int]]) -> None:
        """
        前に移動することができる部屋(before_room_info)を作る.
        """
        room_x_pos = self.room_pos[1]
        room_y_pos = self.room_pos[0]
        
        try:
            x, y = room_x_pos-1, room_y_pos-1   # 左上の部屋
            if ((x < 0) or (y < 0)):
                pass
            elif (type(dungeon_map[x][y]) == Room):
                self.before_room_info[Room.UPPER_LEFT_ROOM] = (y, x)
        except:
            pass
        
        try:
            x, y = room_x_pos-1, room_y_pos+1   # 左下の部屋.
            if ((x < 0) or (y < 0)):
                pass
            elif (type(dungeon_map[x][y]) == Room):
                self.before_room_info[Room.LOWER_LEFT_ROOM] = (y, x)
        except:
            pass
               
    def process(self, player: Player, ai = None) -> None:
        """
        部屋に存在するイベントを処理する.
        Args: 
            player (Player) : 部屋に到達したプレイヤー.
        """
        for room_event in self.room_event_info:
            room_event.process(player, ai)
    
    
class Dungeon:
    def __init__(self, dungeon_info_list: list[list[list[Union[TreasureRoom, WeaponRoom, GoldRoom, EventRoom, ShopRoom, KeyRoom, BossKeyRoom, MonsterRoom]]]], player: Player):
        """
        ダンジョン全体の情報を持つクラス.\n
        Args:
            dungeon_info_list (list[list[list[Union[TreasureRoom, WeaponRoom, GoldRoom, EventRoom, ShopRoom, KeyRoom, BossKeyRoom, MonsterRoom]]]]) : ダンジョンの各部屋の情報.\n
            player (Player) : プレイヤーの情報.
        Vars:
            dungeon_list (list[list[Room]]) : ダンジョン全体のマップを保持.
            player (Player) : プレイヤーの情報を保持.
        """
        self.dungeon_list: list[list[Room]] = []
        self.player = player
        self.dungeon_make(dungeon_info_list)
        self.dungeon_list[3][0].room_hide = False   # スタート部屋
        self.dungeon_list[3][0].reached = True
        self.dungeon_list[3][6].room_hide = False   # ボス部屋.
        
        self.room_hide_check()
        
    def list_transpose(self, l: list) -> list:
        """
        transpose(転置)を行う.
        Args:
            l (list) : 転置前のlist.
        Returns:
            transposed list.
        Example:
            l = [
                [0, 1], 
                [2, 3]
            ]\n
            self.list_transpose(l)
            >>> [
                [0, 2], 
                [1, 3]
            ]
        """
        l = [list(x) for x in list(zip(*l))]
        return l
        
    def dungeon_make(self, dungeon_info_list: list[list[list[Union[TreasureRoom, WeaponRoom, GoldRoom, EventRoom, ShopRoom, KeyRoom, BossKeyRoom, MonsterRoom]]]]) -> None:
        """
        ダンジョンを生成する.
        Args:
            dungeon_info_list (list[list[list[Union[TreasureRoom, WeaponRoom, GoldRoom, EventRoom, ShopRoom, KeyRoom, BossKeyRoom, MonsterRoom]]]]) : ダンジョンの情報を保持するlist.
        
        """
        dungeon_room_num_list = [len(i) for i in dungeon_info_list]
        max_room_num = max(dungeon_room_num_list)
        floor_center_num = round((max_room_num * 2 - 1)/2)
        floor_num = len(dungeon_info_list)
        self.dungeon_list = [[0 for i in range(max_room_num * 2 - 1)] for j in range(floor_num)]
        transposed_dungeon_list = self.list_transpose(self.dungeon_list)
        
        for i, (floor_list, room_num, floor_info) in enumerate(zip(transposed_dungeon_list, dungeon_room_num_list, dungeon_info_list)):
            first_room_index = floor_center_num - room_num
            room_index_list = [first_room_index + i*2 for i in range(room_num)]
            
            for room_index, room_info in zip(room_index_list, floor_info):
                floor_list[room_index] = Room(room_info, (room_index, i))
            
        self.dungeon_list: list[list[Room]] = self.list_transpose(transposed_dungeon_list)
        
        for room_list in self.dungeon_list:
            for room in room_list:
                if (type(room) == Room):
                    room.next_room_make(self.dungeon_list)
                    room.before_room_make(self.dungeon_list)
        
    def dungeon_show(self) -> None:
        """
        ダンジョンを表示する.
        """
        self.room_hide_check()
        room_show = [[0 for _ in range(len(self.dungeon_list[0]))] for _ in range(len(self.dungeon_list) * 3)]
        
        now_room = self.dungeon_list[self.player.now_loc[0]][self.player.now_loc[1]]
        next_player_room = [i for i in list(now_room.next_room_info.values()) if i != None]
        before_player_room = [i for i in list(now_room.before_room_info.values()) if i != None]
        
        for floor, floor_num in zip(self.dungeon_list, [i*3 for i in range(len(room_show)*2)]):
            for i in range(3):
                for room_num, room in enumerate(floor):
                    if (room == 0):
                        room_show[floor_num+i][room_num] = "             "
                    else:
                        if (room.room_hide == True):   # 部屋情報が隠されているときは?をつける.
                            room_info = "?"
                        elif (room.room_hide == False):
                            room_info = room.room_info
                            
                        if (i == 1):
                            if (self.player.now_loc == room.room_pos):   # プレイヤーがいるところにPをつける.
                                if (len(room_info) == 0):
                                    room_info = self.room_info_make(f"P{room_info}", room)
                                else:
                                    room_info = self.room_info_make(f"P-{room_info}", room)
                                room_info = self.room_back_ground_make(room_info, room)
                                
                            else:
                                room_info = self.room_info_make(f"{room_info}", room)
                                
                            if (room.reached == True):   # 既に到達した部屋にFlagをつける.
                                room_info = room_info.replace(" ", "", 1)
                                room_info = "F" + room_info
                            
                            if (True):   # 次に到達できる部屋に色付けを行う.
                                for next_room in next_player_room:   # 次に移動できる部屋.
                                    if (next_room == room.room_pos):
                                        room_info = self.room_back_ground_make(room_info, room, False)
                                
                                for before_room in before_player_room:   # 前に移動できる部屋.
                                    if (before_room == room.room_pos):
                                        if (room.reached == True):
                                            room_info = self.room_back_ground_make(room_info, room, False)
                            
                            room_show[floor_num+i][room_num] = room_info
                        elif (i == 0):
                            room_show[floor_num+i][room_num] = "-------------"
                        else:
                            room_show[floor_num+i][room_num] = "-------------"

        dungeon = ""
        for floor in room_show:
            floor_room = ""
            for room in floor:
                floor_room += room
            floor_room += "\n"
            dungeon += floor_room
            
        print(dungeon)
        
    def room_info_make(self, before_room_info: str = "", room: Room = None) -> str:
        """
        部屋の情報から、部屋のstringを作る.\n
        Args:
            before_room_info (str) : 元となる部屋の情報.\n
            room (Room) : 部屋の情報.
        Example: 
            before_room_info("P-G")\n
            >>> "|   P-G   |"\n
            before_room_info("M-G-W")\n
            >>> "|  M-G-W  |"\n
        """ 
        after_room_info = "             "
        before_room_info = self.process_done_check(before_room_info, room)
        
        if (before_room_info == "P-"):   # 部屋の情報が削除された後に、残ったものを処理する.
            before_room_info = "P"
        elif (before_room_info == "P--"):
            before_room_info = "P"
        elif (before_room_info == "P---"):
            before_room_info = "P"
        elif (before_room_info == "P"):
            before_room_info = "P"
        elif (before_room_info == "-"):
            before_room_info = ""
        elif (before_room_info == "--"):
            before_room_info = ""
        elif (before_room_info == "---"):
            before_room_info = ""
        
        if (len(before_room_info) == 0):   # 部屋の内容がなくなってしまったとき.
            after_room_info = "|           |"
        else:
            before_room_info = self.gold_replace(before_room_info, room)
            
            if (len(before_room_info) == "?"):   # roomの情報が隠されているとき
                after_room_info = "|     ?     |"
            elif (len(before_room_info) == 1):   # 長さ1のとき(G, M, S, Kなど) >>> |    G    |
                after_room_info = f"|     {before_room_info}     |"
            elif (len(before_room_info) == 3):   # 長さ3のとき(G-W, M-G, P-Wなど) >>> |   G-W   |
                after_room_info = f"|    {before_room_info}    |"
            elif (len(before_room_info) == 5):   # 長さ5のとき(P-G-W, M-G-Wなど) >>> |  P-G-W  |
                after_room_info = f"|   {before_room_info}   |"
            elif (len(before_room_info) == 7):   # 長さ7のとき(P-M-G-Wなど) >>> | P-M-G-W |
                after_room_info = f"|  {before_room_info}  |"
            elif (len(before_room_info) == 9):   # 長さ9のとき(P-M-01G-Wなど) >>> | P-M-01G-W |
                after_room_info = f"| {before_room_info} |"
                    
            after_room_info = self.room_color_replace(after_room_info, room)
            
        return after_room_info
    
    def process_done_check(self, before_string: str = "", room: Room = None) -> str:
        """
        ルームの情報から、process_done(そのプロセスが行われたかの変数)
        Args:
            before_string (str) : 元の文字列.\n
            room (Room) : 部屋の情報.
        Return:
            process_doneの情報をもとに、変更した部屋の情報を持つ文字列.
        """
        after_string: str = before_string
        for room_event in room.room_event_info:
            try:
                if (room_event.process_done == True):   # プロセスが既に行われているなら.
                    after_string = after_string.replace(room_event.id, "")
                                
                else:   # まだプロセスが行われていないなら.
                    pass
            except:   # process_doneが存在しない部屋.
                pass
        return after_string
    
    def gold_replace(self, before_string: str = "", room: Room = None) -> str:
        """
        ゴールドの表示を変更する.
        Args:
            before_string (str) : 元の文字列.\n
            room (Room) : 部屋の情報.
        Return:
            変更したゴールドの情報を持つ文字列.
            
        Examples:
            replace_room_color("|   G   |", room)
            >>> "|   01G   |"
        """
        gold_num = -1
        if ("G" in before_string):
            for room_info in room.room_event_info:
                if (room_info.id == GOLDROOM):
                    gold_num = room_info.gold
        
        if (gold_num <= 0):
            return before_string
        else:
            before_string = before_string.replace("G", f"0{gold_num}G")
            return before_string
        
    def room_color_replace(self, before_string: str = "", room: Room = None) -> str:
        """
        roomの情報に、Monster(M)かWeapon(W)がある時に、色を変更する.\n
        Args:
            before_string (str) : 元の文字列.\n
            room (Room) : 部屋の情報.
        Return:
            変更した色の情報を持つ文字列.
            
        Examples:
            replace_room_color("|   M   |", "\033[31m")
            >>> "|   "\033[31m" + M + "\033[0m"   |"
        """
        COLOR = ""
        if ("M" in before_string):
            for room_info in room.room_event_info:
                if (room_info.id == MONSTERROOM):
                    COLOR = room_info.monster.color
                    
        elif ("W" in before_string):
            for room_info in room.room_event_info:
                if (room_info.id == WEAPONROOM):
                    COLOR = room_info.weapon.color
                    
        if (len(COLOR) == 0):
            return before_string
        else:
            s = before_string
            
            rep_m = COLOR + "M" + END
            rep_w = COLOR + "W" + END
            s = s.replace("M", rep_m)
            s = s.replace("W", rep_w)
            return s
        
    def room_back_ground_make(self, before_string: str = "", room: Room = None, is_player: bool = True) -> str:
        """
        roomの情報に、player(P)がある時に、背景色を変更する.\n
        Args:
            before_string (str) : 元の文字列.\n
            room (Room) : 部屋の情報.
            is_player (bool) : プレイヤーの部屋であるか.
        Return:
            変更した色の情報を持つ文字列.
        """
        PLAYER_BG_COLR = "\033[48;2;200;200;200m"   # 白色背景.
        NEXT_BG_COLR = "\033[48;2;50;50;50m"   # 薄い白色背景.
        END = "\033[0m"
        
        color_flag = False
        
        after_string = before_string
        if (is_player == True):
            for color_code in COLOR_DICT.values():
                if (color_flag == False):
                    if (color_code in after_string):   # 色が含まれている時.
                        after_string = after_string.replace(color_code, color_code + PLAYER_BG_COLR).replace(END, END + PLAYER_BG_COLR)
                        color_flag = True
                        
            return PLAYER_BG_COLR + after_string + END
        
        else:
            for color_code in COLOR_DICT.values():
                if (color_flag == False):
                    if (color_code in after_string):   # 色が含まれている時.
                        after_string = after_string.replace(color_code, color_code + NEXT_BG_COLR).replace(END, END + NEXT_BG_COLR)
                        color_flag = True
                        
            return NEXT_BG_COLR + after_string + END
            
    def room_hide_check(self) -> None:
        """
        部屋が隠されているかの情報を更新する.
        """
        player_pos = self.player.now_loc
        room_in_player = self.dungeon_list[player_pos[0]][player_pos[1]]
        
        next_room: tuple[int, int] = (0, 0)
        next_to_next_room: tuple[int, int] = (0, 0)
       
        for next_room in [room for room in room_in_player.next_room_info.values() if room != None]:
            self.dungeon_list[next_room[0]][next_room[1]].room_hide = False
            for next_to_next_room in [room for room in self.dungeon_list[next_room[0]][next_room[1]].next_room_info.values() if room != None]:
                self.dungeon_list[next_to_next_room[0]][next_to_next_room[1]].room_hide = False
        
    def room_contents_show(self) -> None:
        """
        部屋の中身の意味を表示する.
        """
        self.player.player_show()
        
        room_contents = "部屋の情報 : " +  "[W : 武器] [G : ゴールド] [! : ショップ] [E : イベント] [K : 鍵] [B : ボス鍵] [T : 宝箱] [M : モンスター]"
        print(room_contents)
        print("-" * 150)
        
    def screen_delete(self) -> None:
        """
        コンソール画面を消去する.
        """
        os.system("cls")
        print("\n")
            
    def user_input_q(self) -> None:
        """
        ユーザーのq入力を受け付ける.
        """
        sleep(1)
        user_input = input("終了するには、qキーを押してください : ")
        while (True):
            if (user_input == "q"):
                break
            else:
                user_input = input("もう一度入力してください. (qキーで終了) : ")
    
    def player_act(self, typ: str = "") -> None:
        """
        プレイヤーの行動選択.
        Args:
            typ (str) : プレイヤーの入力値.
        """
        if (typ == "m"):
            print(f"({COLOR_DICT['Yellow']}M{END} -> HP : 5, ATK : 2")
            print(f"({COLOR_DICT['Green']}M{END} -> HP : 11, ATK : 2")
            print(f"({COLOR_DICT['Red']}M{END} -> HP : 9, ATK : 7")
            print(f"({COLOR_DICT['Cyan']}M{END} -> HP : 17, ATK : 5")
            print(f"({COLOR_DICT['White']}M{END} -> HP : 21, ATK : 3")
            print(f"({COLOR_DICT['Magenta']}M{END} -> HP : 29, ATK : 8")
            self.user_input_q()
        
        elif (typ == "w"):
            print(f"水色武器({COLOR_DICT['Cyan']}W{END}) -> ATK : 1")
            print(f"青色武器({COLOR_DICT['Blue']}W{END}) -> ATK : 3")
            print(f"緑色武器({COLOR_DICT['Green']}W{END}) -> ATK : 4")
            print(f"紫色武器({COLOR_DICT['Magenta']}W{END}) -> ATK : 5")
            print(f"黄色武器({COLOR_DICT['Yellow']}W{END}) -> ATK : 5")
            print(f"赤色武器({COLOR_DICT['Red']}W{END}) -> ATK : 6")
            print("桃色武器     -> ATK : 6")
            print("オレンジ色武器 -> ATK : 7\n")
            self.user_input_q()
        
        elif (typ == "s"):
            print("HP10回復薬 -> 必要ゴールド5")
            print("スタミナ3回復薬 -> 必要ゴールド5")
            print("黄色武器 -> 必要ゴールド4")
            print("ピンク色武器 -> 必要ゴールド6")
            self.user_input_q()
            
        elif (typ == "e"):
            print("ランダムで")
            print("HPの10回復")
            print("スタミナの3回復")
            print("5ゴールド獲得")
            self.user_input_q()
        
        elif (typ == "t"):
            self.rule_show()
            typ = ""
        
        elif (typ  == "1"):
            try:
                now_room: Room = self.dungeon_list[self.player.now_loc[0]][self.player.now_loc[1]]
                next_room: tuple[int, int] = now_room.next_room_info[typ]
                self.player.now_loc = next_room
                self.dungeon_list[next_room[0]][next_room[1]].reached = True
            except:
                print("行き止まりです")
        
        elif (typ == "2"):
            try:
                now_room: Room = self.dungeon_list[self.player.now_loc[0]][self.player.now_loc[1]]
                next_room: tuple[int, int] = now_room.next_room_info[typ]
                self.player.now_loc = next_room
                self.dungeon_list[next_room[0]][next_room[1]].reached = True
            except:
                print("行き止まりです")
            
        elif (typ == "8"):
            try:
                now_room: Room = self.dungeon_list[self.player.now_loc[0]][self.player.now_loc[1]]
                next_room: tuple[int, int] = now_room.before_room_info[typ]
                self.player.now_loc = next_room
            except:
                print("行き止まりです")
        
        elif (typ == "9"):
            try:
                now_room: Room = self.dungeon_list[self.player.now_loc[0]][self.player.now_loc[1]]
                next_room: tuple[int, int] = now_room.before_room_info[typ]
                self.player.now_loc = next_room
            except:
                print("行き止まりです")
            
    def user_input(self, ai) -> None:
        """
        プレイヤーの行動を入力する.
        """
        now_room: Room = self.dungeon_list[self.player.now_loc[0]][self.player.now_loc[1]]
        next_room_info = now_room.next_room_info
        before_room_info = now_room.before_room_info
        move_list = []
        move_info = ""
        room: Room = None
        
        if (next_room_info["1"] != None):   # 右上の部屋が存在するなら.
            move_info += "[1キーでは右上の部屋へ移動できます] "
            move_list.append("1")
            
        if (next_room_info["2"] != None):   # 右下の部屋が存在するなら.
            move_info += "[2キーでは右下の部屋へ移動できます] "
            move_list.append("2")
            
        if (before_room_info["8"] != None):   # 左上の部屋が存在するなら.
            room = self.dungeon_list[before_room_info["8"][0]][before_room_info["8"][1]]
            try:
                if (room.reached == True):
                    move_info += "[8キーでは左上の部屋へ移動できます] "
                    move_list.append("8")
            except:
                pass
                
        if (before_room_info["9"] != None):   # 左下の部屋が存在するなら.
            room = self.dungeon_list[before_room_info["9"][0]][before_room_info["9"][1]]
            try:
                if (room.reached == True):
                    move_info += "[9キーでは左下の部屋へ移動できます] "
                    move_list.append("9")
            except:
                pass
            
        print("[tキーでチュートリアルをもう一度確認できます] [mキーではモンスター情報の確認できます] [sキーではショップ情報の確認できます] [eキーではイベント情報の確認できます] [wキーではブキ情報の確認できます]")
        print("-" * 150)
        print(move_info)
        print("-" * 150)
        
        print("\r" + "行動するコマンドを入力してください : ", end="")   # 誤ったinputがされたら、そのinput文を消去して、綺麗に出力.

        print("")
        
        #人工知能　aiの行動選択
        act = ai.act()
        
            
        while (True):
            input("何かキーを押して次に進む")
            if act in ["t", "m", "s", "e", "w"]:
                self.player_act(act)
                break
                
            elif (act in move_list):
                if ((act in ["1", "2"]) and (next_room_info[act] == BOSS_ROOM_POSITION)):
                    if (self.player.boss_key_exist):
                        self.player_act(act)
                        break
                    else:
                        # sys.stdout.write("\033[0K\033[0A%s" % act)
                        # sys.stdout.flush()
                        print("\r" + "ボス鍵が無いと入れません. もう一度入力してください : ", end="")
                        act = ai.act().rstrip("")
                else:
                    self.player_act(act)
                    break
            else:
                # sys.stdout.write("\033[0K\033[1A%s" % act)
                # sys.stdout.flush()
                print("\r" + "行動するコマンドをもう一度入力してください : ", end="")
                act = ai.act()
               
    def restart_select(self, ai) -> None:
        """
        プレイヤーが敗北したときに、やり直しを行う.
        """
        print("\r" + "やり直しますか? y/n : ", end="")
        user_input = ai.input_y()
        # user_input = input("").rstrip("")
        
        while (True):
            if (user_input == "y"):
                return True
            elif (user_input == "n"):
                return False
            else:
                # sys.stdout.write("\033[0K\033[1A%s" % user_input)
                # sys.stdout.flush()
                print("\r" + "もう一度入力してください y/n : ", end="")
                user_input = input().rstrip("")
        
    def reset(self) -> None:
        """
        やり直しをする際にダンジョンを初期化する関数.
        """
        for room_list in self.dungeon_list:
            for room in room_list:
                try:
                    room_info = room.room_event_info
                    room_pos = room.room_pos
                    room_hide = room.room_hide
                    for event_info in room_info:
                        if(event_info.id == TREASUREROOM):
                            event_info.__init__(event_info.gold, event_info.weapon)

                        elif(event_info.id == WEAPONROOM):
                            event_info.__init__(Weapon(event_info.weapon.name, event_info.weapon.attack, event_info.weapon.color))
                    
                        elif(event_info.id == GOLDROOM):
                            event_info.__init__(event_info.gold)

                        elif(event_info.id == MONSTERROOM):
                            event_info.__init__(Monster(event_info.monster.id, event_info.monster.name, event_info.monster.init_hp, event_info.monster.attack, event_info.monster.boss_check, event_info.monster.color))

                        else:
                            event_info.__init__()
                            
                    room.__init__(room_info, room_pos)
                    room.next_room_make(self.dungeon_list)
                    room.before_room_make(self.dungeon_list)
                    if (room_hide == False):
                        room.room_hide = False

                except:
                    pass
                
        self.dungeon_list[3][0].reached = True

    def rule_show(self, sleep_time: int = 0) -> None:
        """
        ルール(チュートリアル)を表示する.
        Args:
            sleep_time (int) : 時間差でルールを表示するための時間.
        """
        print("ESCAPE")
        print("あなたはダンジョンに落ちてしまいました.")
        print("あなたはボス鍵を入手してボスを倒さなければいけません.")
        print("ボスを倒してダンジョンを脱出しましょう.")
        sleep(sleep_time)
        print()
        print("ルール説明")
        print("あなたは隣接している部屋に移動することができます.")
        print("スタミナを1だけ消費して移動することができます.")
        print("一度行った部屋であれば、スタミナを1だけ消費して1マス戻ることもできます.")
        print("あなたは行動可能な2マス先の部屋しか見ることができません.")
        print("一度見えた部屋はその後も見えた状態のままです.")
        print("あなたのいるマスは濃い白色で表されています.")
        print("あなたの行動可能なマスは薄い白色で表されています.")
        sleep(sleep_time)
        print()
        print("戦闘について")
        print("モンスター(M)がいる部屋に到達すると、自動で戦闘が開始します.")
        print("あなたが先行し、あなた、モンスター、あなたと、交互に攻撃します.")
        print("与える・受けるダメージは、攻撃力の値のままです.")
        print("武器を取得することで、あなたの攻撃力を高めることができます.")
        sleep(sleep_time)
        print()
        print("部屋について")
        print("各部屋にはいくつかの効果があります.")
        print("Wがある部屋には武器が存在します. 武器をゲットすることで、攻撃力を高めることができます.")
        print("Gがある部屋にはゴールドが存在します. ゴールドを入手することで、ショップで買い物ができます. 0NG(Nは自然数)でNゴールドがあることを示しています.")
        print("!がある部屋にはショップが存在します. ショップではゴールドを使って、買い物ができます.")
        print("Eがある部屋にはイベントが存在します. ランダムでHPの10回復、スタミナの3回復、お金の取得ができます.")
        print("Kがある部屋には鍵が存在します. 宝箱を開けるための鍵を入手することができます.")
        print("Bがある部屋にはボス鍵が存在します.")
        print("Tがある部屋には宝箱が存在します.")
        print("Mがある部屋にはモンスターが存在します.")
        print("部屋の横にFがある部屋は既に到達した部屋です.")
        sleep(sleep_time)
        print()
        
        print("\r" + "ルール説明を終わるには、qキーを押してください : ", end="")
        _input = input("").rstrip("")
        # sys.stdout.write("\033[0K\033[0A%s" % _input)
        # sys.stdout.flush()
            
        while (True):
            if (_input == "q"):
                print("ゲームスタート!")
                sleep(0.5)
                break
            else:
                # sys.stdout.write("\033[0K\033[1A%s" % _input)
                # sys.stdout.flush()
                print("\r" + "もう一度入力してください(qキーで終了) : ", end="")
                _input = input().rstrip("")

    def advice_show(self) -> None:
        """
        敗北時のTipsを表示する.
        """
        # self.screen_delete()
        print("宝箱とイベントマスを踏むことが勝利の近道")
        self.user_input_q()
        # self.screen_delete()
        

class Node: # 幅優先探索を行う際にノードの役割をするクラス
    def __init__(self, parent, position: list[int]=None) -> None:
        """
        初期化関数
        
        Args:
            parent (Node): 親のNodeクラス
            position (list[int]): 部屋の座標

        Vars:
            parent (Node): 親のNodeクラス
            position (list[int]): 部屋の座標
        """
        self.parent: Node = parent
        self.position: list[int] = position


#人工知能クラス
class AI():
    def __init__(self, player, dungeon):
        """
        ダンジョン全体の情報を持つクラス.\n
        Args:
            player (Player) : プレイヤークラス.
            dungeon (Dungeon) : ダンジョンクラス
        Vars:
            treasure_pos(list[int]) : 宝箱の場所を保持、幅優先探索で用いる
            shop_pos(list[int]) : ショップの場所を保持、幅優先探索で用いる
            get_treasure(bool) : 宝箱を取得したかどうか
            importance(list[Room]) : 見つけた重要なマス
            searched_importance([list[Room]]) : 幅優先探索で探索済みの重要なマス
            is_buy(bool) : 購入画面にいるかどうか
            is_go_boss(bool) : ボス部屋に行くかどうか
            queue (list[Node]) : 幅優先探索に用いるキュー           
            visited (list[Node]) : 幅優先探索に用いる訪れたかどうかのリスト
            path (list[int]) : 幅優先探索で求めたルートを保存する
            directions (list[int]) : pathを入力する1,2,8,9に置き換えたもの。これを基にAIは行動する
            failed (bool) : 幅優先探索が失敗したかどうか。失敗したら、隠れたマスを目指して行動する
            player (Player) : プレイヤークラス
            dungeon (Dungeon) : ダンジョンクラス
        """
        self.treasure_pos: list[int] = []
        self.shop_pos: list[int] = []
        self.get_treasure: bool = False
        self.importance: list[Room] = []
        self.searched_importance = []
        self.is_buy: bool = False
        self.is_go_boss: bool = False

        self.queue: list[Node] = None           
        self.visited: list[Node] = []           
        self.path: list[int] = []                            
        self.directions: list[int] = []

        self.failed = False

        self.player = player
        self.dungeon = dungeon


        #幅優先探索の結果を用いて、ゴールまでの経路を作成する関数
    def return_path (self, node):
        #　出力経路リストの初期化
        path = []
        current = node
        # 現在の部屋がスタートになるまで迷路の場所を保存
        while current is not None:
            path.append(current.position)
            current = current.parent
        # 作成した経路はゴールノードからスタートノードまでなので逆方向にする
        path = path[::-1]
        # 戻り値は作成した経路
        return path

    def find_path(self, goal = None) -> None:
        """
        スタートから目的地までの経路を作成する関数
        作成した経路はself.pathに格納される
        Args:
            start (list[int]): スタート地点の座標
            aim (str): 目的地を決めるための目標
            prince (Hero): プリンス
        """
        #　スタートを作成
        begin_room = Node(None, list(self.player.now_loc))
        if (goal == None):
            flag = True
            count = 0
            #目的地の決定
            while flag and count < len(self.importance):
                #重要なマスから候補を持ってくる
                goal = self.importance[count]
                count += 1
                #一番最初はflagをFalseにして終了してよい
                if len(self.searched_importance) == 0:
                    flag = False
                for i in range(len(self.searched_importance)):
                    #すでに探索済みなら、breakしてfor文を終了
                    if (goal == self.searched_importance[i]):
                        break
                else:
                    flag = False
                
                #まだ鍵を持っていないなら宝箱の場所に行かないようにする
                if goal == self.treasure_pos:
                    if self.player.key_exist == False:
                        flag =True
                    
                #まだ宝箱を開けていないならショップに行かないようにする
                elif (goal == self.shop_pos):
                    if self.get_treasure == False:
                        flag = True

        else:
            pass
        print(f"選んだゴールはこれです{goal}")
            
        #ゴールを作成
        goal_room = Node(None, list(goal))
        
        # まだ訪問されていないノードと既に訪問されたノードを初期化。
        # 既に訪問されたノードは同じノードをもう1回訪問しないためのリスト
        self.queue = []
        self.visited = []

        # スタートノードはまだ訪問されていないので未訪問リストに保存
        self.queue.append(begin_room)
        
        # 2次元の迷路の可能な移動
        move = [[-1, 1],    # 右上
                [1, 1],    # 右下
                [-1, -1],     # 左上
                [1, -1]]     # 左下
        
        # ゴールを発見するまでのループ（まだ訪問されていない部屋がある限る続く）
        while len(self.queue) > 0:
            #　次に展開するノードは待ち行列の先頭なので待ち行列から取って、待ち行列から削除
            current_room = self.queue.pop(0)
            # 次に展開するノードを既に訪問された部屋に追加
            self.visited.append(current_room)
            
            # 展開のために選んだ部屋がゴールならば探索終了
            if current_room.position == goal_room.position:
                self.path = self.return_path(current_room)
                if goal in self.searched_importance:
                    return 
                #探索が終わったので、探索済みに登録
                self.searched_importance.append(goal)
                return
            
            # ノードを展開する。全ての可能な行動を把握
            # 可能な移動先のノードを保存するためのリストを初期化
            children = []
            for new_position in move:
                # 次の場所を把握
                room_position = [current_room.position[0] + new_position[0],
                                current_room.position[1] + new_position[1]]
                #　迷路から出ていないことを確認
                if (room_position not in DUNGEON_MAP):
                    continue
                
                #戻るときに訪れていなければ、いけないのでcontinue
                if new_position[1] < 0:
                    if self.dungeon.dungeon_list[room_position[0]][room_position[1]].reached == False:
                        continue
                    
                # 可能な移動先。その移動先の部屋を作成
                new_room = Node(current_room, room_position)

                # 可能な移動先の部屋を保存
                children.append(new_room)
    
            # 全ての作成された移動先の部屋に対して、既に訪問されたかどうか、未訪問部屋の中に既にあるかどうかを確認
            for child_room in children:
                # 子の場所は既に訪問されたら追加しない
                for visited_room in self.visited:
                    if child_room.position == visited_room.position:
                        break
                else:               
                    # まだ訪問されていない部屋の中に同じダンジョンの場所があるならば追加しない
                    for room in self.queue:
                        if child_room.position == room.position:
                            break
                    else:
                        #　未訪問部屋にない場合、未訪問部屋に追加
                        self.queue.append(child_room)
        
    # 購入画面の行動を行う関数
    def buy(self):
        select = ""
        need_stamina = BOSS_ROOM_POSITION[1] - self.player.now_loc[1]
        if (self.player.stamina < need_stamina) and (self.player.gold >= 5) :
            select = MEDICINE_RECOVER_STAMINA

        elif (self.player.weapon.attack < 6) and (self.player.gold >= 6):
            select = PINK_WEAPON

        elif (self.player.weapon.attack < 5) and (self.player.gold >= 4):
            select = YELLOW_WEAPON

        elif self.player.gold >= 5:
            select = MEDICINE_RECOVER_HP

        else:
            select = "q"

        return str(select)

    #行動を行う関数
    def act(self):
        direction = ""
        #購入画面なら購入処理を行う
        if self.is_buy:
            select = self.buy()
            return select
        
        #探索して求めた経路があればそれを基に行動
        elif self.directions:
            print("保存されたdirectionsを基に動いています")
            direction = self.directions.pop(0)
            return direction
        
        #経路探索かランダムに動く
        else:
            #隠れているマスを先に把握しておく
            hide_rooms = []
            for y, x in DUNGEON_MAP:
                if self.dungeon.dungeon_list[y][x].room_hide:
                    hide_rooms.append(self.dungeon.dungeon_list[y][x])

            #重要なマスを指定された分探索していたらボス部屋への経路探索
            if (len(self.searched_importance)) >= IMPORTANT_ROOM_NUM:
                print("他に重要なマスが無ければボス部屋へ向かいます")
                goal = BOSS_ROOM_POSITION
                self.is_go_boss = True    
                self.importance.append(BOSS_ROOM_POSITION)
                self.find_path()   
                for step in range(1, len(self.path)):
                    dir = [self.path[step][0] - self.path[step-1][0], self.path[step][1] - self.path[step-1][1]]
                    self.directions.append(DIR_DICT[tuple(dir)])
                direction = self.directions.pop(0)     
            
            #もし、新しく見つけた重要なマスがあり、幅優先探索に前回失敗していなければ
            elif self.search_importance() and self.failed == False:
                print("")
                print(f"aiのpathはこれです→{self.path}")
                print()
                print("重要なマスへの幅優先探索を行います")
                self.find_path()
                print(f"進むべき道は{self.path}")
                if len(self.path) >= 2:
                    for step in range(1, len(self.path)):
                        dir = [self.path[step][0] - self.path[step-1][0], self.path[step][1] - self.path[step-1][1]]
                        self.directions.append(DIR_DICT[tuple(dir)])
                    direction = self.directions.pop(0)
                        
                else:
                    self.failed = True
                    print("経路探索失敗")

            #隠れているマスがまだあったら
            elif hide_rooms:
                print(f"隠れているマスへの幅優先探索を行います")
                # if hide_rooms.room_pos <= 3:

                goal = hide_rooms.pop(0)
                self.find_path(goal.room_pos)
                print(f"進むべき道は{self.path}")
                for step in range(1, len(self.path)):
                    dir = [self.path[step][0] - self.path[step-1][0], self.path[step][1] - self.path[step-1][1]]
                    self.directions.append(DIR_DICT[tuple(dir)])
                self.failed = False
                direction = self.directions.pop(0)
                
            else:
                print("\n\n\nランダムに動きました\n\n\n")
                random_direction = random.choice(["1", "2", "8", "9"])
                direction = random_direction
        return direction
    
    #yを返すメソッド
    def input_y(self):
        return "y"
    
    #qを返すメソッド
    def input_q(self):
        return "q"
    
    #見えるマスを把握する関数
    def search_can_see(self):
        can_see_rooms = []
        for y, x in DUNGEON_MAP:
            if self.dungeon.dungeon_list[y][x].room_hide == False:
                can_see_rooms.append(self.dungeon.dungeon_list[y][x])
        
        return can_see_rooms

    #重要なマスを見つける関数
    def search_importance(self):
        can_see_rooms = self.search_can_see()
        #まだ、探索していない重要なマスがあればTrue
        new_importance = False
        for room in can_see_rooms:
            for room_event in room.room_event_info:
                if room_event.id in IMPORTANT_ROOMS:
                    #宝箱を見つけたら場所を保管しておく
                    if room_event.id == TREASUREROOM:
                        self.treasure_pos = room.room_pos
                    #ショップを見つけたら場所を保管しておく
                    elif room_event.id == SHOPROOM:
                        self.shop_pos = room.room_pos
                    #まだ、探索されていなかったら
                    if (room.room_pos) not in self.searched_importance:
                        new_importance = True
                        #まだ重要なマスとして知られていなかったら
                        if room.room_pos not in self.importance:
                            self.importance.append(room.room_pos)
                    
        return new_importance


#人工知能　ランダムAI
# class random_AI():
#     def __init__(self, player, dungeon):
#         self.importance: list[Room] = []
#         self.is_buy: bool = False

#         self.queue: list[Node] = None           
#         self.visited: list[Node] = []           
#         self.path: list[int] = []                            
#         self.directions: list[int] = []

#         self.player = player
#         self.dungeon = dungeon

#     def buy(self):
#         select = ""
#         need_stamina = BOSS_ROOM_POSITION[1] - self.player.now_loc[1]
#         if (self.player.stamina < need_stamina) and (self.player.gold >= 5) :
#             select = MEDICINE_RECOVER_STAMINA

#         elif (self.player.weapon.attack < 6) and (self.player.gold >= 6):
#             select = PINK_WEAPON

#         elif (self.player.weapon.attack < 5) and (self.player.gold >= 4):
#             select = YELLOW_WEAPON

#         elif self.player.gold >= 5:
#             select = MEDICINE_RECOVER_HP

#         else:
#             select = "q"

#         return str(select)

#     def act(self):
#         if self.is_buy:
#             select = self.buy()
#             return select

#         else:
#             random_direction = random.choice(["1", "2", "8", "9"])
#             direction = random_direction

#         return direction
    
#     def input_y(self):
#         return "y"
    
#     def input_q(self):
#         return "q"
    
#     def search_can_see(self):
#         can_see_rooms = []
#         for y, x in DUNGEON_MAP:
#             if self.dungeon.dungeon_list[y][x].room_hide == False:
#                 can_see_rooms.append(self.dungeon.dungeon_list[y][x])
        
#         return can_see_rooms

#     #重要なマスを見つける関数
#     def search_importance(self):
#         can_see_rooms = self.search_can_see()
#         for room in can_see_rooms:
#             for room_event in room.room_event_info:
#                 # self.event_exist_dic[room_event.id] = True
#                 if room.room_info in IMPORTANT_ROOMS:
#                     if room.room_pos not in self.importance:
#                         self.importance.append(room.room_pos)           
            

def main():
    dungeon_1_info_list = [
                            [[StartRoom()]], 
                            [[GoldRoom(2)], [WeaponRoom(Weapon("水色武器", 1, COLOR_DICT["Cyan"]))]], 
                            [[MonsterRoom(Monster(1, "黄色敵", 5, 2, False, COLOR_DICT["Yellow"])), GoldRoom(3)], [MonsterRoom(Monster(1, "黄色敵", 5, 2, False, COLOR_DICT["Yellow"])), GoldRoom(4)], [EventRoom()]], 
                            [[KeyRoom()], [EventRoom()], [MonsterRoom(Monster(2, "緑敵", 11, 2, False, COLOR_DICT["Green"])), GoldRoom(5), WeaponRoom(Weapon("青色武器", 3, COLOR_DICT["Blue"]))], [TreasureRoom(10, Weapon("オレンジ色武器", 7, COLOR_DICT["Magenta"]))]], 
                            [[BossKeyRoom()], [ShopRoom()], [MonsterRoom(Monster(3, "赤色敵", 9, 7, False, COLOR_DICT["Red"]))]], 
                            [[MonsterRoom(Monster(4, "水色敵", 17, 5, False, COLOR_DICT["Cyan"]))], [MonsterRoom(Monster(5, "白色敵", 21, 3, False, COLOR_DICT["White"]))]], 
                            [[MonsterRoom(Monster(6, "紫色敵", 29, 8, True, COLOR_DICT["Magenta"]))]]
                        ]

    dungeon_2_info_list = [
                            [[StartRoom()]], 
                            [[GoldRoom(2)], [WeaponRoom(Weapon("水色武器", 1, COLOR_DICT["Cyan"]))]], 
                            [[MonsterRoom(Monster(1, "黄色敵", 5, 2, False, COLOR_DICT["Yellow"])), GoldRoom(4)], [MonsterRoom(Monster(2, "緑色敵", 11, 2, False,  COLOR_DICT["Green"])), GoldRoom(3)], [EventRoom()]], 
                            [[KeyRoom()], [MonsterRoom(Monster(3, "赤色敵", 9, 7, False, COLOR_DICT["Red"])), WeaponRoom(Weapon("青色武器", 3, COLOR_DICT["Blue"]))], [GoldRoom(5)], [TreasureRoom(10, Weapon("オレンジ色武器", 7))]], 
                            [[BossKeyRoom()], [ShopRoom()], [GoldRoom(5)]], 
                            [[MonsterRoom(Monster(4, "水色敵", 17, 5, False, COLOR_DICT["Blue"]))], [MonsterRoom(Monster(5, "白色敵", 21, 3, False, COLOR_DICT["White"]))]], 
                            [[MonsterRoom(Monster(6, "紫色敵", 29, 8, True, COLOR_DICT["Magenta"]))]]
                        ]
    
    dungeon_3_info_list = [
                        [[StartRoom()]], 
                        [[GoldRoom(3)], [WeaponRoom(Weapon("水色武器", 1, COLOR_DICT["Cyan"]))]], 
                        [[MonsterRoom(Monster(1, "黄色敵", 5, 2, False, COLOR_DICT["Yellow"])), GoldRoom(2)], [MonsterRoom(Monster(2, "緑", 11, 2, False, COLOR_DICT["Green"])), GoldRoom(4)], [KeyRoom()]], 
                        [[GoldRoom(5)], [MonsterRoom(Monster(3, "赤敵", 9, 7, False, COLOR_DICT["Red"])), WeaponRoom(Weapon("青色武器", 3, COLOR_DICT["Blue"]))], [ShopRoom()], [EventRoom()]], 
                        [[BossKeyRoom()],[MonsterRoom(Monster(4, "水色敵", 17, 5, False, COLOR_DICT["Cyan"]))], [GoldRoom(5)]], 
                        [[TreasureRoom(10, Weapon("オレンジ色武器", 7))], [MonsterRoom(Monster(5, "白色敵", 21, 3, False, COLOR_DICT["White"])),GoldRoom(5)]], 
                        [[MonsterRoom(Monster(6, "紫色敵", 29, 8, True, COLOR_DICT["Magenta"]))]]
                        ]
    
    dungeon_info = random.choice([dungeon_1_info_list, dungeon_2_info_list, dungeon_3_info_list])
    
    player = Player()
    dungeon = Dungeon(dungeon_1_info_list, player)
    #人工知能　aiクラスの作成
    ai = AI(player, dungeon)
    # dungeon.screen_delete()
    
    # dungeon.rule_show(1)
    # dungeon.screen_delete()
    
    dungeon.room_contents_show()
    dungeon.dungeon_show()
    dungeon.user_input(ai)
    # dungeon.screen_delete()
    
    while True:
        if (player.stamina > 0):
            player.stamina -= 1
            room_now = dungeon.dungeon_list[player.now_loc[0]][player.now_loc[1]]
            room_now.process(player, ai)   # 部屋処理.
            
            if (player.win_check == True):
                player.calculate_score()
                print(f"Your Score: {player.score}")
                print("ゲーム終了")
                break
            
            elif (player.lose_check == True):
                player.calculate_score()
                input_key = dungeon.restart_select(ai)   # やり直しキーの受付. この中でゲーム終了まで行う
                if (input_key):
                    player.__init__()   # プレイヤーの初期化.
                    # dungeon.advice_show()
                    dungeon.reset()   # 部屋情報の初期化. 最悪マスをもう一回隠しても良い.
                    ai.__init__(player, dungeon) #人工知能の初期化
                else:
                    print("ゲーム終了")
                    break
            else:
                pass
   
        else:
            print("スタミナが切れてしまったので冒険者は力尽きてしまった...")
            player.calculate_score()
            input_key = dungeon.restart_select(ai)
            
            if (input_key):
                    player.__init__()   # プレイヤーの初期化.
                    # dungeon.advice_show()
                    dungeon.reset()   # 部屋情報の初期化. 最悪マスをもう一回隠しても良い.
                    ai.__init__(player, dungeon) #人工知能の初期化
            else:
                print("ゲーム終了")
                break
    
        dungeon.room_contents_show()
        dungeon.dungeon_show()
        dungeon.user_input(ai) #人工知能の行動選択
        # dungeon.screen_delete()
        

if __name__ == "__main__":
    main()
    