"""
Program that will allow passerbys to text if my dog is barking from the balcony while I am not home.
If trigerred, a Raspberry Pi will initiate mists to spray forcing her back inside.
If she is not barking, they can trigger a treat to be deployed.
"""

treat_count = 0
mist_count = 0

while True:
    command = input("Text WOOF if she is barking \nText TREAT if she is being a good girl ")
    if command.lower().strip() == "treat" and treat_count < 5:
        print("Good girls get all the treats!")
        treat_count += 1
        print(treat_count)
        "engage treat deploy function"
        "snap photo function"

    elif command.lower().strip() == "treat":
        print("Coco is out of treats for the day due to being such a good girl!")
        "snap photo function"

    elif command.lower().strip() == "woof" and mist_count < 10:
        print("Engaging the mists of silence!")
        mist_count += 1
        print(mist_count)
        "engage mister function"
        "snap photo function"

    elif command.lower().strip() == "woof":
        print("We are out of water")
        "snap photo function"

    else:
        print("We received your message, but it wasn't one of the valid commands (WOOF or TREAT). We will record it as feedback. Thank you!")
        "snap photo function"
        print(treat_count)
