**Team Members:** Wes Convery, Ido Pesok, Arne Noori
 
### Ideas:

I think Poker GTO application is our best idea. But here are all of our ideas:

1. **Movie Recommendation System**: Use knowledge about a person’s preferences and hobbies, along with information about movies, to determine the movies that a person may like. Information about movies can be obtained from a movies database (IMDB or a Kaggle dataset).
Objective: Develop a system that recommends movies based on individual preferences and hobbies.
Method: Utilize a database of movies and existing projects linked in the references SWI Prolog and Prolog-based systems.
Key Features:
- User ratings for watched movies to enhance recommendations.
- Handling new users with no rating history.
Things to think about: consider incorporating a feature that allows users to rate movies they've watched. This could provide additional data to inform the recommendation engine. Also, consider how you might handle new users who don't have a history of ratings or preferences yet

References:
https://github.com/Nirban1996/Movie-Recommendation-System-Using-Prolog
https://github.com/Ranim1997/Movie-Recommendation-System-Prolog
 
2. **Birthday gift advisor:** Based on knowledge about a person, knowledge about liking of people in general, etc., designing a system that will recommend a gift for your friend/relatives. (https://chromewebstore.google.com/detail/birthday-calendar-exporte/imielmggcccenhgncmpjlehemlinhjjo). 

Objective: Create a system that recommends personalized gifts for friends or relatives based on their interests.
Knowledge Base: Compile a database of potential gifts categorized by interests, age groups, and occasions.
Rule-Based Engine: Use Prolog to define rules that match gift options to the extracted user data, considering general trends in gift preferences.
Inspiration: Investigate s(ASP) system-based birthday gift recommendation engines. A related project is a recommendation system for birthday gifts developed using the s(ASP) system. The s(ASP) system is a goal-directed or query-driven Answer Set Programming (ASP) execution engine.

3. **Sentiment Analysis with Prolog:**  Sentiment analysis involves determining the sentiment expressed in a piece of text, such as a review or social media post.

Objective: Classify text into positive, negative, or neutral sentiments. For example, you could define a rule that associates the word "love" with positive sentiment and the word "hate" with negative sentiment. We could also use Prolog's pattern-matching capabilities to identify and handle negations, which can reverse the sentiment expressed by a word or phrase
Methodology:
- Define a sentiment lexicon in Prolog.
- Develop rules for sentiment analysis, considering context and negations.https://redchippoker.com/preflop-poker-charts/
Objective: Develop a system that determines the sentiment of text data, such as reviews or social media posts.
Knowledge Base: Define a lexicon of words and phrases associated with positive, negative, or neutral sentiments.
Rule-Based Analysis: Implement rules in Prolog to classify text based on the presence of sentiment indicators and the context, such as negations or intensity modifiers.

4. **Game playing AI:** A system for playing a card game or board game (most likely poker)

Objective: Use Prolog to develop AI for complex games like Poker or Monopoly, which require strategic reasoning.

Potential games: Sudoku, 8-Puzzle, Cluem Connect-4, Battleship, Poker

We could use Prolog to represent the game state and define rules for how the game state changes in response to player actions, utilizing prolog's ability to handle recursion and its built-in search mechanism. For example, we could use these features to implement a game AI that plans its actions by searching through the possible sequences of moves to find a sequence that leads to a winning game state.

If Poker, we could use Game Theory Optimal (https://www.888poker.com/magazine/strategy/beginners-guide-gto-poker) and create a useful application for a user to practice whether or not they should play their cards according to GTO.

Knowledge Base: Represent the game state and rules within Prolog, including chance elements and player interactions.

Considerations:
- Handling complex games or rules.
- Utilizing machine learning for AI improvement.

References:
https://mitpress.mit.edu/9780262691635/the-art-of-prolog/
https://redchippoker.com/preflop-poker-charts/
https://www.metalevel.at/prolog/puzzles
https://www.reddit.com/r/prolog/comments/isiviv/coding_challenge_20_2_weeks_poker_hand_analyser/


5. **Prolog and TensorFlow Combined:** Integrate Prolog's logical reasoning with TensorFlow's deep learning capabilities to create a hybrid AI system.
Knowledge Base: Use Prolog for tasks that require knowledge representation and logical inference, such as data preprocessing or query formulation.
Application:
- Prolog for knowledge representation and logical inference.
- TensorFlow for pattern recognition and predictive tasks.
Existing Work: Zamia AI project, which is an open-source AI system that combines Python, TensorFlow, and Prolog.

Reference: https://github.com/gooofy/zamia-ai