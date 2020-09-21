# Car Share IOT

**Car Share IoT** is our project for final assignment of Programming IoT Course. It is a automatic car share system with a web application which allow user to rent a car through the website, report the car status, lock and unlock the car using traditional password, facial recognition or bluetooth. The web application is also a platform to manage and track the car rental history, car status and basic analytics for manager. 

## Table of Contents

- [Installation](#installation)
- [Features](#features)
- [Documentation](#Documentation)

---

## Installation

Overall, the project have two main parts: `masterpi` and `agentpi`. The `materpi` hold the code for web application and the `agentpi` hold the methods for unlock the car such as facial recognition, bluetooth. 

### Clone 

- Clone this repo to your local machine using `https://github.com/thanhlongb/car-share-iot`

```shell
$ git clone https://github.com/thanhlongb/car-share-iot
```

### Setup

> Go to the `masterpi` folder to install the project dependencies in requirements file

```shell
$ cd masterpi
$ pip3 install -r requirements.txt
```

> After installation is complete, go to the `masterpi` to run the web application

```shell
$ cd masterpi
$ python3 run.py
```

> To run the console in `agentpi`

```shell
$ cd agentpi
$ workon 
$ python3 main.py
```

> Connect the `masterpi` and `agentpi`  

For **masterpi**    

```shell
$ cd pisocket
$ python3 server.py 
```

For **agentpi**
```shell
$ cd pisocket
$ python3 client.py 
```
---

## Features
---
There are 4 types of user will interact with the application:   
- Customer  
- Engineer  
- Manager   
- Admin  

The role is defined by user's credentials when login to the website. Different user will have different access and function in the application. 
### Features for customer  
- Register new account
- login using account which is registered
- Search available car
- See car details
- Book a car
- View the bookings history
- Cancel booking
- Unlock the car using account or facial recognition
- Report to matain car  
### Engineer  
- Receive notification when a car need to repaired
- Check the car location
- Unlock the car by facial recognition, account
- Unlock car automatically by bluetooth
- Chang the status of the car  
### Manager
- Show list of car reports
- Assign task for engineer 
- Dashboard to show some data analytics which have several charts for business analytics  
### Admin
- View car rental history
- CRUD on car and user
- Report car with issue

## Documentation
---

The project documentation is build by using Sphinx. The document can be find on the `docs` folder of `masterpi` or `agentpi`.  

We have create 4 accounts present 4 types of users in the application:
- customer
    - username: `user`
    - password: `user`
- engineer
    - username: `engineer`
    - password: `engineer`
- manager
    - username: `manager`
    - password: `manager`
- customer
    - username: `customer`
    - password: `customer`  
### Git
The project is developed with the support of Git for code management.   

![git_commit_summarize](./img/git-commit-summarize.png)  
![git_branches](./git-branches.png)

### Trello  
In the development process, our team decided to applied scrum methodology to planning and developing the product. Firstly, our teams develop user stories based on the document. Then we decided that each sprint length is a week, after each sprint, a meeting is conducted to review the work and move to next sprint. 

![trello](./Trello.png)

