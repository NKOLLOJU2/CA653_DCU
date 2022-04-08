from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium import webdriver                    # importing web driver tool for automation
import time
import pandas as pd


# Function to get glassdoor salaries
def getAllDataScienceJobs(number_of_jobs, verbose):
    options = webdriver.ChromeOptions()  # Accessing webdriver

    # give the Absolute path of the chromedriver.
    driver = webdriver.Chrome(
        r"C:\Users\dell\Desktop\DataScience_Salary\chromedriver", options=options)
    driver.set_window_size(1120, 1020)

    # general format of the link
    url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword=data+scientist&locT=C&locId=1147401&locKeyword=San%20Francisco,%20CA&jobType=all&fromAge=-1&minSalary=0&includeNoSalaryJobs=true&radius=100&cityId=-1&minRating=0.0&industryId=-1&sgocId=-1&seniorityType=all&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0'
    driver.get(url)
    jobs = []

    while len(jobs) < number_of_jobs:  # looking for new jobs

        time.sleep(4)  # set sleep time based on internet speed

        try:
            driver.find_element(by=By.CLASS_NAME, value="selected").click()  # signup prompt
        except ElementClickInterceptedException:
            pass

        try:
            driver.find_element(by=By.CLASS_NAME, value="ModalStyle__xBtn___29PT9").click()  # clicking X.
        except NoSuchElementException:
            pass

        # passing onto each job in the page
        buttons = driver.find_element(by=By.XPATH,
                                      value="jl")  # Job Listing. Buttons to be clicked
        for job_button in buttons:

            print("The Progress: {}".format("" + str(len(jobs)) + "/" + str(num_of_jobs)))
            if len(jobs) >= num_of_jobs:
                break

            job_button.click()
            time.sleep(0.5)
            collectedSuccessfully = False

            while not collectedSuccessfully:
                try:
                    companyName = driver.find_element(by=By.XPATH, value='.//div[@class="employerName"]').text
                    loc = driver.find_element(by=By.XPATH, value='.//div[@class="location"]').text
                    jobTitle = driver.find_element(by=By.XPATH, value='.//div[contains(@class, "title")]').text
                    jobDescription = driver.find_element(by=By.XPATH,
                                                         value='.//div[@class="jobDescriptionContent desc"]').text
                    collectedSuccessfully = True
                except:
                    time.sleep(5)

            try:
                salaryEstimation = driver.find_element(by=By.XPATH, value='.//span[@class="gray small salary"]').text
            except NoSuchElementException:
                salaryEstimation = -1

            try:
                ratings = driver.find_element(by=By.XPATH, value='.//span[@class="rating"]').text
            except NoSuchElementException:
                ratings = -1

                # Debugging
            if verbose:
                print("Job Title: {}".format(jobTitle))
                print("Salary Estimate: {}".format(salaryEstimation))
                print("Job Description: {}".format(jobDescription[:500]))
                print("Rating: {}".format(ratings))
                print("Company Name: {}".format(companyName))
                print("Location: {}".format(loc))

            # Entering into the Company tab

            try:
                driver.find_element(by=By.XPATH, value='.//div[@class="tab" and @data-tab-type="overview"]').click()

                try:
                    '''
                     <div class="infoEntity">
                        <span class="value">San Francisco, CA</span>
                    '''
                    head_quarters = driver.find_element(by=By.XPATH,
                                                        value='.//div[@class="infoEntity"]//label[text()="Headquarters"]//following-sibling::*').text
                except NoSuchElementException:
                    head_quarters = -1

                try:
                    size = driver.find_element(by=By.XPATH,
                                               value='.//div[@class="infoEntity"]//label[text()="Size"]//following-sibling::*').text
                except NoSuchElementException:
                    size = -1

                try:
                    founded = driver.find_element(by=By.XPATH,
                                                  value='.//div[@class="infoEntity"]//label[text()="Founded"]//following-sibling::*').text
                except NoSuchElementException:
                    founded = -1

                try:
                    typeofownership = driver.find_element(by=By.XPATH,
                                                          value='.//div[@class="infoEntity"]//label[text()="Type"]//following-sibling::*').text
                except NoSuchElementException:
                    typeofownership = -1

                try:
                    industry = driver.find_element(by=By.XPATH,
                                                   value='.//div[@class="infoEntity"]//label[text()="Industry"]//following-sibling::*').text
                except NoSuchElementException:
                    industry = -1

                try:
                    sector = driver.find_element(by=By.XPATH,
                                                 value='.//div[@class="infoEntity"]//label[text()="Sector"]//following-sibling::*').text
                except NoSuchElementException:
                    sector = -1

                try:
                    revenue = driver.find_element(by=By.XPATH,
                                                  value='.//div[@class="infoEntity"]//label[text()="Revenue"]//following-sibling::*').text
                except NoSuchElementException:
                    revenue = -1

                try:
                    competitor = driver.find_element(by=By.XPATH,
                                                     value='.//div[@class="infoEntity"]//label[text()="Competitors"]//following-sibling::*').text
                except NoSuchElementException:
                    competitors = -1

            except NoSuchElementException:  # Rarely, some job postings do not have the "Company" tab.
                head_quarters = -1
                size = -1
                founded = -1
                typeofownership = -1
                industry = -1
                sector = -1
                revenue = -1
                competitor = -1

            if verbose:
                print("Head quarter: {}".format(head_quarters))
                print("Size: {}".format(size))
                print("Founded: {}".format(founded))
                print("Type of Ownership: {}".format(typeofownership))
                print("Industry: {}".format(industry))
                print("Sector: {}".format(sector))
                print("Revenue: {}".format(revenue))
                print("Competitors: {}".format(competitor))


            jobs.append({"Job Title": jobTitle,
                         "Salary Estimate": salaryEstimation,
                         "Job Description": jobDescription,
                         "Rating": ratings,
                         "Company Name": companyName,
                         "Location": loc,
                         "Headquarters": head_quarters,
                         "Size": size,
                         "Founded": founded,
                         "Type of ownership": typeofownership,
                         "Industry": industry,
                         "Sector": sector,
                         "Revenue": revenue,
                         "Competitors": competitor})
            # adding the jobs
        # button next page
        try:
            driver.find_element(by=By.XPATH, value='.//li[@class="next"]//a').click()
        except NoSuchElementException:
            print("Scraping terminated before getting threshold number of jobs. Needed {}, got {}.".format(num_of_jobs,
                                                                                                           len(jobs)))
            break

    return pd.DataFrame(jobs)  # This line converts into a pandas DataFrame.


if __name__ == '__main__':
    df = getAllDataScienceJobs(5, True)
    df.tocsv("data_glassdoor.csv")