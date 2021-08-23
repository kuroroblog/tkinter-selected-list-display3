import tkinter as tk
from tkinter import filedialog
import csv
import os

class Application(tk.Frame):
    # listbox Widgetに関する情報を格納する変数
    listBox = None
    # listbox Widgetに関する情報を格納する変数
    listBox1 = None

    # scale Widgetに関する情報を格納する変数
    fromScale = None
    # scale Widgetに関する情報を格納する変数
    toScale = None

    # csvデータに関する情報を格納する変数
    listboxData = {}

    # ボタンが選択された場合に、実行される関数
    def getFromToList(self):
        # listbox Widgetの現在選択している選択肢の、index(位置番号)を取得
        selectIdx = self.listBox.curselection()
        # csvの取得を完了しておらず、選択肢が表示されていないことを加味する。
        if len(selectIdx) > 0:
            # from行からto行の値をprintする。
            print(self.listBoxData[selectIdx[0]]['list'][self.fromScale.get() - 1 : self.toScale.get()])

    # ボタンが選択された場合に、実行される関数
    def clickBtn(self):
        # 単数ファイルを選択するためのdialogになります。
        # filetypes : csvファイルのみを選択できるようにする。
        # initialdir : filedialogを初回表示するディレクトリの設定。
        # 戻り値 : Openを選択してファイルを開いた場合 : ファイルパス, Cancelを選択した場合 : ''
        # filedialogについて : https://kuroro.blog/python/Um9TeIMMJAZdFqTYKVE6/
        filename = filedialog.askopenfilename(
            filetypes=[('csv files', '*.csv')], initialdir=os.getcwd())

        if not filename == '':
            # 参考 : https://intellectual-curiosity.tokyo/2020/11/29/python%E3%81%A7csv%E8%AA%AD%E3%81%BF%E6%9B%B8%E3%81%8D%E3%81%99%E3%82%8B%E6%96%B9%E6%B3%95%EF%BC%88%E3%83%98%E3%83%83%E3%83%80%E3%83%BC%E3%81%AE%E3%81%BF%E3%80%81%E3%83%98%E3%83%83%E3%83%80%E3%83%BC/
            with open(filename, 'r') as f:
                reader = csv.reader(f)
                # ヘッダーの読み込み
                headerList = reader.__next__()
                # 2回目以降に別のcsvファイルを読み込むことを想定して、リセットする。
                self.listBoxData = {}
                # tk.END : 末尾
                self.listBox.delete(0, tk.END)
                # tk.END : 末尾
                self.listBox1.delete(0, tk.END)

                for i in range(0, len(headerList)):
                    self.listBoxData[i] = {}
                    self.listBoxData[i]['name'] = headerList[i]
                    self.listBoxData[i]['list'] = []

                    # listbox Widgetへ選択肢を追加する。
                    # tk.END : 末尾
                    self.listBox.insert(tk.END, headerList[i])

                cnt = 0
                for rowList in reader:
                    cnt += 1
                    for j in range(0, len(rowList)):
                        self.listBoxData[j]['list'].append(rowList[j])

                # 選択されるcsvファイルの行数に応じて、scale Widgetの上限値(to)を変更する。
                self.fromScale.configure(to=cnt)
                self.toScale.configure(to=cnt)

    # listbox Widgetの選択肢が変更された場合に、実行する関数を設定。
    def getListFromSelectIdx(self, event):
        # listbox Widgetの現在選択している選択肢の、index(位置番号)を取得
        selectIdx = self.listBox.curselection()
        # csvの取得を完了しておらず、選択肢が表示されていないことを加味する。
        if len(selectIdx) > 0:
            self.listBox1.delete(0, tk.END)
            for list in self.listBoxData[selectIdx[0]]['list']:
                self.listBox1.insert(tk.END, list)

    def __init__(self, master=None):
        # Windowの初期設定を行う。
        super().__init__(master)

        # Windowへタイトルをつける。
        self.master.title("チョイス")
        # Windowの画面サイズを設定する。
        # geometryについて : https://kuroro.blog/python/rozH3S2CYE0a0nB3s2QL/
        self.master.geometry("700x700")

        # Windowを親要素として、frame Widget(Frame)を作成する。
        # Frameについて : https://kuroro.blog/python/P20XOidA5nh583fYRvxf/
        frame = tk.Frame(self.master)
        # Windowを親要素とした場合に、frame Widget(Frame)をどのように配置するのか?
        # packについて : https://kuroro.blog/python/UuvLfIBIEaw98BzBZ3FJ/
        frame.pack()

        # frame Widget(Frame)を親要素として、listbox Widgetを作成する。
        # height : 選択肢の表示数を設定。
        # selectmode : listbox Widgetの選択方法を設定。
        # Listboxについて : https://kuroro.blog/python/XMWVRR2MEZAe4bpPDDXE/
        self.listBox = tk.Listbox(frame, height=30, selectmode="single")

        # frame Widget(Frame)を親要素として、listbox Widgetをどのように配置するのか?
        # gridについて : https://kuroro.blog/python/JoaowDiUdLAOj3cSBxiX/
        self.listBox.grid(row=0, column=0)

        # listbox Widgetの選択肢が変更された場合に、実行する関数を設定。
        # 第一引数 : sequence(イベント内容(ボタンを選択する、文字を入力するなど)を設定)
        # 第二引数 : func(第一引数のイベント内容(ボタンを選択する、文字を入力するなど)が実行された場合に、呼ばれる関数を設定)
        # bindについて :  https://kuroro.blog/python/eI5ApJE1wkU7bHsuwk0H/
        self.listBox.bind("<<ListboxSelect>>", self.getListFromSelectIdx)

        # frame Widget(Frame)を親要素として、listbox Widgetを作成する。
        # height : 選択肢の表示数を設定。
        # selectmode : listbox Widgetの選択方法を設定。
        # Listboxについて : https://kuroro.blog/python/XMWVRR2MEZAe4bpPDDXE/
        self.listBox1 = tk.Listbox(frame, height=30, selectmode="single")

        # frame Widget(Frame)を親要素として、listbox Widgetをどのように配置するのか?
        # gridについて : https://kuroro.blog/python/JoaowDiUdLAOj3cSBxiX/
        self.listBox1.grid(row=0, column=1)

        # frame Widget(Frame)を親要素として、button Widgetを作成する。
        # text : テキスト情報
        # command : ボタンを選択した場合に、実行する関数を設定。self.clickBtnとする。
        # Buttonについて : https://kuroro.blog/python/oFju6EngDtcYtIiMIDf1/
        btn = tk.Button(frame, text="選択", command=self.clickBtn)

        # frame Widget(Frame)を親要素として、button Widgetをどのように配置するのか?
        # gridについて : https://kuroro.blog/python/JoaowDiUdLAOj3cSBxiX/
        btn.grid(row=1, column=0, columnspan=2)

        # frame Widget(Frame)を親要素として、scale Widgetを作成する。
        # from_ : scale Widgetの値に下限を設ける。
        # orient : scale Widgetの表示方向を設定。水平方向へ変更する。
        # Scaleについて : https://kuroro.blog/python/DUvG7YaE2i6jLwCxdPXJ/
        self.fromScale = tk.Scale(frame, from_=1, orient=tk.HORIZONTAL)
        # frame Widget(Frame)を親要素として、scale Widgetをどのように配置するのか?
        # gridについて : https://kuroro.blog/python/JoaowDiUdLAOj3cSBxiX/
        self.fromScale.grid(row=2, column=0, columnspan=2)

        # frame Widget(Frame)を親要素として、scale Widgetを作成する。
        # from_ : scale Widgetの値に下限を設ける。
        # orient : scale Widgetの表示方向を設定。水平方向へ変更する。
        # Scaleについて : https://kuroro.blog/python/DUvG7YaE2i6jLwCxdPXJ/
        self.toScale = tk.Scale(frame, from_=1, orient=tk.HORIZONTAL)
        # frame Widget(Frame)を親要素として、scale Widgetをどのように配置するのか?
        # gridについて : https://kuroro.blog/python/JoaowDiUdLAOj3cSBxiX/
        self.toScale.grid(row=3, column=0, columnspan=2)

        # frame Widget(Frame)を親要素として、button Widgetを作成する。
        # text : テキスト情報
        # command : ボタンを選択した場合に、実行する関数を設定。self.getFromToListとする。
        # Buttonについて : https://kuroro.blog/python/oFju6EngDtcYtIiMIDf1/
        btn = tk.Button(frame, text="from行からto行まで取得", command=self.getFromToList)
        # frame Widget(Frame)を親要素として、button Widgetをどのように配置するのか?
        # gridについて : https://kuroro.blog/python/JoaowDiUdLAOj3cSBxiX/
        btn.grid(row=4, column=0, columnspan=2, pady=(5, 5))

# Tkinter初学者参考 : https://docs.python.org/ja/3/library/tkinter.html#a-simple-hello-world-program
if __name__ == "__main__":
    # Windowを生成する。
    # Windowについて : https://kuroro.blog/python/116yLvTkzH2AUJj8FHLx/
    root = tk.Tk()

    app = Application(master=root)

    # Windowをループさせて、継続的にWindow表示させる。
    # mainloopについて : https://kuroro.blog/python/DmJdUb50oAhmBteRa4fi/
    app.mainloop()
