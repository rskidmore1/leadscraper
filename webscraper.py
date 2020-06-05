import requests
from bs4 import BeautifulSoup

#enter yelp url here


#Edit me here
#=======================================================

'''
yelpCounties = ['https://www.yelp.com/search?find_desc=Plumbers&find_loc=Orange+County%2C+CA&ns=1',
                'https://www.yelp.com/search?find_desc=Plumbers&find_loc=Los%20Angeles%2C%20CA',
                'https://www.yelp.com/search?find_desc=Plumbers&find_loc=San%20Diego%2C%20CA',
                'https://www.yelp.com/search?find_desc=Plumbers&find_loc=San%20Francisco%2C%20CA',
                'https://www.yelp.com/search?find_desc=Plumbers&find_loc=Sacramento%2C%20CA'] 
'''

#CaliforniaLocations = ['orange county, CA', 'san diego, CA', 'los angeles, CA',  'san Francisco, CA', 
#'Sacramento, CA', 'Riverside County, CA', 'Bakersfield, CA'] #DONE WITH CALIFORNIA FOR NOW
#CAindustries = ['plumbers', 'HVAC', 'electrical,  'landscaping', 'roofing', 'irrigation', 'cleaning',  'mobile mechanic', 'autoparts delivery', 'flooring', 'pest control'] 


#westerstates = ['portland, OR', 'bend, OR', 'seattle, WA', 'spokane, WA', 'yakima, WA', 'las vegas, NV', 'reno, NV', 'phoenix, AZ', 'tucson, AZ', 'flag staff, az', 'prescott, az', 'sedona, az' ] #do texas and florida
#westernindustries = ['hvac', 'plumbing']

locations = ['portland, OR']
industries = ['hvac'] 

#https://www.yelp.com/search?find_desc=Plumbers&find_loc=Orange%20County%2C%20CA&ns=1&start=40


#=======================================================


#finds string between two values 
def between(value, a, b):
    # Find and validate before-part.
    pos_a = value.find(a)
    if pos_a == -1: return ""
    # Find and validate after part.
    pos_b = value.rfind(b)
    if pos_b == -1: return ""
    # Return middle part.
    adjusted_pos_a = pos_a + len(a)
    if adjusted_pos_a >= pos_b: return ""
    return value[adjusted_pos_a:pos_b]




counter = 0
allCompanies = []
for industry in industries:
    
    

    for location in locations:
        if ' ' in industry:
            industry = industry.replace(' ', '+')
        if ' ' in location:
            location = location.replace(' ', '+')
        if ',' in location:
            location = location.replace(',', '%2C')
        print(industry)
        print(location)
        
        url = 'https://www.yelp.com/search?find_desc='  + industry +'&find_loc=' + location
        print(url)
        

        profilesList = []

        
        #Make loop item URL
        for x in range(0,20): #EDIT FOR MORE OR LESS LEADS
            urlToAdd = url + '&start=' + str(counter)
            counter = counter + 20
            print(urlToAdd)
            profilesList.append(urlToAdd) 



        


            

        for u in profilesList: 
            page = requests.get(u)
            soup = BeautifulSoup(page.content, 'html.parser')
            htmlString = str(soup)
            allResults = htmlString.split('All Results</h3')
            

            ##Geting business  URLs from directory 
            hrefSplit = allResults[1].split('href="/bi')

            #Gets company profile urls 
            urls = [ ] 
            for x in hrefSplit:
                rawURL = []
                url = between(x, 'z/', '" na')
                if len(url) < 400:
                    questionPos = url.find('?')
                    noQuestionMark = url[0:questionPos]
                    formatURL = 'https://www.yelp.com/biz/' + noQuestionMark
                    
                    if formatURL != 'https://www.yelp.com/biz/':
                        #print(formatURL)
                        urls.append(formatURL)

            #Removes company urls 
            urls = list(dict.fromkeys(urls))



            print(urls)
               
            for url in urls:     
                #Pulling company pforfile 
                profileURL = url
                getProfile = requests.get(profileURL)
                profile = BeautifulSoup(getProfile.content, 'html.parser')

                

                #get company name 
                nameRaw = profile.find('meta', attrs={'property': 'og:title'}) 

                nameAmpCheck = between(str(nameRaw), 'content="', ' - ')

                if( '&amp;' in nameAmpCheck):
                    name = nameAmpCheck.replace('&amp;', '&')
                else: 
                    name = nameAmpCheck


                #get cityState
                cityStateRaw = profile.find('meta', attrs={'property': 'og:title'})

                cityState = between(str(cityStateRaw), ' - ', '" ')

                try: 
                    city, state = cityState.split(', ')
                    print('city'+ city)
                    print('state'+ state)
                except ValueError:
                    city = cityState
                    state = ''

                #get phone 
                phoneRaw = profile.find('span', attrs={'itemprop': 'telephone'})

                phoneToStrip = between(str(phoneRaw), '">', '</')

                phone = phoneToStrip.strip()



                #Get owner 
                ownerRaw = profile.find('p', attrs={'class': 'lemon--p__373c0__3Qnnj text__373c0__2pB8f text-color--normal__373c0__K_MKN text-align--left__373c0__2pnx_ text-weight--bold__373c0__3HYJa'})

                ownerToStrip = between(str(ownerRaw), '">', '</')

                owner = ''
                FirstName = '' 
                LastName = ''
                print(owner)
                if('<span' in ownerToStrip): 
                    LastName = name
                    
                    
                else:
                    owner = ownerToStrip.strip()
                    try: 
                        FirstName, LastName = owner.split(' ')
                    except ValueError:
                        LastName = owner 

                


                #get website 
                websiteRaw = profile.find_all('a', attrs={'class':  'lemon--a__373c0__IEZFH link__373c0__29943 link-color--blue-dark__373c0__1mhJo link-size--default__373c0__1skgq' })

                website_link_typePos = str(websiteRaw).find('website_link_type') - 100

                websiteStr = str(websiteRaw)

                getURLBlock = websiteStr[website_link_typePos : str(websiteRaw).find('website_link_type')]

                website = between(getURLBlock, '2F%2F' , '&amp' )

                #get yelp link 
                yelpLink = url

                companyToAdd = {}
                companyToAdd['Company'] = name
                companyToAdd['Shipping_City__c'] = city
                companyToAdd['Shipping_State__c'] = state
                companyToAdd['Phone'] = phone
                companyToAdd['FirstName'] = FirstName
                companyToAdd['LastName'] = LastName
                companyToAdd['Website'] = website
                companyToAdd['Industry'] = industry
                companyToAdd['Fleet_Size__c'] = 0
                companyToAdd['Yelp__c'] = yelpLink
                companyToAdd['LeadSource'] = 'Yelp'

                allCompanies.append(companyToAdd)
                
                print(name, cityState, phone, owner, website)
                print()

def Remove(duplicate): 
    final_list = [] 
    for num in duplicate: 
        if num not in final_list:
            final_list.append(num) 
    return final_list 
          
# Driver Code 
allCompanies = Remove(allCompanies)
 

print(*allCompanies,sep=',\n')
  
    