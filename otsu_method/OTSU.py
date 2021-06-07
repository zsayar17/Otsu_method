import cv2
import numpy as np



path="fotografci.jpeg"


img=cv2.imread(path)#resimi okuduk


img= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)



img = cv2.resize(img,(224,224))



shappe=img.shape
m=shappe[0]#satır sayısı
n=shappe[1]#sütun sayısı



def graytobw(img,tresh,m,n):# 1  ve 0 a döndürdük pikselleri yani siyah ve beyaza çevirdik

    newİmage=np.zeros(m*n).reshape(m,n) #yeni bir liste oluşturduk 0lardan oluşan m satır n sütun kadar 
    for i in range(0,m):
        for j in range(0,n):
            if (img[i][j]>=tresh): #denk gelen değer eşiklikden büyük eşitse 1 değilse 0 yap dedik
                newİmage[i][j]=1
            else:
                newİmage[i][j]=0
    return newİmage


def howmany(img,m,n):#grinin aralığı olan 0dan 256 ya kadar kaçar tane piksel var onu hesapladık 
    newlist=[]
        
    for i in range(0,256):
        count=0
            
            
        for j in range(0,m):
            for q in range(0,n):
                   
                if img[j][q]==i:
                    count+=1
        newlist.append(count)
    return newlist
    
class Otsu:
    
    def __init__(self,m,n,baslangıc,liste,howmany):
        self.m=m
        self.n=n
        self.howmany=howmany
        self.baslangıc=baslangıc
        self.liste= liste
        self.mean=self.calculatemean()
        
    

    
    
    def calculateweight(self,x,y):#ağrlığı hesapladık  
        weight=0
        
        
        for i in self.liste:
        
            weight+=i#toplam kaç tane  onu hesapladık mesela gelen listede 0,5,7,8 geldi diyelim  0dan 0 tane var 1 den 5 tane  2 den 7 tane bunları çarpıp  topladık
           
        
        weight=weight/(self.m*self.n)
        
        return weight
    
    
    
    
    def calculatemean(self):#ortalamayı hesapladık
        mean=0
        toplam=0
     
        
        for i in range(self.baslangıc,self.baslangıc+len(self.liste)):#hangi pikselden  kaç tane varsa çarpıp topladık
                
            mean+=i*self.howmany[i]
            
            
        for i in self.liste:  # toplam kaç tane  onu hesapladık mesela gelen listede 0,5,7,8 geldi diyelim  0dan 0 tane var 1 den 5 tane  2 den 7 tane bunları çarpıp  topladık
            toplam+=i
            
        try:
            
            mean=mean/toplam #ortalamayı hesapladık
        except:
            mean=0
        finally:
            return mean 
    
    
    
       
    def calculatevariance(self):#varyansı hesapladık
        toplam=0
        variance=0
        
        for i in self.liste:  # toplam kaç tane  onu hesapladık mesela gelen listede 0,5,7,8 geldi diyelim  0dan 0 tane var 1 den 5 tane  2 den 7 tane bunları çarpıp  topladık
            
            toplam+=i
        
        for i in range(self.baslangıc,self.baslangıc+len(self.liste)):#pikselleri ortalamalar ile çarptık

            a=(i-self.mean)*(i-self.mean)*self.howmany[i]
            variance+=a
            
    
        try:
            variance=variance/toplam
        except:
            variance=0
        finally:
            return variance 

           

x=howmany(img, m, n)

def esikbul(img):  #esiklerini bulduk ve aralarında ki en küçük eşiği return ile yolladık
    
    
    for i in range(0,len(img)+1):
        
        if img[:i]==[]:
            backgroundvariance=0
            backgroundweight=0
            
        else:#backgtound için hesaplamalar yaptık
            
            
            
            background=Otsu(m,n,0,img[:i],x) 
            backgroundweight=background.calculateweight(m,n)
            
            backgroundvariance=background.calculatevariance()
        if img[i:]==[]:
            frontgroundvariance=0
            frontgroundweight=0
            
        else:#frontground için hesaplamalar yaptık
            
            frontground=Otsu(m,n,i,img[i:],x)
            frontgroundweight=frontground.calculateweight(m,n)
            
            frontgroundvariance=frontground.calculatevariance() 
            
            
            
        esiklik=(backgroundvariance*backgroundweight)+(frontgroundvariance+frontgroundweight)
        if i==0: #ilk eşikliğe ilk sırada ki değeri verdik
            esiklikk=esiklik=(backgroundvariance*backgroundweight)+(frontgroundvariance+frontgroundweight)
       
        if (esiklik<esiklikk): #eğer sırada ki eşiklik dahan önce ki en küçük eşiklikten küçükse yeni esikkliği ona atadık 
            esiklikk=esiklik
            tresh=i
    
    return tresh
            
        
        
tresh=esikbul(x)
newimage=graytobw(img, tresh, m, n)



    
    
        


    
    
    

