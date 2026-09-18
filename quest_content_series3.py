"""Playable content for Faith-Trails Series 3: Courage & Leadership."""


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
    """Create a child-sized WEB memory-verse activity."""
    return {
        "type": "memory_verse",
        "verse": text,
        "reference": reference,
        "reference_options": [reference, *other_references],
    }


SERIES_3_CONTENT = {
    "david-goliath": {
        "title": "David & Goliath",
        "intro_scenes": [
            {
                "type": "story",
                "emoji": "📣",
                "text": "For forty days, the giant Goliath challenged Israel's army. The soldiers were frightened, and no one wanted to face him.",
            },
            {
                "type": "story",
                "emoji": "🥖",
                "text": "Young David came to the camp to bring food to his brothers. When he heard Goliath insult the living God, David offered to fight him.",
            },
            {
                "type": "story",
                "emoji": "🐑",
                "text": "David told King Saul how God had helped him protect his sheep from a lion and a bear. He trusted God to help him again.",
            },
            {
                "type": "story",
                "emoji": "🪨",
                "text": "David took off Saul's heavy armor. He chose five smooth stones from a brook and walked toward Goliath with his shepherd's sling.",
            },
        ],
        "outro_scenes": [
            {
                "type": "story",
                "emoji": "🙏",
                "text": "David told Goliath that he came in the name of Yahweh. David knew the battle belonged to God, not to the strongest weapon.",
            },
            {
                "type": "story",
                "emoji": "🎯",
                "text": "David ran forward, placed one stone in his sling, and struck Goliath. God gave David victory, and Israel saw that God could use a faithful young shepherd.",
            },
        ],
        "interactive_by_difficulty": {
            "easy": matching("Help David collect the things he used after hearing the whole story!", [
                ("stone-1", "🪨", "Smooth stone 1"),
                ("stone-2", "🪨", "Smooth stone 2"),
                ("stone-3", "🪨", "Smooth stone 3"),
                ("stone-4", "🪨", "Smooth stone 4"),
                ("stone-5", "🪨", "Smooth stone 5"),
            ]),
            "medium": sequence("Put David's courageous steps in story order!", [
                ("hear", "📣", "David hears Goliath"),
                ("offer", "🙋", "David offers to fight"),
                ("remember", "🐑", "David remembers God's help"),
                ("stones", "🪨", "David chooses five stones"),
                ("victory", "🎯", "God gives David victory"),
            ]),
            "hard": sequence("Arrange the complete David and Goliath story!", [
                ("challenge", "📣", "Goliath challenges Israel"),
                ("food", "🥖", "David brings food"),
                ("volunteer", "🙋", "David volunteers"),
                ("testimony", "🐑", "David remembers past rescues"),
                ("armor", "🛡️", "David removes the armor"),
                ("faith", "🙏", "David speaks with faith"),
                ("stone", "🎯", "David's stone strikes Goliath"),
            ]),
        },
        "quiz_bank_by_difficulty": {
            "easy": [
                quiz("Who challenged Israel's army?", "Goliath", "Samuel", "Jonah"),
                quiz("What did David carry as his weapon?", "A sling", "A sword", "A spear"),
                quiz("Who gave David courage?", "God", "Goliath", "His brothers"),
            ],
            "medium": [
                quiz("Why did David believe God would help him?", "God had helped him before", "David had magic stones", "Saul promised he could not lose"),
                quiz("Why did David remove Saul's armor?", "He was not used to it", "It belonged to Goliath", "It was broken"),
                quiz("How many smooth stones did David choose?", "Five", "Two", "Twelve"),
            ],
            "hard": [
                quiz("What did David say belonged to Yahweh?", "The battle", "Goliath's armor", "The valley"),
                quiz("What did David's victory teach Israel?", "God saves through faithful people", "Only giants can lead", "Weapons decide every battle"),
                quiz("What prepared David to face Goliath?", "Trust built while caring for sheep", "Training in Saul's army", "A secret map"),
            ],
        },
        "quiz_count_by_difficulty": {"easy": 2, "medium": 3, "hard": 3},
        "verse_bank_by_difficulty": {
            "easy": [verse("The battle is Yahweh's.", "1 Samuel 17:47", "1 Samuel 7:47", "2 Samuel 17:47")],
            "medium": [verse("When I am afraid, I will put my trust in you.", "Psalm 56:3", "Psalm 55:3", "Psalm 65:3")],
            "hard": [verse("I come to you in the name of Yahweh of Armies.", "1 Samuel 17:45", "1 Samuel 17:35", "2 Samuel 17:45")],
        },
        "lesson": "Real courage comes from remembering God's faithfulness and trusting Him with the challenge ahead.",
    },

    "apostles-pentecost": {
        "title": "The Apostles and Pentecost",
        "intro_scenes": [
            {
                "type": "story",
                "emoji": "🕊️",
                "text": "Before Jesus returned to heaven, He promised that the Holy Spirit would give His followers power to tell people everywhere about Him.",
            },
            {
                "type": "story",
                "emoji": "☁️",
                "text": "The apostles watched Jesus rise into the sky. Then they returned to Jerusalem, obeyed His instructions, and prayed together while they waited.",
            },
            {
                "type": "story",
                "emoji": "🔥",
                "text": "On Pentecost, a sound like a mighty wind filled the house. Flames like tongues of fire appeared, and everyone was filled with the Holy Spirit.",
            },
        ],
        "outro_scenes": [
            {
                "type": "story",
                "emoji": "🌍",
                "text": "The apostles spoke in languages they had never learned. Visitors from many nations heard the wonderful works of God in their own languages.",
            },
            {
                "type": "story",
                "emoji": "📖",
                "text": "Peter stood and boldly explained the good news about Jesus. About three thousand people believed and were baptized that day.",
            },
            {
                "type": "story",
                "emoji": "🤲",
                "text": "The apostles kept teaching about Jesus. Through the Holy Spirit they prayed, spoke boldly, cared for people, and performed signs and miracles.",
            },
        ],
        "interactive_by_difficulty": {
            "easy": matching("Match each Pentecost sign with the story you just learned!", [
                ("wind", "💨", "Mighty wind"),
                ("fire", "🔥", "Flames like fire"),
                ("languages", "🌍", "Many languages"),
            ]),
            "medium": sequence("Put the Pentecost events in order!", [
                ("promise", "🕊️", "Jesus promises the Holy Spirit"),
                ("wait", "🙏", "The apostles pray and wait"),
                ("spirit", "🔥", "The Holy Spirit fills them"),
                ("languages", "🌍", "People hear many languages"),
                ("preach", "📖", "Peter preaches about Jesus"),
            ]),
            "hard": sequence("Arrange the apostles' complete courage journey!", [
                ("promise", "🕊️", "Jesus promises power"),
                ("ascend", "☁️", "Jesus returns to heaven"),
                ("prayer", "🙏", "The followers pray together"),
                ("wind", "💨", "A mighty sound fills the house"),
                ("fire", "🔥", "The Holy Spirit fills them"),
                ("sermon", "📖", "Peter shares the good news"),
                ("ministry", "🤲", "The apostles serve boldly"),
            ]),
        },
        "quiz_bank_by_difficulty": {
            "easy": [
                quiz("Who filled the apostles with power?", "The Holy Spirit", "A king", "The Roman army"),
                quiz("What sound filled the house?", "A mighty wind", "A roaring lion", "A trumpet parade"),
                quiz("Who preached about Jesus?", "Peter", "Goliath", "Pharaoh"),
            ],
            "medium": [
                quiz("Why did the apostles remain in Jerusalem?", "Jesus told them to wait", "They were building a palace", "They had lost their map"),
                quiz("What amazed the visitors at Pentecost?", "They heard their own languages", "The building disappeared", "Peter became a king"),
                quiz("How many people believed that day?", "About three thousand", "About twelve", "About fifty"),
            ],
            "hard": [
                quiz("What gave the apostles courage to preach?", "The Holy Spirit", "Their education", "Their wealth"),
                quiz("What message did Peter boldly explain?", "The good news about Jesus", "How to become a soldier", "How to build a temple"),
                quiz("How did the apostles continue Jesus' work?", "They taught, served, and performed miracles", "They hid from everyone", "They became earthly kings"),
            ],
        },
        "quiz_count_by_difficulty": {"easy": 2, "medium": 3, "hard": 3},
        "verse_bank_by_difficulty": {
            "easy": [verse("They were all filled with the Holy Spirit.", "Acts 2:4", "Acts 1:4", "Acts 4:2")],
            "medium": [verse("They spoke the word of God with boldness.", "Acts 4:31", "Acts 3:41", "Acts 1:31")],
            "hard": [verse("You will receive power when the Holy Spirit has come upon you.", "Acts 1:8", "Acts 2:8", "Acts 8:1")],
        },
        "lesson": "The Holy Spirit gives Jesus' followers courage and power to share the good news and serve others.",
    },

    "gideon": {
        "title": "Gideon",
        "intro_scenes": [
            {
                "type": "story",
                "emoji": "🌾",
                "text": "Israel's enemies, the Midianites, kept taking their food. Gideon hid in a wine press while he separated wheat, trying not to be seen.",
            },
            {
                "type": "story",
                "emoji": "😇",
                "text": "Yahweh's angel greeted Gideon as a mighty man of valor. Gideon felt small, but God promised to be with him and use him to rescue Israel.",
            },
            {
                "type": "story",
                "emoji": "🔥",
                "text": "God patiently gave Gideon signs that confirmed His promise. Gideon obeyed God, tore down an idol, and called Israel's soldiers together.",
            },
        ],
        "outro_scenes": [
            {
                "type": "story",
                "emoji": "💧",
                "text": "God reduced Gideon's large army until only three hundred men remained. Everyone would know that God—not the size of the army—gave the victory.",
            },
            {
                "type": "story",
                "emoji": "🏺",
                "text": "Each man carried a trumpet, a clay jar, and a torch. At Gideon's signal they blew the trumpets, broke the jars, raised the lights, and shouted.",
            },
            {
                "type": "story",
                "emoji": "🎺",
                "text": "The Midianite army became confused and fled. Gideon and his three hundred men followed God's unusual plan, and God rescued Israel.",
            },
        ],
        "interactive_by_difficulty": {
            "easy": matching("Gather the three things Gideon's men carried!", [
                ("trumpet", "🎺", "Trumpet"),
                ("jar", "🏺", "Clay jar"),
                ("torch", "🔥", "Torch"),
            ]),
            "medium": sequence("Put Gideon's battle plan in order!", [
                ("choose", "💧", "God chooses three hundred men"),
                ("surround", "🌙", "They surround the camp"),
                ("blow", "🎺", "They blow the trumpets"),
                ("break", "🏺", "They break the jars"),
                ("shine", "🔥", "They raise their torches"),
            ]),
            "hard": sequence("Arrange Gideon's full journey from fear to leadership!", [
                ("hide", "🌾", "Gideon hides while working"),
                ("call", "😇", "God calls Gideon"),
                ("signs", "🔥", "God confirms His promise"),
                ("obey", "🙏", "Gideon obeys"),
                ("reduce", "💧", "The army becomes three hundred"),
                ("plan", "🏺", "They follow God's plan"),
                ("victory", "🎺", "The enemy flees"),
            ]),
        },
        "quiz_bank_by_difficulty": {
            "easy": [
                quiz("Where was Gideon hiding while working?", "In a wine press", "In a palace", "In a boat"),
                quiz("How many men remained with Gideon?", "Three hundred", "Three thousand", "Thirty"),
                quiz("Who gave Israel victory?", "God", "The clay jars", "The Midianites"),
            ],
            "medium": [
                quiz("Why did God make Gideon's army smaller?", "So Israel would know God saved them", "There was not enough food", "Gideon wanted to go home"),
                quiz("What was hidden inside the clay jars?", "Torches", "Water", "Bread"),
                quiz("What happened when Gideon's men followed the plan?", "The enemy became confused and fled", "The torches went out", "The walls fell"),
            ],
            "hard": [
                quiz("How did God describe Gideon before Gideon felt brave?", "A mighty man of valor", "A famous king", "A skilled giant"),
                quiz("What changed Gideon from fearful to courageous?", "Trusting God's presence and promise", "Finding a larger sword", "Becoming the oldest soldier"),
                quiz("What leadership lesson does Gideon's small army teach?", "Faithful obedience matters more than numbers", "Leaders should work alone", "Only large groups can succeed"),
            ],
        },
        "quiz_count_by_difficulty": {"easy": 2, "medium": 3, "hard": 3},
        "verse_bank_by_difficulty": {
            "easy": [verse("Yahweh is with you, you mighty man of valor!", "Judges 6:12", "Judges 7:12", "Joshua 6:12")],
            "medium": [verse("Surely I will be with you, and you shall strike the Midianites as one man.", "Judges 6:16", "Judges 6:6", "Joshua 6:16")],
            "hard": [verse("I will save you by the three hundred men who lapped, and deliver the Midianites into your hand.", "Judges 7:7", "Judges 6:7", "Joshua 7:7")],
        },
        "lesson": "God sees what we can become and gives courage to ordinary people who trust and obey Him.",
    },

    "esther": {
        "title": "Esther",
        "intro_scenes": [
            {
                "type": "story",
                "emoji": "👧",
                "text": "Esther was a young Jewish woman raised by her cousin Mordecai. She lived in Persia, far from the land of her ancestors.",
            },
            {
                "type": "story",
                "emoji": "👑",
                "text": "Esther was chosen to become queen. Mordecai advised her wisely, but Esther did not yet tell the palace that she was Jewish.",
            },
            {
                "type": "story",
                "emoji": "📜",
                "text": "A proud official named Haman made a terrible plan against the Jewish people. Mordecai asked Esther to speak to the king and help save them.",
            },
        ],
        "outro_scenes": [
            {
                "type": "story",
                "emoji": "⏳",
                "text": "Mordecai reminded Esther that she might have become queen for such a time as this. Esther chose courage even though approaching the king uninvited was dangerous.",
            },
            {
                "type": "story",
                "emoji": "🙏",
                "text": "Esther asked the Jewish people in Susa to fast with her for three days. Then she put on her royal clothing and entered the king's court.",
            },
            {
                "type": "story",
                "emoji": "✨",
                "text": "The king welcomed Esther and listened to her. Esther revealed Haman's plan, the Jewish people were rescued, and their sorrow was turned into joy.",
            },
        ],
        "interactive_by_difficulty": {
            "easy": matching("Gather the three things that helped Esther act courageously!", [
                ("purpose", "⏳", "A special purpose"),
                ("support", "🙏", "Her people's support"),
                ("courage", "👑", "Courage to speak"),
            ]),
            "medium": sequence("Put Esther's courageous choices in order!", [
                ("learn", "📜", "Esther learns about the danger"),
                ("message", "⏳", "Mordecai sends his message"),
                ("fast", "🙏", "Esther asks everyone to fast"),
                ("approach", "👑", "Esther approaches the king"),
                ("speak", "🗣️", "Esther speaks for her people"),
            ]),
            "hard": sequence("Arrange Esther's complete leadership journey!", [
                ("raised", "👧", "Mordecai raises Esther"),
                ("queen", "👑", "Esther becomes queen"),
                ("plot", "📜", "Haman makes his plan"),
                ("appeal", "⏳", "Mordecai asks Esther to act"),
                ("fast", "🙏", "The people fast together"),
                ("court", "🏛️", "Esther enters the court"),
                ("rescue", "✨", "Her people are rescued"),
            ]),
        },
        "quiz_bank_by_difficulty": {
            "easy": [
                quiz("Who raised Esther?", "Mordecai", "Haman", "Gideon"),
                quiz("What position did Esther receive?", "Queen", "Priest", "General"),
                quiz("Who did Esther courageously approach?", "The king", "Goliath", "Pharaoh"),
            ],
            "medium": [
                quiz("Why did Mordecai ask Esther to speak?", "Her people were in danger", "He wanted a royal feast", "The palace needed repairs"),
                quiz("What did Esther ask the people to do first?", "Fast with her", "Leave Persia", "Build an army"),
                quiz("How did the king respond when Esther entered?", "He welcomed her", "He sent her away", "He did not see her"),
            ],
            "hard": [
                quiz("What did 'for such a time as this' help Esther understand?", "Her position could serve God's purpose", "She should hide forever", "She had become more important than others"),
                quiz("What made Esther's leadership courageous?", "She acted for others despite the risk", "She already knew the outcome", "She commanded a large army"),
                quiz("What happened after Esther exposed Haman's plan?", "Her people were rescued", "Haman became king", "Mordecai left Persia"),
            ],
        },
        "quiz_count_by_difficulty": {"easy": 2, "medium": 3, "hard": 3},
        "verse_bank_by_difficulty": {
            "easy": [verse("Who knows if you haven't come to the kingdom for such a time as this?", "Esther 4:14", "Esther 3:14", "Esther 5:14")],
            "medium": [verse("Go, gather all the Jews who are found in Susa, and fast for me.", "Esther 4:16", "Esther 4:6", "Esther 5:16")],
            "hard": [verse("And if I perish, I perish.", "Esther 4:16", "Esther 2:16", "Esther 8:16")],
        },
        "lesson": "Courageous leaders use the place God has given them to protect and serve other people.",
    },

    "jericho": {
        "title": "The Battle of Jericho",
        "intro_scenes": [
            {
                "type": "story",
                "emoji": "🏰",
                "text": "After Israel crossed the Jordan River, the strong city of Jericho stood ahead. Its gates were tightly closed, and its high walls looked impossible to overcome.",
            },
            {
                "type": "story",
                "emoji": "📣",
                "text": "God gave Joshua an unusual plan. The soldiers would march around Jericho with seven priests, seven trumpets, and the ark of the covenant.",
            },
            {
                "type": "story",
                "emoji": "🤫",
                "text": "For six days, the people marched around the city once each day. They obeyed Joshua and stayed quiet while the priests blew their trumpets.",
            },
        ],
        "outro_scenes": [
            {
                "type": "story",
                "emoji": "7️⃣",
                "text": "On the seventh day, Israel marched around Jericho seven times. At the end of the seventh trip, the priests gave a long trumpet blast.",
            },
            {
                "type": "story",
                "emoji": "🎺",
                "text": "Joshua told the people to shout because God had given them the city. The people shouted, and the walls of Jericho fell down.",
            },
            {
                "type": "story",
                "emoji": "❤️",
                "text": "Joshua kept the spies' promise and rescued Rahab and her family. Israel learned that faith means trusting and following God's instructions.",
            },
        ],
        "interactive_by_difficulty": {
            "easy": matching("Gather the important parts of God's Jericho plan!", [
                ("people", "👣", "Marching people"),
                ("trumpets", "🎺", "Priests' trumpets"),
                ("shout", "📣", "The final shout"),
            ]),
            "medium": sequence("Put the seventh day's events in order!", [
                ("march", "👣", "March seven times"),
                ("blast", "🎺", "Priests blow the trumpets"),
                ("command", "📣", "Joshua gives the command"),
                ("shout", "🗣️", "The people shout"),
                ("walls", "🏰", "The walls fall"),
            ]),
            "hard": sequence("Arrange the complete Jericho story!", [
                ("city", "🏰", "Jericho is tightly closed"),
                ("plan", "📣", "God gives Joshua a plan"),
                ("six", "6️⃣", "Israel marches for six days"),
                ("seven", "7️⃣", "They circle seven times"),
                ("trumpets", "🎺", "The trumpets sound"),
                ("shout", "🗣️", "The people shout"),
                ("rahab", "❤️", "Rahab's family is rescued"),
            ]),
        },
        "quiz_bank_by_difficulty": {
            "easy": [
                quiz("Who led Israel at Jericho?", "Joshua", "Goliath", "Haman"),
                quiz("What happened when the people shouted?", "The walls fell", "The river parted", "A storm began"),
                quiz("Whose family was rescued?", "Rahab's family", "Goliath's family", "Haman's family"),
            ],
            "medium": [
                quiz("How many days did Israel march around Jericho?", "Seven days", "Three days", "Forty days"),
                quiz("How many times did they march on the seventh day?", "Seven times", "One time", "Twelve times"),
                quiz("Why did Israel follow such an unusual plan?", "They trusted and obeyed God", "They had no leader", "They wanted to practice marching"),
            ],
            "hard": [
                quiz("What did the ark represent among the marching people?", "God's presence with Israel", "Joshua's treasure", "A weapon made by the soldiers"),
                quiz("What did Hebrews say caused Jericho's walls to fall?", "Faith", "A giant hammer", "An earthquake predicted by Joshua"),
                quiz("How did Joshua show faithful leadership?", "He followed God's plan and kept the promise to Rahab", "He changed the plan each day", "He entered the city alone"),
            ],
        },
        "quiz_count_by_difficulty": {"easy": 2, "medium": 3, "hard": 3},
        "verse_bank_by_difficulty": {
            "easy": [verse("Shout, for Yahweh has given you the city!", "Joshua 6:16", "Joshua 5:16", "Judges 6:16")],
            "medium": [verse("By faith the walls of Jericho fell down after they had been encircled for seven days.", "Hebrews 11:30", "Hebrews 10:30", "Joshua 11:30")],
            "hard": [verse("Behold, I have given Jericho into your hand, with its king and the mighty men of valor.", "Joshua 6:2", "Joshua 2:6", "Judges 6:2")],
        },
        "lesson": "Faithful leadership listens to God, follows His instructions, and keeps promises to other people.",
    },
}
