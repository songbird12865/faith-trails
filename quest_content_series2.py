"""Playable content for Faith-Trails Series 2: Family & Trust."""


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


def quiz(prompt, correct, *incorrect):
    """Create a multiple-choice question with the correct answer first."""
    return {
        "type": "quiz",
        "prompt": prompt,
        "options": [correct, *incorrect],
        "correct_index": 0,
    }


def verse(text, reference, *other_references):
    """Create a memory-verse activity with reference choices."""
    return {
        "type": "memory_verse",
        "verse": text,
        "reference": reference,
        "reference_options": [reference, *other_references],
    }


SERIES_2_CONTENT = {
    "abraham": {
        "title": "Abraham",
        "intro_scenes": [
            {
                "type": "story",
                "emoji": "🏕️",
                "text": "God told Abram to leave his home and travel to a land that God would show him. Abram obeyed, even though he did not know every step ahead.",
            },
            {
                "type": "story",
                "emoji": "🌍",
                "text": "God promised to make Abram's family into a great nation and to bless all the families of the earth through him.",
            },
            {
                "type": "story",
                "emoji": "⭐",
                "text": "Years passed, and Abram and Sarai still had no child. God took Abram outside and told him to look at the stars. His family would one day be too great to count.",
            },
        ],
        "interactive_by_difficulty": {
            "easy": sequence("Put these moments from Abraham's journey in order!", [
                ("call", "👣", "God calls Abram"),
                ("stars", "⭐", "God shows him the stars"),
                ("isaac", "👶", "Isaac is born"),
            ]),
            "medium": sequence("Arrange these promises and events in order!", [
                ("leave", "🏕️", "Abram leaves home"),
                ("land", "🗺️", "God leads him to a new land"),
                ("stars", "⭐", "God promises a great family"),
                ("believe", "🙏", "Abram believes God"),
                ("isaac", "👶", "Isaac is born"),
            ]),
            "hard": sequence("Build Abraham's trust journey in its full order!", [
                ("call", "📣", "God calls Abram"),
                ("obey", "👣", "Abram obeys and travels"),
                ("promise", "🌍", "God promises blessing"),
                ("wait", "⌛", "Abram and Sarai wait"),
                ("stars", "⭐", "God renews His promise"),
                ("faith", "🙏", "Abram believes the LORD"),
                ("isaac", "👶", "God gives them Isaac"),
            ]),
        },
        "outro_scenes": [
            {
                "type": "story",
                "emoji": "🙏",
                "text": "Abram believed the LORD. God later gave him the name Abraham, meaning that he would become the father of many nations.",
            },
            {
                "type": "story",
                "emoji": "👶",
                "text": "At God's appointed time, Sarah gave birth to Isaac. What seemed impossible became possible because God kept His promise.",
            },
        ],
        "quiz_bank_by_difficulty": {
            "easy": [
                quiz("Who told Abram to leave his home?", "God", "Pharaoh", "Isaac"),
                quiz("What did God tell Abram to count?", "The stars", "The tents", "The sheep"),
                quiz("What was the name of Abraham and Sarah's son?", "Isaac", "Jacob", "Samuel"),
            ],
            "medium": [
                quiz("Why did Abram begin his journey?", "He trusted and obeyed God", "He was following a map", "He wanted to become a king"),
                quiz("What did the stars represent?", "The great family God promised", "The distance to Egypt", "The number of Abram's servants"),
                quiz("What new name did God give Abram?", "Abraham", "Israel", "Benjamin"),
            ],
            "hard": [
                quiz("What does Abraham's waiting teach us?", "God remains faithful even when His promise takes time", "God forgets promises that take too long", "People should never ask God questions"),
                quiz("How would Abraham's family bless the world?", "God's saving plan would come through his family", "They would own every nation", "They would build the largest city"),
                quiz("Why was Isaac's birth remarkable?", "Abraham and Sarah were very old", "Isaac was born in a palace", "No one had promised his birth"),
            ],
        },
        "quiz_count_by_difficulty": {"easy": 2, "medium": 3, "hard": 3},
        "verse_bank_by_difficulty": {
            "easy": [verse("He believed in the LORD.", "Genesis 15:6", "Genesis 12:6", "Exodus 15:6")],
            "medium": [verse("He believed in the LORD, who credited it to him for righteousness.", "Genesis 15:6", "Genesis 15:16", "Hebrews 15:6")],
            "hard": [verse("He believed in the LORD, who credited it to him for righteousness.", "Genesis 15:6", "Genesis 12:3", "Romans 15:6")],
        },
        "lesson": "We can trust God while we wait because He always keeps His promises.",
    },

    "jacob": {
        "title": "Jacob",
        "intro_scenes": [
            {
                "type": "story",
                "emoji": "🏃",
                "text": "Jacob had made selfish choices that hurt his brother Esau. He left home frightened and uncertain about his future.",
            },
            {
                "type": "story",
                "emoji": "🪨",
                "text": "One night, Jacob rested his head on a stone and dreamed of a stairway reaching from earth to heaven, with God's angels going up and down.",
            },
            {
                "type": "story",
                "emoji": "🪜",
                "text": "God promised to be with Jacob, protect him wherever he went, and bring him home again. Jacob named the place Bethel, which means House of God.",
            },
        ],
        "interactive_by_difficulty": {
            "easy": sequence("Put these moments from Jacob's journey in order!", [
                ("leave", "🏃", "Jacob leaves home"),
                ("dream", "🪜", "Jacob sees the stairway"),
                ("return", "🤝", "Jacob and Esau meet again"),
            ]),
            "medium": sequence("Arrange Jacob's journey home!", [
                ("leave", "🏃", "Jacob leaves home"),
                ("promise", "🪜", "God promises to be with him"),
                ("family", "🏕️", "Jacob grows a large family"),
                ("pray", "🙏", "Jacob prays before meeting Esau"),
                ("embrace", "🤝", "Esau welcomes Jacob"),
            ]),
            "hard": sequence("Put Jacob's changing-life moments in order!", [
                ("wrong", "💔", "Jacob's choices hurt Esau"),
                ("flee", "🏃", "Jacob leaves home"),
                ("bethel", "🪜", "God speaks at Bethel"),
                ("years", "⌛", "Many years pass"),
                ("fear", "😟", "Jacob fears meeting Esau"),
                ("israel", "🌅", "God gives Jacob the name Israel"),
                ("peace", "🤝", "The brothers meet in peace"),
            ]),
        },
        "outro_scenes": [
            {
                "type": "story",
                "emoji": "🙏",
                "text": "Many years later, God told Jacob to return home. Jacob was afraid Esau might still be angry, so he prayed and asked God for help.",
            },
            {
                "type": "story",
                "emoji": "🌅",
                "text": "During the night, Jacob wrestled until daybreak and received a new name: Israel. His new name marked a changed life under God's blessing.",
            },
            {
                "type": "story",
                "emoji": "🤝",
                "text": "When Esau saw Jacob, he ran to meet him and embraced him. God had protected Jacob, brought him home, and opened the way for peace.",
            },
        ],
        "quiz_bank_by_difficulty": {
            "easy": [
                quiz("What did Jacob see in his dream?", "A stairway reaching to heaven", "A giant boat", "A burning bush"),
                quiz("What did God promise Jacob?", "To be with him", "To make him a king that night", "To keep him away from home forever"),
                quiz("Who welcomed Jacob when he returned?", "His brother Esau", "Pharaoh", "Samuel"),
            ],
            "medium": [
                quiz("Why was Jacob afraid to return home?", "His choices had hurt Esau", "He had forgotten the road", "He had lost all his animals"),
                quiz("What did Jacob do before meeting Esau?", "He prayed for God's help", "He built a tower", "He returned to Bethel alone"),
                quiz("What new name did Jacob receive?", "Israel", "Abraham", "Judah"),
            ],
            "hard": [
                quiz("What did Jacob's new name represent in this story?", "A changed life under God's blessing", "A secret name to hide from Esau", "A title that made him king"),
                quiz("How did God fulfill His Bethel promise?", "He stayed with Jacob and brought him home", "He kept Jacob from ever facing Esau", "He made Jacob's journey easy"),
                quiz("What does the reunion with Esau show?", "God can help restore damaged relationships", "Wrong choices never have consequences", "Jacob no longer needed God"),
            ],
        },
        "quiz_count_by_difficulty": {"easy": 2, "medium": 3, "hard": 3},
        "verse_bank_by_difficulty": {
            "easy": [verse("Behold, I am with you.", "Genesis 28:15", "Genesis 18:15", "Exodus 28:15")],
            "medium": [verse("Behold, I am with you, and will keep you, wherever you go.", "Genesis 28:15", "Genesis 28:5", "Psalm 28:15")],
            "hard": [verse("Behold, I am with you, and will keep you, wherever you go, and will bring you again into this land. For I will not leave you until I have done that which I have spoken of to you.", "Genesis 28:15", "Genesis 32:28", "Deuteronomy 28:15")],
        },
        "lesson": "God stays with us, changes our hearts, and helps us make peace when we have done wrong.",
    },

    "ruth": {
        "title": "Ruth",
        "intro_scenes": [
            {
                "type": "story",
                "emoji": "😢",
                "text": "Naomi had lost her husband and her sons in the land of Moab. She decided to return to Bethlehem, but she told her daughters-in-law to remain with their families.",
            },
            {
                "type": "story",
                "emoji": "❤️",
                "text": "Ruth would not abandon Naomi. She promised to go wherever Naomi went and said, 'Your people will be my people, and your God my God.'",
            },
            {
                "type": "story",
                "emoji": "🌾",
                "text": "In Bethlehem, Ruth gathered leftover grain so she and Naomi would have food. She worked faithfully in a field belonging to a kind man named Boaz.",
            },
        ],
        "interactive_by_difficulty": {
            "easy": sequence("Put Ruth's acts of love in order!", [
                ("stay", "❤️", "Ruth stays with Naomi"),
                ("glean", "🌾", "Ruth gathers grain"),
                ("family", "👶", "Ruth's family brings Naomi joy"),
            ]),
            "medium": sequence("Arrange Ruth and Naomi's new beginning!", [
                ("return", "👣", "Naomi returns to Bethlehem"),
                ("promise", "❤️", "Ruth promises to stay"),
                ("work", "🌾", "Ruth works in the fields"),
                ("kindness", "🤲", "Boaz protects and helps Ruth"),
                ("obed", "👶", "Obed is born"),
            ]),
            "hard": sequence("Put the full story of faithfulness in order!", [
                ("loss", "😢", "Naomi's family suffers loss"),
                ("bethlehem", "👣", "Naomi heads to Bethlehem"),
                ("loyalty", "❤️", "Ruth chooses Naomi and God"),
                ("glean", "🌾", "Ruth gleans in Boaz's field"),
                ("refuge", "🕊️", "Boaz praises Ruth's faith"),
                ("redeem", "🤝", "Boaz becomes family redeemer"),
                ("line", "👑", "Their family leads toward King David"),
            ]),
        },
        "outro_scenes": [
            {
                "type": "story",
                "emoji": "🤲",
                "text": "Boaz had heard how faithfully Ruth cared for Naomi. He protected her and made sure she could gather plenty of grain.",
            },
            {
                "type": "story",
                "emoji": "🕊️",
                "text": "Boaz said Ruth had come to take refuge under the wings of the LORD. In time, Boaz married Ruth and welcomed her into his family.",
            },
            {
                "type": "story",
                "emoji": "👑",
                "text": "Ruth and Boaz had a son named Obed. Obed became the grandfather of King David, and Ruth became part of the family line that would lead to Jesus.",
            },
        ],
        "quiz_bank_by_difficulty": {
            "easy": [
                quiz("Who did Ruth promise to stay with?", "Naomi", "Sarah", "Esther"),
                quiz("What did Ruth gather in the field?", "Grain", "Fish", "Stones"),
                quiz("Who showed kindness to Ruth?", "Boaz", "Pharaoh", "Goliath"),
            ],
            "medium": [
                quiz("Why did Ruth go to Bethlehem?", "She chose to remain with Naomi", "She wanted to become queen", "She was looking for Moses"),
                quiz("How did Ruth provide food?", "She gathered leftover grain", "She sold jewelry", "She owned a large farm"),
                quiz("What did Boaz admire about Ruth?", "Her faithful care for Naomi", "Her royal clothing", "Her great wealth"),
            ],
            "hard": [
                quiz("What did Ruth mean by choosing Naomi's God?", "She placed her faith in the God of Israel", "She planned to return to Moab", "She wanted Boaz's land"),
                quiz("How did Boaz act as a family redeemer?", "He protected the family's future and married Ruth", "He sent Ruth away", "He made Naomi work for him"),
                quiz("Why is Ruth's family important later in the Bible?", "Her family line leads to David and Jesus", "Her family built the temple", "Her family ruled Egypt"),
            ],
        },
        "quiz_count_by_difficulty": {"easy": 2, "medium": 3, "hard": 3},
        "verse_bank_by_difficulty": {
            "easy": [verse("Where you go, I will go.", "Ruth 1:16", "Ruth 2:16", "Esther 1:16")],
            "medium": [verse("Where you go, I will go; and where you stay, I will stay.", "Ruth 1:16", "Ruth 1:6", "Ruth 4:16")],
            "hard": [verse("Don't urge me to leave you, and to return from following you, for where you go, I will go; and where you stay, I will stay. Your people will be my people, and your God my God.", "Ruth 1:16", "Ruth 2:12", "Ruth 4:14")],
        },
        "lesson": "Faithful love stays, serves, and trusts that God can create a new beginning.",
    },

    "samuel": {
        "title": "Samuel",
        "intro_scenes": [
            {
                "type": "story",
                "emoji": "🙏",
                "text": "Hannah prayed for a child and promised to dedicate him to the LORD. God answered her prayer, and she named her son Samuel.",
            },
            {
                "type": "story",
                "emoji": "🕯️",
                "text": "While Samuel was still young, he served God at the tabernacle under the priest Eli. One night, as Samuel lay down, he heard someone call his name.",
            },
            {
                "type": "story",
                "emoji": "👂",
                "text": "Samuel ran to Eli and said, 'Here I am.' But Eli had not called him. This happened three times before Eli understood that the LORD was calling Samuel.",
            },
        ],
        "interactive_by_difficulty": {
            "easy": sequence("Put Samuel's nighttime answers in order!", [
                ("call", "📣", "Samuel hears his name"),
                ("eli", "🏃", "Samuel runs to Eli"),
                ("listen", "👂", "Samuel listens to God"),
            ]),
            "medium": sequence("Arrange the night God called Samuel!", [
                ("sleep", "🌙", "Samuel lies down"),
                ("voice", "📣", "A voice calls Samuel"),
                ("run", "🏃", "Samuel runs to Eli"),
                ("teach", "🕯️", "Eli explains who is calling"),
                ("answer", "👂", "Samuel answers the LORD"),
            ]),
            "hard": sequence("Put Samuel's call and response in exact order!", [
                ("serve", "🕯️", "Samuel serves at the tabernacle"),
                ("first", "1️⃣", "The LORD calls the first time"),
                ("second", "2️⃣", "The LORD calls the second time"),
                ("third", "3️⃣", "The LORD calls the third time"),
                ("understand", "💡", "Eli understands"),
                ("fourth", "📣", "The LORD calls again"),
                ("respond", "👂", "Samuel listens and responds"),
            ]),
        },
        "outro_scenes": [
            {
                "type": "story",
                "emoji": "🕯️",
                "text": "Eli told Samuel that if the voice called again, he should say, 'Speak, LORD; for your servant hears.'",
            },
            {
                "type": "story",
                "emoji": "📣",
                "text": "The LORD called, 'Samuel! Samuel!' Samuel listened and answered. God gave him a message that required courage to share truthfully.",
            },
            {
                "type": "story",
                "emoji": "🌱",
                "text": "Samuel grew, and the LORD was with him. All Israel came to recognize that God had established Samuel as His prophet.",
            },
        ],
        "quiz_bank_by_difficulty": {
            "easy": [
                quiz("Who called Samuel during the night?", "The LORD", "David", "Moses"),
                quiz("Who did Samuel run to first?", "Eli", "Hannah", "Saul"),
                quiz("What did Samuel do when God called?", "He listened", "He hid", "He left the tabernacle"),
            ],
            "medium": [
                quiz("Why did Samuel keep running to Eli?", "He thought Eli was calling him", "He wanted a lamp", "He was afraid of the dark"),
                quiz("What did Eli finally understand?", "The LORD was calling Samuel", "Hannah had returned", "The lamp had gone out"),
                quiz("What answer did Eli teach Samuel?", "Speak, LORD; for your servant hears", "Please call again tomorrow", "I already know the message"),
            ],
            "hard": [
                quiz("What showed that Samuel was willing to serve?", "He listened and truthfully delivered God's message", "He demanded to become priest", "He refused to speak to Eli"),
                quiz("What happened as Samuel grew?", "The LORD was with him", "He returned permanently to Hannah", "He became king of Egypt"),
                quiz("What can we learn from Eli's role?", "Wise helpers can teach us to recognize and answer God", "Only adults can hear God", "Samuel did not need guidance"),
            ],
        },
        "quiz_count_by_difficulty": {"easy": 2, "medium": 3, "hard": 3},
        "verse_bank_by_difficulty": {
            "easy": [verse("Speak; for your servant hears.", "1 Samuel 3:10", "1 Samuel 3:1", "2 Samuel 3:10")],
            "medium": [verse("Speak; for your servant hears.", "1 Samuel 3:10", "1 Samuel 3:19", "1 Kings 3:10")],
            "hard": [verse("The LORD came, and stood, and called as at other times, 'Samuel! Samuel!' Then Samuel said, 'Speak; for your servant hears.'", "1 Samuel 3:10", "1 Samuel 3:9", "1 Samuel 3:20")],
        },
        "lesson": "God calls us to listen, respond, and faithfully share the truth He gives us.",
    },
}
