import pandas as pd
import sys
import datetime
import eel

RECEIPT_FOLDER="./receipt"

### 商品クラス
class Item:
    def __init__(self,item_code,item_name,price):
        self.item_code=item_code
        self.item_name=item_name
        self.price=price

### オーダークラス
class Order:
    def __init__(self,item_master):
        self.item_order_list=[]
        self.item_count_list=[]
        self.item_master=item_master
        self.set_datetime()
        
    def set_datetime(self):
        self.datetime = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    
    def add_item_order(self,item_code,item_count):
        self.item_order_list.append(item_code)
        self.item_count_list.append(item_count)
        
    def view_item_list(self):
        for item in self.item_order_list:
            print("商品コード:{}".format(item))
            
    # オーダー番号から商品情報を取得する
    def get_item_data(self,item_code):
        for m in self.item_master:
            if item_code == m.item_code:
                return m.item_name,m.price
    
    # オーダー入力
    def input_order(self, buy_item_code, buy_item_count):
        item = self.get_item_data(buy_item_code)
        if item!=None:
            print("{0} ({1}円)が登録されました".format(item[0], item[1]))
            eel.view_buy_item("{0} ({1}円)が登録されました".format(item[0], item[1]))
            self.add_item_order(buy_item_code,buy_item_count)
        else:
            print("「{}」は商品マスタに存在しません".format(buy_item_code))
            eel.view_buy_item("「{}」は商品マスタに存在しません".format(buy_item_code))


    def order_detail(self):
        number = 1
        self.sum_price = 0
        self.sum_count = 0
        self.receipt_name = "receipt_{}.log".format(self.datetime)
        self.write_receipt("-----------------------------------------------")
        self.write_receipt("オーダー登録された商品一覧\n")
        eel.view_sum_order("オーダー登録された商品一覧\n")
        for item_order,item_count in zip(self.item_order_list,self.item_count_list):
            result = self.get_item_data(item_order)
            self.sum_price += result[1] * int(item_count)
            self.sum_count += int(item_count)
            receipt_data = "{0}.{2}({1}) : ￥{3:,}　{4}個 = ￥{5:,}".format(number, item_order, result[0], result[1], item_count, int(result[1]) * int(item_count))
            self.write_receipt(receipt_data)
            eel.view_sum_order(receipt_data)
            number += 1
        # 合計金額、個数の表示
        self.write_receipt("-----------------------------------------------")
        eel.view_sum_order("-----------------------------------------------")
        self.write_receipt("合計金額:￥{0} {1}個".format(self.sum_price,self.sum_count))
        eel.view_sum_order("合計金額:￥{0} {1}個".format(self.sum_price,self.sum_count))
    
    def calc_money(self, payment_amount):
        if len(self.item_order_list) >= 1:
            self.change_money = int(payment_amount) - self.sum_price
            if self.change_money >= 0:
                self.write_receipt("お預り:￥{}".format(payment_amount))
                eel.view_payment("お預り:￥{}".format(payment_amount))
                self.write_receipt("お釣り：￥{}".format(self.change_money))
                eel.view_payment("お釣り：￥{}".format(self.change_money))
                print("ありがとうございました。")
                eel.view_payment("ありがとうございました。")
            else:
                print("￥{}　円不足しています。再度入力してください".format(self.change_money))
                eel.view_payment("￥{}　円不足しています。再度入力してください".format(self.change_money))

    def write_receipt(self,text):
        print(text)
        with open(RECEIPT_FOLDER + "\\" + self.receipt_name,mode="a",encoding="utf-8_sig") as f:
            f.write(text+"\n")
        
### マスタ登録
def regist_item_by_csv(csv_name):
    print("------- マスタ登録開始 ---------")
    item_master = []
    count=0
    try:
        # item_codeの0が落ちるため、dtypeを設定
        item_master_df = pd.read_csv("./{}".format(csv_name), dtype = {"item_code":object})
        for item_code,item_name,price in zip(list(item_master_df["item_code"]),list(item_master_df["item_name"]),list(item_master_df["price"])):
            item_master.append(Item(item_code,item_name,price))
            print("{}({})".format(item_name,item_code))
            count+=1
        print("{}品の登録を完了しました。".format(count))
        print("------- マスタ登録完了 ---------")
        return item_master
    except:
        print("マスタ登録が失敗しました")
        print("------- マスタ登録完了 ---------")
        sys.exit()
