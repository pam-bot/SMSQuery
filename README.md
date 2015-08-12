# SMSante
SMSante is an SMS app that allows users to text their town name to a number and receive back information concerning known Ebola outbreaks close to their location and the presence of hospital beds near them. It consists of two parts (spread in two repos), [SMSQuery](https://github.com/pamela-wu/SMSQuery) and [SMSBeds](https://github.com/pamela-wu/SMSBeds), because each one serves a different group of people and thus needs its own phone number. [SMSQuery](https://github.com/pamela-wu/SMSQuery) is geared towards regular citizens who want to inquire after information regarding outbreaks and beds, and [SMSBeds]() is for on-the-ground hospital and aid workers who want to use SMS text messages to update databases in real time.

This project arose out of [HackEbola2014](http://www.nyu.edu/about/news-publications/publications/connect-information-technology/2014/12/02/nyu-tries-to--hack--ebola.advancedsearch.html?) hosted by the [Greenhouse](http://greenhousestories.com/) at the NYU Polytechnic. I was partnered with Arnav Sood, who originally sketched out the idea, and I wrote the code. We won a $500 startup grant from NYU Poly and presented an updated prototype at their Engineering Fair. Now, it's being hosted on the Google Cloud to take advantage of their servers and their API. Other people who made a valiant effort to bring this project to reality include Aissata Camara, Co-founder of There Is No Limit, Aditya Brahmabhatt, Bertha Teresa Jimenez, and Professor Anne-Laure Fayard.

## How SMSQuery Works
A phone number that is linked to the app from an SMS API provider - Twilio is used here - gets widely distributed. Let's say it's 1-555-555-1111. You, as one of the denizens of the area, text that number one word: the name of where you are. SMSQuery is hooked up to Google Maps API and is designed to handle any towns, cities, or provinces, or countries. It takes an internal database pulled from [cmrivers/ebola](https://github.com/cmrivers/ebola) and the Google Maps Distance Matrix API pulls out how far you are from the nearest outbreak. It also checks the MySQL database being updated by SMSBeds for hospital information. You text it "Mamou", which is a city in Guinea. What you get back is this:

>Vous avez cherché à Mamou. Ebola est détecté dans la ville Pita dans la direction NW à environ 77 km. Dernière mise à jour: 2015-02-22 22:48:15. L'hôpital Hospital1 de Conakry dispose de 2 lits maintenant. Dernière mise à jour: 2015-02-22 22:48:15. L'hôpital Hospital2 de Mamou dispose de 3 lits maintenant. Dernière mise à jour: 2015-02-22 22:48:15.

It's in French because this was originally designed to service African countries, and while there's a variety of different languages to choose from, French is the most widespread, the easiest to work with, and a better bet than English. Each response component is individually timestamped by the database.

If you're in an infected region, you will get this:

>Vous avez cherché à Conakry. Votre ville Conakry est touchés par le virus Ebola. Dernière mise à jour: 2015-02-22 22:48:15.

If your input can't be matched with a known Google Maps location, you get this:

>S'il vous plaît excuser notre erreur. Taper le nom de votre ville et essayez à nouveau. Par example, 'Mamou'.

## How SMSBeds Works
Another phone number is linked to the app, let's say it's 1-555-555-2222. You're a hospital worker assigned to count the beds in a hospital called Hospital1 (I'm great at naming things) and you've been given a phone from the aid group. You count that, in total, there are now 6 beds available in the hospital. You text that number "1234 6", which is the hospital ID followed by the number of beds. The app will check that you're texting from an authorized phone number, your hospital ID is correct, and that your entries are in a valid format. If successful, you will get the following message:

>Merci pour votre entrée. Vos données ont été saisies.

If you're an authorized user but your entry doesn't make sense to the app logic, you will get this back:

>Désolé, une erreur s'est produite lors de la saisie de vos données. S'il vous plaît essayer à nouveau et entrer votre ID de l'hôpital et le nombre de lits.

Otherwise, you get this:

>Désolé, soit votre numéro de téléphone n'est pas enregistré ou votre ID de l'hôpital n'est pas correct. Si vous enregistré, s'il vous plaît essayer à nouveau et entrer votre ID de l'hôpital et le nombre de lits.

## Additional Features
All users of both SMSQuery and SMSBeds get logged into a database that keeps track of both each SMS input and unique users of both systems. It hasn't been built into the system yet, but in theory, unique users could be sent PSAs concerning health best practices to combat misinformation in the face of an alarming international health crisis.



