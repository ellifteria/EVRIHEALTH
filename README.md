# EVRIHEALTH

## Because everyone deserves access to healthcare.

---

## Inspiration
According to Gallup, in 2019, 1 in 4 Americans claimed that they, or a family member, delayed treatment for a serious medical condition due to the cost of healthcare. In the same year, taking into account those who delayed treatment for a less serious medical condition, 1 in 3 Americans delayed seeking medical care due to their financial constraints. Since then, the problem has only gotten significantly worse. The consequences of delaying medical care include deteriorating health conditions, later diagnoses, and earlier deaths. That this problem is occurring in the wealthiest nation on Earth is especially lamentable. The problem is perhaps worst in the state of Texas, which has the highest medically uninsured population in the entire country. 

## What it does
My project, EVRIHEALTH, seeks to solve this issue within the state of Texas. Under Texas law, all non-profit hospitals in the state are required to provide some free or discounted medical care to individuals unable to afford medical treatment or without health insurance. This free or discounted medical care is known as "charity care," and similar such programs exist across the country. However, this program is not largely unknown amongst the general public. As a result, the cost of healthcare still provides a significant barrier for many, especially for those of lower socioeconomic standing, from accessing medical care.

EVRIHEALTH helps solve this problem by allowing people to easily determine if they are eligible to receive charity care from the Texas Health hospital system by answering a few questions. After checking their eligibility, the program also allows users to complete a digital version of the financial assistance application directly from the site. Additionally, users can get estimates for the cost of their medical procedures at various Texas Health facilities across the state. Outside of these functions, EVRIHEALTH provides publicity for an important government program many don't take advantage of, resulting in unnecessary suffering and mortality.

## How I built it
I built the application using flask and python. I used a series of HTML forms to get the user's input for their financial and other information needed to determine their eligibility for receiving financial assistance at a Texas Health hospital. Then, using a combination of python libraries, I created a pdf watermark containing the user's application data located at the corresponding locations on the application on the corresponding page and merged the watermark and the blank application into a new pdf file with a randomly generated file name stored in the browser session based on the time and the user's IP address. After the pdf has been displayed to the user where they are able to download it, the pdf file is deleted to remove the user's data and the session is cleared. 

I also used python to read in excel files containing the average costs of various medical procedures at each Texas Health hospital and store the relevant information so that it may be displayed to users. This allows users to get estimates for the cost of their medical procedures so that they can make educated decisions about their ability to afford medical treatment and qualify for financial assistance.

While the majority of the code is written in python, the webpages are all designed using HTML and styled with CSS. Additionally, javascript is used to make the responsive top navigation bar, allowing EVRIHEALTH to be used easily on both desktop and mobile browsers, extending EVRIHEALTH's reach.

The entire project is being hosted using Heroku to allow users to access it.

## Challenges I ran into
This project involved a lot of "first"s for me, meaning I ran into several challenges while completing it.

+ This was my first time completing a hackathon on my own. This meant that I had to learn to handle every aspect of completing the final project.
+ This was also my first time using flask to create a website. While I have experience programming in python, I had to learn how to use flask on the fly.
+ This was also my first time attempting to deploy an application. I had to learn how to deploy my flask app to Heroku in order to have it accessible for judging. My first attempt to deploy the project used the Google Apps Engine; however, after a long time trying to get the app to run, I realized I had to switch to another service or else risk running out of time to finish my project. Therefore, I decided to try and use Heroku, which, after figuring out how to use it after not reading the documentation, I managed to get working.

## Accomplishments that I'm proud of
I am most proud that I managed to complete the entire project--design the front end, develop the back end, create graphics--completely on my own within the hackathon's time limit.

Technically, I'm most proud that I learned how to deploy an application to a cloud platform: Heroku. I didn't have any experience deploying applications to the web before and so am proud that I managed to learn how to do so on a tight schedule, especially since deploying apps to the web is a useful skill for future projects.

## What I learned
+ I taught myself how to deploy applications to cloud platforms.
+ I taught myself how to write flask applications.
+ I taught myself how to use HTML forms and create HTML buttons.
+ I taught myself CSS styling.

## What's next for EVRIHEALTH
After this hackathon, I plan to continue to develop EVRIHEALTH. Currently, EVRIHEALTH only has functionality for around three dozen hospitals across the state of Texas. There are more non-profit and public hospitals in Texas not covered by EVRIHEALTH. Therefore, I plan to add all the hospitals offering charity care in Texas. This will allow people to find more access to free and discounted medical care throughout the state. Since there are similar charity care programs across the United States, the application has significant room to expand beyond Texas. I plan to add the same eligibility checking and application completion functions for hospital systems in other states so that people of lower socioeconomic status everywhere in the United States have access to free and discounted healthcare.
