BOOMWRS is a wordle type game developed using HTML, CSS, JS and Python.

<h2>What is the mechanism?</h2>
Boomwrs is a primarily terminal based wordle game which now has been connected as web experience. If you really want it to enjoy on your terminal, just run "py main.py". Likewise, with the help of flask, this game is web based. It works in the mechanism as it is given order to select any random word from a word list containing 10000+ words that are frequently used. The word list is selected to have words only ranging its length from 3 to 6 letters. So the app extracts any one word, delivers it as wordle and the player/user tries to guess the word in 6 chances. And to validate if the word entered by the user is valid word in the dictionary, nltk and wordfreq and other python libraries are used.

Interfaces:

<img width="717" height="550" alt="Screenshot 2026-10-13 214301" src="https://github.com/user-attachments/assets/ee7c98a1-ff16-45c6-8640-769bab3f9fa9" />


<img width="912" height="863" alt="Screenshot 2026-10-13 215130" src="https://github.com/user-attachments/assets/d0cab704-d4a6-4658-be24-57a5ea37ad52" />

<h3>Prerequisties</h3>
Make sure you have the following installed on your system:
- Python ( v3.8 or later)                    
- pip (Python package Manager)
<h3>Required Python Dependencies:</h3>
nltk                                       
flask                                    
wordfreq                                            
dotenv ( optional - for setting up .env file for hidden / secret keys )       
gunicorn (optional - for setting up in own hosting service )      

<h2>Installation & Setup</h2>
1.Clone the repository:
Use command: git clone https://github.com/CuteSagar19/Boomwrs.git
Then
Open your terminal or Code Editor terminal.
cd Boomwrs or cs /path/Boomwrs

2. Create a virtual Environment
   It is recommended to use virtual environment of python for cleaner management of dependencies.
   Run the following in your terminal:
   
   -ON WINDOWS:   
   python -m venv
   venv\Scripts\activate.ps1

   -ON macOS/Linux:   
   python3 -m venv venv
   source venv/bin/activate

4. Install Python Dependencies:
   Run: pip install -r requirements.txt
5. <h2>Run the APP</h2>
  <h5>To play in terminal:</h5> Run py main.py ( to play the wordle game on console or terminal )
  <h5>To have web experience</h5>: Run py app.py ( to run the python environment and whole program as a web experience. After running the command, head to the url http://127.0.0.1/5000 on your web browser to play the game.)

  Contributors and more:
The major contributor of the project is Hidwen which is also my another github account. But since i had removed my os to install new but stored previous files, git thought i was the same old user with that username and stored it as contributor which i didnt noticed. So the contributors for this project is Hidwen and CuteSagar19 or Me and Myself. Sorry if this confuses you all.
