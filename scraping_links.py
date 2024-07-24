from bs4 import BeautifulSoup
import requests

def main(URL):
    
    File = open("out.csv", "a")
    
    HEADERS  = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
    
    webpage = requests.get(URL, headers=HEADERS)

    # Creating the Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "lxml")
    
    try:
        # Outer Tag Object
        for div in soup.findAll("div", attrs={"class": 'bxc-grid_image bxc-gridimage--light bxc-gridimage--beauty bxc-grid_image--beauty'}):
            links = [a['href'] for a in div.find_all('a', href=True)]
            with open("out.txt", "a") as file:
                for link in links:
                    file.write("https://www.amazon.in"+link+"\n")

    except AttributeError:
        moblinks = "NA"


if __name__ == '__main__':
  # opening our url file to access URLs
    file = open("url.txt", "r")
 
    # iterating over the urls
    for links in file.readlines():
        main(links)