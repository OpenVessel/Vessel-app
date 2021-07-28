from operator import itemgetter

def validate_header(header):
    print(type(header))
    #flask app recevies request we can call headers attribute 
    ## WSGI headers are stored as tuples in a list 
    # read more at https://werkzeug.palletsprojects.com/en/2.0.x/datastructures/

    """
    <bound method Headers.get_all of EnvironHeaders([('Host', '127.0.0.1:5000'), 
    ('Connection', 'keep-alive'), 
    ('Pragma', 'no-cache'), 
    ('Cache-Control', 'no-cache'),
    ('Sec-Ch-Ua', '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"'),
    ('Sec-Ch-Ua-Mobile', '?0'), 
    ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'), 
    ('Content-Type', 'application/json'), 
    ('Accept', '*/*'), ('Origin', 'http://localhost:3000'), 
    ('Sec-Fetch-Site', 'cross-site'), 
    ('Sec-Fetch-Mode', 'cors'), 
    ('Sec-Fetch-Dest', 'empty'), 
    ('Accept-Encoding', 'gzip, deflate, br'), 
    ('Accept-Language', 'en-US,en;q=0.9'), 
    ('Dnt', '1'), ('Sec-Gpc', '1')])>
    """
    
    header_data = header.get_all('Origin') #get_all puts the object into list of tuples
    # print(header_data)
    ## http://localhost:3000 needs to be replaced with .env file var of the other server ip
    if header_data[0] == 'http://localhost:3000':
        print("request is accept")
    else:
        print("deined false request")
    

    return 