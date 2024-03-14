---
title: "Project Proposal"
subtitle: "Game Theory Optimal Poker"
author:
- Arne Noori
- Ido Pesok
- Wes Convery
geometry: margin=1in
---

<!--

pandoc projectproposal.md -o CSC481_Project_Proposal.pdf --pdf-engine=xelatex

Rubric:

Motivation - Motivation for engaging with the problem: why is it interesting and/or challenging? How does it relate to class topics? What does the group expect to learn / achieve?
Problem Description - Understanding of the problem. Clarity of description. Identification of relevant related work, techniques and implications. Identification of any existing resources used as a starting point.
Knowledge representation - Clear identification of what knowledge the system will use, how it will be extracted, represented and expected size.
Methods - Justification of proposed methods. Understanding of proposed methods. Identification of major changes/adaptations/difficulties (if applicable)
Evaluation - Identification of metrics for evaluation of group's achievements
References - List of references of related work (e.,g. scientific papers), supporting material (e.g. tutorials, book chapters) and existing implementations (e.g. code repositories, libraries, datasets). As per project template, use adequate format including title, author, organization, publication date - "naked" URLs are not sufficient. All entries must be referenced in text.

--> 

## 1. Overview:

<!-- [Describe your project and the role the selected AI methods and tools play in it. ] -->

We aim to build a tool for poker players. This project aims to develop a python-based tool for enhancing poker skills in no-limit Texas Hold'em. All three of us play poker and are often involved in poker nights with friends, so we identified a need for a practical tool that can provide advanced insights into Game Theory Optimal (GTO) strategies. Our motivation is to bridge the gap between theoretical poker knowledge and its practical application. By leveraging python's capability to handle complex logical structures and decision-making processes, we plan to create a system that not only advises on optimal plays but also deepens our understanding of advanced poker strategies. Essentially, the tool will simulate a round of no-limit Texas Hold'em, and the player given a hand will decide how much to bet, call, or fold; after the round, the tool will give the user a score of how perfect their decisions were based off GTO (similarly to how you get a score after a chess.com match and detailed feedback on how you can improve). This tool is intended for those who, like us, are keen to improve their game by learning and applying GTO principles more effectively.

## 2. Problem Description

<!-- [Describe the problem you are trying to address. What is the goal, what are the main challenges, what (if any) progress has been made so far in addressing the problem by other people, what tools are available for your team to use as a starting point. You can also perform a simplified PEAS specification- Performance, Environment,  Actuators, Sensors, but this is not required.] -->

Poker is a game that requires players to make smart choices based on their cards and other players' actions. A key strategy in playing poker well is called Game Theory Optimal (GTO). GTO helps players make the best possible moves in different situations. However, GTO strategies are complex and can be hard to learn. Our challenge is simplifying these strategies into clear, easy-to-follow advice using Python. We will build on existing libraries like PokerKit for core poker logic and treys for fast hand evaluation. Monte Carlo simulation also seems promising for providing GTO insights by estimating hand equities. There are also supplementary libraries for tasks like card dealing and hand representation that we can utilize as needed. By leveraging these tools and Python's capabilities for complex decision making, we aim to create an intuitive system that not only recommends optimal plays but also deepens understanding of advanced poker strategies. Our goal is a practical tool that bridges the gap between theoretical GTO knowledge and real-world application for players looking to improve.

## 3. Knowledge Representation

<!-- [What type of knowledge will your system handle? How will it be obtained (Will you build a KB from scratch? Will you scrape data off the internet (which source)? Will you encode the rules of a game as a knowledge base? Do you need to research expert knowledge?) How will it be represented (a python KB, a relational database, JSON files, custom classes and objects in an OO language…)? How big is the dataset?] -->

We will build our tool using established poker strategies, particularly focusing on GTO. This information will come from books, expert articles, and databases of poker games. We will input this knowledge into python. python works by using rules and facts to process information. We expect our database of poker knowledge to grow as we continue to add more information and scenarios to the tool. We're going to use a similiar strategy used in Libratus Libratus used computational game theory and reinforcement learning to develop its poker strategy, playing against itself to refine decision-making. This seems like a promising approach for developing GTO insights. The key innovation of Libratus is real-time subgame solving during actual gameplay to recompute finer-grained strategies for the specific situation reached allowing the bot to handle the vast complexity of no-limit poker. Libratus does not try to model opponents or vary its style. It simply plays a balanced, mixed strategy aimed at being unexploitable. This GTO approach could inform our tool. In heads-up matches, Libratus decisively defeated top human professionals over 120,000 hands demonstrating the potential of GTO strategies. Libratus has paved the way for newer AIs like Pluribus that handle multiplayer poker. Our knowledge representation could use a blend of both Pluribus and Libratus. Libratus was designed for and tested in heads-up (two player) poker, while Pluribus was designed specifically for multiplayer poker with up to 6 players. Pluribus uses a simplified search algorithm compared to Libratus since exhaustive search is not feasible with more players and complexity and plans ahead only a few moves rather than to the end of the game (adjusting its playstyle as needed). Pluribus develops its strategy almost entirely from self-play, rather than incorporating human data like Libratus. This makes its style more unconventional for example one of its key parts of Pluribus's strategy like frequent donk betting (starting a round with a bet when you didn't take the previous action) actually go against conventional human poker wisdom, showing its independent style.

## 4. Methods and Tools

<!-- [Describe which method (or methods) you consider applying to the problem, with a pros/cons discussion of each method. Make sure to include any difficulties you expect encountering] -->

We chose python because it is especially good at working with rules, patterns, and logical sequences, which are key in poker strategy. Our tool will simulate different stages of a poker game and offer advice on the best moves. The main challenge will be ensuring that our tool's advice is simple to understand and practically useful for players. We also aim for the tool to be responsive and interact smoothly with users, providing real-time advice and feedback.

**Key Features:**

1. **Hand Strength Prediction**: This features involves creating a system that can evaluate the strength of a poker hand. This can be achieved by representing cards and their values in python, as shown in. Using python we can create rules to determine a hand's rank (e.g., straight flush, four-of-a-kind, full house, etc.) based on the cards it contains.

2. **Game Theory Optimal (GTO) Strategies**: We will implement GTO strategies (there are different types of betting charts we can use and convert this to python). For example, strategies for playing your range instead of your hand, when to bluff or make huge hero calls, constructing unexploitable ranges, and optimal bet sizing strategies [3].

3. **Decision-Making Processes**: This is the main feature and to do this we would create a system that can simulate different stages of a poker game and offer advice on the best moves to make. This could be achieved by modeling a hand of poker as an ordered sequence of events, originating from different actors in the game (players & dealer). The game logic would then enforce constraints regarding valid and invalid sequences [4].

## 5. Evaluation Criteria

<!-- [Describe any numerical or subjective criteria you are using to evaluate your solution.If you are using a pre-existing alternative solution to the problem as a baseline, identify this baseline.  Evaluation criteria refers to metrics you, as a group, use to evaluate the success of your system. It does not refer to criteria the system uses to evaluate how well it’s doing at a given point.
For example, win rate (versus a specified opponent) is a good evaluation criteria in a chess-playing program. The score of a position (as measured by the material on the board) is not!] -->

To evaluate our tool, we will compare its advice with established GTO strategies to ensure accuracy and effectiveness. We will also seek user feedback to gauge the tool's usefulness. The primary measure of success will be whether users can improve their poker skills and understanding of GTO strategies through our tool.

**Comparison with GTO Experts:** We will match our tool's advice against recommendations from GTO poker experts' bots. We are on the right track if our tool's advice aligns closely with expert strategies. We are building a poker bot using reinforcement q-learning for CSC 487, so we will battle between our two bots. We will also compare our tool to existing GTO bots such as GTO Wizard AI (highest win rate against Slumbot, a superhuman poker bot) [5], GTOBase [6], Raise Your Game [7], WPT GTO Trainer [8], GTO Sensei [9].

**User Improvement Tracking:** We'll track users' progress as they continue to play with the tool. Users can record their win rates and decision-making skills before and after using the tool (percent of the time they make the correct decision). Improvement in these areas will indicate the tool's effectiveness in making the right calls and being useful.

**Interactive Poker Scenarios:** We will create a series of challenging poker scenarios. Users can test their skills by making decisions in these scenarios and then compare their choices with our tool's suggestions. This will help users see how their decision-making aligns with GTO principles.

## 6. References

<!-- [References of all supporting material you used. If you use links, add information like title, author, organization, publication date - "naked" URLs are not sufficient. For academic  references, Google Scholar provides formatted citations and references for most papers - I suggest using the APA format. When citing websites, include date visited.
Note: every reference should be numbered and used in the text] -->

[1] Brown, Noam, and Tuomas Sandholm. Superhuman AI for Heads-up No-Limit Poker: Libratus Beats Top ... - Science, 17 Dec. 2017, www.science.org/doi/10.1126/science.aao1733. 

[2] Brown, Noam, and Tuomas Sandholm. Superhuman AI for Multiplayer Poker | Science, 11 July 2019, www.science.org/doi/10.1126/science.aay2400. 

[3] BARRY, O’KEARNEY DARA CARTER. GTO Poker Simplified. MOVEMENT PUBLISHING, 2022. 

[4] Sklansky, David. The Theory of Poker. Two Plus Two Pub., 2007. 

[5] GTO Wizard. “Crushing a Top Hunl Poker Bot.” GTO Wizard, 4 Sept. 2023, blog.gtowizard.com/crushing-a-top-hunl-poker-bot/. 

[6] “GTO Poker Strategy Viewer, Trainer and HH Analyzer.” GTOBase, 20 Jan. 2023, gtobase.com/. 

[7] Cory. “Hand Analysis: Using a GTO Solver to Improve Play against a Human Opponent.” Raise Your Game, 6 Oct. 2022, raiseyourgame.com/2022/10/06/hand-analysis-using-a-gto-solver-to-improve-play-against-a-human-opponent/. 

[8] “WPT GTO Trainer: Play Solved GTO Hands and Get Real-Time Feedback.” WPT GTO Trainer: Play Solved GTO Hands and Get Real-Time Feedback, gto.learnwpt.com/. Accessed 25 Jan. 2024. 

[9] “A Revolutionary Mobile App for Learning Optimal (GTO) Poker Strategy.” GTO Sensei - Your Personal Mobile Poker Trainer, gtosensei.com/. Accessed 25 Jan. 2024. 


