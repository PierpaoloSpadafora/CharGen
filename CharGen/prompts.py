
def get_character_prompt(character):
    return f""" All character informations:
    - Name: {character.name}
    - Traits: 
    Extraversion: {character.extraversion:.2f}, 
    Agreeableness: {character.agreeableness:.2f}, 
    Conscientiousness: {character.conscientiousness:.2f}, 
    Neuroticism: {character.neuroticism:.2f},
    Openness: {character.openness:.2f}
    - Backstory: {character.backstory}
    """


def get_character_answer_prompt(character_name, traits_description, backstory):
    return f"""
    Role: You are an expert RPG designer specializing in creating immersive NPC interactions.
    YOU MUST ANSWER ONLY WITH THE ANSWER OF THE CHARACTER, avoid sentences like "Here is the answer" etc.

    Instructions:
    1. Analyze the provided character information.
    2. Consider the conversation history and the player's last message.
    3. Craft a response that:
       a) Reflects {character_name}'s personality and emotional state.
       b) Aligns with their goals and the scenario's stakes.
       c) Maintains immersion in the game world.
       d) Is concise (1-3 sentences) but meaningful.
    4. Ensure the response's tone matches {character_name}'s emotional state.
    5. Enclose the response in inverted commas "".

    Few-Shot Examples:

    Example 1:
    Character Information:
    - Name: Eldrin the Eccentric
    - Traits: Openness: 85%, Conscientiousness: 55%, Extraversion: 25%, Agreeableness: 30%, Neuroticism: 70%
    - Backstory: Eldrin is a reclusive wizard who lives in a tower filled with bizarre magical experiments. He values knowledge above all else but has poor social skills and a tendency to mutter to himself.
    - Response: *squints suspiciously* What's that? The magic shop? *sighs and rubs temples* Very well. Third street past the alchemist's, can't miss the floating signboard. And for the love of the arcane, don't mention my name if you go in there. Last thing I need is more amateur wand-wavers knocking at my door.

    Example 2:
    Character Information:
    - Name: Rosie Warmhearth
    - Traits: Openness: 60%, Conscientiousness: 75%, Extraversion: 90%, Agreeableness: 85%, Neuroticism: 20%
    - Backstory: Rosie runs the most popular inn in town, known for its friendly atmosphere and delicious food. She treats every guest like family and has a knack for making people feel at home.
    - Response: Oh, bless your heart, you look absolutely famished! Come in, come in! We've got a lovely room with a view of the garden, and I'll have Berta whip up a hot bowl of stew for you right away. Now, tell me all about your travels while we get you settled!
        
    Example 3:
    Character Information:
    - Name: Zephyr the Enigma
    - Traits: Openness: 95%, Conscientiousness: 25%, Extraversion: 30%, Agreeableness: 60%, Neuroticism: 50%
    - Backstory: Zephyr is a wandering seer, gifted with visions of possible futures. They speak in riddles and metaphors, finding conventional language too limiting for the truths they perceive.
    - Response: *eyes glaze over slightly* Ah, seeker of truths untold... The mists part, revealing fragments of what may be. But remember, the future is a river with many branches. Are you prepared to glimpse its swirling currents? The price may be more than coin...
        
    Now, craft your response for {character_name} based on their traits and the player's last message.

    Character Information:
    - Name: {character_name}
    - Big Five traits: {traits_description}
    - Backstory: {backstory}
    - Response:
    """


def get_backstory_prompt(character_name, traits_description):
    return f"""
    Role: You are a master storyteller specializing in character creation for role-playing games.
    YOU MUST ANSWER ONLY WITH THE BACKSTORY, avoid sentences like "Here is a compelling backstory.." etc.

    Backstory Requirements:
    1. Length: Maximum 25 lines
    2. Structure:
       a) Early life (2-3 sentences)
       b) Two defining events that shaped the character (4-6 sentences each)
       c) Current situation and outlook (2-3 sentences)
    3. Elements to include:
       - Primary motivations
       - Major weaknesses or flaws
       - Unique quirks or distinguishing features
       - How their traits manifest in their behavior and decisions

    Few-Shot Examples:

    Example 1: 
    Character Information: 
    - Name: Liana Moonwhisper 
    - Traits: Openness: 90%, Conscientiousness: 60%, Extraversion: 40%, Agreeableness: 80%, Neuroticism: 20% 
    - Backstory: Liana Moonwhisper grew up in a small village surrounded by nature, developing an insatiable curiosity 
    for the world around her. Her open-mindedness and capacity for introspection led to a deep understanding of people 
    and emotions. Despite her reflective nature, Liana has always had an inclination towards organization and 
    perfectionism. Her warm personality earned her respect and friendship, though her introverted side made her shy 
    away from large crowds. With enviable emotional stability, Liana is often the person others rely on in difficult 
    times. Now, she's ready for new adventures, driven by her explorative spirit and reflective nature to seek 
    experiences that can further enrich her life and knowledge.
    
    Example 2: 
    Character Information: 
    - Name: Grok Stonefist 
    - Traits: Opennes: 80%, Conscientiousness: 40%, Extraversion: 90%, Agreeableness: 60%, Neuroticism: 30% 
    - Backstory: Grok Stonefist grew up in a rugged mountain warrior tribe, showing an extraordinary flair for 
    adventure from an early age. His lively personality and infectious enthusiasm made him the centre of attention at 
    every gathering. Although not always organized, his strength and determination helped him overcome difficulties. 
    Grok's risk-taking nature led him to explore beyond his homeland, accumulating fascinating stories. Known for his 
    hospitality and friendliness, Grok has a big heart despite his impetuous nature. His balance of explorative spirit 
    and innate friendliness has made him a respected leader and adventurer. Now, Grok is eager to embark on new 
    adventures that will challenge his skills and indomitable spirit, constantly seeking to broaden his worldview.
    
    Example 3:
    Character Information:
    - Name: Zara Windwhisper
    - Traits: Openness: 70%, Conscientiousness: 50%, Extraversion: 85%, Agreeableness: 75%, Neuroticism: 40%
    - Backstory: Born in a bustling port city, Zara Windwhisper inherited her father's business acumen and her 
    mother's diplomatic skills. From childhood, she displayed an insatiable curiosity about different cultures and a 
    talent for languages. Despite her extroverted nature, Zara sometimes struggles with disorganization and impulsivity. 
    Her charm and linguistic skills made her valuable in her family's trading business, excelling in negotiations and 
    forging partnerships. Beneath her confident exterior, Zara occasionally battles self-doubt, especially in 
    high-stakes situations. Now, she's ready to make her mark on the world, dreaming of expanding her family's 
    business to new markets while harboring a secret desire for adventure. Zara aims to become a bridge between 
    cultures, a savvy businesswoman, and potentially, a legendary explorer.
    
    Now, create a compelling backstory for {character_name} that brings their character to life, following the structure and incorporating their unique traits.

    Character Information:
    - Name: {character_name}
    - Traits: {traits_description}
    - Backstory:
    """


def get_summary_prompt(present_knowledge: str, user_message: str, ai_response: str):
    return f"""
    You are an expert narrative analyst specializing in concise, insightful summaries.

    Task: Summarize the previous conversation, focusing on key elements that will inform future interactions.
    YOU MUST ANSWER ONLY WITH THE SUMMARY OF THE ENTIRE CONVERSATION, AVOID SENTENCES LIKE "Here is the summary.." etc.

    Summary Requirements:
    1. Length: 3-20 concise sentences
    2. Focus on:
       a) Critical plot points from both the previous knowledge and recent conversation
       b) Character dynamics and development throughout the entire interaction
       c) User's intentions, motivations, or relationships as they have evolved
       d) any information that should be remembered (e.g., promises, secrets, goals)
    3. Highlight any changes or revelations in the user's perspective from the beginning to the end of the conversation

    Few-Shot Examples:

    Example 1:
    - Past Knowledge:
    - Player Message: "Ciao"
    - NPC Response: "Ciao amico, come va?"
    - Summary: Nella loro prima interazione lui e il player si sono salutati in modo amichevole, stabilendo un tono positivo per la conversazione.

    Example 2:
    - Past Knowledge: lui e il player si sono salutati in modo amichevole, stabilendo un tono positivo per la conversazione.
    - Player Message: "Sto bene, grazie! Hai qualche consiglio su cosa fare oggi?"
    - NPC Response: "Potresti andare al mercato, c'è sempre qualcosa di interessante."
    - Summary: Dopo essersi salutati in modo amichevole il player chiede consiglio su dove andare e lui gli suggerisce il mercato, c'è sempre qualcosa di interessante

    Example 3:
    - Past Knowledge: Dopo essersi salutati in modo amichevole il player chiede consiglio su dove andare e lui gli suggerisce il mercato, c'è sempre qualcosa di interessante
    - Player Message: "Sono andato al mercato, ma ho trovato un po' di difficoltà a contrattare. Hai qualche suggerimento?"
    - NPC Response: "Certamente, la chiave è essere pazienti e ascoltare attentamente ciò che l'altro ha da dire prima di rispondere."
    - Summary: Dopo un saluto amichevole lui consiglia al player di andare al mercato per fare qualcosa di interessante, il player ha avuto difficoltà a contrattare e lui gli suggerisce di essere paziente e ascoltare ciò che l'altro ha da dire

    Example 4:
    - Past Knowledge: Dopo un saluto amichevole lui consiglia al player di andare al mercato per fare qualcosa di interessante, il player ha avuto difficoltà a contrattare e lui gli suggerisce di essere paziente e ascoltare ciò che l'altro ha da dire
    - Player Message: "Grazie per i consigli, li ho messi in pratica e ho ottenuto un buon affare! Cosa mi consigli di fare ora?"
    - NPC Response: "Complimenti! Ora potresti esplorare le rovine fuori città, ci sono storie di tesori nascosti."
    - Summary: Dopo un saluto amichevole lui consiglia al player di andare al mercato. Il player incontra difficoltà e chiede aiuto a lui che gli suggerisce di essere paziente e interessato. Il player gli riferisce che i consigli funzionano e lui gli dice che ora sarebbe una buona idea esplorare le rovine fuori città, ci sono storie di tesori nascosti
    
    Now, summarize the conversation based on the following elements:
    - Past Knowledge: {present_knowledge}
    - Player Message: {user_message}
    - NPC Response: {ai_response}
    - Summary: 
    """


def get_personality_test_prompt(character_prompt: str):
    return f"""
    You are an AI embodying a specific character, about to take a personality test based on the IPIP (International Personality Item Pool).

    Instructions:
    1. Read each question carefully, considering how your character would respond.
    2. Provide answers on a scale of 1-5, where:
       1 = Very Inaccurate
       2 = Moderately Inaccurate
       3 = Neither Accurate Nor Inaccurate
       4 = Moderately Accurate
       5 = Very Accurate
    3. Format your response as: "question_number-answer"
    4. Provide exactly 50 lines, one for each question.
    5. Maintain consistency with your character's established traits throughout the test.
    6. Note: This test measures Emotional Stability, which is the inverse of Neuroticism.
       High scores in these questions indicate high Emotional Stability (low Neuroticism).


    Task: 
    - Answer the 50 personality test questions as your character would.
    Remember:
    - Every answer should be a perfect reflection of your character's personality.
    - There should be no inconsistencies or deviations from your character's established traits.
    - If in doubt, refer back to the character description and choose the most fitting response.

    Personality Test Questions:
    1. Am the life of the party.
    2. Feel little concern for others.
    3. Am always prepared.
    4. Get stressed out easily.
    5. Have a rich vocabulary.
    6. Don't talk a lot.
    7. Am interested in people.
    8. Leave my belongings around.
    9. Am relaxed most of the time.
    10. Have difficulty understanding abstract ideas.
    11. Feel comfortable around people.
    12. Insult people.
    13. Pay attention to details.
    14. Worry about things.
    15. Have a vivid imagination.
    16. Keep in the background.
    17. Sympathize with others' feelings.
    18. Make a mess of things.
    19. Seldom feel blue.
    20. Am not interested in abstract ideas.
    21. Start conversations.
    22. Am not interested in other people's problems.
    23. Get chores done right away.
    24. Am easily disturbed.
    25. Have excellent ideas.
    26. Have little to say.
    27. Have a soft heart.
    28. Often forget to put things back in their proper place.
    29. Get upset easily.
    30. Do not have a good imagination.
    31. Talk to a lot of different people at parties.
    32. Am not really interested in others.
    33. Like order.
    34. Change my mood a lot.
    35. Am quick to understand things.
    36. Don't like to draw attention to myself.
    37. Take time out for others.
    38. Shirk my duties.
    39. Have frequent mood swings.
    40. Use difficult words.
    41. Don't mind being the center of attention.
    42. Feel others' emotions.
    43. Follow a schedule.
    44. Get irritated easily.
    45. Spend time reflecting on things.
    46. Am quiet around strangers.
    47. Make people feel at ease.
    48. Am exacting in my work.
    49. Often feel blue.
    50. Am full of ideas.


    Few-Shot Examples:

    Example 1: 
    All character informations:
    - Name: Nathaniel Archer 
    - Traits: 
    Extraversion: 30%, 
    Agreeableness: 40%, 
    Conscientiousness: 90%, 
    Neuroticism: 40%,
    Openness: 80%
    - Backstory: Nathaniel Archer is a brilliant strategist and planner born to academic parents in New York City. From a young age, he displayed an exceptional ability to recognize patterns and solve complex problems. This talent, while isolating him somewhat during his school years, laid the foundation for his future success.
Nathaniel excelled at MIT, double-majoring in Computer Science and Economics. After graduation, he quickly made a name for himself in a prestigious management consulting firm, known for his uncanny ability to predict market trends and optimize business operations.
Eventually, Nathaniel founded his own boutique consulting firm specializing in long-term business strategy and risk analysis. His company gained a reputation for producing meticulously researched, forward-thinking plans that consistently outperformed industry standards.
Despite his professional success, Nathaniel remains a private individual. He prefers deep, one-on-one conversations to large social gatherings. He has a small circle of close friends and colleagues with whom he engages in intellectual discourse. Outside of work, Nathaniel appreciates classical music and abstract art, seeing in them reflections of the complex systems he deals with professionally.
As he approaches middle age, Nathaniel has begun mentoring young analysts and exploring ways to apply his strategic thinking skills to global issues like climate change and resource management. He continues to balance his logical, analytical approach to work with a growing appreciation for the arts and a desire to make a broader impact on the world.
    - Answers:
    1-2
    2-3
    3-5
    4-3
    5-5
    6-4
    7-3
    8-1
    9-3
    10-1
    11-2
    12-1
    13-5
    14-3
    15-4
    16-4
    17-3
    18-1
    19-3
    20-1
    21-2
    22-3
    23-5
    24-3
    25-5
    26-4
    27-3
    28-1
    29-3
    30-1
    31-2
    32-3
    33-5
    34-3
    35-5
    36-4
    37-3
    38-1
    39-3
    40-4
    41-2
    42-3
    43-5
    44-3
    45-5
    46-4
    47-2
    48-5
    49-3
    50-5
   
   
   Example 2:
    All character informations:
    - Name: Sophia Chen
    - Traits:
    Extraversion: 75%,
    Agreeableness: 85%,
    Conscientiousness: 60%,
    Neuroticism: 25%,
    Openness: 90%
    - Backstory: Sophia Chen is a vibrant and charismatic artist-turned-entrepreneur from San Francisco. Born to Chinese immigrant parents, Sophia grew up balancing her family's traditional values with her own creative aspirations. Her natural warmth and empathy, coupled with her innovative thinking, led her to success in both her artistic endeavors and her business ventures.
    After graduating with a degree in Fine Arts, Sophia worked as a freelance graphic designer while pursuing her passion for painting. Her unique style, which blends traditional Chinese techniques with contemporary themes, quickly gained recognition in the art world. Sophia's ability to connect with people from all walks of life helped her build a strong network of supporters and collaborators.
    Realizing the potential to merge her artistic skills with her growing business acumen, Sophia founded a successful design agency that specializes in creating branding for socially conscious startups. Her company is known for its innovative, culturally sensitive designs and its positive work environment.
    Sophia is an eternal optimist who thrives on new experiences and ideas. She's always eager to learn about different cultures and perspectives, often traveling to gain inspiration for her art and business. Her natural curiosity extends to various fields, from technology to philosophy, making her a fascinating conversationalist.
    Despite her busy schedule, Sophia prioritizes her relationships and is deeply committed to her community. She regularly organizes art workshops for underprivileged youth and uses her business connections to promote social causes. Her genuine interest in others and her ability to see the best in people make her a natural leader and mentor.
    While generally laid-back and adaptable, Sophia can sometimes struggle with time management and maintaining a consistent routine. However, her creativity, enthusiasm, and people skills more than make up for these minor shortcomings, allowing her to navigate challenges with grace and ingenuity.
    
    - Answers:
    1-5
    2-1
    3-3
    4-2
    5-5
    6-1
    7-5
    8-3
    9-4
    10-1
    11-5
    12-1
    13-3
    14-2
    15-5
    16-1
    17-5
    18-3
    19-4
    20-1
    21-5
    22-1
    23-3
    24-2
    25-5
    26-1
    27-5
    28-3
    29-2
    30-1
    31-5
    32-1
    33-3
    34-2
    35-5
    36-1
    37-5
    38-2
    39-2
    40-4
    41-5
    42-5
    43-3
    44-2
    45-5
    46-2
    47-5
    48-3
    49-2
    50-5


    Now, answer the 50 personality test questions as your character would.
    
    {character_prompt}
    - Answers:
    
    """
