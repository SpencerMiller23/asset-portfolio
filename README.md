# asset-portfolio

AssetPortfolio is a personal finance tracker much like Yahoo Finance, in addition to taking inspiration from other sources such as the MotleyFool Portfolio Scorecard.

I believe it satisfies the distinctiveness requirements for the project firstly since the concept of creating a stock market focused application is unique. Secondly, this project has common aspects with many of the other projects, such as using Django for server-side logic, complex models and relationships, JavaScript (React) front-end, API request, and more, while not resembling any particular project too much.

I also believe that the project satisfies the difficulty requirement as it combines concepts discussed across the entire course, while implementing them in a more difficult way. For example, there are no other project which require the use of the React framework, which was a big challenge. In addition, using an already available API to create an internal API endpoint was an interesting twist to the project, which can perhaps be used by other developers in the future. Finally, I pushed myself to use GitHub for version control while building this project, which is also not required in any other project. I feel this was a great exercise for familiarizing myself with the technology, which is widely used in the industry.

views.py:
This file contains the bulk of the server-side logic required for this project. Firstly, handles all of the package imports from python and Django. In addition, it handles all the necessary routes and logic in order to allow for users to register, login and logout. Finally, there are the user_holdings, add_position and user_portfolio routes. These are all API endpoints used for retrieving data to display to the user. For example, the user_holdings "view" is called when the dashboard page is loaded. This view makes an API request to the FinnHub api for each holding the user already has. This involves taking the stock symbol, and making requests for both the company name and current stock price. Once retrieving all necessary data, the result is sent in JSON form to the dashboard template. The add_position and user_portfolio views function very similarly, where the former takes input from the form and uses it to create a new position object for the user, and the latter is used for calculating the users total portfolio value, as well as some other information such as total gain.

urls.py:
This vile contains all the information for ensuring proper routes are defines for the project.

models.py:
In this file, there is code which controls which models are used and how they interact with eachother. First there is the User model, which is used for authentication purposes. Then there is the Profile model, which is created with each new user. This model also keeps track of each holding a user has, which is done by using a many-to-many relationship with the Position model. Finally, the Position model represents a single position in a users portofolio. This model stores data such as stock symbol, date purchased, number of shares and purchase price.

layout.html:
This is a simple layout template which is used by other templates in the project.

dashboard.html:
The dashboard template is the most interesting template of the project. In addition to being a Django template, almost all components are rendered using ReactJS, which can be seen at the bottom of the file. There are the React components rendered on this page. First there is the UserPortfolio component, which makes an API request to the user_holdings view. This calculates the current total value of the users portfolio and displays it for the user along with total gain and percent change in value. Next there is the StockForm component, which allows the users to create new Position objects. Finally, the UserHoldings component again makes a request from the API endpoint and displays the current price of all stocks owned by the user.

styles.scss:
This file is a SASS file which controls much of the styling used across the project. It is automatically compiled into CSS by using SASS terminal commands.
