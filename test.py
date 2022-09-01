import bs4
import requests
import bs4
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"} # информация для сервера
# city = 'екатеринбург'
def pog(city):
    r = requests.get(f"https://www.google.com/search?q="+"weather" + city).content # запрос
    print(r) # если ответ на запрос имеет код 200, то все хорошо
    soup = bs4.BeautifulSoup(r, 'html.parser' )
    temp = soup.find( 'div' , attrs = { 'class' : 'BNeawe iBp4i AP7Wnd' }).text
    return temp


# str = soup.find( 'div' , attrs = { 'class' : 'BNeawe tAd8D AP7Wnd' }).text
# # format the data
# data = str .split( ' ' )
# time = data[ 0 ]
# sky = data[ 1 ]
#
# # list having all div tags having particular clas sname
# listdiv = soup.findAll( 'div' , attrs = { 'class' : 'BNeawe s3v9rd AP7Wnd' })
# # particular list with required data
# strd = listdiv[ 5 ].text
# # formatting the string
# pos = strd.find( 'Wind' )
# other_data = strd[pos:]
#
# print ( "Temperature is" , temp)
# print ( "Time: " , time)
# print ( "Sky Description: " , sky)
# print (other_data)