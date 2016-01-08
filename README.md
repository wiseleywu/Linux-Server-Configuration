# Udacity Fullstack Nanodegree Portfolio

Here are the running instructions for each of the projects

## 1. Movie Trailers Website
Please refer to https://github.com/wiseleywu/P1-fresh_tomatoes, this will be merged to the current directory in the future

## 2. Tournament Results
- Clone this repository
- Launch the Vagrant VM
- Navigate to [vagrant/tournament] (vagrant/tournament)
- Run [tournament_test.py] (vagrant/tournament/tournament_test.py) to perform unit tests
- Run [tournament.py] (vagrant/tournament/tournament.py) to engage in demo mode, which provide extra functionalities such as:
  - Compatible with odd number of players by assigning one random player a "bye" for each round
  - Support games where draw is possible
  - When two players have the same number of wins, rank them according to OMW (Opponent Match Wins), the total number of wins by players they have played against

## 3. Item Catalog
- Clone this repository
- Navigate to [vagrant/web_catalog] (vagrant/web_catalog)
- Modify line 121 of [populator.py] (vagrant/web_catalog/populator.py) with your name, g-mail address, and a link of your profile picture (optional)
- Launch the Vagrant VM
- Run [database_setup.py] (vagrant/web_catalog/database_setup.py) to initialize the catalog database
- Run [populator.py] (vagrant/web_catalog/populator.py) to populate database with pre-defined users and items
- Run [project.py] (vagrant/web_catalog/project.py) and navigate to [http://localhost:5000/] (http://localhost:5000/) in your browser
- Sign in with your google account at top right corner of the website. Once signed in, you will be able to see what you can and cannot modify on the website
- To test Facebook Sign in, either make sure your g-mail address is the same as your Facebook login or modify [populator.py] (vagrant/web_catalog/populator.py) with the proper credentials

## 4. Conference application
- [Download][1] and install Google App Engine SDK for Python
- Clone this repository
- Update the value of 'application' in 'app.yaml' to the app ID you have registered in the [Google Developers Console][2] and would like to use to host your instance of this sample
- Update the values at the top of 'settings.py' to reflect the respective client IDs you have registered in the Developers Console
- Update the value of CLIENT ID at Line 89 in 'static/js/app.js' to the Web client ID
- Deploy the app on to local web server by invoking the following command in console: '$ dev_appserver.py ConferenceCentral_Complete/'. Visit the local server address at [localhost:8080][3] (by default)
- Upload the app to Google App Engine by invoking the following command in console: '$ appcfg.py -A YOUR_PROJECT_ID update ConferenceCentral_Complete/'. Visit the deployed application at https://[YOUR_PROJECT_ID].appspot.com/

[1]: https://cloud.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python
[2]: https://console.developers.google.com/
[3]: http://localhost:8080/
