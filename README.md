# Noki

This is a generalized tool to create Whatsapp/SMS surveys using Twilio API. See the demo here: https://youtu.be/_OMRHVFTDAU

More information about the idea can be found here: https://share.nuclino.com/p/DESDR-Survey-Tool-yjKGW4mhV8nuGCmHrO5QtQ

Below are the instructions for running it locally

### Environment Setup
- The app requires connection to a postgres database
- Using a virtual environment is preferred though not required.
- Under the root directory, run `pip install -r requirements.txt` to load all the packages.


### Run it Locally
- The main file is noki.py
- The followings are the configurations needed to run it locally:
    - Set up your Twilio account
    - Run `./ngrok http 5000` to start tunneling, where "5000" is the port number the flask app running on. 
    ngrok would provide a forwarding address for your localhost.
    (You can download ngrok from https://ngrok.com/download)
    - In Debugger / Webhook & Email Triggers, set the webhook to "<forwarding_address_by_ngrok>/sms" (e.g. http://d978fead6bfb.ngrok.io/sms)

- Finally, run `python noki.py`
- You can visit: http://localhost:5000 in your browser to access the admin UI


Author: Abhyuday Bharat

Contact: ab5434@columbia.edu

Updated on Sep 26, 2023
