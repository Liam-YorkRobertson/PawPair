# PawPair
![PawPair logo](https://imgur.com/a/d5v8N46)  
## Introduction
Welcome to PawPair, a web application designed to bring canine enthusiasts together, fostering connections and interactions between dogs and their owners.
**Deployment:** [PawPair Web App](https://liamyork.pythonanywhere.com/)
**Author:** Liam-York Robertson
**My LinkedIn:** [LinkedIn Profile](https://www.linkedin.com/in/liam-york-robertson) 
**Final Project Blog Article:** [Read Blog Post](https://medium.com/@liamyorkdeonrobertson/my-first-web-application-pawpair-631030ddf0d5) 
## The Inspiration Behind the Project
![PawPair Screenshot](https://imgur.com/a/bUvyNPk) 
The project was inspired by my dog, Zascha, a 6-year-old golden border retriever that we adopted from a shelter. My fascination with her parent breeds and cross-breeds during my teenage years led to the idea of creating the web application. Originally considering a stock market-related app, I came across IdeaDog (which had nothing to do with dogs funnily enough), inspiring me to develop a platform for connecting people interested in cross-breeding their dogs.
## Installation
To run PawPair locally, follow these steps:
1. Clone the repository: `git clone https://github.com/yourusername/PawPair.git`
2. Navigate to the project directory: `cd PawPair`
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Run the application: `python app.py`
## Usage
![PawPair chatroom](https://imgur.com/a/BcQjUOs) 
PawPair provides a user-friendly interface for dog owners to:
- Register and create a profile for their dogs.
- Connect with other users interested in cross-breeding.
- Explore dog breeds and find potential matches.
- Consult professionals on compatibility of their dogs.
## Contributing
Contributions are welcome! To contribute to PawPair, follow these steps:
1. Fork the repository.
2. Create a new branch: `git checkout -b feature/new-feature`
3. Make your changes and commit: `git commit -m "Add new feature"`
4. Push to the branch: `git push origin feature/new-feature`
5. Open a pull request.
## Related Projects
Check out these related projects:
- [IdeaDog](https://github.com/bdbaraban/ideadog) - A platform for sharing and exploring creative ideas.
- [Wag!](https://wagwalking.com/) – A dog walking and babysitting website
## Technical Challenges and Solutions
### Frontend and Backend Technologies
- **Frontend:** The project uses HTML, CSS, and JavaScript, with Flask templates for server-side rendering.
- **Backend:** Powered by Python, the Flask framework, and MySQL for database management.
- **Real-time Communication:** Implemented Socket.IO for real-time chat functionality.
- **External Services:** Google Maps API integration enhances location-based features.
### Struggles and Learning Moments
Encountering anticipated challenges during the project, time constraints led to the exclusion of certain functionalities, such as an extensive dashboard for professional breeders and a different chatroom for users and breeders. The most demanding aspect was implementing the chatroom functionality using socket.io, involving multiple database tables, Flask routes, JavaScript methods, and jQuery. As the sole contributor, I navigated various online resources and used AI to comprehend and address these concepts. Micro-adjustments to the code were crucial in resolving issues, and a small workaround ensured dynamic message loading in the chatroom. Another hurdle involved CSS styling without frameworks, requiring extensive development and adjustments for visual appeal. Overall, bug fixing emerged as the most challenging technical aspect of the project.
## Licensing

PawPair is licensed under the [MIT License](PawPair/LICENSE).
