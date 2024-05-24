import random


def generate_domain():
    words = [
        "apple", "banana", "cherry", "dog", "elephant", "fish", "grape", "house", "ice", "jacket",
        "kite", "lemon", "mouse", "nest", "orange", "pear", "queen", "rabbit", "snake", "tiger",
        "umbrella", "violet", "water", "xylophone", "yellow", "zebra", "ant", "bird", "cat", "duck",
        "egg", "frog", "goat", "hat", "ink", "jellyfish", "kiwi", "lion", "monkey", "nut", "owl",
        "peach", "quilt", "rose", "squirrel", "tree", "unicorn", "van", "whale", "xylograph", "yacht",
        "zeppelin", "airplane", "boat", "car", "dinosaur", "earth", "fire", "ghost", "hammer", "island",
        "jungle", "key", "lake", "mountain", "notebook", "ocean", "planet", "quill", "rain", "star",
        "tornado", "umbrella", "volcano", "wonder", "xylophone", "yoyo", "zoo", "atom", "book", "cloud",
        "dragon", "elephant", "flower", "guitar", "heart", "ice cream", "jacket", "kangaroo", "laptop", "moon",
        "nest", "oasis", "pencil", "quilt", "rainbow", "sun", "turtle", "unicorn", "vase", "wind",
        "xylophone", "yacht", "zebra", "anchor", "balloon", "cactus", "diamond", "eagle", "fireworks", "globe",
        "honey", "iceberg", "jet", "knight", "lighthouse", "mountain", "night", "octopus", "planet", "queen",
        "rocket", "sunset", "trumpet", "umbrella", "volcano", "waterfall", "xylophone", "yoga", "zeppelin", "astronaut",
        "bee", "carousel", "diamond", "earthquake", "flamingo", "giraffe", "helicopter", "island", "jigsaw", "kayak",
        "lily", "mango", "nebula", "ocean", "penguin", "quartz", "rose", "sailboat", "telescope", "unicorn",
        "vortex", "waterfall", "xylophone", "yeti", "zeppelin", "anchor", "beehive", "campfire", "dolphin", "eclipse",
        "flute", "guitar", "hiking", "igloo", "jellybean", "knight", "leopard", "mushroom", "nightingale", "octopus",
        "planetarium", "quill", "rainforest", "starfish", "tornado", "umbrella", "volleyball", "wave", "xylophone", "yacht",
        "zephyr", "arrow", "bear", "cloud", "dragonfly", "elephant", "firefly", "gorilla", "honeycomb", "island",
        "jupiter", "kiwi", "lighthouse", "moon", "night", "owl", "peacock", "quasar", "rose", "sapphire",
        "tiger", "ufo", "volcano", "whale", "xylophone", "yarn", "zeppelin", "apple", "bee", "cherry",
        "dragon", "elephant", "flamingo", "giraffe", "hedgehog", "iguana", "jellyfish", "koala", "lizard", "mango",
        "narwhal", "owl", "panda", "quokka", "rhinoceros", "sunflower", "tiger", "umbrella", "vampire", "waterfall",
        "xylophone", "yeti", "zebra", "almond", "butterfly", "caterpillar", "daisy", "eagle", "fox", "giraffe",
        "hamster", "iguana", "jaguar", "kangaroo", "lion", "mongoose", "nightingale", "ostrich", "peacock", "quail",
        "rabbit", "seahorse", "tiger", "umbrella", "vulture", "wombat", "xylophone", "yak", "zebra", "albatross",
        "bison", "crocodile", "dolphin", "elephant", "flamingo", "giraffe", "hippopotamus", "iguana", "jaguar", "koala",
        "lemur", "macaw", "nightingale", "octopus", "penguin", "quail", "rabbit", "shark", "tiger", "umbrella",
        "vampire", "whale", "xylophone", "yak", "zebra", "almond", "butterfly", "caterpillar", "daisy", "eagle",
        "fox", "giraffe", "hamster", "iguana", "jaguar", "kangaroo", "lion", "mongoose", "nightingale", "ostrich",
        "peacock", "quail", "rabbit", "seahorse", "tiger", "umbrella", "vulture", "wombat", "xylophone", "yak",
        "zebra", "albatross", "bison", "crocodile", "dolphin", "elephant", "flamingo", "giraffe", "hippopotamus", "iguana"
    ]

    tld = [".info", ".click", ".site", ".space"]

    random_words = random.sample(words, 2)
    hyphenated_name = "-".join(random_words)
    domain = hyphenated_name + random.sample(tld, 1)[0]

    return domain

    
