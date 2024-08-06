# tWIZY CLI application

![Website Mock Up](readme/mockup.png)

## Table of Contents

- [Project Description](#project-description)
  - [Purpose](#purpose)
  - [User Demographics](#user-demographics)
- [UX Design](#ux-design)
  - [User Stories](#user-stories)
  - [Structure](#structure)
- [Features](#features)
  - [Existing Features](#existing-features)
  - [Future Features](#future-features)
- [Technical Overview](#technical-overview)
  - [Architecture](#project-architecture)
  - [Flowchart](#flowchart)
  - [Data Model](#data-model)
- [Technologies](#technologies)
- [Deployment](#deployment)
  - [Github](#github)
  - [Heroku](#heroku)
- [Testing](#testing)
  - [User Stories Testing](#user-stories-testing)
  - [Manual Testing](#manual-testing)
  - [Unit Testing](#unit-testing)
  - [Automated Testing](#automated-testing)
- [Credits](#credits)
  - [Media](#media)
  - [Code](#code)
- [Acknowledgments](#acknowledgments)

# Project Description

tWIZY is a CLI-based quiz game that challenges players with a variety of common questions. Players can earn points by answering questions correctly to achieve high scores, with the goal of becoming a champion on the leaderboard.

The game uses Google Sheets as a database to store both the quiz questions and the records of top players. This setup allows for easy updates and management of data.

tWIZY game is deployed on Heroku, making it accessible and convenient for players to enjoy from anywhere.

The tWIZY CLI app is built using Python and a little HTML, CSS as a Portfolio Project#3 for the Code Institute's Full Stack Developer(e-Commerce) course.

[The live tWIZY CLI application](https://twizy-60a6fbc7304c.herokuapp.com/)

## Purpose

tWIZY is a quiz game that’s easy to play and manage. It’s perfect for anyone who wants to test their knowledge, learn new things, and enjoy some friendly competition.

The app was created as part of a project portfolio to demonstrate the development and deployment of a CLI-based quiz game. It showcases skills in coding, database integration, and deployment on platforms like Heroku.

## User Demographics

tWIZY game could be interesting for a variety of users:

- from trivia lovers, who enjoys a good game,
- to tech enthusiasts, who are interested in learning about projects with Google Sheets and Heroku.

# UX Design

## User Stories

## Structure

# Features

## Existing Features

## Future Features

# Technical Overview

## Architecture

## Flowchart

## Data Model

# Technologies

## Languages

- Python
- HTML5
- CSS

## Frameworks, Libraries & Apps

| Name                                                         | Purpose                                                 |
| :----------------------------------------------------------- | :------------------------------------------------------ |
| Heroku                                                       | Launch and host the CLI app                             |
| Google Spreadsheets API                                      | Store data                                              |
| Python Pytest                                                | Unit-testing                                            |
| Favicon.cc                                                   | Create website favicon                                  |
| [Dreamstudio.ai](https://beta.dreamstudio.ai)                | Create the tWIZY background image                       |
| [Photopea](https://www.photopea.com/)                        | Work with images (resize, convert, etc)                 |
| [GoDaddy](https://www.godaddy.com/)                          | Generate WIZY logo                                      |
| [Vmake.ai](https://vmake.ai/image-outpainting)               | Expand the image                                        |
| [Imagecolorpicker](https://imagecolorpicker.com)             | Color picker                                            |
| [Coolors](https://coolors.co)                                | Color pallete                                           |
| [Ezgif](https://ezgif.com/)                                  | Video editor                                            |
| [Websitemockupgenerator](https://websitemockupgenerator.com) | Create the README Mockup image                          |
| [LucidChart](https://lucid.app)                              | Create flowcharts                                       |
| Balsamiq                                                     | Build interface website wireframes                      |
| Git                                                          | Use for version control                                 |
| GitHub                                                       | Store the source code and deploy and host the live site |
| GitPod                                                       | Set up and run project code                             |
| [Pep8ci.herokuapp](https://pep8ci.herokuapp.com)             | Validate Python code                                    |
| W3C HTML Markup Validator                                    | Validate HTML code                                      |
| W3C Jigsaw CSS Validator                                     | Validate CSS code                                       |
| Code Institute's Python Template                             | Generate the workspace for tWIZY project                |

# Deployment

## How to clone

1. Visit the [tWIZY repository](https://github.com/tayapro/twizy) on GitHub.
2. Click the **Code** button on the right side of the screen, select **HTTPs**, and copy the provided link.
3. Open a terminal and navigate to the directory where you want to clone the repository.
4. On the command line, type `git clone`, paste the copied URL, and press the **Enter** key to begin the process.

> [!NOTE]
> To get everything set up, install the packages listed in the requirements.txt file. Run the command in the terminal:
> `pip3 install -r requirements.txt`
> This project uses confidential credentials, like `CREDS.json` to work with Google's spreadsheets, make sure to add it manually.

## Heroku

Heroku is a cloud platform that enables easy building, deploying, and managing of applications,
and it was chosen for the tWIZY project.

> [!NOTE]
> To ensure that the requirements.txt file includes all necessary dependencies, run the command in the terminal:
> `pip3 freeze > requirements.txt`
> After updating the file, commit the changes to GitHub.

Deployment steps:

1. Fork or clone the [tWIZY repository](https://github.com/tayapro/twizy).
2. Access your Heroku account.
3. Set up a new application on Heroku.
4. Configure Settings:
   In the Settings tab:
   Add the required environmental variables in the Config Vars section:

   - `CREDS`: Google service account credentials. \
      How to get it, see Google's [service account credentials](https://cloud.google.com/iam/docs/service-account-creds) documentation.
   - `PORT`: Set this to `8000`.

   In the Buildpacks subsection, set the buildpacks in the following order: `Python` **first**, then `Node.js`.

5. Deploy the App:
   In the Deploy tab:

   - Under App connected to GitHub, configure GitHub integration.

   In the Manual deploy subsection, select the main branch and click "Deploy Branch" to deploy the app.

# Testing

## User Stories Testing

## Manual Testing

## Unit Testing

## Validator testing

# Credits

## Media

- Background image has been generated by [dreamstudio.ai](https://beta.dreamstudio.ai/)

## Code

- The setup for work with Google speadsheets is adapted from the "Love Sandwiches" lesson.

# Acknowledgments

Huge thanks to my mentor, Ronan McClelland, for all his help and advice. \
He’s given me great tips and resources that really improved my coding and testing skills.
