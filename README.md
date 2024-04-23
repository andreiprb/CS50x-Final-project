# QUIZ
#### Video Demo:  https://youtu.be/0-ZibSFqTpY
#### Project description (found also in the video subtitles):

##### Hello, my name is Priboi Andrei, from Brasov, Romania, and this is my final project for CS50. This project is a quiz developed using Flask, Python, and SQL.

##### As a normal user, you can take the quiz and see your score afterward. If you're not satisfied with your score, you can opt to retake the quiz. A user can retake as many quizzes as they want under the same entry, so long as they do not log out. Once you logged out, registering with the same username will result in a different entry, based on the numeric id displayed after the username.

##### If you try to register as an admin (username: admin), the site will prompt you for a password (set by default to 1234). Logging in as an admin will give you access to the list of questions, permission to add or delete questions, and permission to delete entries. An admin can not access the quiz page, and a regular user can not access the functions displayed to admins.

##### Every time you start a quiz, the questions will be shuffled in order to prevent cheating. If a user fails to provide an answer, the page will prompt for the answer again, giving a warning. If a user refreshes the page while taking the quiz, nothing will happen. The quiz will be opened from the same point it was left off.

#### Files description

##### The main app.py file is the backend of the web app. It is written in Flask and Python, With some SQL too. I have taken use of the login_required function from FINANCE in order to build my site, as well as some other functions and libraries I documented from the internet.

##### The templates folder includes all of the HTML files.

##### I have decided to use the index and layout files synonymously, as a user never gets to visit the index file. Instead, a user is redirected to the register page by visiting index from the search bar. So, the index.html file is the layout of the whole application.

##### The register.html file is a page built extending index using Jinja, that prompts a user for a username. Multiple people can choose the same username, as the entries are differentiated by a numeric id. If the user decides to register as an admin (username: admin), the same register page will prompt the user for a password, set by default to 1234. Logging in as an admin gives youn access to the question list. Admins also have the power to add questions, to delete questions, and also to delete previous entries, from the question list and previous entries pages. If an admin tries to visit the quiz page from the search bar, the user will be logged out and redirected to the register page.

##### The add.html file is a page that prompts an admin for a new question to be added. The admin must provide a question, a correct answer, as well as 3 wrong answers to be displayed when taking the quiz. If an admin fails to provide one of these 5 requirements, the page will reload, prompting for them again, giving the user a warning.

##### The questions.html file is a page that outputs to the admin the list of questions currently indexed in the quiz. The page also displays some statistics regarding the number of times a specific question has been answered correctly, and in total. The table also includes some buttons, giving the page functionality. An admin can choose to delete a question from the quiz, or to delete the quiz completely, by pressing the 'Delete all questions' button situated at the top of the table (the button is displayed only if the quiz contains questions).

##### The statistic.htmlfile is a page that shows any user the list of previous entries. Once a user has completed the quiz, their entry will appear in the statistic page, as well as their score. If a user is unhappy with their current score, they can opt to retake the quiz, as long a they have not logged out of the session yet. Retaking the quiz will erase their current entry from the table, the new entry being inserted back only on quiz completion. The page warns the user about this, instructing them not to retake a quiz and quit half-way. If an user decides to log in as an admin, the page also displays buttons similar to the ones found in the questions page, giving an admin the power to delete any (or all) previous entry/ies.

##### Finally, the quiz.html file is a page that allows users to take the quiz. When an user accesses the page via the button from the nav, or from the search bar (GET request), the app will shuffle the quiz and store it in a temporary table in the database. This method allows the app to prevent cheating or memorising the answers. Also, this way of shuffling prevents the app from reshuffling the quiz when refreshing the page, only the answers being shuffled upon refreshing the page. If a user fails to provide an answer, the page will reload, prompting him for the answer again, giving him a warning in the lines of 'Please provide an answer'. Every time a question is answered, the app checks if the answer is correct, updating the score and the number of correct answers for that specific question. If the user provides an incorrect answer, the app only updates the total number of answers for that specific question. Upon completion, the user is redirected to the statistic page, in order to see their score.

#### The final.db file contains 4 tables: entries, admin, questions and temp.

##### The entries table contains the username provided at registration, a numeric id, the score and a bool named 'completed', whose value is 'false' by default. Upon completing the quiz, the status changes to 'true'. The statistic page only displays the entries where 'completed' is set to 'true'. Retaking the quiz will reset the value to 'false'. Upon logging out, if your session ends with the status of completion as 'false', the entry will be deleted from the database.

##### The questions table contains the question itself, a correct answer, 3 wrong ones, the number of correct and total answers to the question, and a numeric id. When an admin inserts a new question to the quiz, the app will initialize the question with the number of correct and total answers as 0. Two questions can have identical answers or text, since they are being differentiated by their id.

##### The temp table is a copy of the questions table that omits the 'correct' and 'total' columns. Every time the quiz page is visited with a GET request, the temp table is populated with a shuffled version of the questions table (the quiz). This prevents cheating or memorising the answers.

##### Finally, the admin table contains the id of the admin (1), the username (set by default to 'admin'), and the password (set by default to 1234).