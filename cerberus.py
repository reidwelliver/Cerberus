from HTMLParser import HTMLParser
from bs4 import BeautifulSoup
from multiprocessing import Process, Lock
import urllib2
import csv
import pickle


f = open('data.txt', 'w')

csv_arr = []
companies = []
companies_owned = []
total_checked = 0

price_book_f = 1
beta_f = 1
div_yield_f = 0
mark_cap_act_f = 200 * 1000000

def add_ticker():
    print "enter ticker"
    n=raw_input()
    print "enter numberowned"
    m=raw_input()
    companies_owned[n]=m

def ticker():
    path = "companylist.csv"
    csv_file = open(path, 'rb');
    csv_reader = csv.reader(csv_file, delimiter = ",", quotechar = "\"")
    for row in csv_reader:
        csv_arr.append((row[0], row[1]))
    # while True:
    #     print "Enter Your Portfolio for tailored search"
    #     print "type ticker symbol to view holdings"
    #     print "type 'add' to add companies or 'quit' to continue to search"
    #     x=raw_input()
    #     if x=='quit':
    #         break
    #     if x in companies_owned.keys():
    #         print companies_owned[x], x
    #     if x=='add':
    #         add_ticker()

def funct(start, fin, thread_num):
    global div_yield_f
    global mark_cap_act_f
    global beta_f
    global price_book_f

    print start, " - ", fin, ": ", thread_num, " Thread Started"
    global total_checked
    for i in range (start, fin):
        # print i
        # print "thread: ", thread_num, " :   ", i, " - ", fin
        total_checked += 1
        try:
            cnn = 'http://money.cnn.com/quote/quote.html?symb=' + csv_arr[i][0]
            cnn_soup = BeautifulSoup(urllib2.urlopen(cnn))
            nasdaq = 'http://www.nasdaq.com/symbol/' + csv_arr[i][0]
            nasdaq_soup = BeautifulSoup(urllib2.urlopen(nasdaq))
            price_book = cnn_soup.find('td', text = "Price/Book").next_sibling.text
            div_yield = cnn_soup.find('td', text = "Dividend yield").next_sibling.text
            # beta = nasdaq_soup.find(text="Beta").findNext('td').contents[0]
            if float(price_book) < price_book_f:
                companies.append([csv_arr[i][0], price_book])
                mark_cap = cnn_soup.find('td', text = "Market cap").next_sibling.text[1:]
                mark_cap_act = ((float)(mark_cap[:-1]))
                if mark_cap[-1:] == "B":
                    mark_cap_act = (int)(mark_cap_act * 1000000000)
                if mark_cap[-1:] == "M":
                    mark_cap_act = (int)(mark_cap_act * 1000000)
                if mark_cap_act > mark_cap_act_f:
                    print csv_arr[i][0] , "   ", price_book, "   ", mark_cap, "   ", div_yield, "   ", "Beta =", beta, csv_arr[i][1], " Progress: ", i, " of 3250 checked."
                    # pass
                    # f.write(csv_arr[i][0] , "   ", price_book, "   ", mark_cap, "   ", csv_arr[i][1], "\n")
            if i % 20 == 0:
                pass
                            
        except Exception as e:
            print e
            pass

def main():
    global div_yield_f
    global mark_cap_act_f
    global beta_f
    global price_book_f

    print "Enter params"
    print "Enter price_book \n"
    price_book_f = raw_input();
    print "Enter beta"
    beta_f = raw_input()
    print "Enter div yield"
    div_yield_f = raw_input();
    params = {"price_book":price_book_f, "beta":beta_f, "div_yield":div_yield_f}
    ticker()
    for u in range(0, len(csv_arr)/50):
            # print u
        Process(target = funct, args = (u * 50, (u + 1) * 50, u)).start()
    # Process(target = funct, args = (0, 21)).start()
    # p.start()
        

main()


