"""Playable content for Faith-Trails Series 4: Wisdom & Faithfulness."""


def sequence(prompt, items):
    """Create a sequence activity from (id, emoji, label) tuples."""
    return {
        "type": "interactive",
        "subtype": "sequence",
        "prompt": prompt,
        "items": [
            {"id": item_id, "emoji": emoji, "label": label}
            for item_id, emoji, label in items
        ],
    }


def matching(prompt, items):
    """Create a tap-to-move matching activity."""
    return {
        "type": "interactive",
        "subtype": "matching",
        "prompt": prompt,
        "items": [
            {"id": item_id, "emoji": emoji, "label": label}
            for item_id, emoji, label in items
        ],
    }


def quiz(prompt, correct, *incorrect):
    """Create a multiple-choice question with the correct answer first."""
    return {
        "type": "quiz",
        "prompt": prompt,
        "options": [correct, *incorrect],
        "correct_index": 0,
    }


def verse(text, reference, *other_references):
    """Create an age-appropriate World English Bible memory-verse activity."""
    return {
        "type": "memory_verse",
        "verse": text,
        "reference": reference,
        "reference_options": [reference, *other_references],
    }


SERIES_4_CONTENT = {
    "solomon": {
        "title": "Solomon",
        "intro_scenes": [
            {
                "type": "story",
                "emoji": "👑",
                "text": "Solomon became king of Israel after his father David. He loved God and wanted to lead God's people well.",
            },
            {
                "type": "story",
                "emoji": "🌙",
                "text": "One night at Gibeon, God appeared to Solomon in a dream and said, 'Ask what I shall give you.'",
            },
            {
                "type": "story",
                "emoji": "🙏",
                "text": "Solomon did not ask for riches or a long life. He asked for an understanding heart so he could judge wisely between good and evil.",
            },
        ],
        "outro_scenes": [
            {
                "type": "story",
                "emoji": "✨",
                "text": "God was pleased with Solomon's request. He gave Solomon great wisdom and also gave him riches and honor.",
            },
            {
                "type": "story",
                "emoji": "⚖️",
                "text": "Soon two women came to Solomon with a difficult disagreement. Solomon listened carefully and used wisdom to discover which woman truly loved the baby as his mother.",
            },
            {
                "type": "story",
                "emoji": "📖",
                "text": "All Israel heard about Solomon's wise judgment. They respected him because they saw that God had given him wisdom to lead with justice.",
            },
        ],
        "interactive_by_difficulty": {
            "easy": matching("Choose the things that show Solomon wanted to be a wise king!", [
                ("listen", "👂", "Listen carefully"),
                ("pray", "🙏", "Ask God for help"),
                ("fair", "⚖️", "Judge fairly"),
            ]),
            "medium": sequence("Put Solomon's wisdom story in order!", [
                ("king", "👑", "Solomon becomes king"),
                ("dream", "🌙", "God speaks in a dream"),
                ("request", "🙏", "Solomon asks for wisdom"),
                ("gift", "✨", "God grants his request"),
                ("judgment", "⚖️", "Solomon judges wisely"),
            ]),
            "hard": sequence("Arrange Solomon's complete wisdom journey!", [
                ("rule", "👑", "Solomon begins to rule"),
                ("offer", "🌙", "God offers Solomon a gift"),
                ("humility", "🙏", "Solomon admits he needs help"),
                ("wisdom", "✨", "God gives wisdom"),
                ("case", "👩‍🍼", "Two women bring a hard case"),
                ("discern", "⚖️", "Solomon discovers the truth"),
                ("respect", "📖", "Israel respects God's wisdom"),
            ]),
        },
        "quiz_bank_by_difficulty": {
            "easy": [
                quiz("What did Solomon ask God to give him?", "Wisdom", "A larger palace", "A stronger army"),
                quiz("Who gave Solomon wisdom?", "God", "A merchant", "A soldier"),
                quiz("What job did Solomon have?", "King of Israel", "Fisherman", "Shepherd boy"),
            ],
            "medium": [
                quiz("Why did Solomon ask for an understanding heart?", "To lead God's people well", "To win every race", "To build the tallest tower"),
                quiz("Where did God speak to Solomon?", "In a dream at Gibeon", "Inside Noah's ark", "Beside the Red Sea"),
                quiz("How did Israel respond to Solomon's wise judgment?", "They respected him", "They chose a different king", "They ignored the decision"),
            ],
            "hard": [
                quiz("Why was God pleased with Solomon's request?", "He valued wisdom for serving others", "He asked to become famous", "He refused to lead Israel"),
                quiz("What did the difficult case reveal about Solomon?", "God had given him discernment", "He never needed to listen", "He judged by wealth"),
                quiz("What is biblical wisdom?", "Using God's truth to choose what is right", "Knowing the most facts", "Always getting what we want"),
            ],
        },
        "quiz_count_by_difficulty": {"easy": 2, "medium": 3, "hard": 3},
        "verse_bank_by_difficulty": {
            "easy": [verse("Yahweh gives wisdom.", "Proverbs 2:6", "Proverbs 1:6", "Proverbs 3:6")],
            "medium": [verse("If any of you lacks wisdom, let him ask of God.", "James 1:5", "James 2:5", "1 John 1:5")],
            "hard": [verse("Trust in Yahweh with all your heart, and don't lean on your own understanding.", "Proverbs 3:5", "Proverbs 2:5", "Proverbs 4:5")],
        },
        "lesson": "True wisdom begins with trusting God and helps us make fair, loving choices for other people.",
    },

    "ten-commandments": {
        "title": "The Ten Commandments",
        "intro_scenes": [
            {
                "type": "story",
                "emoji": "🏕️",
                "text": "After God rescued Israel from Egypt, the people camped near Mount Sinai. God had brought them safely through the wilderness.",
            },
            {
                "type": "story",
                "emoji": "⛰️",
                "text": "God called Moses up the mountain. Thunder, lightning, a thick cloud, and a trumpet sound reminded everyone that God is holy.",
            },
            {
                "type": "story",
                "emoji": "📜",
                "text": "God gave His people ten important commandments. The first commandments taught them to worship God alone and honor His name.",
            },
        ],
        "outro_scenes": [
            {
                "type": "story",
                "emoji": "🕊️",
                "text": "God also taught them to keep the Sabbath holy and to honor their fathers and mothers.",
            },
            {
                "type": "story",
                "emoji": "❤️",
                "text": "The other commandments taught the people to respect life, remain faithful in marriage, tell the truth, and respect what belonged to someone else.",
            },
            {
                "type": "story",
                "emoji": "🤝",
                "text": "The commandments showed Israel how to love God and live faithfully with one another. God's instructions protected their worship, families, truth, and neighbors.",
            },
        ],
        "interactive_by_difficulty": {
            "easy": matching("Gather choices that follow God's loving instructions!", [
                ("worship", "🙏", "Worship God"),
                ("honor", "👨‍👩‍👧", "Honor parents"),
                ("truth", "💬", "Tell the truth"),
                ("kindness", "🤝", "Respect others"),
            ]),
            "medium": matching("Sort the commandments into love for God and love for people!", [
                ("god-alone", "🙏", "Worship God alone"),
                ("holy-name", "✨", "Honor God's name"),
                ("sabbath", "🕊️", "Keep the Sabbath holy"),
                ("parents", "👨‍👩‍👧", "Honor parents"),
                ("truth", "💬", "Tell the truth"),
                ("property", "🏠", "Respect what belongs to others"),
            ]),
            "hard": sequence("Put the ten commandments into their Bible order!", [
                ("one-god", "1️⃣", "No other gods"),
                ("idols", "2️⃣", "Do not make idols"),
                ("name", "3️⃣", "Honor God's name"),
                ("sabbath", "4️⃣", "Remember the Sabbath"),
                ("parents", "5️⃣", "Honor father and mother"),
                ("life", "6️⃣", "Do not murder"),
                ("marriage", "7️⃣", "Be faithful in marriage"),
                ("steal", "8️⃣", "Do not steal"),
                ("witness", "9️⃣", "Do not give false testimony"),
                ("covet", "🔟", "Do not covet"),
            ]),
        },
        "quiz_bank_by_difficulty": {
            "easy": [
                quiz("Who received the commandments from God?", "Moses", "David", "Jonah"),
                quiz("Where did God give the commandments?", "Mount Sinai", "Jericho", "Bethlehem"),
                quiz("How many commandments did God give?", "Ten", "Five", "Twelve"),
            ],
            "medium": [
                quiz("What do the first commandments teach?", "How to honor and worship God", "How to build a palace", "How to choose a king"),
                quiz("Which commandment protects truth?", "Do not give false testimony", "Build an altar", "Count the stars"),
                quiz("What does it mean to covet?", "To wrongly desire what belongs to another", "To share what we have", "To thank God"),
            ],
            "hard": [
                quiz("What had God done before giving Israel the commandments?", "Rescued them from slavery", "Made Solomon king", "Sent them to Babylon"),
                quiz("How did Jesus summarize God's law?", "Love God and love your neighbor", "Gather wealth and power", "Never speak to strangers"),
                quiz("Why are God's commands a gift?", "They teach faithful love and protect relationships", "They make people earn God's rescue", "They remove every hard choice"),
            ],
        },
        "quiz_count_by_difficulty": {"easy": 2, "medium": 3, "hard": 3},
        "verse_bank_by_difficulty": {
            "easy": [verse("Honor your father and your mother.", "Exodus 20:12", "Exodus 20:2", "Exodus 12:20")],
            "medium": [verse("You shall have no other gods before me.", "Exodus 20:3", "Exodus 20:13", "Exodus 3:20")],
            "hard": [verse("You shall love Yahweh your God with all your heart, with all your soul, and with all your might.", "Deuteronomy 6:5", "Deuteronomy 5:6", "Joshua 6:5")],
        },
        "lesson": "God's commandments teach us to love Him first and to treat other people with honor, truth, and care.",
    },

    "elijah": {
        "title": "Elijah",
        "intro_scenes": [
            {
                "type": "story",
                "emoji": "☀️",
                "text": "King Ahab and many people in Israel had turned away from God to worship Baal. God sent the prophet Elijah to call them back.",
            },
            {
                "type": "story",
                "emoji": "⛰️",
                "text": "On Mount Carmel, Elijah asked the people how long they would waver between two choices. If Yahweh was God, they should follow Him.",
            },
            {
                "type": "story",
                "emoji": "🐂",
                "text": "Elijah and the prophets of Baal each prepared a sacrifice without lighting a fire. The true God would answer by sending fire.",
            },
        ],
        "outro_scenes": [
            {
                "type": "story",
                "emoji": "📣",
                "text": "The prophets of Baal called out for hours, but no voice answered. Their altar remained cold and silent.",
            },
            {
                "type": "story",
                "emoji": "💧",
                "text": "Elijah repaired God's altar, placed the sacrifice on it, and poured water over everything. Then he prayed that the people would know Yahweh is God.",
            },
            {
                "type": "story",
                "emoji": "🔥",
                "text": "God's fire fell and consumed the sacrifice. The people bowed down and cried, 'Yahweh, He is God!' Their hearts began turning back to Him.",
            },
        ],
        "interactive_by_difficulty": {
            "easy": matching("Gather the parts of Elijah's altar story!", [
                ("stones", "🪨", "Altar stones"),
                ("water", "💧", "Water"),
                ("prayer", "🙏", "Elijah's prayer"),
                ("fire", "🔥", "God's fire"),
            ]),
            "medium": sequence("Put the Mount Carmel events in order!", [
                ("choice", "↔️", "Elijah asks the people to choose"),
                ("altars", "🐂", "Two sacrifices are prepared"),
                ("silence", "🤫", "Baal does not answer"),
                ("water", "💧", "Elijah pours water"),
                ("answer", "🔥", "God answers by fire"),
            ]),
            "hard": sequence("Arrange Elijah's complete faithfulness challenge!", [
                ("unfaithful", "👑", "Israel turns from God"),
                ("gather", "⛰️", "Everyone gathers on Carmel"),
                ("question", "↔️", "Elijah challenges their divided loyalty"),
                ("baal", "📣", "Baal's prophets call out"),
                ("repair", "🪨", "Elijah repairs God's altar"),
                ("pray", "🙏", "Elijah prays"),
                ("fire", "🔥", "Yahweh answers"),
            ]),
        },
        "quiz_bank_by_difficulty": {
            "easy": [
                quiz("Who was God's prophet on Mount Carmel?", "Elijah", "Goliath", "Haman"),
                quiz("How did God answer Elijah's prayer?", "He sent fire", "He sent a boat", "He built a wall"),
                quiz("What did the people say?", "Yahweh is God", "Baal is king", "Elijah is lost"),
            ],
            "medium": [
                quiz("Why did Elijah challenge the people?", "They were wavering between Yahweh and Baal", "They wanted a new palace", "They had forgotten the road home"),
                quiz("What happened when Baal's prophets called out?", "No one answered", "Fire fell immediately", "Rain filled the altar"),
                quiz("Why did Elijah pour water on the altar?", "To show that only God could send the fire", "To wash the stones", "To make the sacrifice disappear"),
            ],
            "hard": [
                quiz("What did Elijah ask God to change?", "The people's hearts", "The mountain's height", "Ahab's clothing"),
                quiz("What did the repaired altar represent?", "Israel returning to covenant faithfulness", "A new home for Elijah", "A monument to Baal"),
                quiz("What does Elijah's courage teach believers?", "Stand for God even when many people disagree", "Faith never requires patience", "Winning arguments is most important"),
            ],
        },
        "quiz_count_by_difficulty": {"easy": 2, "medium": 3, "hard": 3},
        "verse_bank_by_difficulty": {
            "easy": [verse("Yahweh, he is God!", "1 Kings 18:39", "1 Kings 17:39", "2 Kings 18:39")],
            "medium": [verse("If Yahweh is God, follow him.", "1 Kings 18:21", "1 Kings 18:12", "2 Kings 18:21")],
            "hard": [verse("The God who answers by fire, let him be God.", "1 Kings 18:24", "1 Kings 17:24", "2 Kings 18:24")],
        },
        "lesson": "Faithfulness means choosing God wholeheartedly and trusting Him even when we seem to stand alone.",
    },

    "nehemiah": {
        "title": "Nehemiah",
        "intro_scenes": [
            {
                "type": "story",
                "emoji": "😢",
                "text": "Nehemiah served the Persian king far from Jerusalem. When he heard that Jerusalem's walls were broken and its gates burned, he wept, fasted, and prayed.",
            },
            {
                "type": "story",
                "emoji": "👑",
                "text": "The king noticed Nehemiah's sadness and asked what he needed. Nehemiah prayed quietly, then bravely requested permission and supplies to rebuild Jerusalem.",
            },
            {
                "type": "story",
                "emoji": "🌙",
                "text": "After arriving, Nehemiah inspected the damaged walls at night. Then he told the people how God had helped him and invited them to rebuild together.",
            },
        ],
        "outro_scenes": [
            {
                "type": "story",
                "emoji": "🧱",
                "text": "Families repaired different sections of the wall. Priests, craftspeople, rulers, and neighbors all worked side by side.",
            },
            {
                "type": "story",
                "emoji": "🛡️",
                "text": "Enemies mocked and threatened them, but Nehemiah prayed and organized guards. The builders kept working with courage and stayed ready to protect one another.",
            },
            {
                "type": "story",
                "emoji": "🎉",
                "text": "The wall was completed in only fifty-two days. Even Israel's enemies understood that God had helped the people accomplish this great work.",
            },
        ],
        "interactive_by_difficulty": {
            "easy": matching("Gather what Nehemiah and the builders needed!", [
                ("prayer", "🙏", "Prayer"),
                ("bricks", "🧱", "Building materials"),
                ("team", "🤝", "Teamwork"),
                ("courage", "🛡️", "Courage"),
            ]),
            "medium": sequence("Put Nehemiah's rebuilding steps in order!", [
                ("news", "😢", "Nehemiah hears the news"),
                ("pray", "🙏", "He prays"),
                ("ask", "👑", "He asks the king"),
                ("inspect", "🌙", "He inspects the wall"),
                ("build", "🧱", "The people rebuild"),
            ]),
            "hard": sequence("Arrange the complete wall-building journey!", [
                ("report", "😢", "Jerusalem's trouble is reported"),
                ("fast", "🙏", "Nehemiah fasts and prays"),
                ("permission", "👑", "The king gives permission"),
                ("survey", "🌙", "Nehemiah surveys the damage"),
                ("organize", "🤝", "Families receive sections"),
                ("resist", "🛡️", "The people resist discouragement"),
                ("complete", "🎉", "The wall is completed"),
            ]),
        },
        "quiz_bank_by_difficulty": {
            "easy": [
                quiz("What did Nehemiah help rebuild?", "Jerusalem's wall", "Noah's ark", "Solomon's throne"),
                quiz("What did Nehemiah do before acting?", "He prayed", "He hid", "He held a feast"),
                quiz("Who worked on the wall?", "Many families and neighbors", "Nehemiah alone", "Only the king"),
            ],
            "medium": [
                quiz("Why was Nehemiah sad?", "Jerusalem's wall and gates were ruined", "He had lost a race", "The king had moved away"),
                quiz("When did Nehemiah inspect the wall?", "At night", "During a parade", "At noon before the king"),
                quiz("How did the people respond to threats?", "They prayed, guarded, and kept building", "They abandoned Jerusalem", "They argued with one another"),
            ],
            "hard": [
                quiz("What made Nehemiah an effective leader?", "Prayer, planning, courage, and teamwork", "Working without anyone's help", "Ignoring every problem"),
                quiz("What did the completed wall show Israel's enemies?", "God had helped the builders", "The Persian army did all the work", "Jerusalem no longer needed God"),
                quiz("How long did rebuilding take?", "Fifty-two days", "Seven years", "Forty days"),
            ],
        },
        "quiz_count_by_difficulty": {"easy": 2, "medium": 3, "hard": 3},
        "verse_bank_by_difficulty": {
            "easy": [verse("The joy of Yahweh is your strength.", "Nehemiah 8:10", "Nehemiah 7:10", "Nehemiah 9:10")],
            "medium": [verse("The God of heaven will prosper us.", "Nehemiah 2:20", "Nehemiah 3:20", "Nehemiah 2:2")],
            "hard": [verse("Remember the Lord, who is great and awesome.", "Nehemiah 4:14", "Nehemiah 4:4", "Nehemiah 5:14")],
        },
        "lesson": "Faithful work begins with prayer and continues with courage, planning, and people serving together.",
    },

    "job": {
        "title": "Job",
        "intro_scenes": [
            {
                "type": "story",
                "emoji": "🏡",
                "text": "Job was a faithful man who loved God. He had a large family, many animals, and a respected place in his community.",
            },
            {
                "type": "story",
                "emoji": "💔",
                "text": "In a short time, Job lost his children, his possessions, and his health. He grieved deeply, but he still worshiped God.",
            },
            {
                "type": "story",
                "emoji": "🗣️",
                "text": "Job's friends came to sit with him. Later they argued that Job must have caused his suffering, but they did not understand what had happened.",
            },
        ],
        "outro_scenes": [
            {
                "type": "story",
                "emoji": "❓",
                "text": "Job honestly brought his pain and questions to God. He did not understand his suffering, yet he knew his Redeemer lived.",
            },
            {
                "type": "story",
                "emoji": "🌪️",
                "text": "God spoke to Job from a whirlwind and reminded him of the greatness and wisdom shown throughout creation. Job learned that God's understanding was far greater than his own.",
            },
            {
                "type": "story",
                "emoji": "🌅",
                "text": "Job humbly trusted God. God corrected Job's friends, restored Job's health and household, and surrounded him with family and comfort again.",
            },
        ],
        "interactive_by_difficulty": {
            "easy": matching("Choose faithful things Job did during a hard time!", [
                ("grieve", "😢", "He honestly grieved"),
                ("worship", "🙏", "He worshiped God"),
                ("ask", "❓", "He brought questions to God"),
                ("trust", "❤️", "He kept trusting"),
            ]),
            "medium": sequence("Put Job's journey in order!", [
                ("blessed", "🏡", "Job lives faithfully"),
                ("loss", "💔", "Job experiences loss"),
                ("friends", "🗣️", "His friends speak"),
                ("god", "🌪️", "God answers Job"),
                ("restore", "🌅", "God restores Job"),
            ]),
            "hard": sequence("Arrange Job's complete faith journey!", [
                ("faithful", "🏡", "Job honors God"),
                ("suffering", "💔", "Suffering enters his life"),
                ("worship", "🙏", "Job worships while grieving"),
                ("debate", "🗣️", "Friends give incomplete answers"),
                ("hope", "❤️", "Job confesses hope"),
                ("whirlwind", "🌪️", "God reveals His greatness"),
                ("humility", "🌅", "Job trusts and is restored"),
            ]),
        },
        "quiz_bank_by_difficulty": {
            "easy": [
                quiz("Who did Job continue to worship?", "God", "A king", "His friends"),
                quiz("Who came to sit with Job?", "His friends", "Goliath", "Pharaoh"),
                quiz("Did Job understand why everything happened?", "No", "Yes, immediately", "His friends explained it perfectly"),
            ],
            "medium": [
                quiz("What mistake did Job's friends make?", "They assumed Job caused his suffering", "They refused to visit him", "They took Job to Egypt"),
                quiz("How did God speak to Job?", "From a whirlwind", "From a burning bush", "Through a palace messenger"),
                quiz("What gave Job hope?", "He knew his Redeemer lived", "He knew he would become king", "He expected his friends to solve everything"),
            ],
            "hard": [
                quiz("What did God's questions about creation teach Job?", "God's wisdom is greater than human understanding", "Job should never ask honest questions", "Creation happened without God's care"),
                quiz("What does Job's story teach about suffering?", "Suffering is not always punishment for a person's sin", "Good people never face hardship", "Friends always know why suffering happens"),
                quiz("How did Job respond after God spoke?", "He answered with humility and trust", "He demanded to rule creation", "He stopped believing in God"),
            ],
        },
        "quiz_count_by_difficulty": {"easy": 2, "medium": 3, "hard": 3},
        "verse_bank_by_difficulty": {
            "easy": [verse("Blessed be Yahweh's name.", "Job 1:21", "Job 2:21", "Job 1:12")],
            "medium": [verse("But as for me, I know that my Redeemer lives.", "Job 19:25", "Job 18:25", "Job 29:25")],
            "hard": [verse("I know that you can do all things, and that no purpose of yours can be restrained.", "Job 42:2", "Job 41:2", "Job 40:2")],
        },
        "lesson": "We can speak honestly to God in hard times and trust His wisdom even when we do not understand.",
    },
}
