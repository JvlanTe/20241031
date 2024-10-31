import tkinter
from tkinter import ttk, Button, Label, Entry, messagebox
import json
import requests
import os
import dotenv
from dotenv import load_dotenv

load_dotenv(override=True)

subdomain = os.getenv("kintone_url")

app_id = os.getenv("app_id")

api_token = os.getenv("kintone_api")

url = f"https://{subdomain}.cybozu.com/k/v1/record.json"

headers = {"X-Cybozu-API-Token": api_token, "Content-Type": "application/json"}


# def submit_form():
#     name = entry_name.get()
#     fur = entry_fur.get()
#     postal_code = entry_postal.get()
#     address = entry_address.get()
#     address_number = entry_address_number.get()
#     selected_department = dropdown_department.get()

#     print("氏名：", name)
#     print("フリガナ：", fur)
#     print("郵便番号：", postal_code)
#     print("住所：", address)
#     print("番地：", address_number)
#     print("所属部署：", selected_department)


def search_address():
    zipcode = entry_postal.get().strip()
    if not zipcode:
        messagebox.showwarning("入力エラー", "郵便番号を入力してください。")

        return
    address_number = entry_postal.get()
    response = requests.get(f"https://zipcloud.ibsnet.co.jp/api/search?zipcode={address_number}")
    data = response.json()

    address1 = data["results"][0]["address1"]
    address2 = data["results"][0]["address2"]
    address3 = data["results"][0]["address3"]

    address = f"{address1}{address2}{address3}"
    entry_address.insert(0, address)


def my_app3():
    name = entry_name.get()
    fur = entry_fur.get()
    postal_code = entry_postal.get()
    address = entry_address.get()
    address_number = entry_address_number.get()
    selected_department = dropdown_department.get()

    data = {
        "app": app_id,
        "record": {
            "name": {"value": name},
            "fur": {"value": fur},
            "postal": {"value": postal_code},
            "address": {"value": address},
            "address_number": {"value": address_number},
            "department": {"value": selected_department},
        },
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:  # 200が正常の応答
        result_label.config(text="データが正常に登録されました")
        print("データが正常に追加されました")
        entry_name.delete(0, tkinter.END)
        entry_fur.delete(0, tkinter.END)
        entry_postal.delete(0, tkinter.END)
        entry_address.delete(0, tkinter.END)
        entry_address_number.delete(0, tkinter.END)
        dropdown_department.delete(0, tkinter.END)
    else:
        result_label.config(text="データが登録できませんでした")
        print("エラーが発生しました", response.status_code)

    print("氏名：", name)
    print("フリガナ：", fur)
    print("郵便番号：", postal_code)
    print("住所：", address)
    print("番地：", address_number)
    print("所属部署：", selected_department)


root = tkinter.Tk()
root.title("社員登録画面")

label_name = Label(root, text="氏名：")
label_name.grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_name = Entry(root)
entry_name.grid(row=0, column=1, padx=10, pady=5)

label_fur = Label(root, text="フリガナ：")
label_fur.grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_fur = Entry(root)
entry_fur.grid(row=1, column=1, padx=10, pady=5)

label_postal = Label(root, text="郵便番号：")
label_postal.grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_postal = Entry(root)
entry_postal.grid(row=2, column=1, padx=10, pady=5)

auto_fill_button = Button(root, text="住所自動入力", command=search_address)
auto_fill_button.grid(row=2, column=2, padx=5, pady=5)

label_address = Label(root, text="住所：")
label_address.grid(row=3, column=0, padx=10, pady=5, sticky="e")
entry_address = Entry(root)
entry_address.grid(row=3, column=1, padx=10, pady=5)

label_address_number = Label(root, text="番地：")
label_address_number.grid(row=4, column=0, padx=10, pady=5, sticky="e")
entry_address_number = Entry(root)
entry_address_number.grid(row=4, column=1, padx=10, pady=5)

label_department = Label(root, text="所属部署：")
label_department.grid(row=5, column=0, padx=10, pady=5, sticky="e")
department = ["経理部", "開発部"]
dropdown_department = ttk.Combobox(root, values=department, state="readonly")
dropdown_department.set(department[0])
dropdown_department.grid(row=5, column=1, padx=10, pady=5)

submit_button = Button(root, text="登録", command=my_app3)
submit_button.grid(row=6, column=0, columnspan=3, pady=20)

result_label = Label(root, text="")
result_label.grid(row=7, column=0, columnspan=3, pady=25)

root.mainloop()
