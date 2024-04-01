import tkinter as tk
import tkinter.font as tkFont
import sqlite3
from tkcalendar import DateEntry
from tkinter import messagebox


root = tk.Tk()
root.title("Günlük Uygulaması")
root.minsize(400, 600)

font1 = tkFont.Font(family="Open Sans", size=24)
font2 = tkFont.Font(family="Lato", size=10)
font3 = tkFont.Font(family="italic", size=12)

conn = sqlite3.connect('gunlukler.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS gunlukler
             (tarih TEXT, baslik TEXT, icerik TEXT)''')
conn.commit()

def remove_widgets():
    for widget in root.winfo_children():
        widget.destroy()

def yazıyı_sil():
    başlıkgirdi.delete(0, tk.END)
    içerikgirdi.delete("1.0", tk.END)


def bilgileriKaydet():
    tarih = tarihgirdi.get()
    baslik = başlıkgirdi.get()
    icerik = içerikgirdi.get("1.0", tk.END)
    yazıyı_sil()



    if not tarih.strip() or not baslik.strip() or not icerik.strip():
        messagebox.showerror("Hata  !", "Tarih , başlık ve içerik bilgilerini doldurmadınız !! ")
        return
    else :
        c.execute("INSERT INTO gunlukler (tarih, baslik, icerik) VALUES (?, ?, ?)", (tarih, baslik, icerik))
        conn.commit()
        tk.messagebox.showinfo("Bilgi", "Veriler başarıyla kaydedildi!")


def YeniGünlükOlustur():
    remove_widgets()



    cerceve2 = tk.LabelFrame(root, bg="light blue", cursor="star")
    cerceve2.pack(side="top", fill="both", expand=True)

    framebaslık2 = tk.Label(cerceve2, text="Günlük Oluşturma İşlemleri", font=font1, background="light blue")

    global tarihgirdi, başlıkgirdi, içerikgirdi

    tarih = tk.Label(cerceve2, text="Tarih : ", font=font3, background="light blue")
    tarihgirdi = DateEntry(cerceve2, width=50, font=font3)

    başlık = tk.Label(cerceve2, text="Başlık : ", font=font3, background="light blue")
    başlıkgirdi = tk.Entry(cerceve2, width=78)


    içerik = tk.Label(cerceve2, text="İçerik : ", font=font3, background="light blue")
    içerikgirdi = tk.Text(cerceve2, width=59, height=20)



    geridön = tk.Button(
        cerceve2,
        text="Geri Dön",
        bg="palevioletred",
        fg="black",
        activebackground="pink",
        activeforeground="black",
        height=2,
        width=10,
        cursor="hand2",
        command=page1,
        font=font3
    )
    kayıt = tk.Button(
        cerceve2,
        text="Kaydet",
        bg="palevioletred",
        fg="black",
        activebackground="pink",
        activeforeground="black",
        height=2,
        width=10,
        cursor="hand2",
        command=bilgileriKaydet,
        font=font3
    )
    framebaslık2.grid(row=0,column=1)
    tarih.grid(row=1, column=0, sticky="w")
    tarihgirdi.grid(row=1, column=1, padx=5, pady=5)
    başlık.grid(row=2, column=0, sticky="w")
    başlıkgirdi.grid(row=2, column=1, padx=5, pady=5)
    içerik.grid(row=3, column=0, sticky="w")
    içerikgirdi.grid(row=3, column=1, padx=5, pady=5)
    kayıt.grid(row=4, column=0, columnspan=2, pady=5)
    geridön.grid(row=5, column=0, columnspan=2, pady=5)

def GünlükleriListele():
    remove_widgets()

    cerceve3 = tk.LabelFrame(root, bg="light blue", cursor="star")
    cerceve3.pack(side="top", fill="both", expand=True)


    framebaslık3 = tk.Label(cerceve3, text="Günlük Listeleme İşlemleri", font=font1, background="light blue")
    framebaslık3.pack()


    c.execute("SELECT * FROM gunlukler")
    günlükler = c.fetchall()

    table_frame = tk.Frame(cerceve3, bg="cadetblue4")
    table_frame.pack(pady=10)

    table_canvas = tk.Canvas(table_frame, bg="cadetblue4")
    table_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    table_scroll = tk.Scrollbar(table_frame, orient=tk.VERTICAL, command=table_canvas.yview)
    table_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    table_canvas.configure(yscrollcommand=table_scroll.set)

    table = tk.Frame(table_canvas, bg="cadetblue4")
    table_canvas.create_window((0, 0), window=table, anchor='nw')

    tk.Label(table, text="Tarih", font=font3, bg="gray73", borderwidth=1, relief="solid").grid(row=0, column=0, padx=5, pady=5, sticky="ew")
    tk.Label(table, text="Başlık", font=font3, bg="gray73", borderwidth=1, relief="solid").grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    tk.Label(table, text="İçerik", font=font3, bg="gray73", borderwidth=1, relief="solid").grid(row=0, column=2, padx=5, pady=5, sticky="ew")

    for index, günlük in enumerate(günlükler, start=1):
        tarih, baslik, icerik = günlük
        tk.Label(table, text=tarih, font=font3, bg="white", borderwidth=1, relief="solid", wraplength=150).grid(row=index, column=0, padx=5, pady=5, sticky="ew")
        tk.Label(table, text=baslik, font=font3, bg="white", borderwidth=1, relief="solid", wraplength=150).grid(row=index, column=1, padx=5, pady=5, sticky="ew")
        içerik_label = tk.Label(table, text=icerik, font=font3, bg="white", borderwidth=1, relief="solid", wraplength=150)
        içerik_label.grid(row=index, column=2, padx=5, pady=5, sticky="ew")
        içerik_label.bind("<Configure>", lambda e: table_canvas.configure(scrollregion=table_canvas.bbox("all")))

    def on_mousewheel(event):
        table_canvas.yview_scroll(-1 * int(event.delta / 120), "units")

    table_canvas.bind_all("<MouseWheel>", on_mousewheel)

    geridön = tk.Button(
        cerceve3,
        text="Geri Dön",
        bg="palevioletred",
        fg="black",
        activebackground="pink",
        activeforeground="black",
        height=2,
        width=10,
        cursor="hand2",
        command=page1,
        font=font3
    )
    geridön.pack(pady=10)


def GünlükleriDüzenle():
    remove_widgets()

    cerceve5 = tk.LabelFrame(root, bg="light blue", cursor="star")
    cerceve5.pack(side="top", fill="both", expand=True)

    framebaslık3 = tk.Label(cerceve5, text="Günlük Güncelleme İşlemleri", font=font1, background="light blue")
    framebaslık3.pack()

    canvas = tk.Canvas(cerceve5, bg="light blue")
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(cerceve5, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    günlükler_frame = tk.Frame(canvas, bg="cadetblue4")
    canvas.create_window((0, 0), window=günlükler_frame, anchor="nw")

    c.execute("SELECT * FROM gunlukler")
    günlükler = c.fetchall()

    def veriyi_düzenle(baslik):
        c.execute("SELECT * FROM gunlukler WHERE baslik=?", (baslik,))
        günlük = c.fetchone()

        remove_widgets()

        cerceve6 = tk.LabelFrame(root, bg="light blue", cursor="star")
        cerceve6.pack(side="top", fill="both", expand=True)

        framebaslık3 = tk.Label(cerceve6, text="Günlük Güncelleme İşlemleri", font=font1, background="light blue")
        framebaslık3.pack()

        tarih_label = tk.Label(cerceve6, text="Tarih : ", font=font3, background="light blue")
        tarih_label.pack()
        tarihgirdi = DateEntry(cerceve6, width=50, font=font3)
        tarihgirdi.pack()
        tarihgirdi.set_date(günlük[0])

        başlık_label = tk.Label(cerceve6, text="Başlık : ", font=font3, background="light blue")
        başlık_label.pack()
        başlıkgirdi = tk.Entry(cerceve6, width=78)
        başlıkgirdi.pack()
        başlıkgirdi.insert(0, günlük[1])

        içerik_label = tk.Label(cerceve6, text="İçerik : ", font=font3, background="light blue")
        içerik_label.pack()
        içerikgirdi = tk.Text(cerceve6, width=59, height=20)
        içerikgirdi.pack()
        içerikgirdi.insert(tk.END, günlük[2])

        def güncelle():
            yeni_tarih = tarihgirdi.get()
            yeni_başlık = başlıkgirdi.get()
            yeni_içerik = içerikgirdi.get("1.0", tk.END)

            if not yeni_tarih.strip() or not yeni_başlık.strip() or not yeni_içerik.strip():
                messagebox.showerror("Hata  !", "Tarih , başlık ve içerik bilgilerini doldurmadınız !! ")
                return
            else:
                c.execute("UPDATE gunlukler SET tarih=?, baslik=?, icerik=? WHERE baslik=?",
                          (yeni_tarih, yeni_başlık, yeni_içerik, baslik))
                conn.commit()
                messagebox.showinfo("Bilgi", "Veri başarıyla güncellendi.")
                GünlükleriDüzenle()

        kaydet = tk.Button(
            cerceve6,
            text="Kaydet",
            bg="palevioletred",
            fg="black",
            activebackground="pink",
            activeforeground="black",
            height=2,
            width=10,
            cursor="hand2",
            command=güncelle,
            font=font3
        )
        kaydet.pack(pady=10)

        geriDön = tk.Button(
            cerceve6,
            text="Geri Dön",
            bg="palevioletred",
            fg="black",
            activebackground="pink",
            activeforeground="black",
            height=2,
            width=10,
            cursor="hand2",
            command=GünlükleriDüzenle,
            font=font3
        )
        geriDön.pack(pady=10)

    for günlük in günlükler:
        tarih, baslik, icerik = günlük
        düzenleme_bilgisi = f"Tarih: {tarih}, Başlık: {baslik}"
        düzenle_frame = tk.Frame(günlükler_frame, bg="cadetblue4", pady=5, padx=10)
        düzenle_frame.pack(anchor="center", fill="x")
        düzenle = tk.Button(
            düzenle_frame,
            text=düzenleme_bilgisi,
            bg="lavenderblush4",
            fg="black",
            activebackground="lavenderblush3",
            activeforeground="black",
            height=2,
            width=50,
            cursor="hand2",
            command=lambda baslik=baslik: veriyi_düzenle(baslik),
            font=font3
        )
        düzenle.pack()

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    günlükler_frame.bind("<Configure>", on_configure)

    canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

    alt_cerceve = tk.Frame(cerceve5, bg="light blue")
    alt_cerceve.pack(fill="both")

    geridön = tk.Button(
        alt_cerceve,
        text="Geri Dön",
        bg="palevioletred",
        fg="black",
        activebackground="pink",
        activeforeground="black",
        height=2,
        width=10,
        cursor="hand2",
        command=page1,
        font=font3
    )
    geridön.pack(pady=10, padx=(100, 100))


def GünlükleriSil():
    remove_widgets()

    cerceve4 = tk.LabelFrame(root, bg="light blue", cursor="star")
    cerceve4.pack(side="top", fill="both", expand=True)

    framebaslık = tk.Label(cerceve4, text="Silme İşlemleri", font=font1 ,background="light blue")
    framebaslık.pack()

    c.execute("SELECT * FROM gunlukler")
    günlükler = c.fetchall()

    table_frame = tk.Frame(cerceve4, bg="cadetblue4")
    table_frame.pack(pady=10)

    table_canvas = tk.Canvas(table_frame, bg="cadetblue4")
    table_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    table_scroll = tk.Scrollbar(table_frame, orient=tk.VERTICAL, command=table_canvas.yview)
    table_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    table_canvas.configure(yscrollcommand=table_scroll.set)

    table = tk.Frame(table_canvas, bg="cadetblue4")
    table_canvas.create_window((0, 0), window=table, anchor='nw')

    tk.Label(table, text="Tarih", font=font3, bg="gray73", borderwidth=1, relief="solid").grid(row=0, column=0, padx=5, pady=5, sticky="ew")
    tk.Label(table, text="Başlık", font=font3, bg="gray73", borderwidth=1, relief="solid").grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    tk.Label(table, text="İçerik", font=font3, bg="gray73", borderwidth=1, relief="solid").grid(row=0, column=2, padx=5, pady=5, sticky="ew")

    for index, günlük in enumerate(günlükler, start=1):
        tarih, baslik, icerik = günlük
        tk.Label(table, text=tarih, font=font3, bg="white", borderwidth=1, relief="solid", wraplength=150).grid(row=index, column=0, padx=5, pady=5, sticky="ew")
        tk.Label(table, text=baslik, font=font3, bg="white", borderwidth=1, relief="solid", wraplength=150).grid(row=index, column=1, padx=5, pady=5, sticky="ew")
        içerik_label = tk.Label(table, text=icerik, font=font3, bg="white", borderwidth=1, relief="solid", wraplength=150)
        içerik_label.grid(row=index, column=2, padx=5, pady=5, sticky="ew")
        içerik_label.bind("<Configure>", lambda e: table_canvas.configure(scrollregion=table_canvas.bbox("all")))

    def on_mousewheel(event):
        table_canvas.yview_scroll(-1 * int(event.delta / 120), "units")

    table_canvas.bind_all("<MouseWheel>", on_mousewheel)

    geridön = tk.Button(
        cerceve4,
        text="Geri Dön",
        bg="palevioletred",
        fg="black",
        activebackground="pink",
        activeforeground="black",
        height=2,
        width=10,
        cursor="hand2",
        command=page1,
        font=font3
    )

    silinecek_veri_label = tk.Label(cerceve4, text="Silmek istediğiniz verinin başlığını girin:", font=font3, background="light blue")
    silinecek_veri_label.pack()

    silinecek_veri = tk.Entry(cerceve4, width=50)
    silinecek_veri.pack(pady=5)
    silinecek_veri.focus()

    def sil():
        silinecek_başlık = silinecek_veri.get()

        c.execute("SELECT * FROM gunlukler WHERE baslik=?", (silinecek_başlık,))
        veri = c.fetchone()

        if veri is None:
            messagebox.showwarning("Uyarı", "Bu başlıkta bir veri bulunamadı.")
        else:
            c.execute("DELETE FROM gunlukler WHERE baslik=?", (silinecek_başlık,))
            conn.commit()
            messagebox.showinfo("Bilgi", "Veri başarıyla silindi.")
            GünlükleriSil()

    silme_butonu = tk.Button(
        cerceve4,
        text="Veriyi Sil",
        bg="palevioletred",
        fg="black",
        activebackground="pink",
        activeforeground="black",
        height=2,
        width=10,
        cursor="hand2",
        command=sil,
        font=font3
    )

    silme_butonu.pack(pady=10)
    geridön.pack(pady=10)


def page1():
    remove_widgets()

    cerceve1 = tk.LabelFrame(root, bg="light blue", cursor="star")
    cerceve1.pack(side="top", fill="both", expand=True)

    label1 = tk.Label(
        cerceve1,
        text="MENÜ",
        font=font1,
        background="light blue")

    buton = tk.Button(
        cerceve1,
        text="Yeni Günlük Oluştur",
        bg="palevioletred",
        fg="black",
        activebackground="pink",
        activeforeground="black",
        height=5,
        width=20,
        cursor="hand2",
        command=YeniGünlükOlustur,
        font=font2
    )
    buton1 = tk.Button(
        cerceve1,
        text="Günlükleri Listele",
        bg="palevioletred",
        fg="black",
        activebackground="pink",
        activeforeground="black",
        height=5,
        width=20,
        cursor="hand2",
        command=GünlükleriListele,
        font=font2
    )
    buton2 = tk.Button(
        cerceve1,
        text="Günlükleri Düzenle",
        bg="palevioletred",
        fg="black",
        activebackground="pink",
        activeforeground="black",
        height=5,
        width=20,
        cursor="hand2",
        command=GünlükleriDüzenle,
        font=font2
    )

    buton3 = tk.Button(
        cerceve1,
        text="Günlükleri Sil",
        bg="palevioletred",
        fg="black",
        activebackground="pink",
        activeforeground="black",
        height=5,
        width=20,
        cursor="hand2",
        command=GünlükleriSil,
        font=font2
    )
    label1.pack(pady=10)
    buton.pack(pady=10)
    buton1.pack(pady=10)
    buton2.pack(pady=10)
    buton3.pack(pady=10)

page1()
root.mainloop()
