next_page = ['c', 'ah', 'abyr ne>', 'a ge "L']

cu_url = 'https://www.mywsba.org/PersonifyEbusiness/LegalDirectory.aspx?ShowSearchResults=TRUE&State=CA&Page=0'
n_url = 'https://www.mywsba.org/PersonifyEbusiness/LegalDirectory.aspx?ShowSearchResults=TRUE&State=CA&Page='
c_url = cu_url.split('=')[-1]
c_url2 = int(c_url)+1
print(c_url2)
page_id =0 
page_num = 0
for n in next_page:
    if n.startswith('a'):
        page_num+=1
        next_url = f'{n_url}{page_num}'
        print(next_url)