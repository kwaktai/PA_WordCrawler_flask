import tkinter as tk
from tkinter import ttk
import word_crawler_clipboard as wcc
import data_exporter as de


def start_crawling():
    input_text = text_input.get("1.0", "end-1c")
    wcc.main(input_text)
    table = wcc.get_table()
    de.save_data(table)
    status_label.config(text="완료: 데이터가 저장되었습니다.")


def exit_app():
    root.destroy()


root = tk.Tk()
root.title("WordCrawler")

mainframe = ttk.Frame(root, padding="10")
mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

text_input = tk.Text(mainframe, wrap="word", width=40, height=10)
text_input.grid(column=0, row=1, columnspan=3, padx=5, pady=5)

start_button = ttk.Button(mainframe, text="크롤링 시작", command=start_crawling)
start_button.grid(column=0, row=0, padx=5, pady=5)

status_label = ttk.Label(mainframe, text="준비 중")
status_label.grid(column=1, row=0, padx=5, pady=5)

exit_button = ttk.Button(mainframe, text="종료", command=exit_app)
exit_button.grid(column=2, row=0, padx=5, pady=5)

root.mainloop()
