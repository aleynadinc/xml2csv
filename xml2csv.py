import xml.etree.ElementTree as ET
import os
###İstenmeyen data silme
def sil(silinecek,data): ## Birden fazla xml verisi üst üste konulduğundan dolayı verilerin öznitelikleri haricindeki aynı isimdeki liste isimlerinin bulunduğu satırlar silinir
    while True:
        if data.count(silinecek)!=0: ## data.count ile parantez içerisindeki elemanın kaç tane olduğunu görürüz
            data.remove(silinecek)  ## Eğer data.count bize 0 değerini vermemişse bu elemanı sil dedim
        else: ##Eğer data.count sıfır elemanı vermişse döngü sonlansın dedik
            break

dizin = input("Hedef klasör dizini : ") ## Dosların bulunduğu hedef klasör dizini yazılır
os.chdir(dizin) ## Dosyaların bulunduğu hedef klasör dizinine os modülü aracılığı ile geçiş yapılır
dosyalistesi = os.listdir(os.getcwd()) ## Hedef klasördeki dosyalar liste içerisine alınır

sira = 1
for i in dosyalistesi: ## For döngüsü sayesinde Hedef klasördeki dosyalar numaralar ile kullanıcı için sıralanır
    i = str(i)
    print("{} -) {}".format(sira,i)) ## Önce dosya numarası sonra dosyanın adı yazılır
    sira+=1

secilen_dosya_listesi= [] ## İleride seçilecek dosyaların bir liste içerisinde tutulabilmesi için boş bir liste oluşturulur
print("\nSeçeceğiniz dosyaların sırasıyla numarasını giriniz. Eğer seçiminiz bittiyse 'e' ya da 'E' harfini giriniz : ")

sira = 1
while True: ## Kullanıcı 'e' ya da 'E' harfleri girene kadar dosya numaraları ile seçmek istedikleri dosyaları seçerler ve bu dosyalar oluşturulan seçili dosya listesi içerisine eklenir
    secim = input("{}. seçiminiz : ".format(sira))
    sira+=1
    if secim == "e" or secim == "E":
        break
    else:
        secilen_dosya_listesi.append(dosyalistesi[int(secim)-1])

print("--- Seçilen dosyalar ---")
sira = 1
for i in secilen_dosya_listesi: ## For döngüsü ile seçim sıra numarası ile birlikte kullanıcıya gösterilir
    print("{} -) {}".format(sira,i))
    sira+=1

bozuk_dosyalar = [] ## Programda karşılaşılabilecek olası hatalı veya bozuk dosyaların uygulama sonrası gözükebilmesi için boş bir liste oluşturulur
saglam_dosyalar = [] ## Programda sorunsuz bir şekilde csv dosyasına dönüştürülen dosyalar listelenir

for okunan_dosya_adi in secilen_dosya_listesi: ## Seçilen dosya adı kadar dönen bir for döngüsü yapılır. Bu sayede program tüm dosyalar dönüştürülene kadar çalışacaktır

    while True: ## Olası hatalı dosyaların programı kapatma ihtimaline karşılık while True döngüsü yazılır. Bu sayede program çalışırken uygulamadaki bir dosya eğer bozuksa program kapanmadan for döngüsündeki bir sonraki seçili dosyaya geçilebilecektir 

        okunan_dosya_adi=str(okunan_dosya_adi) ## Seçilen dosya adının okunabilir bir dosya adı olması için string formatına dönüştürülür
        dosya_adi=okunan_dosya_adi+".csv" ## Yeni oluşan csv dosyasının ismi okunan dosya ile aynı olarak belirlenir ancak sonuna .csv uzantısı konur

        print("\n------- {} ------- ".format(okunan_dosya_adi)) ### For döngüsü sırasında hangi dosyada işlem yapıldığı kullanıcıya gösterilir
        
        with open(okunan_dosya_adi,"r",encoding="utf-8") as file: ## Okunan dosya 'r' parametresi (read) ile okunarak okunur (utf-8 ile Türkçe karakterler okunabilir hale gelir)
            data=""
            for i in file: ## Okunan dosyadaki her eleman bir data (yeni oluşturulan boş string) değişkeni içerisine eklenir. 
                data+=i 

        ## < > bunların arasındakini almadım (tempuriorg vs)
        data1 = ""
        buton = 1
        datakume = []

        for i in data: ## Data değişkeni içerisinde kullanılmayan kümelerden kurtulmak için buton mantığı ile bir for döngüsü yapılır.
            ## Okunan karakterler, içerisinde kullanılmayan satırların bazılarından arındırılmış olan bir data1 değişkeni içerisine atılır
            ## Bu döngüde ana kural, eğer data değişkeninde < işaretine gelinirse buton değişkeni 2 olacak ve bundan sonraki karakterleri okumayacaktır.
            ## > okuna geldikten sonra buton değişkeni tekrar 1 olarak bundan sonraki karakterleri almaya devam edecektir
            if i=="<":
                buton=2
            elif i==">":
                buton=1
            if buton==1 and i!=">":
                data1+=i

        data = data1.replace("\n\n", "\n")  ## Data değişkeni içerisindeki boş satırları silmeye yaramaktadır.
        data = data.replace("&lt;",
                            "<")  ## Kopyalama işlemi sonrası gelen ve normalde ok işareti olması gereken kümeler/satırlar replace ile düzeltilir
        data = data.replace("&gt;", ">")

        data = data.splitlines(True)  ##Her bir satırı bir listenin elemanı olarak almaya yarar

        if data[0]=="\n": #ilk satır boşluk ise ("\n" ise) siler
            data.remove(data[0])

        datailk = [data[0],data[1],data[2],data[3],data[4]] ## İlk 5 satırı datailk değişkeninin içine atar
        uzunluk = len(data) 
        datason = [data[uzunluk-2],data[uzunluk-1]] #son iki satırı datason değişkeninin içine atar


        ### Program başında yazılan sil fonksiyonu ile -birden fazla xml dosyası birleştirildiği için- gereksiz ve tekrar eden kümeler/satırlar silinir
        sil('<Table>\n',data)
        sil('  <Table_Detail>\n',data)
        sil('    <Table_Name>kbs_kapa.REHBER.kbs_kapa</Table_Name>\n',data)
        sil('  </Table_Detail>\n',data)
        sil('  <Data>\n',data)
        sil('</Table>\n',data)
        sil('  </Data>\n',data)
        sil('</Table>',data)
        sil('  <Data />\n',data)


        dataorta = ""
        for i in data: ##Liste olan data değişkeni string formatına çevrilerek dataorta adında bir değişkene atar.
            dataorta+=i


        datailkstring = ""
        for i in datailk: ##Liste olan datailk değişkeni string hale çevrilerek ve buna datailkstring değişkenine atar
            datailkstring+=i

        datasonstring = ""
        for i in datason: ##Liste olan datason değişkeni string hale çevrilerek ve buna datasonstring değişkenine atar
            datasonstring+=i

        data = str(datailkstring)+str(dataorta)+str(datasonstring) # Sonuç olarak hatalardan arındırılmış bir data klasörü oluşturulmuş olur

        try:  ## Kopyalama işlemi veya başka işlemler sırasında oluşabilecek veya yapılmış olası hataların programı kapatmaması için try fonksiyonu kullanılır
            myroot = ET.fromstring(data)  ##xml formatındaki veriyi işlemeye yarar
            saglam_dosyalar.append(
                okunan_dosya_adi)  ## Eğer dosya sağlam ise hata vermediği için saglam_dosyalar listesi içerisine kaydedilir
        except:
            print("\n {} isimli dosya hatalıdır.".format(okunan_dosya_adi))
            bozuk_dosyalar.append(okunan_dosya_adi) ## Eğer dosya bozuk/hatalı bir dosya ise bozuk_dosyalar listesi içerisine atılır ve while True döngüsü sonlandırılarak for döngüsüne geri geçiş yapılır
            break

        j = len(myroot[1]) #Veri sayısını verir
        l = len(myroot[1][0]) #öznitelik sayısını verir

        print("\nVeri sayısı :",j)
        print("Öznitelik sayısı : ",l)
        print("\n")


        with open(dosya_adi,"w",encoding="utf-8") as file:

            for k in range(0,l): ##Öznitelik isimleri
                a = myroot[1][0][k]
                stra = str(a) ## özniteliğin yazdığı elementi stringe cevir
                stra = stra.split("'") ##Kesme işaretine göre listeler
                stra = stra[1] ##Liste içindeki 2. elemanı yani öznitelik ismini alır
                if k==l-1: ##Öznitelikleri virgülle ayırmaya yarar. Eğer son elemana gelindiyse virgül koymaz.
                    print("{}".format(stra))
                    file.write("{}\n".format(stra)) ## csv dosyasına yazar (son eleman olduğu için virgülsüz)
                else:
                    print("{},".format(stra),end="")
                    file.write("{},".format(stra)) ## csv dosyasına yazar (virgüllü)


            for i in range(0,j): ##Veriler
                for k in range(0,l):
                    a = myroot[1][i][k]
                    if k==l-1:
                        print("{}".format(a.text))  ## a.text diyince özniteliğe karşılık gelen veriyi buluruz
                        file.write("{}\n".format(a.text))
                    else:
                        print("{},".format(a.text),end="")
                        file.write("{},".format(a.text))
        break ##while True döngüsü, hatasız çalışsa da sonsuza kadar dönmemesi ve bir önceki for döngüsüne geçiş yapılarak sonraki okunanacak dosyaya geçilebilmesi için sonlandırılır


print("\n\nDönüştürülemeyen bozuk dosyalar listesi : ",bozuk_dosyalar)
print("\nDönüştürülebilen saglam dosyalar listesi : ",saglam_dosyalar)

input("\nProgramı kapatmak için bir tuşa basınız...") ## Programın bir exe dosyası niteliği taşıyarak çalışma olasılığına karşı aniden kapanmaması için kullanıcıya programı kapatma fırsatı sunar.