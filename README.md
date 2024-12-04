## Inspiration
QuetzAI was born out of the need to make information in museums **accessible** to all ages. This information is often specialized and therefore many people do not retain the information on display efficiently.

## What it does
QuetzAI reads QRs that contain the information of an historical object and do an **abstractive summary** of the information according to the **visitor's age**. Finally, after 10 objects scanned, there is the possibility to put on practice the new knowledge acquired by a trivia activity, where the questions are **generated dynamically** according to the scanned information and visitor's age.  

## How we built it
We built a web application using **HTML**, **CSS** and **JavaScript** for the user interface, but the magic happens behind. There is a **Relational Data Base** where we store the visitor's information and object's information, using queries where **Gemini** creates abstractive summaries based on visitor's age, and storing this at the DB, and finally using these summaries to create **personalized questions** where visitors can put their knowledge on practice.  

## What's next for QuetzAI: A new way to visit museums?
An awesome question! This web application is generalized, letting museums of all the world and all tematices use this app, so their visitors can learn more having fun in the process.
