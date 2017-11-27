import bs4
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import curses
import webbrowser
def curses_main(args):
    stdscr = curses.initscr()
    pad_height, pad_width = stdscr.getmaxyx()
    pad = curses.newpad(200,100)
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.cbreak()

    stdscr.keypad(True)
    curses.noecho()
    curses.curs_set(0)
    news_list=get_articles()
    selected_item_number = 0

    while True:
        pad.addstr(0,0, "Habrahabr RSS. (j,k - to navigate, l - to select, q - to exit)")
        y=2
        item_number = 0
        for item in news_list:

            if item_number == selected_item_number:
                attribute = curses.color_pair(1)
            else:
                attribute = curses.color_pair(2)
            pad.addstr(y,2, item.title.text, attribute)
            y += 2
            item_number += 1
        stdscr.refresh()
        pad.refresh(0,0,0,0,pad_height-1,pad_width-1)

        c = pad.getch()
        if c == ord("q"):
            break   #exit from script
        if c == ord("j"):
            selected_item_number += 1
            if selected_item_number > (len(news_list)-1):
                selected_item_number = 0
        if c == ord("k"):
            selected_item_number -= 1
            if selected_item_number < 0:
                selected_item_number = len(news_list)-1
        if c == ord("l"):
            webbrowser.open(news_list[selected_item_number].link.text, 2) #open a selected article in a default browser
            break #exit from script
def get_articles():
    ''' Get last articles from Habr

    No arguments

    Returns: list of bs4.element.Tag objects
    '''
    my_url="https://habrahabr.ru/rss/hubs/"
    Client=urlopen(my_url)

    xml_page=Client.read()
    Client.close()

    soup_page=soup(xml_page, "xml")
    news_list=soup_page.findAll("item")
    return news_list

curses.wrapper(curses_main)
curses.endwin()
