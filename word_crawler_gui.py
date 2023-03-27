import tkinter as tk
from tkinter import ttk
import word_crawler_clipboard as wcc
import data_exporter as de


def start_crawling():
    input_text = text_box.get("1.0", tk.END).strip()
    if input_text:
        status_label.config(text="번역 중")
        root.update_idletasks()
        wcc.main(input_text)
        table = wcc.get_table()
        de.save_data(table)
        status_label.config(text="완료: 데이터가 저장되었습니다.")
        text_box.delete(1.0, tk.END)
        text_box.insert(tk.END, wcc.get_original_text())
        text_box.tag_add(tk.SEL, "1.0", tk.END)
    else:
        status_label.config(text="오류: 텍스트 박스가 비어있습니다.")


def exit_app():
    root.destroy()


root = tk.Tk()
root.title("WordCrawler")

mainframe = ttk.Frame(root, padding="10")
mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

start_button = ttk.Button(mainframe, text="크롤링 시작", command=start_crawling)
start_button.grid(column=0, row=0, padx=5, pady=5)

status_label = ttk.Label(mainframe, text="준비 중")
status_label.grid(column=1, row=0, padx=5, pady=5)

exit_button = ttk.Button(mainframe, text="종료", command=exit_app)
exit_button.grid(column=2, row=0, padx=5, pady=5)

text_box = tk.Text(mainframe, wrap=tk.WORD, width=50, height=25)
text_box.grid(column=0, row=1, columnspan=3,
              padx=5, pady=5, sticky=(tk.W, tk.E))

root.mainloop()
