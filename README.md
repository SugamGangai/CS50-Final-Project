# Personal Budget Tracker
# Video Demo: https://youtu.be/eRBag0_okdM
# Description: 
Personal budget tracker is a web based program by me i.e Sugam Gangai as CS50 final project. Being at last stage of my teenage, I thought of importance of finance is going to be an important aspect in my adulthood, so I decided to work on this. It helps user to record, view and monitor their financial status.

I have used HTML, CSS and javascript for the web end program. I have used flask and jingo to work with user's input and functionality with data. I also have used charts,js for the interactive statistics for the user. additionally I used CS50's codespace and some elements of finance problem set to make it work smooth.

The project directory contains static folder which contains style.css file which has shaped the output of the program. The templates folder contains all the html pages of the web program that interacts with each other according to the users need. Project directory also contains app.py which handles all the backend working with flask and all; helpers.py is also present there to make it smooth. "pbt,db" stores all the tables used in this program.

Layout.html page works as the building template of the web page containing overall basic elements of the program including the navbar which redirects to all the pages of the program.
Login.html asks the user to submit a form of field username and password. It takes the user input and yells at user if it empty or it doesnot match but gives access to the verified user. besides that in nav bar the is aslo a register but for the new user to sign up. It redirects to the register.html page which asks user to submit a form with input fields like username, password and confirm password. It also yells the user if any of the input field is empty or confirm password and password doesnot match or username already exist before else it lets the user to the home page.

In the home it show user the total saving, total expenses and net amount remaing from user as well as a bar graph for different category. the add.html lets a user to add spending or income submiting a form contain input field with drop down, radio button as well. The view.html lets the user view their transaction history as a bank statement as well as gives flexibility to user to filter down the statement according to their choice. It also lets the user to delte any statement the would like to delte from the database.

The stat.hrml lets the user to view his spending and expense habit in for detail way with visuals of charts.js. profile.html redirected when the profile icon is clicked which pops the user with message and option to change password as well in the nav bar.

In this project I have used boxicons,com for a icon adn chatgpt for some error correction as well as for some css design. And This was Personal Budget Tracker.
 <br>
     By - Sugam Gangai