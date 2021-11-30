import os
import requests
from dotenv import load_dotenv, find_dotenv

# This allows us to to find the environment variables for the API Get requests 
load_dotenv(find_dotenv())
# This is the main function where all of the user interface occurs
# It will continously run until the user quits  
def main():
    print("Welcome to the ticket viewer!")
    while(True):
            inp = input("Type 'm' for menu or 'q' to quit: ")
            if inp == "q" :
                break
            if inp == "m":
                while True:
                    print("    Press 1 to view all tickets")
                    print("    Press 2 to select a specific ticket")
                    option = input("    Press 'q' to go back to home screen: ")
                    
                    if option == "q":
                        break
                    elif option == "1": 
                        ListAll()
                    elif option == "2":
                        number = totTickets()
                        id = input("    Please enter a number between 1 and " + str(number) + ": ")
                        while int(id) <= 0 or int(id) > number:
                            id = input("    Please enter a number between 1 and " + str(number) + ": ")
                        ListSpecific(id)
                    else: 
                        print("     Please enter a valid option")

# This is the API request that will get all of the tickets and send them to a helper function to parse
# the data to output it 
# This function also includes the logic to make sure that only a maximum of 25 items are displayed and you
# can move back and forth between pages
def ListAll(): 
    password= os.getenv('PASS')
    user = os.getenv('USER_N')
    domainName = os.getenv('DOMAIN_NAME')

    try:
        response = requests.get('https://'+ domainName + '.zendesk.com/api/v2/tickets.json?page[size]=25', auth =(user,password))
    except requests.HTTPError as exception:
        print(exception)
    print(response.json())
    
    ParseAllJson(response.json())

    print('\n')
    option = 'a'
    while True:
        print('\n')
        if option == 'q':
            break
        temp = response.json()
        hasMore = temp['meta']['has_more']
        checkPrev = temp['tickets'][0]['id']
        prev = temp['links']['prev']
        
        # This ensures that we give the correct prompt for the user based off of current index
        if hasMore:
            next = temp['links']['next']
            if checkPrev == 1:
                option = input("    Enter 'n' for next page and 'q' to quit: ")
            else:
                option = input("    Enter 'n' for next page and 'p for previous page and 'q' to quit: ")
        else: 
            option = input("    Enter 'p for previous page and 'q' to quit: ")

        # This block makes sure that if there is a next page then it can be selected otherwise you can't go
        # to next page
        if option == 'n':
            if next == None:
                option = input("    Enter 'p' for previous page and 'q' to quit: ")
                continue
            try:
                response = requests.get(next, auth =(user,password))
            except requests.HTTPError as exception:
                print(exception)
            ParseAllJson(response.json())

        # This block makes sure that if there is a previous page it can be selected otherwise it can't be selected
        if option == 'p':
            if checkPrev == 1:
                option = input("    Enter 'n' for next page and 'q' to quit: ")
                continue
            try:
                response = requests.get(prev, auth =(user,password))
            except requests.HTTPError as exception:
                print(exception)
            ParseAllJson(response.json())

        


# This function parses the JSON response body from the get all tickets and outputs the information to screen
def ParseAllJson(content):
        for ticket in content["tickets"]:
            id = ticket["id"]
            type = ticket["type"]
            subject = ticket["subject"]
            print("Ticket id: " + str(id) + " type: " + str(type) + " subject: " + subject)

# This function uses the id given from the user to get the specific ticket that was requested by the user
def ListSpecific(id):
    api = os.getenv('API_KEY')
    user = os.getenv('USER_NAME')
    domainName = os.getenv('DOMAIN_NAME')
    try:
        req = 'https://' + domainName + '.zendesk.com/api/v2/tickets/' + str(id) + '.json'
        response = requests.get(req, auth=(user, api))
    except requests.HTTPError as exception:
        print(exception)
    ParseJson(response.json())

# This parses only one ticket and displays it onto the screen
def ParseJson(content):
    ticket = content['ticket']
    id = ticket.get('id')
    type = ticket.get('type')
    subject = ticket.get('subject')
    created_at = ticket.get('created_at')
    status = ticket.get('status')
    print("Ticket id: " + str(id) + "\ntype: " + str(type) + "\nsubject: " + str(subject) + "\ncreated at: " + created_at + "\nstatus: " + status)

# This request returns the total number of tickets
def totTickets():
    api = os.getenv('API_KEY')
    user = os.getenv('USER_NAME')
    domainName = os.getenv('DOMAIN_NAME')
    try:
        response = requests.get('https://'+ domainName + '.zendesk.com/api/v2/tickets/count.json', auth=(user, api))
    except requests.HTTPError as exception:
        print(exception)
    Json = response.json()
    count = Json['count']

    return count['value']

if __name__ == "__main__":
    main()
        