Canvas Course Resource Downloader
This Python script automates the process of downloading resources from your Canvas courses. It uses Selenium to navigate through the Canvas website, locate course materials, and download them into organized folders on your local machine.

Features
Automated Login: Logs into your Canvas account using Selenium.
Course Navigation: Navigates to each course and identifies weeks with downloadable resources.
Resource Download: Downloads all available resources into organized folders named after the respective weeks and courses.
Error Handling: Handles common errors such as missing elements or download failures.
Prerequisites
Python 3.x
Google Chrome browser
Chromedriver (automatically downloaded and set up by the script if not present)


Installation
Clone the repository:

git clone <repository_url>
cd <repository_directory>

Usage
Configure your credentials:

Set your Canvas username and password in the USERNAME and PASSWORD variables in the script.
Run the script:

python canvas_downloader.py

Approve the 2FA request:

If prompted, approve the login attempt using your authenticator app.
Wait for the script to complete:

The script will navigate through your courses, download resources, and save them in organized folders.

This script provides a streamlined method to automate the download of course resources from Canvas, ensuring that you have all your educational materials organized and available locally.

Feel free to contribute or report issues for improvements!
