import scrapy

class BarSpider(scrapy.Spider):
    name = 'bar'
    start_urls = ['https://www.mywsba.org/PersonifyEbusiness/LegalDirectory.aspx?ShowSearchResults=TRUE&State=CA&Page=0']
    
    def parse(self, response):
        rows = response.css('tr.grid-row') # Select all the 20 rows
        
        for row in rows:
            base_url = 'https://www.mywsba.org/PersonifyEbusiness/LegalDirectory/LegalProfile.aspx?Usr_ID='
            pro_link = row.css('tr.grid-row::attr(onclick)').get().split('=')[2].replace("'", "")
            url = base_url+pro_link
            yield scrapy.Request(url, callback=self.detail) # send request each row and pass to the detail method
        
        # Next page functionality
        next_page = response.css('td[colspan] table td a::text').getall() # Get pagination list
        n_url = 'https://www.mywsba.org/PersonifyEbusiness/LegalDirectory.aspx?ShowSearchResults=TRUE&State=CA&Page=' # New url
        page_url = response.request.url # Get current url
        page_id = page_url.split('=')[-1] # get current page id as string value
        page_num = int(page_id)+1 # Convert it to int and plus 1 for next page
        
        for n in next_page:
            if n.startswith('Next Page'): # Check if Next page is available or not
                next_url = f'{n_url}{page_num}'
                yield scrapy.Request(next_url, callback=self.parse) # If so then call the parse method again
    
    def detail(self, response):
        first_name = response.css('span.name::text').get().strip().split(' ')[0]
        last_name = response.css('span.name::text').get().strip().split(' ')[-1]
        full_name = response.css('span.name::text').get()
        licence_num = response.css('span#dnn_ctr2977_DNNWebControlContainer_ctl00_lblMemberNo::text').get()
        license_type = response.css('span#dnn_ctr2977_DNNWebControlContainer_ctl00_lblLicenseType::text').get()
        e_to_p = response.css('span#dnn_ctr2977_DNNWebControlContainer_ctl00_lblEligibleToPractice::text').get()
        license_status = response.css('span#dnn_ctr2977_DNNWebControlContainer_ctl00_lblStatus::text').get()
        WSBA_admit_date = response.css('span#dnn_ctr2977_DNNWebControlContainer_ctl00_lblWaAdmitDate::text').get()
        # Contact information
        email = response.css('span#dnn_ctr2977_DNNWebControlContainer_ctl00_lblEmail a span::text').get()
        try:
            phone = response.css('span#dnn_ctr2977_DNNWebControlContainer_ctl00_lblPhone::text').get().strip()
        except:
            phone = ''
        company_address = response.css('span#dnn_ctr2977_DNNWebControlContainer_ctl00_lblAddCompanyName::text').get()
        addr = response.css('span#dnn_ctr2977_DNNWebControlContainer_ctl00_lblAddress::text').getall()
        address = addr[-3]
        city = addr[-2].split(',')[0]
        state = ' '.join(addr).split(',')[1].strip().rsplit()[0]
        #if not state.isupper(): state = ' '.join(addr).split(',')[2].strip().rsplit()[0]
        zip_code = ''.join(addr).split(state)[-1].split('-')[0].strip()
        profile_url = response.request.url
        
        data = {
            'First_Name':first_name,
            'Last_Name':last_name,
            'Full_name': full_name,
            'License_Number':licence_num,
            'License Type':license_type,
            'Eligible_To_Practice':e_to_p,
            'License Status':license_status,
            'WSBA_Admit_Date':WSBA_admit_date,
            'Email_Address': email,
            'Phone_Number':phone,
            'Company_address':company_address,
            'Address':address,
            'City':city,
            'State':state,
            'Zip_code':zip_code,
            'Profile_link':profile_url
        }
        yield data # That is the data we're looking for
