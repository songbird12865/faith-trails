"""Age-appropriate alternate story openings and endings for each quest.

Easy retains the approved original script. These scene-specific Medium and Hard
lines keep the existing illustrations and order. Regenerate narration after any
edit to this file; audio filenames are calculated from the exact spoken text.
"""

STORY_VARIANTS = {
    "creation": {
        "medium": {0: "At the beginning of everything, God made the heavens and the earth. The earth was empty and dark, but God was already there, ready to fill His world with life.", -1: "God looked at all He had created and called it very good. On the seventh day He rested, showing that His work of creation was complete."},
        "hard": {0: "Before there were people, animals, plants, or even light, God was there. The earth was dark and empty. Then God began His work of bringing order and life into the world.", -1: "After making the world and its living creatures, God saw that everything was very good. He rested on the seventh day, marking the end of His work of creation."},
    },
    "noahs-ark": {
        "medium": {0: "As people grew more and more unkind, God noticed that Noah still walked with Him. Noah's trust in God would matter when the flood came.", -1: "After the flood, God put a rainbow in the sky. It was the sign of His promise never again to destroy the whole earth with a flood."},
        "hard": {0: "The world had become filled with wrongdoing, but Noah lived differently. He listened to God even when the people around him did not.", -1: "The rainbow reminded Noah of God's covenant after the flood: never again would a flood destroy every living thing on earth. God had remembered Noah and his family."},
    },
    "josephs-coat": {
        "medium": {0: "Jacob gave Joseph a colorful coat to show how much he loved him. That special gift soon caused trouble between Joseph and his brothers.", -1: "In Egypt, Joseph was far from the family he knew. Even when life felt unfair, he could trust that God had not forgotten him."},
        "hard": {0: "Joseph's father Jacob showed him special favor by giving him a beautiful coat. His brothers could see the difference, and jealousy began to grow.", -1: "Being taken to Egypt was frightening and unjust for Joseph. His story did not end there: God was still with him, even in a place he had never planned to go."},
    },
    "red-sea": {
        "medium": {0: "God saw how His people suffered as slaves in Egypt. He planned to bring them out so they could live in freedom.", -1: "Moses lifted his staff as God had told him. God opened a path through the sea, and the Israelites crossed on dry ground before the waters returned."},
        "hard": {0: "For years the Israelites had been held as slaves in Egypt. God heard their suffering and began His plan to rescue them and lead them toward a new land.", -1: "With the sea ahead and danger behind, the people needed a way forward. God parted the waters when Moses raised his staff, and the people crossed safely on dry land."},
    },
    "david-goliath": {
        "medium": {0: "Every day Goliath challenged Israel's army, and the soldiers were too afraid to face him. The giant's size made victory seem impossible.", -1: "David stepped forward with a sling and a stone. He struck Goliath, and the frightened army saw how God had helped a young shepherd."},
        "hard": {0: "For forty days Goliath called for an Israelite to fight him. His challenge frightened the soldiers, but David would see the battle through his trust in God.", -1: "David did not win by carrying the heaviest armor. He faced Goliath in God's name, used his sling, and showed the army that courage could come from faith."},
    },
    "jonah-big-fish": {
        "medium": {0: "God gave Jonah a message for the people of Nineveh: they needed to turn away from their wrongdoing. Jonah did not want to go.", -1: "Jonah prayed inside the great fish for three days and nights. When God brought him back to dry land, Jonah finally went to Nineveh."},
        "hard": {0: "God sent Jonah to warn Nineveh so its people could change their ways. Jonah knew what God had asked, but he chose to run from that calling.", -1: "The fish became an unexpected place for Jonah to pray and think. After three days and nights, God brought him safely to land and gave him another chance to obey."},
    },
    "daniel-lions-den": {
        "medium": {0: "Even in a kingdom far from home, Daniel kept his habit of praying to God each day. He would not forget whom he trusted.", -1: "An angel kept the lions from hurting Daniel. When the king came in the morning, he found Daniel alive and safe."},
        "hard": {0: "Daniel lived under a foreign king, yet his daily prayers showed where his loyalty belonged. He kept worshiping God even when doing so became dangerous.", -1: "God sent an angel to shut the lions' mouths. Daniel's rescue showed the king that Daniel's faithful prayers had not been in vain."},
    },
    "abraham": {
        "medium": {0: "God asked Abram to leave the place he knew and travel to a land He would show him. Abram began the journey without knowing the whole route.", -1: "At the right time, Sarah had a son named Isaac. After so many years of waiting, Abraham and Sarah could see that God had kept His promise."},
        "hard": {0: "Abram faced a difficult choice when God called him away from home. He trusted God's promise enough to set out, even though the destination was still unknown.", -1: "Isaac's birth came long after Abraham and Sarah had hoped for a child. His arrival showed that God's promise had not expired while they waited."},
    },
    "jacob": {
        "medium": {0: "After hurting his brother Esau with selfish choices, Jacob left home afraid of what might happen next. His journey began with a broken relationship.", -1: "When the brothers met again, Esau ran to embrace Jacob. The reunion brought Jacob safely home and opened a way toward peace."},
        "hard": {0: "Jacob had taken advantage of his brother Esau and now had to leave home. Fear followed him, but God would meet him during the journey and change his life.", -1: "Jacob expected anger when he returned to Esau. Instead, Esau embraced him, and the brothers' meeting became a chance for reconciliation."},
    },
    "ruth": {
        "medium": {0: "Naomi lost her husband and sons while living in Moab. When she decided to go back to Bethlehem, she expected her daughters-in-law to stay behind.", -1: "Ruth and Boaz's son was named Obed. Years later their family included King David, and much later Jesus came from that same family line."},
        "hard": {0: "Grieving the loss of her husband and sons, Naomi prepared to return to Bethlehem. She did not expect Ruth to give up her own home in order to stay beside her.", -1: "The birth of Obed connected Ruth's faithful care for Naomi to a much larger story. Obed became David's grandfather, and Ruth became an ancestor of Jesus."},
    },
    "samuel": {
        "medium": {0: "Hannah asked God for a child and promised that her son would serve Him. When Samuel was born, she remembered her promise.", -1: "As Samuel grew older, God continued to be with him. People throughout Israel recognized that God had chosen him as a prophet."},
        "hard": {0: "Hannah's prayer for a child was answered when Samuel was born. She kept her promise to dedicate him to God, beginning a life in which Samuel would learn to listen carefully.", -1: "Samuel did more than hear one message in the night. As he grew, God established him as a prophet whose words were recognized throughout Israel."},
    },
    "apostles-pentecost": {
        "medium": {0: "Before returning to heaven, Jesus promised His followers help from the Holy Spirit. They would receive power to tell others about Him.", -1: "The apostles continued to speak about Jesus with courage. The Holy Spirit helped them teach, care for people, and do remarkable signs."},
        "hard": {0: "Jesus gave His apostles a mission that would reach beyond their own city. He promised the Holy Spirit would give them the power they needed to be His witnesses.", -1: "Pentecost was the beginning of the apostles' bold witness, not the end. Through the Holy Spirit they taught about Jesus and served people as the good news spread."},
    },
    "gideon": {
        "medium": {0: "Gideon was trying to keep wheat safe because the Midianites kept stealing Israel's food. He worked in a hidden place so they would not see him.", -1: "The Midianites fled in confusion after Gideon's men followed God's plan. Just three hundred soldiers had shown that God could rescue Israel."},
        "hard": {0: "Midianite attacks had left Israel afraid and short of food. Gideon even prepared wheat in a wine press to hide it, yet God was about to call him into a surprising role.", -1: "Gideon's small group trusted God's unusual instructions. The Midianite army fled, showing that Israel's rescue did not depend on having the largest army."},
    },
    "esther": {
        "medium": {0: "Esther was a Jewish girl living in Persia, where her cousin Mordecai raised her. She was far from the homeland of her people.", -1: "The king listened to Esther's brave request. When Haman's plan was exposed, her people were rescued and had reason to celebrate."},
        "hard": {0: "Esther grew up in Persia under the care of her cousin Mordecai. Although she lived far from her people's homeland, her identity would become important at the palace.", -1: "Esther risked speaking up for her people, and the king heard her. Haman's plot was uncovered, changing a time of fear into relief and joy."},
    },
    "jericho": {
        "medium": {0: "Israel had crossed the Jordan, but Jericho stood in the way. Its gates were shut tight and the city was protected by tall walls.", -1: "After the walls fell, Joshua kept the promise made to Rahab. She and her family were brought to safety as Israel entered the city."},
        "hard": {0: "Across the Jordan River, Israel faced Jericho's closed gates and strong walls. They would have to trust God's instructions, even though His plan looked unusual.", -1: "Joshua did not forget Rahab when Jericho fell. Keeping the spies' promise protected her family and showed that trust and obedience included caring for others."},
    },
    "solomon": {
        "medium": {0: "After David, his son Solomon became king. He loved God and wanted the wisdom to lead the people fairly.", -1: "Solomon's decision impressed the people of Israel. They saw that God had given their king wisdom for judging difficult matters."},
        "hard": {0: "Solomon inherited the responsibility of leading Israel after his father David. Loving God, he knew that being king would take more than wealth or power.", -1: "The difficult case showed the people how wisely Solomon could judge. They recognized that his ability to lead with justice was a gift from God."},
    },
    "ten-commandments": {
        "medium": {0: "God had brought Israel out of Egypt and through the wilderness. Now the people camped at Mount Sinai to hear how they should live together.", -1: "The commandments guided Israel's life with God and with their neighbors. They taught the people to protect relationships, speak truthfully, and worship faithfully."},
        "hard": {0: "After rescuing Israel from slavery, God led the people to Mount Sinai. Their freedom came with a new responsibility to live as His people.", -1: "The ten commandments were more than a list to memorize. They shaped Israel's worship and taught the people to respect life, families, truth, and their neighbors."},
    },
    "elijah": {
        "medium": {0: "King Ahab and many Israelites were worshiping Baal instead of God. Elijah was sent to ask them to return to the LORD.", -1: "God answered Elijah's prayer with fire that consumed the sacrifice. The people bowed and declared that the LORD was God."},
        "hard": {0: "Israel's king and many of its people had turned to Baal. Elijah challenged them because they needed to decide whom they would truly worship.", -1: "The fire consumed Elijah's water-soaked sacrifice and showed the people who had answered his prayer. Their cry that the LORD is God marked a turn back toward Him."},
    },
    "nehemiah": {
        "medium": {0: "Far away from Jerusalem, Nehemiah heard that its walls were broken and its gates burned. He was deeply sad and prayed for the city.", -1: "Working together, the people completed the wall in fifty-two days. Even those who had opposed them could see that God had helped."},
        "hard": {0: "Nehemiah served a Persian king when news of Jerusalem's ruined walls reached him. He wept, fasted, and prayed before taking action to help his people.", -1: "The wall was finished after only fifty-two days of shared work and steady courage. The result surprised Israel's enemies and pointed to God's help."},
    },
    "job": {
        "medium": {0: "Job loved God and cared for a large family. He had many animals and was respected by the people who knew him.", -1: "Job trusted God even after the hardest days of his life. God corrected his friends and later gave him comfort, family, and a restored home."},
        "hard": {0: "Job was known for his faith and lived among a large family and many possessions. His trust in God would be tested when life changed suddenly.", -1: "Job could not explain everything that happened to him, but he learned to trust God's wisdom. God addressed his friends' mistaken claims and restored Job's household."},
    },
    "nativity": {
        "medium": {0: "In Nazareth, Gabriel told Mary she would have a son named Jesus. This child was the Son God had promised to send.", -1: "The shepherds went quickly to find the baby Jesus. After meeting Him, they praised God and shared the news they had heard from the angel."},
        "hard": {0: "God's message to Mary came through the angel Gabriel in Nazareth. She learned that Jesus, the promised Son, would be born to her.", -1: "The shepherds followed the angel's message to Bethlehem and found Jesus with Mary and Joseph. They returned praising God and telling others what they had seen."},
    },
    "beatitudes": {
        "medium": {0: "When a crowd gathered, Jesus sat on a mountain and began teaching His disciples. The people heard Him describe what life in God's kingdom is like.", -1: "Jesus called His followers the light of the world. Their kindness and good choices could help others see God's love."},
        "hard": {0: "Jesus taught on a mountainside with His disciples close to Him and the crowds listening. His words turned their attention toward the character of God's kingdom.", -1: "Jesus said His followers should shine like light in the world. Even when it is difficult to do what is right, their actions can point others to God."},
    },
    "good-samaritan": {
        "medium": {0: "A man who studied the law asked Jesus about eternal life. Jesus brought him back to the commands to love God and to love his neighbor.", -1: "The Samaritan also paid for the injured man's care at the inn. Jesus asked who had been a neighbor, and the answer was the one who showed mercy."},
        "hard": {0: "A teacher of the law questioned Jesus about what leads to eternal life. Their conversation turned to loving God fully and loving one's neighbor as oneself.", -1: "The Samaritan's help continued even after he left the inn: he paid for the traveler's care. Jesus made the listener identify mercy by what a person did, then told him to do the same."},
    },
    "feeding-5000": {
        "medium": {0: "Many people followed Jesus after seeing Him heal the sick. He welcomed the crowd and taught them about God's kingdom.", -1: "When everyone had eaten, Jesus asked the disciples to collect the leftovers. They filled twelve baskets with pieces of bread and fish."},
        "hard": {0: "The crowd came to Jesus because they had seen Him heal people. Jesus welcomed them, teaching about God's kingdom before meeting their need for food.", -1: "The crowd ate until they were satisfied, yet food still remained. The disciples gathered twelve baskets of leftovers so that none of the loaves and fish would be wasted."},
    },
    "easter": {
        "medium": {0: "Before He was arrested, Jesus shared the Passover meal with His disciples. He gave them bread and a cup to help them remember what He was about to do for them.", -1: "Jesus was alive again and appeared to His followers. He sent them to tell people everywhere the good news and promised to be with them."},
        "hard": {0: "During the Passover meal, Jesus prepared His disciples for His coming death. The bread and cup would help them remember the gift of His life and His love for them.", -1: "After His resurrection, Jesus met His followers and gave them a mission reaching all nations. He promised His presence as they shared the good news."},
    },
}
