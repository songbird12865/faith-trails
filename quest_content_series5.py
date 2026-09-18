"""Playable content for Faith-Trails Series 5: Jesus & the Good News."""


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
    """Create a project-owner-approved memory-verse activity."""
    return {
        "type": "memory_verse",
        "verse": text,
        "reference": reference,
        "reference_options": [reference, *other_references],
    }


SERIES_5_CONTENT = {
    "nativity": {
        "title": "The Nativity",
        "intro_scenes": [
            {
                "type": "story",
                "emoji": "👼",
                "text": "God sent the angel Gabriel to Mary in Nazareth. Gabriel told her that she would give birth to Jesus, God's promised Son.",
            },
            {
                "type": "story",
                "emoji": "💭",
                "text": "An angel also spoke to Joseph in a dream. Joseph trusted God, took Mary as his wife, and prepared to care for Jesus.",
            },
            {
                "type": "story",
                "emoji": "🐴",
                "text": "Mary and Joseph traveled to Bethlehem for the census. The town was crowded, and there was no guest room available for them.",
            },
        ],
        "outro_scenes": [
            {
                "type": "story",
                "emoji": "👶",
                "text": "Jesus was born in Bethlehem. Mary wrapped Him in cloths and laid Him in a manger, because there was no room in the inn.",
            },
            {
                "type": "story",
                "emoji": "✨",
                "text": "Angels appeared to shepherds in nearby fields. They announced good news of great joy: a Savior, Christ the Lord, had been born.",
            },
            {
                "type": "story",
                "emoji": "🐑",
                "text": "The shepherds hurried to Bethlehem and found Mary, Joseph, and Jesus. They praised God and told others everything the angel had said.",
            },
        ],
        "interactive_by_difficulty": {
            "easy": matching("Gather the people and signs from Jesus' birth!", [
                ("mary", "👩", "Mary"),
                ("joseph", "🧔", "Joseph"),
                ("baby", "👶", "Baby Jesus"),
                ("shepherds", "🐑", "Shepherds"),
            ]),
            "medium": sequence("Put the Nativity events in order!", [
                ("promise", "👼", "Gabriel visits Mary"),
                ("dream", "💭", "Joseph trusts God's message"),
                ("journey", "🐴", "They travel to Bethlehem"),
                ("birth", "👶", "Jesus is born"),
                ("news", "✨", "Angels tell the shepherds"),
                ("visit", "🐑", "Shepherds visit Jesus"),
            ]),
            "hard": sequence("Arrange the complete Nativity journey!", [
                ("gabriel", "👼", "Gabriel announces God's promise"),
                ("joseph", "💭", "Joseph obeys after his dream"),
                ("bethlehem", "🛤️", "Mary and Joseph reach Bethlehem"),
                ("manger", "👶", "Jesus is laid in a manger"),
                ("angels", "✨", "Heaven announces the Savior"),
                ("shepherds", "🐑", "Shepherds find the child"),
                ("witness", "📣", "Shepherds share the good news"),
            ]),
        },
        "quiz_bank_by_difficulty": {
            "easy": [
                quiz("Where was Jesus born?", "Bethlehem", "Jericho", "Nineveh"),
                quiz("Who heard the angels' good news?", "Shepherds", "Sailors", "Soldiers"),
                quiz("Where did Mary lay baby Jesus?", "In a manger", "On a throne", "In a boat"),
            ],
            "medium": [
                quiz("Why did Mary and Joseph travel to Bethlehem?", "For the census", "To meet a king", "To buy a field"),
                quiz("What title did the angel give Jesus?", "Savior, Christ the Lord", "Governor of Rome", "Captain of Israel"),
                quiz("What did the shepherds do after seeing Jesus?", "Praised God and shared the news", "Kept it completely secret", "Returned to sleep without speaking"),
            ],
            "hard": [
                quiz("How does the Nativity show God's faithfulness?", "God fulfilled His promise to send the Savior", "God made Bethlehem wealthy", "God removed every difficult journey"),
                quiz("Why is the angels' message called good news for all people?", "Jesus came as the promised Savior", "Only shepherds could receive it", "It announced a new Roman ruler"),
                quiz("What faithful response did Mary and Joseph share?", "They trusted and obeyed God's word", "They demanded every detail first", "They stayed in Nazareth"),
            ],
        },
        "quiz_count_by_difficulty": {"easy": 2, "medium": 3, "hard": 3},
        "verse_bank_by_difficulty": {
            "easy": [verse("Glory to God in the Highest.", "Luke 2:14", "Luke 2:4", "Luke 12:14")],
            "medium": [verse("Let's go to Bethlehem, now, and see this thing that has happened.", "Luke 2:15", "Luke 2:5", "Luke 12:15")],
            "hard": [verse("For there is born to you today, in David's city, a Savior, who is Christ the Lord.", "Luke 2:11", "Luke 2:21", "Luke 12:11")],
        },
        "lesson": "Jesus' birth is good news of great joy: God kept His promise and sent the Savior for all people.",
    },

    "beatitudes": {
        "title": "Jesus' Teachings: The Beatitudes",
        "intro_scenes": [
            {
                "type": "story",
                "emoji": "⛰️",
                "text": "Crowds followed Jesus, so He went up on a mountain and sat down. His disciples came close, and Jesus began to teach them.",
            },
            {
                "type": "story",
                "emoji": "🙏",
                "text": "Jesus said the poor in spirit are blessed because the Kingdom of Heaven is theirs. We depend on God instead of pretending we need nothing.",
            },
            {
                "type": "story",
                "emoji": "🤍",
                "text": "Jesus said those who mourn will be comforted, and the gentle will inherit the earth. God sees sadness and honors humble strength.",
            },
        ],
        "outro_scenes": [
            {
                "type": "story",
                "emoji": "⚖️",
                "text": "Those who hunger and thirst for righteousness will be filled. Jesus teaches us to deeply desire what is right in God's eyes.",
            },
            {
                "type": "story",
                "emoji": "🕊️",
                "text": "The merciful, the pure in heart, and the peacemakers are blessed. God's children show compassion, seek honest hearts, and help people live in peace.",
            },
            {
                "type": "story",
                "emoji": "💡",
                "text": "Jesus said His followers are the light of the world. Even when doing right is difficult, our loving actions can point other people toward God.",
            },
        ],
        "interactive_by_difficulty": {
            "easy": matching("Choose the attitudes Jesus calls blessed!", [
                ("gentle", "🤍", "Be gentle"),
                ("mercy", "❤️", "Show mercy"),
                ("peace", "🕊️", "Make peace"),
                ("right", "⚖️", "Want what is right"),
            ]),
            "medium": matching("Match each Beatitude with a way to live it!", [
                ("depend", "🙏", "Depend on God"),
                ("comfort", "🤗", "Comfort someone who is sad"),
                ("mercy", "❤️", "Forgive and help"),
                ("pure", "✨", "Choose an honest heart"),
                ("peace", "🕊️", "Help people reconcile"),
                ("light", "💡", "Let good works point to God"),
            ]),
            "hard": sequence("Build Jesus' picture of Kingdom character!", [
                ("humble", "🙏", "Depend humbly on God"),
                ("comfort", "🤍", "Receive God's comfort"),
                ("gentle", "🌿", "Practice gentle strength"),
                ("righteous", "⚖️", "Long for righteousness"),
                ("merciful", "❤️", "Give mercy"),
                ("pure", "✨", "Seek a pure heart"),
                ("peace", "🕊️", "Make peace"),
                ("shine", "💡", "Shine through faithful actions"),
            ]),
        },
        "quiz_bank_by_difficulty": {
            "easy": [
                quiz("Where did Jesus teach the Beatitudes?", "On a mountain", "Inside a palace", "On a ship"),
                quiz("Who will be called children of God?", "Peacemakers", "Treasure hunters", "Roman soldiers"),
                quiz("What should Jesus' followers shine like?", "A light", "A crown", "A sword"),
            ],
            "medium": [
                quiz("What does it mean to hunger and thirst for righteousness?", "To deeply desire what is right", "To collect more food", "To avoid helping others"),
                quiz("What does a merciful person do?", "Shows compassion and forgiveness", "Keeps every mistake remembered", "Only helps close friends"),
                quiz("Why should believers let their light shine?", "So good works point people to God", "So everyone praises them", "So they never face hardship"),
            ],
            "hard": [
                quiz("Why are the Beatitudes surprising?", "They call humble, merciful, faithful people truly blessed", "They promise wealth to every disciple", "They honor only powerful leaders"),
                quiz("How is biblical gentleness different from weakness?", "It is humble strength guided by God", "It means never speaking", "It avoids every hard choice"),
                quiz("What connects the Beatitudes to God's Kingdom?", "They describe character shaped by trusting God", "They list jobs for Israel's army", "They replace love with achievement"),
            ],
        },
        "quiz_count_by_difficulty": {"easy": 2, "medium": 3, "hard": 3},
        "verse_bank_by_difficulty": {
            "easy": [verse("You are the salt of the earth.", "Matthew 5:13", "Matthew 5:3", "Matthew 13:5")],
            "medium": [verse("Blessed are the merciful, for they shall obtain mercy.", "Matthew 5:7", "Matthew 5:17", "Matthew 7:5")],
            "hard": [verse("Even so, let your light shine before men, that they may see your good works.", "Matthew 5:16", "Matthew 5:6", "Matthew 16:5")],
        },
        "lesson": "Jesus calls us blessed when we depend on God and live with righteousness, mercy, pure hearts, and peace.",
    },

    "good-samaritan": {
        "title": "The Good Samaritan",
        "intro_scenes": [
            {
                "type": "story",
                "emoji": "❓",
                "text": "A lawyer asked Jesus what he should do to inherit eternal life. Jesus helped him remember God's commands to love God and love his neighbor.",
            },
            {
                "type": "story",
                "emoji": "🛤️",
                "text": "When the man asked, 'Who is my neighbor?' Jesus told a story. A traveler was attacked on the road from Jerusalem to Jericho and left badly hurt.",
            },
            {
                "type": "story",
                "emoji": "🚶",
                "text": "A priest saw the injured man but passed by on the other side. Later a Levite also saw him and passed by without helping.",
            },
        ],
        "outro_scenes": [
            {
                "type": "story",
                "emoji": "❤️",
                "text": "Then a Samaritan came near. Although Samaritans and Jews often treated each other as enemies, he was moved with compassion.",
            },
            {
                "type": "story",
                "emoji": "🩹",
                "text": "The Samaritan bandaged the man's wounds, placed him on his own animal, brought him to an inn, and cared for him.",
            },
            {
                "type": "story",
                "emoji": "🤝",
                "text": "He paid the innkeeper to continue the care. Jesus asked who acted like a neighbor. The lawyer answered, 'The one who showed mercy,' and Jesus said, 'Go and do likewise.'",
            },
        ],
        "interactive_by_difficulty": {
            "easy": matching("Gather the caring choices the Samaritan made!", [
                ("stop", "🛑", "He stopped"),
                ("bandage", "🩹", "He bandaged wounds"),
                ("carry", "🐴", "He carried the man"),
                ("care", "🏠", "He found continued care"),
            ]),
            "medium": sequence("Put the Good Samaritan story in order!", [
                ("hurt", "🛤️", "A traveler is hurt"),
                ("priest", "🚶", "A priest passes by"),
                ("levite", "🚶", "A Levite passes by"),
                ("compassion", "❤️", "A Samaritan stops"),
                ("inn", "🏠", "He brings the man to an inn"),
                ("mercy", "🤝", "Jesus says to show mercy"),
            ]),
            "hard": sequence("Arrange the lesson from question to faithful action!", [
                ("question", "❓", "The lawyer asks about eternal life"),
                ("command", "📖", "Love God and your neighbor"),
                ("danger", "🛤️", "A traveler needs help"),
                ("avoid", "🚶", "Two religious men pass by"),
                ("compassion", "❤️", "The Samaritan draws near"),
                ("sacrifice", "🩹", "He gives time, care, and money"),
                ("likewise", "🤝", "Jesus calls us to active mercy"),
            ]),
        },
        "quiz_bank_by_difficulty": {
            "easy": [
                quiz("Who stopped to help the injured man?", "A Samaritan", "A king", "A fisherman"),
                quiz("Where did the Samaritan take the man?", "To an inn", "To a palace", "To a boat"),
                quiz("What did Jesus say to do?", "Go and do likewise", "Walk away quickly", "Help only friends"),
            ],
            "medium": [
                quiz("Why was the Samaritan's help surprising?", "His people and the injured man's people were often enemies", "He owned the road", "He was the man's brother"),
                quiz("What moved the Samaritan to act?", "Compassion", "A reward", "Fear of the priest"),
                quiz("Who acted as a true neighbor?", "The one who showed mercy", "The first person to see the man", "The person with the highest title"),
            ],
            "hard": [
                quiz("How did Jesus redefine the lawyer's question about a neighbor?", "He focused on becoming a merciful neighbor", "He limited neighbors to one community", "He said knowledge alone was enough"),
                quiz("What made the Samaritan's mercy costly?", "He gave time, supplies, transportation, and money", "He only offered advice", "He asked the injured man to pay first"),
                quiz("What does this parable teach about loving enemies?", "Compassion crosses social and religious barriers", "Mercy belongs only within our group", "We should wait until helping feels easy"),
            ],
        },
        "quiz_count_by_difficulty": {"easy": 2, "medium": 3, "hard": 3},
        "verse_bank_by_difficulty": {
            "easy": [verse("Go and do likewise.", "Luke 10:37", "Luke 10:27", "Luke 7:10")],
            "medium": [verse("Now which of these three do you think seemed to be a good neighbor?", "Luke 10:36", "Luke 10:26", "Luke 16:10")],
            "hard": [verse("You shall love the Lord your God with all your heart, with all your soul, with all your strength, and with all your mind.", "Luke 10:27", "Luke 10:37", "Luke 20:17")],
        },
        "lesson": "A neighbor is someone who draws near with compassion. Jesus calls us to show practical mercy, even across barriers.",
    },

    "feeding-5000": {
        "title": "Feeding the 5,000",
        "intro_scenes": [
            {
                "type": "story",
                "emoji": "👥",
                "text": "A great crowd followed Jesus because they had seen Him heal the sick. Jesus welcomed them and taught them about God's Kingdom.",
            },
            {
                "type": "story",
                "emoji": "🌄",
                "text": "As the day grew late, the disciples worried about feeding everyone. Jesus already knew what He would do and invited them to trust Him.",
            },
            {
                "type": "story",
                "emoji": "🧺",
                "text": "Andrew found a boy who had five barley loaves and two fish. It looked far too small for a crowd of about five thousand people.",
            },
        ],
        "outro_scenes": [
            {
                "type": "story",
                "emoji": "🙏",
                "text": "Jesus told the people to sit down on the grass. He took the loaves, gave thanks to God, and began distributing the food.",
            },
            {
                "type": "story",
                "emoji": "🐟",
                "text": "Jesus also shared the two fish. Everyone received as much as they wanted, and the entire crowd ate until they were satisfied.",
            },
            {
                "type": "story",
                "emoji": "🧺",
                "text": "Jesus told the disciples to gather what remained so nothing would be wasted. They filled twelve baskets with leftover pieces from the loaves and the fish.",
            },
        ],
        "interactive_by_difficulty": {
            "easy": matching("Gather what was part of Jesus' miracle!", [
                ("loaves", "🍞", "Five loaves"),
                ("fish", "🐟", "Two fish"),
                ("people", "👥", "A large crowd"),
                ("baskets", "🧺", "Twelve baskets left"),
            ]),
            "medium": sequence("Put the feeding miracle in order!", [
                ("crowd", "👥", "The crowd follows Jesus"),
                ("need", "🌄", "The disciples see a need"),
                ("lunch", "🧺", "A boy offers five loaves and two fish"),
                ("thanks", "🙏", "Jesus gives thanks"),
                ("eat", "🐟", "Everyone eats enough"),
                ("leftovers", "🧺", "Twelve baskets remain"),
            ]),
            "hard": sequence("Arrange the complete lesson of trust and provision!", [
                ("welcome", "👥", "Jesus welcomes and teaches the crowd"),
                ("question", "❓", "Jesus tests the disciples' faith"),
                ("small", "🧺", "A small lunch is brought"),
                ("seat", "🌿", "The people sit on the grass"),
                ("gratitude", "🙏", "Jesus thanks the Father"),
                ("abundance", "🐟", "Everyone receives enough"),
                ("stewardship", "🧺", "Nothing is wasted"),
            ]),
        },
        "quiz_bank_by_difficulty": {
            "easy": [
                quiz("How many loaves did the boy have?", "Five", "Two", "Twelve"),
                quiz("How many fish did the boy have?", "Two", "Five", "Twelve"),
                quiz("Who multiplied the food?", "Jesus", "Andrew", "The crowd"),
            ],
            "medium": [
                quiz("What did Jesus do before distributing the food?", "He gave thanks", "He sent everyone away", "He counted Roman coins"),
                quiz("How much did the people eat?", "As much as they wanted", "One bite each", "Only the children ate"),
                quiz("How many baskets of pieces remained?", "Twelve", "Five", "Two"),
            ],
            "hard": [
                quiz("Why did Jesus ask Philip where to buy bread?", "To test him, because Jesus knew what He would do", "Because Jesus had no plan", "To send Philip away"),
                quiz("What does gathering the leftovers teach?", "God's abundance should still be handled without waste", "The miracle had failed", "Only leftovers mattered"),
                quiz("What truth did Jesus later teach using bread?", "He is the bread of life", "Bread earns eternal life", "Physical food is all people need"),
            ],
        },
        "quiz_count_by_difficulty": {"easy": 2, "medium": 3, "hard": 3},
        "verse_bank_by_difficulty": {
            "easy": [verse("Jesus said, \"Have the people sit down.\"", "John 6:10", "John 6:1", "John 10:6")],
            "medium": [verse("He who comes to me I will in no way throw out.", "John 6:37", "John 6:27", "John 7:36")],
            "hard": [verse("I am the bread of life. Whoever comes to me will not be hungry.", "John 6:35", "John 5:36", "John 16:5")],
        },
        "lesson": "Jesus cares about people's needs. We can offer what we have, thank God, and trust His abundant provision.",
    },

    "easter": {
        "title": "Easter",
        "intro_scenes": [
            {
                "type": "story",
                "emoji": "🍞",
                "text": "Easter is when we remember our Lord's great love! Mean people called for His arrest. Before His arrest, Jesus shared the Passover meal with His disciples. He gave them bread and a cup of wine to remember His loving sacrifice.",
            },
            {
                "type": "story",
                "emoji": "🙏",
                "text": "Jesus prayed in the garden of Gethsemane and chose to obey the Father. He was arrested, even though He had done nothing wrong.",
            },
            {
                "type": "story",
                "emoji": "✝️",
                "text": "Jesus was crucified and died. His followers grieved, but Jesus gave His life willingly to save us from sin and bring us back to God.",
            },
        ],
        "outro_scenes": [
            {
                "type": "story",
                "emoji": "🪨",
                "text": "Jesus' body was placed in a tomb, and a large stone covered the entrance. His friends believed their hope had ended.",
            },
            {
                "type": "story",
                "emoji": "🌅",
                "text": "On the first day of the week, women came to the tomb and found the stone rolled away. An angel announced, 'He is not here, for He has risen.'",
            },
            {
                "type": "story",
                "emoji": "✨",
                "text": "The risen Jesus appeared to His followers. He told them to share the good news with all nations and promised, 'I am with you always.'",
            },
        ],
        "interactive_by_difficulty": {
            "easy": matching("Gather the signs of the Easter good news!", [
                ("cross", "✝️", "Jesus gave His life"),
                ("stone", "🪨", "The stone was rolled away"),
                ("tomb", "🌅", "The tomb was empty"),
                ("alive", "✨", "Jesus is alive"),
            ]),
            "medium": sequence("Put the Easter story in order!", [
                ("meal", "🍞", "Jesus shares the Last Supper"),
                ("prayer", "🙏", "Jesus prays in Gethsemane"),
                ("cross", "✝️", "Jesus dies on the cross"),
                ("burial", "🪨", "Jesus is placed in a tomb"),
                ("empty", "🌅", "The tomb is found empty"),
                ("risen", "✨", "Jesus appears alive"),
            ]),
            "hard": sequence("Arrange the Easter journey from sacrifice to mission!", [
                ("remember", "🍞", "Jesus explains His sacrifice"),
                ("submit", "🙏", "Jesus obeys the Father"),
                ("sacrifice", "✝️", "Jesus gives His life for sinners"),
                ("sealed", "🪨", "The tomb is closed"),
                ("victory", "🌅", "God raises Jesus from the dead"),
                ("worship", "🙌", "The disciples worship the risen Lord"),
                ("mission", "🌍", "Jesus sends them to all nations"),
            ]),
        },
        "quiz_bank_by_difficulty": {
            "easy": [
                quiz("What did the women find on Easter morning?", "An empty tomb", "A new palace", "A fishing boat"),
                quiz("What happened to Jesus?", "He rose from the dead", "He remained in the tomb", "He traveled to Rome"),
                quiz("Who announced that Jesus had risen?", "An angel", "A Roman emperor", "An innkeeper"),
            ],
            "medium": [
                quiz("Why did Jesus give His life?", "To save us from sin and bring us to God", "To become a Roman king", "To avoid teaching the crowds"),
                quiz("How did the women leave the empty tomb?", "With fear and great joy", "With no message to share", "Believing they were lost"),
                quiz("What did Jesus promise His followers?", "I am with you always", "You will never face trouble", "Stay only in Galilee"),
            ],
            "hard": [
                quiz("What does the resurrection reveal about Jesus' death?", "His loving sacrifice defeated sin and death", "His mission had ended in failure", "The disciples rescued Him"),
                quiz("How did the risen Jesus turn grief into mission?", "He appeared alive and sent His followers to make disciples", "He told everyone to remain silent", "He asked them to rebuild the tomb"),
                quiz("Why is Easter central to the good news?", "Jesus died for our sins and rose in victory", "It celebrates the disciples' courage alone", "It teaches that death had the final word"),
            ],
        },
        "quiz_count_by_difficulty": {"easy": 2, "medium": 3, "hard": 3},
        "verse_bank_by_difficulty": {
            "easy": [verse("He is not here, for he has risen.", "Matthew 28:6", "Matthew 28:16", "Matthew 26:8")],
            "medium": [verse("Go quickly and tell his disciples, 'He is risen from the dead.'", "Matthew 28:7", "Matthew 18:27", "Matthew 27:8")],
            "hard": [verse("Go and make disciples of all nations, baptizing them in the name of the Father, and of the Son, and of the Holy Spirit.", "Matthew 28:19", "Matthew 18:29", "Matthew 19:28")],
        },
        "lesson": "Jesus gave His life for us and rose again. Because He is alive, we have hope and can share His good news.",
    },
}
