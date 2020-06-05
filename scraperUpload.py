from simple_salesforce import Salesforce

#enter yelp url here


sf = Salesforce(username='USERNAME ', password='PASSWORD', security_token='API_KEY')

#Put leads here 
#=======================================================

data  = ['PUT LEADS HERE ']    

#=======================================================



#upload
sf.bulk.Lead.insert(data)



  
