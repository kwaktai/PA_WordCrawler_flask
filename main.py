import word_crawler_clipboard as wcc
import data_exporter as de


def main():
    wcc.main()
    table = wcc.get_table()
    de.save_data(table)


if __name__ == "__main__":
    main()
