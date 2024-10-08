
# A Deep Dive into OpenAI

![Finished Application](images/Stock-Sentiment2.png)

## [Deployed Application](https://gr8tscott-github-io.onrender.com/)

I set out to and succeeded in building an application that uses the OpenAI platform/framework to fetch news articles on publicly traded companies, feed them into the AI for analysis, and output a sentiment (buy, sell, hold).  By building this project I was able to gain key experience and insight into OpenAI, AGI, and APIs that will serve me for years to come as these tools and softwares become more and more prevalent in our day to day.

# Proposed Timeline
| **Milestone** | **Description** | **Expectations Met?**  |   
|---------------|-----------------|------------------------|
| 1 Frontend App started            |  Create the basic structure for the Flask application               |   Yes                     |  
| 2 OpenAI API API Hookup            | Set up the OpenAI API to work with my application                |    Yes                    |   
| 3 Webscrape Article Data            |    Provide webscraping script with article and verify it properly scrapes the data             |    Yes                    |   
| 4 Send Webscraped Data to AI           |  Send the webscraped data to the AI and send it's response of the analyzed data back.               |     Yes                   |   
| 5 Database to track AI responses            |  Create a database to keep track of the AI responses, try to tie in live stock data to track over time               | Yes                         | 
| 6 CSS for App           |  Build out the application, make it look nice, display the database tracked data                      |Yes   | 
| 7 Bonus: Automate Webscraper (webcrawler?)            | Set up the web scraper to automatically search articles on stocks (at specified time, 9am EST before markets open)                |   No                     |   
| 8 Bonus: Deploy App  | Deploy the application using Render  | Yes    |

# Weekly Updates
## Week 12
**What happened last week?**
This last week I was able to tie in my database to the application to keep track of the AI analysis of the stocks. 

**What do I plan to do this week?** 
I need to finish up the CSS for the application and hopefully deploy it for viewing. There are a few more things I'd like but will wrap things up for this class regarding the project. I will also finish up my final project report.

**Are there any temporary roadblocks?**
No roadblocks outside of finalizing other class projects/exams.

**How can I make the process work better?**
Focus on wrapping up the project to as close to completeness as possible in the next few days.


## Week 11
**What happened last week?**
I wasn't able to make as much progress on the database as I had hoped this last week. I made some CSS updates and a few tweaks to the database but it still has a ways to go.

**What do I plan to do this week?** 
I need to finish tying in my database to the application to track the accuracy of the application. I also need to finalize the CSS for the frontend as well.

**Are there any temporary roadblocks?**
Inundated with end of semester exams and projects, along with family events, requiring significant portions of time.

**How can I make the process work better?**
Planning a set time in the coming days to finalize my project.


## Week 10
**What happened last week?**
I was able to build the skeleton for my database. 

**What do I plan to do this week?** 
I still need to tie the database into the rest of my app so that it is properly tracking the AI responses. I will also need to see if I can tie in a financial API to get current stock data.

**Are there any temporary roadblocks?**
I had some surprise exams and lost a few days to being violently sick.

**How can I make the process work better?**
Process is going well, need to keep making forward progress.


## Week 9
**What happened last week?**
I spent this last week getting my project caught back up after technical difficulties. We are almost back on track and hopefully will start moving forward on next stages. Produced and turned in the Project Update Report. 

**What do I plan to do this week?** 
I want to start building the database to store the responses from the AI this week. 

**Are there any temporary roadblocks?**
Traveling this week and will have some time constraints.

**How can I make the process work better?**
Process is going well, need to keep making forward progress.


## Week 8
**What happened last week?**
This past week I was not able to make very much forward progress on my project. I had a technical issue that led to a local commit/git issue that forced me to recover from a much earlier version and spent a good portion of time bringing the project back up to speed, still somewhat behind where I was but life goes on and this gives the opportunity to redo previous iterations better.

**What do I plan to do this week?** 
Finish getting my project caught back up. Produce a Project Update Report. 

**Are there any temporary roadblocks?**
Technical difficulties arose but I'm catching up from them and don't think they will hurt the longterm of the project.

**How can I make the process work better?**
Just need to be better about making sure my commits are pushed up more regularly, which has been difficult when working offline as of late.

## Week 7
**What happened last week?**
This week I focused my time on the news article scraping script for my app. I was able to make progress towards getting the script to work functionally with my frontend app so that when a user provides a news article the script scrapes the information and stores it locally. I also researched and reflected on the learning and job search resources available to me.

**What do I plan to do this week?** 
This next week I'm going work on sending the news article data to OpenAI and fine tuning its responses.

**Are there any temporary roadblocks?**
This last week was challenging due to the holiday, exams, and personal life changes; but life goes on and we were able to still make progress.

**How can I make the process work better?**
Blocking out a set couple of hours felt more effective this last week than the start/stop/repeat process I was using before.


## Week 6
**What happened last week?**
This week I was able to hook up my frontend app to the OpenAI API and began crafting the prompt tree for it's input/output. I'm still making tweaks to the prompts to ensure it does exactly as desirable consistently.

**What do I plan to do this week?** 
With the API hooked up and the basic frontend backbone implemented I want to focus my time this next week on the news article scraper which I expect will take a good bit of time to get working properly. I may need to use another API to efficiently search for the right news articles I want.

**Are there any temporary roadblocks?**
More exams and travel this next week so I'll be in the thick of it but will try to get ahead by a length or two.

**How can I make the process work better?**
I have started implementing a schedule but am finding it difficult to plan accordingly since my obligations week to week change so frequently, I'm making the goal to block out a designated couple of hours to make the progress happen rather than starting and stopping multiple times a week as it feels inefficient.


## Week 5
**What happened last week?**
I added a basic flask app that takes user input and added initial webscraping .sh files. The scraper.sh file currently scrapes article title but will expand to include main body text.
After reflecting on my time constraints I've begun planning out a proposed timeline to keep the project on track for completion.
Updated my personal website.

**What do I plan to do this week?** 
This next week I plan to hook up my frontend app to the OpenAI API and will begin crafting the prompt tree for it's input/output.
I have also been exploring other options such as Ollama which may work as a cheaper alternative expecially in the early stages of the app when getting it running. Ollama is an open-source framework that allows users to run large language models (LLMs) locally on their machines. It's designed to be user-friendly, efficient, and scalable, making it a good option for developers and organizations who want to deploy AI models into production.

**Are there any temporary roadblocks?**
I have exams and family obligations this week so making sure to stay up to date on my work expectations for the project.

**How can I make the process work better?**
This week I was able to start getting to the meat of development after doing my research so I've started building momentum and having fun with it. To keep up motivation I'm going to try to maintain forward progress and not get stuck on any one step.


## Week 4
**What happened last week?**
I reviewed and provided advice for my peers assessments. Began working on the web scraping code and researching OpenAI applications to understand how to use it in development.

**What do I plan to do this week?**
Finish my research for OpenAI and finalize the decision for the use plan and approximate budget.  Get personal website up to speed.  Start building the basic framework for the application. Create a schedule for the rest of the summer outlining project deadlines.

**Are there any temporary roadblocks?**
I've been very short on time between other academics, weddings, family, computer suddenly breaking and needing to be  replaced, etc. so it has been a challenge getting good momentum the last few weeks. Hoping to resolve this and have more time moving forward.

**How can I make the process work better?**
After reviewing some of the other project proposals, I noted that one of them had an extremely detailed week by week calendar to set expectations and deadlines for the rest of the semester. I think creating something similar to set minimum expectations per week will be helpful in maintaining a good schedule.


## Week 3
**What happened last week?**
I had a last minute change for my project this week after talking out the goals of my original project with Taylor and some of the other ideas I had in mind. Switched from a ML project to instead do an OpenAI application that analyzes news articles on publicly traded companies and provides a sentiment (buy, sell, hold).
I've started familiarizing myself with the OpenAI Playground tools and started testing ChatGPT's understanding of stock articles and the accuracy of it's assessments.

**What do you plan to do this week?**
Build the foundation for the app and figure out the OpenAI plan that I will use.
Start working on the web scraping code.

**Are there any impediments in your way?**
First time using OpenAI's Playground so it will take some time to learn it.
I'm traveling a lot this week so will need to properly manage my time to get enough done.

**Reflection on the process you used last week, how can you make the process work better?**
Talking over my idea in person with Taylor was really helpful for determining what was possible during the next few months vs what would be a reach (ML) so I want to make a concerted effort to come to more meetups to discuss ideas and processes with my peers.


## Week 2
**What happened last week?**
This week I met with some of my engineering friends to discuss the feasibility of my project and the time constraints. I narrowed down my project goals to be more realistic and started researching image models and training data.
I also started working on my portfolio site as well.

**What is planned for next week?**
I plan to start building the model next week and getting it set up to start training. I'll likely need to spend a lot of the time learning how to build a model to begin with.

**Are there any impediments in your way?**
My usual laptop(Mac) died last week and my new WindowsPC has been putting me through a serious learning curve. I was also sick most of the week and am still recovering.


**How can you make the process work better?**
I need to dedicate some time to learning my new computer and either installing packages that allow me use the same tools I'm used to on my old Mac or learn to work with what I have.
