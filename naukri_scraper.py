#This python code will get the job details from the site(url) and uses the file jobs.sql to insert the data extracted from the site into a database- 'naukri' in the table- 'job_openings'.
#NOTE: before this, a data base of name 'naukri' must be present.



import requests
import bs4
import sys
import psycopg2


def get_jobs():                                                                 #It gets the job details from the given url.
    url = "https://www.naukri.com/jobapi/v3/search?noOfResults=20&urlType=search_by_key_loc&searchType=adv&keyword=full%20stack%20web%20developer&location=bangalore%2Fbengaluru&pageNo=1&experience=0&k=full%20stack%20web%20developer&l=bangalore%2Fbengaluru&experience=0&seoKey=full-stack-web-developer-jobs-in-bangalore-bengaluru&src=jobsearchDesk&latLong=15.133315_78.5162075"

    h = {"appid":"109",
           "systemid":"109"}
    page_content = requests.get(url,headers = h)
    page_data = page_content.json()
    return page_data['jobDetails']

def insert_jobs(jobs):                                                          #It puts the jobs in the database 'naukri'.
    #placeholders
    conn = psycopg2.connect("dbname=naukri")
    cur = conn.cursor()
    for i in jobs:
        title = i['title']
        jobid = i['jobId']
        company_name = i['companyName']
        if 'jdURL' in i:                                                        #This is used because every jod does not have a jdURL.
            jd_url = i['jdURL']
        else:
            jd_url = '-'
        soup = bs4.BeautifulSoup(i['jobDescription'],'lxml')
        job_descript = soup.text

        cur.execute("INSERT INTO job_openings(title,job_id,company_name,jd_url,jd_text) VALUES(%s,%s,%s,%s,%s);",(title,jobid,company_name,jd_url,job_descript))

    conn.commit()

    cur.close()
    conn.close()


#NOTE: before this, a data base of name 'naukri' must be present.
def create_table():                                                                #This creates the table defined in the file - 'jobs.sql'
    conn = psycopg2.connect("dbname=naukri")
    cur = conn.cursor()

    f = open("jobs.sql")
    sql_code = f.read()
    f.close()

    cur.execute(sql_code)
    conn.commit()

    cur.close()
    conn.close()


def main(arg):
    if arg == "create":
        create_table()
    elif arg =="crawl":
        jobs = get_jobs()
        insert_jobs(jobs)
    else:
        print(f"Unknown command '{arg}'")

#print("__name__ is ", __name__)

#if __name__=="__main__":
#    print("I am being run")
#elif __name__!="__main__":
#    print("I am imported")

if __name__=="__main__":              #import gaurd
    main(sys.argv[1])
