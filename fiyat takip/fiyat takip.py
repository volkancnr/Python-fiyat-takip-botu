import requests
import smtplib
import time
from bs4 import BeautifulSoup   

#fiyatını öğrenmek istediğimiz ürünün linki
url = 'https://www.hepsiburada.com/lenovo-v14-g2-itl-intel-core-i5-1135g7-8gb-512gb-ssd-freedos-14-fhd-tasinabilir-bilgisayar-82ka006xtx-p-HBCV00000DBWL5'

#user agent
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}


def check_price():
    #url üzerinden istediğimiz ürünün isim, fiyat verileri 
    page= requests.get(url,headers=headers)
    soup= BeautifulSoup(page.content,'html.parser')
    urun = soup.find(id='product-name').get_text().strip()
    #(ÖNEMLİ!!) Ürün isminde Türkçe karakter olduğu zaman mail kısmında hata verecektir hatanın önüne geçmek için urun değişkeninde Türkçe karakter almayacak şekilde değişkeni sınırlandırıyoruz!!
    urun= urun[0:18]
    print(urun)
    span=  soup.find(id='offering-price')
    fiyat= float(span.attrs.get('content'))
    print(fiyat)

    #mail gelmesini istediğiniz fiyat aralığı
    if fiyat<99999:
       send_mail(urun)

def send_mail(urun):

    gonder='GONDEREN_MAİL'
    #alıcı e-posta
    alici='ALİCİ_MAİL'
    #server başlatıp mail gönderme işlemi
    try:
        server= smtplib.SMTP("smtp.gmail.com",587)
        server.ehlo()
        server.starttls()
        server.login(gonder,'SİFRE')
        subject= urun + 'istedigin fiyata dustu'
        body= 'Bu linkten gidebilirsin=>' + url
        mailcontent = f'To:{alici}\nFrom:{gonder}\nSubject:{subject}\n\n{body}'
        server.sendmail(gonder,alici,mailcontent)

        print("mail Gonderildi")
    except smtplib.SMTPException as e:
        print(e)
    finally:
        server.quit()
#chech_price fonksiyonunu verilen aralıkta döngüde sokma    
while True:
    check_price()
    time.sleep(60*60)
    





