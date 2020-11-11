# SecretSanta
Simple Secret Santa Selector in python emailing selections to each individual using exchange exchangelib.

# Email Credentials
I set up the email notifications using Exchange as the sender. I created a shared mailbox specifically for sending the secret santa notifications.
Enter the username, password, and from email address in the CSV file named emailcredentials.csv. I did not test using a comma in the password, I would avoid this as it may cause issues parsing the CSV.

# Secret Santa Entrants
Enter the details of the entrants into the csv file named christmasnames.csv. The first column must be a unique ID, that is used to ensure nobody selects themself.
The email address is used to send the selection to that user.

# Process of Selections
All names are imported and placed into a list. I duplicate the list and randomize the second one. I then iterate through the first list and delete users from the second list as they are confimed selected.

There is a case where there are an odd number of entrants where the last person may select themself. I have checked for this and restart the selecting process if that happens. There are better ways to do this, but this doesn't need to be highly optimized.

A final email with all selections is sent to the address listed in the emailcredentials.csv file in case anybody deletes or does not receive their selection.
