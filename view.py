import eel
import desktop
import pos_system

ITEM_MASTER_CSV_PATH="./item_master.csv"

app_name="html"
end_point="index.html"
size=(700,600)

@ eel.expose
def add_item_master(csv_name):
    global order
    item_master = pos_system.regist_item_by_csv(csv_name)
    order = pos_system.Order(item_master)

@ eel.expose
def add_order(buy_item_code, buy_iitem_count):
    order.input_order(buy_item_code, buy_iitem_count)

@ eel.expose
def sum_order():
    order.order_detail()

@ eel.expose
def calc_money(payment_amount):
    order.calc_money(payment_amount)

desktop.start(app_name, end_point,size)
#desktop.start(size=size,appName=app_name,endPoint=end_point)