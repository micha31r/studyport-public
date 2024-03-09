# Studyport

### About

Studyport is a grade visualiser for NCEA students, previously called Insightz. This project has been the result of several years of work. I started working on this idea in year ten, but the face of the project has changed drastically over the years. This project was submitted for the Young Innovators Award, winning (senior) first place and the creativity category award. Further recognition followed at Q Awards (a high-school student design competition), where it received Gold for both the Community Good and Digital categories. While successful on many fronts, this project failed to take off. Below is the story of this project and what I learned from it.

### Catalyst

The project's inspiration stemmed from my parents, who needed help understanding the academic/grading system. The school portal lacked visual elements such as graphs to break down academic results. I made the very first version with p5.js. The prototype lacked authentication, and charts were created manually using shape functions. Data extraction was achieved using a Python web scraper, in which you enter your username and password, and it extracts the results table from the school website. Although the prototype was basic, it validated the idea.

### Rising Tension

Over the summer, I recreated the project using Django and Chart.js (this was my first Django project and website deployment 🎉). In this version, all user interaction was through the website, significantly improving user-friendliness, as students could log in and have their results fetched automatically. The subsequent iteration, constructed from the ground up with the same frameworks and libraries, introduced more charts and statistics for students. Additionally, I built a dashboard for teachers that allowed them to see the overall results of a class/subject, etc. The user interface was also drastically improved and made responsive.

### Climax

The final iteration introduced significant changes, including the transition from Insightz to Studyport. Due to concerns surrounding privacy and security issues related to student data, fetching results data via web scraping was no longer viable. The solution was to adopt the directory service provided by the school management system, which would push new data to Studyport, where they are processed and stored in the database. I also added Google OAuth, Google Translate feature, various new graphs, specialised NCEA progress tracking functionalities, and personalised goal tracking. The user interface was completely renovated, featuring multiple colour themes and light and dark modes.

### Resolution

My intention for the final version was to publish it so that other students could use it. But many questions remained: Who will maintain it, provide IT support, and add new features? I was about to start university, and the time commitment and effort would be too high. In addition, I had no monetisation strategies and lacked data on the education market. Would schools/students/parents be willing to pay for it? 

I realised that in an effort to perfect this product, I buried myself in development and failed to recognise a critical aspect of building a product—the customers. The final version looked impressive, perhaps from a purely visual perspective, but it was too complicated for the end users. Charts became less intuitive, and some functionalities provided no meaningful value. The solution to the problem I set out to solve had almost become part of the problem.

This is when I decided to pull the plug.

Was all the effort worth it? I believe so. As a high school student, I gained valuable web development and user interface design skills and became proficient in styling using plain CSS. However, the biggest lesson was that product design and customer research are equally important as the technical aspects. Another takeaway is to find ways to build as fast as possible. The younger me wanted to write everything from scratch, which, in hindsight, was a poor strategy.

So, let the remains of the project serve as a personal milestone and a reminder of the long road ahead.

![enter image description here](https://www.michaelren.dev/media-compressed/studyport/login.jpg)
![enter image description here](https://www.michaelren.dev/media-compressed/studyport/ncea.jpg)
![enter image description here](https://www.michaelren.dev/media-compressed/studyport/goals.jpg)
![enter image description here](https://www.michaelren.dev/media-compressed/studyport/goals-create.jpg)
![enter image description here](https://www.michaelren.dev/media-compressed/studyport/results.jpg)
![enter image description here](https://www.michaelren.dev/media-compressed/studyport/progress.jpg)