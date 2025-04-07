from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ....authors.models import Author
from ....follow.models import Follow
from ....posts.models import Post, Comment, Like
from dodgerblue.settings import NODEHOSTNAME

class Command(BaseCommand):
    help = 'Add initial user and author data to the database'
    def handle(self, *args, **kwargs):

        # Create Users
        admin_user = User.objects.create_user(
            username='admin',
            password='admin',
            is_active=True,
            is_staff=True,
        )

        user1_user = User.objects.create_user(
            username='johndoe',
            password='johndoe',
            is_active=True,
            is_staff=False,
        )

        user2_user = User.objects.create_user(
            username='janedoe',
            password='janedoe',
            is_active=True,
            is_staff=False,
        )

        user3_user = User.objects.create_user(
            username='jacob',
            password='jacob',
            is_active=True,
            is_staff=False,
        )

        user4_user = User.objects.create_user(
            username='barry',
            password='barry',
            is_active=True,
            is_staff=False,
        )

        # Create Authors
        admin_author = Author.objects.create(
            user=admin_user,
            displayName='admin',
            profileImage="https://robohash.org/admin.png",
            page='{}authors/{}'.format(NODEHOSTNAME, admin_user.id),
            host=f'{NODEHOSTNAME}api/',
            is_local=True,
            username='admin',
            state='ACTIVE',
            id_url='{}api/authors/{}'.format(NODEHOSTNAME, admin_user.id),
        )

        user1_author = Author.objects.create(
            user=user1_user,
            displayName='John Doe',
            profileImage="https://robohash.org/JohnDoe.png",
            page='{}authors/{}'.format(NODEHOSTNAME, user1_user.id),
            host=f'{NODEHOSTNAME}api/',
            is_local=True,
            username='johndoe',
            state='ACTIVE',
            id_url='{}api/authors/{}'.format(NODEHOSTNAME, user1_user.id),
        )

        user2_author = Author.objects.create(
            user=user2_user,
            displayName='Jane Doe',
            profileImage="https://robohash.org/JaneDoe.png",
            page='{}authors/{}'.format(NODEHOSTNAME, user2_user.id),
            host=f'{NODEHOSTNAME}api/',
            is_local=True,
            username='janedoe',
            state='ACTIVE',
            id_url='{}api/authors/{}'.format(NODEHOSTNAME, user2_user.id),
        )

        user3_author = Author.objects.create(
            user=user3_user,
            displayName='Jacob',
            profileImage="https://robohash.org/Jacob.png",
            page='{}authors/{}'.format(NODEHOSTNAME, user3_user.id),
            host=f'{NODEHOSTNAME}api/',
            is_local=True,
            username='jacob',
            state='ACTIVE',
            id_url='{}api/authors/{}'.format(NODEHOSTNAME, user3_user.id),
        )

        user4_author = Author.objects.create(
            user=user4_user,
            displayName='Barry',
            profileImage="https://robohash.org/Barry.png",
            page='{}authors/{}'.format(NODEHOSTNAME, user4_user.id),
            host=f'{NODEHOSTNAME}api/',
            is_local=True,
            username='Barry',
            state='ACTIVE',
            id_url='{}api/authors/{}'.format(NODEHOSTNAME, user4_user.id),
        )

        # Create follow relations

        # John doe follows Jane doe
        Follow.objects.create(
            actor=user1_author,
            object=user2_author,
            isPending=False
        )

        # Jane doe follows John doe
        Follow.objects.create(
            actor=user2_author,
            object=user1_author,
            isPending=False
        )

        # Jacob follow requested John doe
        Follow.objects.create(
            actor=user3_author,
            object=user1_author,
            isPending=True
        )

        # John doe follows Jacob
        Follow.objects.create(
            actor=user1_author,
            object=user3_author,
            isPending=False
        )

        # Jane doe follow requested Jacob
        Follow.objects.create(
            actor=user2_author,
            object=user3_author,
            isPending=True
        )

        # Create Posts

        # Public text/plain post by user1
        user1_post_1 = Post.objects.create(
            title='Post 1',
            id_url='{}api/authors/{}/posts/1'.format(NODEHOSTNAME, user1_author.id),
            description='Post 1 description',
            contentType='text/plain',
            content='POST 1 Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
            author=user1_author,
            visibility='PUBLIC',
            page='http://localhost:8000'
        )

        # public text/markdown post by user1
        user1_post_2 = Post.objects.create(
            title='Post 2',
            id_url='{}api/authors/{}/posts/2'.format(NODEHOSTNAME, user1_author.id),
            description='Post 2 description',
            contentType='text/markdown',
            content='# POST 2 \n'+
                    '- Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
            author=user1_author,
            visibility='PUBLIC',
            page=f"{user1_author.id_url}/posts/"
        )

        # public image/png;base64 post by user1
        user1_post_3 = Post.objects.create(
            title='Post 3',
            id_url='{}api/authors/{}/posts/3'.format(NODEHOSTNAME, user1_author.id),
            description='Post 3 description',
            contentType='image/png;base64',
            content='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',
            author=user1_author,
            visibility='PUBLIC',
            page='http://localhost:8000'
        )

        # Unlisted text/plain post by user1
        user1_post_4 = Post.objects.create(
            title='Post 4',
            id_url='{}api/authors/{}/posts/4'.format(NODEHOSTNAME, user1_author.id),
            description='Post 4 description',
            contentType='text/plain',
            content='POST 1 Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
            author=user1_author,
            visibility='UNLISTED',
            page='http://localhost:8000'
        )

        # public text/markdown post by user1
        user1_post_5 = Post.objects.create(
            title='Post 5',
            id_url='{}api/authors/{}/posts/5'.format(NODEHOSTNAME, user1_author.id),
            description='Post 5 description',
            contentType='text/markdown',
            content='# POST 5 \n' +
                    '- Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
            author=user1_author,
            visibility='UNLISTED',
            page='http://localhost:8000'
        )

        # public image/png;base64 post by user1
        user1_post_6 = Post.objects.create(
            title='Post 6',
            id_url='{}api/authors/{}/posts/6'.format(NODEHOSTNAME, user1_author.id),
            description='Post 6 description',
            contentType='application/base64',
            content='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',
            author=user1_author,
            visibility='UNLISTED',
            page='http://localhost:8000'
        )

        user1_post_7 = Post.objects.create(
            title='Post 7',
            id_url='{}api/authors/{}/posts/7'.format(NODEHOSTNAME, user1_author.id),
            description='Post 7 description',
            contentType='text/plain',
            content='POST 7 Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
            author=user1_author,
            visibility='FRIENDS',
            page='http://localhost:8000'
        )

        user1_post_8 = Post.objects.create(
            title='Post 8',
            id_url='{}api/authors/{}/posts/8'.format(NODEHOSTNAME, user1_author.id),
            description='Post 8 description',
            contentType='text/plain',
            content='POST 8 Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
            author=user1_author,
            visibility='DELETED',
            page='http://localhost:8000'
        )

        user2_post_9 = Post.objects.create(
            title='Post 9',
            id_url='{}api/authors/{}/posts/9'.format(NODEHOSTNAME, user2_author.id),
            description='Post 9 description',
            contentType='text/markdown',
            content='# POST 9 \n' +
                    '- Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
            author=user2_author,
            visibility='FRIENDS',
            page='http://localhost:8000'
        )

        user3_post_10 = Post.objects.create(
            title='Post 10',
            id_url='{}api/authors/{}/posts/10'.format(NODEHOSTNAME, user3_author.id),
            description='Post 10 description',
            contentType='text/markdown',
            content='# POST 10 \n' +
                    '- Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
            author=user3_author,
            visibility='DELETED',
            page='http://localhost:8000'
        )

        user4_post_beeMovie = Post.objects.create(
            title='Bee Movie',
            id_url='{}api/authors/{}/posts/11'.format(NODEHOSTNAME, user4_author.id),
            description='Bee Movie',
            contentType='text/plain',
            content="""
                According to all known laws of aviation, there is no way a bee should be able to fly.
                Its wings are too small to get its fat little body off the ground.
                The bee, of course, flies anyway because bees don't care what humans think is impossible.
                Yellow, black. Yellow, black. Yellow, black. Yellow, black.
                Ooh, black and yellow!
                Let's shake it up a little.
                Barry! Breakfast is ready!
                Coming!
                Hang on a second.
                Hello?
                Barry?
                Adam?
                Can you believe this is happening?
                I can't.
                I'll pick you up.
                Looking sharp.
                Use the stairs, Your father paid good money for those.
                Sorry. I'm excited.
                Here's the graduate.
                We're very proud of you, son.
                A perfect report card, all B's.
                Very proud.
                Ma! I got a thing going here.
                You got lint on your fuzz.
                Ow! That's me!
                Wave to us! We'll be in row 118,000.
                Bye!
                Barry, I told you, stop flying in the house!
                Hey, Adam.
                Hey, Barry.
                Is that fuzz gel?
                A little. Special day, graduation.
                Never thought I'd make it.
                Three days grade school, three days high school.
                Those were awkward.
                Three days college. I'm glad I took a day and hitchhiked around The Hive.
                You did come back different.
                Hi, Barry. Artie, growing a mustache? Looks good.
                Hear about Frankie?
                Yeah.
                You going to the funeral?
                No, I'm not going.
                Everybody knows, sting someone, you die.
                Don't waste it on a squirrel.
                Such a hothead.
                I guess he could have just gotten out of the way.
                I love this incorporating an amusement park into our day.
                That's why we don't need vacations.
                Boy, quite a bit of pomp under the circumstances.
                Well, Adam, today we are men.
                We are!
                Bee-men.
                Amen!
                Hallelujah!
                Students, faculty, distinguished bees,
                please welcome Dean Buzzwell.
                Welcome, New Hive City graduating class of 9:15.
                That concludes our ceremonies And begins your career at Honex Industries!
                Will we pick our job today?
                I heard it's just orientation.
                Heads up! Here we go.
                Keep your hands and antennas inside the tram at all times.
                Wonder what it'll be like?
                A little scary.
                Welcome to Honex, a division of Honesco and a part of the Hexagon Group.
                This is it!
                Wow.
                Wow.
                We know that you, as a bee, have worked your whole life to get to the point where you can work for your whole life.
                Honey begins when our valiant Pollen Jocks bring the nectar to The Hive.
                Our top-secret formula is automatically color-corrected, scent-adjusted and bubble-contoured into this soothing sweet syrup with its distinctive golden glow you know as... Honey!
                That girl was hot.
                She's my cousin!
                She is?
                Yes, we're all cousins.
                Right. You're right.
                At Honex, we constantly strive to improve every aspect of bee existence.
                These bees are stress-testing a new helmet technology.
                What do you think he makes?
                Not enough.
                Here we have our latest advancement, the Krelman.
                What does that do?
                Catches that little strand of honey that hangs after you pour it.
                Saves us millions.
                Can anyone work on the Krelman?
                Of course. Most bee jobs are small ones.
                But bees know that every small job, if it's done well, means a lot.
                But choose carefully because you'll stay in the job you pick for the rest of your life.
                The same job the rest of your life? I didn't know that.
                What's the difference?
                You'll be happy to know that bees, as a species, haven't had one day off in 27 million years.
                So you'll just work us to death?
                We'll sure try.
                Wow! That blew my mind!
                "What's the difference?"
                How can you say that?
                One job forever?
                That's an insane choice to have to make.
                I'm relieved. Now we only have to make one decision in life.
                But, Adam, how could they never have told us that?
                Why would you question anything? We're bees.
                We're the most perfectly functioning society on Earth.
                You ever think maybe things work a little too well here?
                Like what? Give me one example.
                I don't know. But you know what I'm talking about.
                Please clear the gate. Royal Nectar Force on approach.
                Wait a second. Check it out.
                Hey, those are Pollen Jocks!
                Wow.
                I've never seen them this close.
                They know what it's like outside The Hive.
                Yeah, but some don't come back.
                Hey, Jocks!
                Hi, Jocks!
                You guys did great!
                You're monsters!
                You're sky freaks! I love it! I love it!
                I wonder where they were.
                I don't know.
                Their day's not planned.
                Outside The Hive, flying who knows where, doing who knows what.
                You can't just decide to be a Pollen Jock. You have to be bred for that.
                Right.
                Look. That's more pollen than you and I will see in a lifetime.
                It's just a status symbol.
                Bees make too much of it.
                Perhaps. Unless you're wearing it and the ladies see you wearing it.
                Those ladies?
                Aren't they our cousins too?
                Distant. Distant.
                Look at these two.
                Couple of Hive Harrys.
                Let's have fun with them.
                It must be dangerous being a Pollen Jock.
                Yeah. Once a bear pinned me against a mushroom!
                He had a paw on my throat, and with the other, he was slapping me!
                Oh, my!
                I never thought I'd knock him out.
                What were you doing during this?
                Trying to alert the authorities.
                I can autograph that.
                A little gusty out there today, wasn't it, comrades?
                Yeah. Gusty.
                We're hitting a sunflower patch six miles from here tomorrow.
                Six miles, huh?
                Barry!
                A puddle jump for us, but maybe you're not up for it.
                Maybe I am.
                You are not!
                We're going 0900 at J-Gate.
                What do you think, buzzy-boy?
                Are you bee enough?
                I might be. It all depends on what 0900 means.
                Hey, Honex!
                Dad, you surprised me.
                You decide what you're interested in?
                Well, there's a lot of choices.
                But you only get one.
                Do you ever get bored doing the same job every day?
                Son, let me tell you about stirring.
                You grab that stick, and you just move it around, and you stir it around.
                You get yourself into a rhythm.
                It's a beautiful thing.
                You know, Dad, the more I think about it,
                maybe the honey field just isn't right for me.
                You were thinking of what, making balloon animals?
                That's a bad job for a guy with a stinger.
                Janet, your son's not sure he wants to go into honey!
                Barry, you are so funny sometimes.
                I'm not trying to be funny.
                You're not funny! You're going into honey. Our son, the stirrer!
                You're gonna be a stirrer?
                No one's listening to me!
                Wait till you see the sticks I have.
                I could say anything right now.
                I'm gonna get an ant tattoo!
                Let's open some honey and celebrate!
                Maybe I'll pierce my thorax. Shave my antennae. Shack up with a grasshopper. Get a gold tooth and call everybody "dawg"!
                I'm so proud.
                We're starting work today!
                Today's the day.
                Come on! All the good jobs will be gone.
                Yeah, right.
                Pollen counting, stunt bee, pouring, stirrer, front desk, hair removal...
                Is it still available?
                Hang on. Two left!
                One of them's yours! Congratulations!
                Step to the side.
                What'd you get?
                Picking crud out. Stellar!
                Wow!
                Couple of newbies?
                Yes, sir! Our first day! We are ready!
                Make your choice.
                You want to go first?
                No, you go.
                Oh, my. What's available?
                Restroom attendant's open, not for the reason you think.
                Any chance of getting the Krelman?
                Sure, you're on.
                I'm sorry, the Krelman just closed out.
                Wax monkey's always open.
                The Krelman opened up again.
                What happened?
                A bee died. Makes an opening. See? He's dead. Another dead one.
                Deady. Deadified. Two more dead.
                Dead from the neck up. Dead from the neck down. That's life!
                Oh, this is so hard!
                Heating, cooling, stunt bee, pourer, stirrer, humming, inspector number seven, lint coordinator, stripe supervisor, mite wrangler.
                Barry, what do you think I should... Barry?
                Barry!
                All right, we've got the sunflower patch in quadrant nine...
                What happened to you?
                Where are you?
                I'm going out.
                Out? Out where?
                Out there.
                Oh, no!
                I have to, before I go to work for the rest of my life.
                You're gonna die! You're crazy! Hello?
                Another call coming in.
                If anyone's feeling brave, there's a Korean deli on 83rd that gets their roses today.
                Hey, guys.
                Look at that.
                Isn't that the kid we saw yesterday?
                Hold it, son, flight deck's restricted.
                It's OK, Lou. We're gonna take him up.
                Really? Feeling lucky, are you?
                Sign here, here. Just initial that.
                Thank you.
                OK.
                You got a rain advisory today, and as you all know, bees cannot fly in rain.
                So be careful. As always, watch your brooms, hockey sticks, dogs, birds, bears and bats.
                Also, I got a couple of reports of root beer being poured on us.
                Murphy's in a home because of it, babbling like a cicada!
                That's awful.
                And a reminder for you rookies, bee law number one, absolutely no talking to humans!
                 All right, launch positions!
                Buzz, buzz, buzz, buzz! Buzz, buzz, buzz, buzz! Buzz, buzz, buzz, buzz!
                Black and yellow!
                Hello!
                You ready for this, hot shot?
                Yeah. Yeah, bring it on.
                Wind, check.
                Antennae, check.
                Nectar pack, check.
                Wings, check.
                Stinger, check.
                Scared out of my shorts, check.
                OK, ladies,
                let's move it out!
                Pound those petunias, you striped stem-suckers!
                All of you, drain those flowers!
                Wow! I'm out!
                I can't believe I'm out!
                So blue.
                I feel so fast and free!
                Box kite!
                Wow!
                Flowers!
                This is Blue Leader, We have roses visual.
                Bring it around 30 degrees and hold.
                Roses!
                30 degrees, roger. Bringing it around.
                Stand to the side, kid.
                It's got a bit of a kick.
                That is one nectar collector!
                Ever see pollination up close?
                No, sir.
                I pick up some pollen here, sprinkle it over here. Maybe a dash over there, a pinch on that one.
                See that? It's a little bit of magic.
                That's amazing. Why do we do that?
                That's pollen power. More pollen, more flowers, more nectar, more honey for us.
                Cool.
                I'm picking up a lot of bright yellow, Could be daisies, Don't we need those?
                Copy that visual.
                Wait. One of these flowers seems to be on the move.
                Say again? You're reporting a moving flower?
                Affirmative.
                That was on the line!
                This is the coolest. What is it?
                I don't know, but I'm loving this color.
                It smells good.
                Not like a flower, but I like it.
                Yeah, fuzzy.
                Chemical-y.
                Careful, guys. It's a little grabby.
                My sweet lord of bees!
                Candy-brain, get off there!
                Problem!
                Guys!
                This could be bad.
                Affirmative.
                Very close.
                Gonna hurt.
                Mama's little boy.
                You are way out of position, rookie!
                Coming in at you like a missile!
                Help me!
                I don't think these are flowers.
                Should we tell him?
                I think he knows.
                What is this?!
                Match point!
                You can start packing up, honey, because you're about to eat it!
                Yowser!
                Gross.
                There's a bee in the car!
                Do something!
                I'm driving!
                Hi, bee.
                He's back here!
                He's going to sting me!
                Nobody move. If you don't move, he won't sting you. Freeze!
                He blinked!
                Spray him, Granny!
                What are you doing?!
                Wow... the tension level out here is unbelievable.
                I gotta get home.
                Can't fly in rain. Can't fly in rain. Can't fly in rain.
                Mayday! Mayday! Bee going down!
                Ken, could you close the window please?
                Ken, could you close the window please?
                Check out my new resume. I made it into a fold-out brochure. You see? Folds out.
                Oh, no. More humans. I don't need this.
                What was that?
                Maybe this time. This time. This time. This time! This time! This... Drapes!
                That is diabolical.
                It's fantastic. It's got all my special skills, even my top-ten favorite movies.
                What's number one? Star Wars?
                Nah, I don't go for that... kind of stuff.
                No wonder we shouldn't talk to them. They're out of their minds.
                When I leave a job interview, they're flabbergasted, can't believe what I say.
                There's the sun. Maybe that's a way out.
                I don't remember the sun having a big 75 on it.
                I predicted global warming. I could feel it getting hotter. At first I thought it was just me.
                Wait! Stop! Bee!
                Stand back. These are winter boots.
                Wait!
                Don't kill him!
                You know I'm allergic to them! This thing could kill me!
                Why does his life have less value than yours?
                Why does his life have any less value than mine? Is that your statement?
                I'm just saying all life has value. You don't know what he's capable of feeling.
                My brochure!
                There you go, little guy.
                I'm not scared of him.It's an allergic thing.
                 Put that on your resume brochure.
                My whole face could puff up.
                Make it one of your special skills.
                Knocking someone out is also a special skill.
                Right. Bye, Vanessa. Thanks.
                Vanessa, next week? Yogurt night?
                Sure, Ken. You know, whatever.
                You could put carob chips on there.
                Bye.
                Supposed to be less calories.
                Bye.
                I gotta say something. She saved my life. I gotta say something.
                All right, here it goes.
                Nah.
                What would I say?
                I could really get in trouble. It's a bee law. You're not supposed to talk to a human.
                I can't believe I'm doing this. I've got to.
                Oh, I can't do it. Come on!
                No. Yes. No. Do it. I can't.
                How should I start it? "You like jazz?" No, that's no good.
                Here she comes! Speak, you fool!
                Hi!
                I'm sorry. You're talking.
                Yes, I know.
                You're talking!
                I'm so sorry.
                No, it's OK. It's fine.
                I know I'm dreaming. But I don't recall going to bed.
                Well, I'm sure this is very disconcerting.
                This is a bit of a surprise to me. I mean, you're a bee!
                I am. And I'm not supposed to be doing this, but they were all trying to kill me.
                And if it wasn't for you... I had to thank you. It's just how I was raised.
                That was a little weird. I'm talking with a bee.
                Yeah.
                I'm talking to a bee. And the bee is talking to me!
                I just want to say I'm grateful.
                I'll leave now.
                Wait! How did you learn to do that?
                What?
                The talking thing.
                Same way you did, I guess. "Mama, Dada, honey." You pick it up.
                That's very funny.
                Yeah.
                Bees are funny. If we didn't laugh, we'd cry with what we have to deal with.
                Anyway... Can I... get you something?
                Like what?
                I don't know. I mean... I don't know. Coffee?
                I don't want to put you out.
                It's no trouble. It takes two minutes.
                It's just coffee.
                I hate to impose.
                Don't be ridiculous!
                Actually, I would love a cup.
                Hey, you want rum cake?
                I shouldn't.
                Have some.
                No, I can't.
                Come on!
                I'm trying to lose a couple micrograms.
                Where?
                These stripes don't help.
                You look great!
                I don't know if you know anything about fashion.
                Are you all right?
                No.
                He's making the tie in the cab as they're flying up Madison.
                He finally gets there.
                He runs up the steps into the church.
                The wedding is on.
                And he says, "Watermelon?
                I thought you said Guatemalan.
                Why would I marry a watermelon?"
                Is that a bee joke?
                That's the kind of stuff we do.
                Yeah, different.
                So, what are you gonna do, Barry?
                About work? I don't know.
                I want to do my part for The Hive, but I can't do it the way they want.
                I know how you feel.
                You do?
                Sure.
                My parents wanted me to be a lawyer or a doctor, but I wanted to be a florist.
                Really?
                My only interest is flowers.
                Our new queen was just elected with that same campaign slogan.
                Anyway, if you look... There's my hive right there. See it?
                You're in Sheep Meadow!
                Yes! I'm right off the Turtle Pond!
                No way! I know that area. I lost a toe ring there once.
                Why do girls put rings on their toes?
                Why not?
                It's like putting a hat on your knee.
                Maybe I'll try that.
                You all right, ma'am?
                Oh, yeah. Fine.
                Just having two cups of coffee!
                Anyway, this has been great.
                Thanks for the coffee.
                Yeah, it's no trouble.
                Sorry I couldn't finish it. If I did, I'd be up the rest of my life.
                Are you...?
                Can I take a piece of this with me?
                Sure! Here, have a crumb.
                Thanks!
                Yeah.
                All right. Well, then... I guess I'll see you around. Or not.
                OK, Barry.
                And thank you so much again... for before.
                Oh, that? That was nothing.
                Well, not nothing, but... Anyway...
                This can't possibly work.
                He's all set to go.
                We may as well try it.
                OK, Dave, pull the chute.
                Sounds amazing.
                It was amazing!
                It was the scariest, happiest moment of my life.
                Humans! I can't believe you were with humans!
                Giant, scary humans!
                What were they like?
                Huge and crazy. They talk crazy.
                They eat crazy giant things.
                They drive crazy.
                Do they try and kill you, like on TV?
                Some of them. But some of them don't.
                How'd you get back?
                Poodle.
                You did it, and I'm glad. You saw whatever you wanted to see.
                You had your "experience." Now you can pick out yourjob and be normal.
                Well...
                Well?
                Well, I met someone.
                You did? Was she Bee-ish?
                A wasp?! Your parents will kill you!
                No, no, no, not a wasp.
                Spider?
                I'm not attracted to spiders.
                I know it's the hottest thing, with the eight legs and all. I can't get by that face.
                So who is she?
                She's... human.
                No, no. That's a bee law. You wouldn't break a bee law.
                Her name's Vanessa.
                Oh, boy.
                She's so nice. And she's a florist!
                Oh, no! You're dating a human florist!
                We're not dating.
                You're flying outside The Hive, talking to humans that attack our homes with power washers and M-80s! One-eighth a stick of dynamite!
                She saved my life! And she understands me.
                This is over!
                Eat this.
                This is not over! What was that?
                They call it a crumb.
                It was so stingin' stripey!
                And that's not what they eat.
                That's what falls off what they eat!
                You know what a Cinnabon is?
                No.
                It's bread and cinnamon and frosting. They heat it up...
                Sit down!
                ...really hot!
                Listen to me!
                We are not them! We're us.
                There's us and there's them!
                Yes, but who can deny the heart that is yearning?
                There's no yearning. Stop yearning. Listen to me!
                You have got to start thinking bee, my friend. Thinking bee!
                Thinking bee.
                Thinking bee.
                Thinking bee! Thinking bee! Thinking bee! Thinking bee!
                There he is. He's in the pool.
                You know what your problem is, Barry?
                I gotta start thinking bee?
                How much longer will this go on?
                It's been three days! Why aren't you working?
                I've got a lot of big life decisions to think about.
                What life? You have no life!
                You have no job. You're barely a bee!
                Would it kill you to make a little honey?
                Barry, come out. Your father's talking to you.
                Martin, would you talk to him?
                Barry, I'm talking to you!
                You coming?
                Got everything?
                All set!
                Go ahead. I'll catch up.
                Don't be too long.
                Watch this!
                Vanessa!
                We're still here.
                I told you not to yell at him.
                He doesn't respond to yelling!
                Then why yell at me?
                Because you don't listen!
                I'm not listening to this.
                Sorry, I've gotta go.
                Where are you going?
                I'm meeting a friend.
                A girl? Is this why you can't decide?
                Bye.
                I just hope she's Bee-ish.
                They have a huge parade of flowers every year in Pasadena?
                To be in the Tournament of Roses, that's every florist's dream!
                Up on a float, surrounded by flowers, crowds cheering.
                A tournament. Do the roses compete in athletic events?
                No. All right, I've got one.
                How come you don't fly everywhere?
                It's exhausting. Why don't you run everywhere? It's faster.
                Yeah, OK, I see, I see.
                All right, your turn.
                TiVo. You can just freeze live TV? That's insane!
                You don't have that?
                We have Hivo, but it's a disease. It's a horrible, horrible disease.
                Oh, my.
                Dumb bees!
                You must want to sting all those jerks.
                We try not to sting. It's usually fatal for us.
                So you have to watch your temper.
                Very carefully.
                You kick a wall, take a walk, write an angry letter and throw it out. Work through it like any emotion: Anger, jealousy, lust.
                Oh, my goodness! Are you OK?
                Yeah.
                What is wrong with you?!
                It's a bug.
                He's not bothering anybody.
                Get out of here, you creep!
                What was that? A Pic 'N' Save circular?
                Yeah, it was. How did you know?
                It felt like about 10 pages. Seventy-five is pretty much our limit.
                You've really got that down to a science.
                I lost a cousin to Italian Vogue.
                I'll bet.
                What in the name of Mighty Hercules is this?
                How did this get here? cute Bee, Golden Blossom, Ray Liotta Private Select?
                Is he that actor?
                I never heard of him.
                Why is this here?
                For people. We eat it.
                You don't have enough food of your own?
                Well, yes.
                How do you get it?
                Bees make it.
                I know who makes it! And it's hard to make it!
                There's heating, cooling, stirring. You need a whole Krelman thing!
                It's organic.
                It's our-ganic!
                It's just honey, Barry.
                Just what?!
                Bees don't know about this! This is stealing! A lot of stealing!
                You've taken our homes, schools,hospitals! This is all we have!
                And it's on sale?! I'm getting to the bottom of this.
                I'm getting to the bottom of all of this!
                Hey, Hector. You almost done?
                Almost.
                He is here. I sense it.
                Well, I guess I'll go home now and just leave this nice honey out, with no one around.
                You're busted, box boy!
                I knew I heard something.
                So you can talk!
                I can talk. And now you'll start talking!
                Where you getting the sweet stuff? Who's your supplier?
                I don't understand.
                I thought we were friends.
                The last thing we want to do is upset bees!
                You're too late! It's ours now!
                You, sir, have crossed the wrong sword!
                You, sir, will be lunch for my iguana, Ignacio!
                Where is the honey coming from? Tell me where!
                Honey Farms! It comes from Honey Farms!
                Crazy person!
                What horrible thing has happened here?
                These faces, they never knew what hit them. And now
                they're on the road to nowhere!
                Just keep still.
                What? You're not dead?
                Do I look dead? They will wipe anything that moves. Where you headed?
                To Honey Farms. I am onto something huge here.
                I'm going to Alaska. Moose blood, crazy stuff. Blows your head off!
                I'm going to Tacoma.
                And you?
                He really is dead.
                All right.
                Uh-oh!
                What is that?!
                Oh, no!
                A wiper! Triple blade!
                Triple blade?
                Jump on! It's your only chance, bee!
                Why does everything have
                to be so doggone clean?!
                How much do you people need to see?!
                Open your eyes!
                Stick your head out the window!
                From NPR News in Washington,
                I'm Carl Kasell.
                But don't kill no more bugs!
                Bee!
                Moose blood guy!!
                You hear something?
                Like what?
                Like tiny screaming.
                Turn off the radio.
                Whassup, bee boy?
                Hey, Blood.
                Just a row of honey jars, as far as the eye could see.
                Wow!
                I assume wherever this truck goes is where they're getting it. I mean, that honey's ours.
                Bees hang tight. We're all jammed in.
                It's a close community.
                Not us, man. We on our own. Every mosquito on his own.
                What if you get in trouble?
                You a mosquito, you in trouble. Nobody likes us. They just smack. See a mosquito, smack, smack!
                At least you're out in the world. You must meet girls.
                Mosquito girls try to trade up, get with a moth, dragonfly. Mosquito girl don't want no mosquito.
                You got to be kidding me!
                Mooseblood's about to leave the building! So long, bee!
                Hey, guys!
                Mooseblood!
                I knew I'd catch y'all down here.
                Did you bring your crazy straw?
                We throw it in jars, slap a label on it, and it's pretty much pure profit.
                What is this place?
                A bee's got a brain the size of a pinhead.
                They are pinheads!
                Pinhead.
                Check out the new smoker.
                Oh, sweet. That's the one you want. The Thomas 3000!
                Smoker?
                Ninety puffs a minute, semi-automatic. Twice the nicotine, all the tar. A couple breaths of this knocks them right out.
                They make the honey, and we make the money.
                "They make the honey, and we make the money"?
                Oh, my!
                What's going on? Are you OK?
                Yeah. It doesn't last too long.
                Do you know you're in a fake hive with fake walls?
                Our queen was moved here. We had no choice.
                This is your queen? That's a man in women's clothes! That's a drag queen!
                What is this?
                Oh, no!
                There's hundreds of them!
                Bee honey.
                Our honey is being brazenly stolen on a massive scale!
                This is worse than anything bears have done! I intend to do something.
                Oh, Barry, stop.
                Who told you humans are taking our honey? That's a rumor.
                Do these look like rumors?
                That's a conspiracy theory. These are obviously doctored photos. How did you get mixed up in this?
                He's been talking to humans.
                What? Talking to humans?!
                He has a human girlfriend. And they make out!
                Make out? Barry!
                We do not.
                You wish you could.
                Whose side are you on?
                The bees!
                I dated a cricket once in San Antonio. Those crazy legs kept me up all night.
                Barry, this is what you want to do with your life?
                I want to do it for all our lives. Nobody works harder than bees!
                Dad, I remember you coming home so overworked
                your hands were still stirring. You couldn't stop.
                I remember that.
                What right do they have to our honey?
                We live on two cups a year. They put it in lip balm for no reason whatsoever!
                Even if it's true, what can one bee do?
                Sting them where it really hurts.
                In the face! The eye!
                That would hurt.
                No.
                Up the nose? That's a killer.
                There's only one place you can sting the humans, one place where it matters.
                Hive at Five, The Hive's only full-hour action news source.
                No more bee beards!
                With Bob Bumble at the anchor desk. Weather with Storm Stinger. Sports with Buzz Larvi. And Jeanette Chung.
                Good evening. I'm Bob Bumble.
                And I'm Jeanette Ohung.
                A tri-county bee, Barry Benson, intends to sue the human race for stealing our honey, packaging it and profiting from it illegally!
                Tomorrow night on Bee Larry King, we'll have three former queens here in our studio, discussing their new book, classy Ladies, out this week on Hexagon.
                Tonight we're talking to Barry Benson.
                Did you ever think, "I'm a kid from The Hive. I can't do this"?
                Bees have never been afraid to change the world.
                What about Bee Oolumbus? Bee Gandhi? Bejesus?
                Where I'm from, we'd never sue humans.
                We were thinking of stickball or candy stores.
                How old are you?
                The bee community is supporting you in this case, which will be the trial of the bee century.
                You know, they have a Larry King in the human world too.
                It's a common name. Next week...
                He looks like you and has a show and suspenders and colored dots...
                Next week...
                Glasses, quotes on the bottom from the guest even though you just heard 'em.
                Bear Week next week! They're scary, hairy and here live.
                Always leans forward, pointy shoulders, squinty eyes, very Jewish.
                In tennis, you attack at the point of weakness!
                It was my grandmother, Ken. She's 81.
                Honey, her backhand's a joke!
                I'm not gonna take advantage of that?
                Quiet, please.
                Actual work going on here.
                Is that that same bee?
                Yes, it is!
                I'm helping him sue the human race.
                Hello.
                Hello, bee.
                This is Ken.
                Yeah, I remember you. Timberland, size ten and a half. Vibram sole, I believe.
                Why does he talk again?
                Listen, you better go 'cause we're really busy working.
                But it's our yogurt night!
                Bye-bye.
                Why is yogurt night so difficult?!
                You poor thing. You two have been at this for hours!
                Yes, and Adam here has been a huge help.
                Frosting...
                How many sugars?
                Just one. I try not to use the competition.
                So why are you helping me?
                Bees have good qualities. And it takes my mind off the shop. Instead of flowers, people are giving balloon bouquets now.
                Those are great, if you're three.
                And artificial flowers.
                Oh, those just get me psychotic!
                Yeah, me too.
                Bent stingers, pointless pollination.
                Bees must hate those fake things!
                Nothing worse than a daffodil that's had work done.
                Maybe this could make up for it a little bit.
                This lawsuit's a pretty big deal.
                I guess.
                You sure you want to go through with it?
                Am I sure? When I'm done with the humans, they won't be able to say, "Honey, I'm home," without paying a royalty!
                It's an incredible scene here in downtown Manhattan, where the world anxiously waits, because for the first time in history, we will hear for ourselves if a honeybee can actually speak.
                What have we gotten into here, Barry?
                It's pretty big, isn't it?
                I can't believe how many humans don't work during the day.
                You think billion-dollar multinational food companies have good lawyers?
                Everybody needs to stay behind the barricade.
                What's the matter?
                I don't know, I just got a chill.
                Well, if it isn't the bee team.
                You boys work on this?
                All rise! The Honorable Judge Bumbleton presiding.
                All right. Case number 4475,
                Superior Court of New York,
                Barry Bee Benson v. the Honey Industry is now in session.
                Mr. Montgomery, you're representing the five food companies collectively?
                A privilege.
                Mr. Benson... you're representing all the bees of the world?
                I'm kidding. Yes, Your Honor, we're ready to proceed.
                Mr. Montgomery, your opening statement, please.
                Ladies and gentlemen of the jury, my grandmother was a simple woman. Born on a farm, she believed it was man's divine right to benefit from the bounty of nature God put before us.
                If we lived in the topsy-turvy world Mr. Benson imagines, just think of what would it mean.
                I would have to negotiate with the silkworm for the elastic in my britches!
                Talking bee!
                How do we know this isn't some sort of holographic motion-picture-capture Hollywood wizardry?
                They could be using laser beams! Robotics! Ventriloquism! Cloning! For all we know, he could be on steroids!
                Mr. Benson?
                Ladies and gentlemen, there's no trickery here. I'm just an ordinary bee. Honey's pretty important to me. It's important to all bees. We invented it! We make it. And we protect it with our lives.
                Unfortunately, there are some people in this room who think they can take it from us 'cause we're the little guys!
                I'm hoping that, after this is all over, you'll see how, by taking our honey, you not only take everything we have but everything we are!
                I wish he'd dress like that all the time. So nice!
                Call your first witness.
                So, Mr. Klauss Vanderhayden of Honey Farms, big company you have.
                I suppose so.
                I see you also own Honeyburton and Honron!
                Yes, they provide beekeepers for our farms.
                Beekeeper. I find that to be a very disturbing term.
                I don't imagine you employ any bee-free-ers, do you?
                No.
                I couldn't hear you.
                No.
                No. Because you don't free bees. You keep bees. Not only that, it seems you thought a bear would be an appropriate image for a jar of honey.
                They're very lovable creatures. Yogi Bear, Fozzie Bear, Build-A-Bear.
                You mean like this?
                Bears kill bees!
                How'd you like his head crashing through your living room?! Biting into your couch! Spitting out your throw pillows! OK, that's enough. Take him away.
                So, Mr. Sting, thank you for being here. Your name intrigues me. Where have I heard it before?
                I was with a band called The Police.
                But you've never been a police officer, have you?
                No, I haven't.
                No, you haven't. And so here we have yet another example of bee culture casually stolen by a human for nothing more than a prance-about stage name.
                Oh, please.
                Have you ever been stung, Mr. Sting? Because I'm feeling a little stung, Sting. Or should I say... Mr. Gordon M. Sumner!
                That's not his real name?! You idiots!
                Mr. Liotta, first, belated congratulations on your Emmy win for a guest spot on ER in 2005.
                Thank you. Thank you.
                I see from your resume that you're devilishly handsome with a churning inner turmoil that's ready to blow.
                I enjoy what I do. Is that a crime?
                Not yet it isn't. But is this what it's come to for you? Exploiting tiny, helpless bees so you don't have to rehearse your part and learn your lines, sir?
                Watch it, Benson! I could blow right now!
                This isn't a goodfella.
                This is a badfella!
                Why doesn't someone just step on this creep, and we can all go home?!
                Order in this court!
                You're all thinking it!
                Order! Order, I say!
                Say it!
                Mr. Liotta, please sit down!
                I think it was awfully nice of that bear to pitch in like that. I think the jury's on our side.
                Are we doing everything right, legally?
                I'm a florist.
                Right. Well, here's to a great team.
                To a great team!
                Well, hello.
                Ken!
                Hello.
                I didn't think you were coming.
                No, I was just late I tried to call, but... the battery.
                I didn't want all this to go to waste,
                so I called Barry. Luckily, he was free.
                Oh, that was lucky.
                There's a little left. I could heat it up.
                Yeah, heat it up, sure, whatever.
                So I hear you're quite a tennis player. I'm not much for the game myself. The ball's a little grabby.
                That's where I usually sit. Right... there.
                Ken, Barry was looking at your resume, and he agreed with me that eating with chopsticks isn't really a special skill.
                You think I don't see what you're doing?
                I know how hard it is to find the right job. We have that in common.
                Do we?
                Bees have 100 percent employment, but we do jobs like taking the crud out.
                That's just what I was thinking about doing.
                Ken, I let Barry borrow your razor for his fuzz. I hope that was all right.
                I'm going to drain the old stinger.
                Yeah, you do that.
                Look at that.
                You know, I've just about had it with your little Mind Games.
                What's that?
                Italian Vogue.
                Mamma mia, that's a lot of pages.
                A lot of ads.
                Remember what Van said, why is your life more valuable than mine?
                Funny, I just can't seem to recall that! I think something stinks in here!
                I love the smell of flowers.
                How do you like the smell of flames?!
                Not as much.
                Water bug! Not taking sides!
                Ken, I'm wearing a Chapstick hat!
                This is pathetic!
                I've got issues!
                Well, well, well, a royal flush!
                You're bluffing.
                Am I?
                Surf's up, dude!
                Poo water!
                That bowl is gnarly. Except for those dirty yellow rings!
                Kenneth! What are you doing?!
                You know, I don't even like honey! I don't eat it!
                We need to talk! He's just a little bee!
                And he happens to be the nicest bee I've met in a long time!
                Long time? What are you talking about?! Are there other bugs in your life?
                 No, but there are other things bugging me in life. And you're one of them!
                Fine! Talking bees, no yogurt night...
                My nerves are fried from riding on this emotional roller coaster!
                Goodbye, Ken.
                And for your information, I prefer sugar-free, artificial sweeteners made by man!
                I'm sorry about all that.
                I know it's got an aftertaste! I like it!
                I always felt there was some kind of barrier between Ken and me. I couldn't overcome it.
                Oh, well.
                Are you OK for the trial?
                I believe Mr. Montgomery is about out of ideas.
                We would like to call Mr. Barry Benson Bee to the stand.
                Good idea! You can really see why he's considered one of the best lawyers...
                Yeah.
                Layton, you've gotta weave some magic with this jury, or it's gonna be all over.
                Don't worry. The only thing I have to do to turn this jury around is to remind them of what they don't like about bees.
                You got the tweezers?
                Are you allergic?
                Only to losing, son. Only to losing.
                Mr. Benson Bee, I'll ask you what I think we'd all like to know.
                What exactly is your relationship to that woman?
                We're friends.
                Good friends?
                Yes.
                How good? Do you live together?
                Wait a minute... Are you her little... bedbug?
                I've seen a bee documentary or two. From what I understand, doesn't your queen give birth to all the bee children?
                Yeah, but...
                So those aren't your real parents!
                Oh, Barry...
                Yes, they are!
                Hold me back!
                You're an illegitimate bee, aren't you, Benson?
                He's denouncing bees!
                Don't y'all date your cousins?
                Objection!
                I'm going to pincushion this guy!
                Adam, don't! It's what he wants!
                Oh, I'm hit!! Oh, lordy, I am hit!
                Order! Order!
                The venom! The venom is coursing through my veins! I have been felled by a winged beast of destruction! You see? You can't treat them like equals! They're striped savages! Stinging's the only thing they know! It's their way!
                Adam, stay with me.
                I can't feel my legs.
                What Angel of Mercy will come forward to suck the poison from my heaving buttocks?
                I will have order in this court. Order! Order, please!
                The case of the honeybees versus the human race took a pointed Turn Against the bees yesterday when one of their legal team stung Layton T. Montgomery.
                Hey, buddy.
                Hey.
                Is there much pain?
                Yeah.
                I... I blew the whole case, didn't I?
                It doesn't matter. What matters is
                you're alive. You could have died.
                I'd be better off dead. Look at me.
                They got it from the cafeteria downstairs, in a tuna sandwich. Look, there's a little celery still on it.
                What was it like to sting someone?
                I can't explain it. It was all... All adrenaline and then...and then ecstasy!
                All right.
                You think it was all a trap?
                Of course. I'm sorry. I flew us right into this.
                What were we thinking? Look at us. We're just a couple of bugs in this world.
                What will the humans do to us if they win?
                I don't know.
                I hear they put the roaches in motels. That doesn't sound so bad.
                Adam, they check in, but they don't check out!
                Oh, my.
                Could you get a nurse to close that window?
                Why?
                The smoke.
                Bees don't smoke.
                Right. Bees don't smoke.
                Bees don't smoke!
                But some bees are smoking.
                That's it! That's our case!
                It is? It's not over?
                Get dressed. I've gotta go somewhere.
                Get back to the court and stall. Stall any way you can.
                And assuming you've done step correctly, you're ready for the tub.
                Mr. Flayman.
                Yes? Yes, Your Honor!
                Where is the rest of your team?
                Well, Your Honor, it's interesting. Bees are trained to fly haphazardly, and as a result, we don't make very good time.
                I actually heard a funny story about...
                Your Honor, haven't these ridiculous bugs taken up enough of this court's valuable time? How much longer will we allow these absurd shenanigans to go on?
                They have presented no compelling evidence to support their charges against my clients, who run legitimate businesses.
                I move for a complete dismissal of this entire case!
                Mr. Flayman, I'm afraid I'm going to have to consider Mr. Montgomery's motion.
                But you can't! We have a terrific case.
                Where is your proof?
                Where is the evidence?
                Show me the smoking gun!
                Hold it, Your Honor!
                You want a smoking gun? Here is your smoking gun.
                What is that?
                It's a bee smoker!
                What, this? This harmless little contraption? This couldn't hurt a fly, let alone a bee.
                Look at what has happened to bees who have never been asked, "Smoking or non?" Is this what nature intended for us? To be forcibly addicted to smoke machines and man-made wooden slat work camps?
                Living out our lives as honey slaves to the white man?
                What are we gonna do?
                He's playing the species card.
                Ladies and gentlemen, please, free these bees!
                Free the bees! Free the bees! Free the bees! Free the bees! Free the bees!
                The court finds in favor of the bees!
                Vanessa, we won!
                I knew you could do it! High-five!
                Sorry.
                I'm OK! You know what this means?
                All the honey will finally belong to the bees.
                Now we won't have to work so hard all the time.
                This is an unholy perversion of the balance of nature, Benson.
                You'll regret this.
                Barry, how much honey is out there?
                All right. One at a time.
                Barry, who are you wearing?
                My sweater is Ralph Lauren, and I have no pants.
                What if Montgomery's right?
                What do you mean?
                We've been living the bee way a long time, 27 million years.
                Congratulations on your victory. What will you demand as a settlement?
                First, we'll demand a complete shutdown of all bee work camps.
                Then we want back the honey that was ours to begin with, every last drop.
                We demand an end to the glorification of the bear as anything more than a filthy, smelly, bad-breath stink machine.
                We're all aware of what they do in the woods.
                Wait for my signal. Take him out.
                He'll have nauseous for a few hours, then he'll be fine.
                And we will no longer tolerate bee-negative nicknames...
                But it's just a prance-about stage name!
                ...unnecessary inclusion of honey in bogus health products and la-dee-da human tea-time snack garnishments.
                Can't breathe.
                Bring it in, boys!
                Hold it right there! Good.
                Tap it.
                Mr. Buzzwell, we just passed three cups and there's gallons more coming!
                I think we need to shut down!
                Shut down? We've never shut down.
                Shut down honey production!
                Stop making honey!
                Turn your key, sir!
                What do we do now?
                Cannonball!
                We're shutting honey production!
                Mission abort.
                Aborting pollination and nectar detail.
                Returning to base.
                Adam, you wouldn't believe how much honey was out there.
                Oh, yeah?
                What's going on? Where is everybody?
                Are they out celebrating?
                They're home.
                They don't know what to do. Laying out, sleeping in.
                I heard your Uncle Carl was on his way to San Antonio with a cricket.
                At least we got our honey back.
                Sometimes I think, so what if humans liked our honey? Who wouldn't?
                It's the greatest thing in the world! I was excited to be part of making it.
                This was my new desk. This was my new job. I wanted to do it really well. And now...
                Now I can't.
                I don't understand why they're not happy.
                I thought their lives would be better!
                They're doing nothing. It's amazing.
                Honey really changes people.
                You don't have any idea what's going on, do you?
                What did you want to show me?
                This.
                What happened here?
                That is not the half of it.
                Oh, no. Oh, my.
                They're all wilting.
                Doesn't look very good, does it?
                No.
                And whose fault do you think that is?
                You know, I'm gonna guess bees.
                Bees?
                Specifically, me.
                I didn't think bees not needing to make honey would affect all these things.
                It's not just flowers. Fruits, vegetables, they all need bees.
                That's our whole SAT test right there.
                Take away produce, that affects the entire animal kingdom.
                And then, of course...
                The human species?
                So if there's no more pollination, it could all just go south here, couldn't it?
                I know this is also partly my fault.
                How about a suicide pact?
                How do we do it?
                I'll sting you, you step on me.
                That just kills you twice.
                Right, right.
                Listen, Barry... sorry, but I gotta get going.
                I had to open my mouth and talk.
                Vanessa?
                Vanessa? Why are you leaving?
                Where are you going?
                To the final Tournament of Roses parade in Pasadena.
                They've moved it to this weekend because all the flowers are dying.
                It's the Last Chance I'll ever have to see it.
                Vanessa, I just wanna say I'm sorry.
                I never meant it to turn out like this.
                I know. Me neither.
                Tournament of Roses.
                Roses can't do sports.
                Wait a minute. Roses. Roses?
                Roses!
                Vanessa!
                Roses?!
                Barry?
                Roses are flowers!
                Yes, they are.
                Flowers, bees, pollen!
                I know.
                That's why this is the last parade.
                Maybe not.
                Could you ask him to slow down?
                Could you slow down?
                Barry!
                OK, I made a huge mistake.
                This is a total disaster, all my fault.
                Yes, it kind of is.
                I've ruined the planet. I wanted to help you with the flower shop. I've made it worse.
                Actually, it's completely closed down.
                I thought maybe you were remodeling.
                But I have another idea, and it's greater than my previous ideas combined.
                I don't want to hear it!
                All right, they have the roses, the roses have the pollen.
                I know every bee, plant and flower bud in this park.
                All we gotta do is get what they've got back here with what we've got.
                Bees.
                Park.
                Pollen!
                Flowers.
                Repollination!
                Across the nation!
                Tournament of Roses, Pasadena, California.
                They've got nothing but flowers, floats and cotton candy.
                Security will be tight.
                I have an idea.
                Vanessa Bloome, FTD.
                Official floral business. It's real.
                Sorry, ma'am. Nice brooch.
                Thank you. It was a gift.
                Once inside, we just pick the right float.
                How about The Princess and the Pea?
                I could be the princess, and you could be the pea!
                Yes, I got it.
                Where should I sit?
                What are you?
                I believe I'm the pea.
                The pea?
                It goes under the mattresses.
                Not in this fairy tale, sweetheart.
                I'm getting the marshal.
                You do that! This whole parade is a fiasco!
                Let's see what this baby'll do.
                Hey, what are you doing?!
                Then all we do is blend in with traffic... without arousing suspicion.
                Once at the airport, there's no stopping us.
                Stop! Security.
                You and your insect pack your float?
                Yes.
                Has it been in your possession the entire time?
                Would you remove your shoes?
                Remove your stinger.
                It's part of me.
                I know. Just having some fun.
                Enjoy your flight.
                Then if we're lucky, we'll have just enough pollen to do the job.
                Can you believe how lucky we are? We have just enough pollen to do the job!
                I think this is gonna work.
                It's got to work.
                Attention, passengers, this is Captain Scott. We have a bit of bad weather in New York. It looks like we'll experience a couple hours delay.
                Barry, these are cut flowers with no water. They'll never make it.
                I gotta get up there and talk to them.
                Be careful.
                Can I get help with the Sky Mall magazine? I'd like to order the talking inflatable nose and ear hair trimmer.
                Captain, I'm in a real situation.
                What'd you say, Hal?
                Nothing.
                Bee!
                Don't freak out! My entire species...
                What are you doing?
                Wait a minute! I'm an attorney!
                Who's an attorney?
                Don't move.
                Oh, Barry.
                Good afternoon, passengers. This is your captain. Would a Miss Vanessa Bloome in 24B please report to the cockpit? And please hurry!
                What happened here?
                There was a DustBuster, a toupee, a life raft exploded.
                One's bald, one's in a boat, they're both unconscious!
                Is that another bee joke?
                No!
                No one's flying the plane!
                This is JFK control tower, Flight 356. What's your status?
                This is Vanessa Bloome. I'm a florist from New York.
                Where's the pilot?
                He's unconscious, and so is the copilot.
                Not good. Does anyone onboard have flight experience?
                As a matter of fact, there is.
                Who's that?
                Barry Benson.
                From the honey trial?! Oh, great.
                Vanessa, this is nothing more than a big metal bee.
                It's got giant wings, huge engines.
                I can't fly a plane.
                Why not? Isn't John Travolta a pilot?
                Yes.
                How hard could it be?
                Wait, Barry!
                We're headed into some lightning.
                This is Bob Bumble. We have some late-breaking news from JFK Airport, where a suspenseful scene is developing.
                Barry Benson, fresh from his legal victory...
                That's Barry!
                ...is attempting to land a plane, loaded with people, flowers and an incapacitated flight crew.
                Flowers?!
                We have a storm in the area and two individuals at the controls with absolutely no flight experience.
                Just a minute. There's a bee on that plane.
                I'm quite familiar with Mr. Benson and his no-account compadres.
                They've done enough damage.
                But isn't he your only hope?
                Technically, a bee shouldn't be able to fly at all.
                Their wings are too small... Haven't we heard this a million times?
                "The surface area of the wings and body mass make no sense."
                Get this on the air!
                Got it.
                Stand by.
                We're going live.
                The way we work may be a mystery to you. Making honey takes a lot of bees doing a lot of small jobs.
                But let me tell you about a small job. If you do it well, it makes a big difference.
                More than we realized. To us, to everyone.
                That's why I want to get bees back to working together. That's the bee way! We're not made of Jell-O.
                We get behind a fellow.
                Black and yellow!
                Hello!
                Left, right, down, hover.
                Hover?
                Forget hover.
                This isn't so hard.
                Beep-beep! Beep-beep!
                Barry, what happened?!
                Wait, I think we were on autopilot the whole time.
                That may have been helping me.
                And now we're not!
                So it turns out I cannot fly a plane.
                All of you, let's get behind this fellow! Move it out!
                Move out!
                Our only chance is if I do what I'd do, you copy me with the wings of the plane!
                Don't have to yell.
                I'm not yelling! We're in a lot of trouble.
                It's very hard to concentrate with that panicky tone in your voice!
                It's not a tone. I'm panicking!
                I can't do this!
                Vanessa, pull yourself together. You have to snap out of it!
                You snap out of it.
                You snap out of it.
                You snap out of it!
                You snap out of it!
                You snap out of it!
                You snap out of it!
                You snap out of it!
                You snap out of it!
                Hold it!
                Why? Come on, it's my turn.
                How is the plane flying?
                I don't know.
                Hello?
                Benson, got any flowers for a happy occasion in there?
                The Pollen Jocks!
                They do get behind a fellow.
                Black and yellow.
                Hello.
                All right, let's drop this tin can on the blacktop.
                Where? I can't see anything. Can you?
                No, nothing. It's all cloudy.
                Come on. You got to think bee, Barry.
                Thinking bee.
                Thinking bee.
                Thinking bee!
                Thinking bee! Thinking bee!
                Wait a minute. I think I'm feeling something.
                What?
                I don't know. It's strong, pulling me.
                Like a 27-million-year-old instinct.
                Bring the nose down.
                Thinking bee!
                Thinking bee! Thinking bee!
                What in the world is on the tarmac?
                Get some lights on that!
                Thinking bee!
                Thinking bee! Thinking bee!
                Vanessa, aim for the flower.
                OK.
                Cut the engines. We're going in on bee power. Ready, boys?
                Affirmative!
                Good. Good. Easy, now. That's it.
                Land on that flower!
                Ready? Full reverse!
                Spin it around!
                Not that flower! The other one!
                Which one?
                That flower.
                I'm aiming at the flower!
                That's a fat guy in a flowered shirt.
                I mean the giant pulsating flower made of millions of bees!
                Pull forward. Nose down. Tail up.
                Rotate around it.
                This is insane, Barry!
                This's the only way I know how to fly.
                Am I koo-koo-kachoo, or is this plane flying in an insect-like pattern?
                Get your nose in there. Don't be afraid. Smell it. Full reverse!
                Just drop it. Be a part of it.
                Aim for the center!
                Now drop it in! Drop it in, woman!
                Come on, already.
                Barry, we did it! You taught me how to fly!
                Yes. No high-five!
                Right.
                Barry, it worked!
                Did you see the giant flower?
                What giant flower? Where? Of course
                I saw the flower! That was genius!
                Thank you.
                But we're not done yet.
                Listen, everyone!
                This runway is covered with the last pollen from the last flowers available anywhere on Earth.
                That means this is our Last Chance. We're the only ones who make honey, pollinate flowers and dress like this.
                If we're gonna survive as a species, this is our moment! What do you say?
                Are we going to be bees, or just Museum of Natural History keychains?
                We're bees!
                Keychain!
                Then follow me! Except Keychain.
                Hold on, Barry. Here. You've earned this.
                Yeah!
                I'm a Pollen Jock! And it's a perfect fit. All I gotta do are the sleeves.
                Oh, yeah.
                That's our Barry.
                Mom! The bees are back!
                If anybody needs to make a call, now's the time. I got a feeling we'll be working late tonight!
                Here's your change. Have a great afternoon! Can I help who's next?
                Would you like some honey with that?
                It is bee-approved. Don't forget these.
                Milk, cream, cheese, it's all me.  And I don't see a nickel!
                Sometimes I just feel like a piece of meat!
                I had no idea.
                Barry, I'm sorry.
                Have you got a moment?
                Would you excuse me?
                My mosquito associate will help you.
                Sorry I'm late.
                He's a lawyer too?
                I was already a blood-sucking parasite. All I needed was a briefcase.
                Have a great afternoon!
                Barry, I just got this huge tulip order, and I can't get them anywhere.
                No problem, Vannie. Just leave it to me.
                You're a lifesaver, Barry. Can I help who's next?
                All right, scramble, jocks! It's time to fly.
                Thank you, Barry!
                That bee is living my life!
                Let it go, Kenny.
                When will this nightmare end?!
                Let it all go.
                Beautiful day to fly.
                Sure is.
                Between you and me,
                I was dying to get out of that office.
                You have got to start thinking bee, my friend.
                Thinking bee!
                Me?
                Hold it. Let's just stop for a second. Hold it.
                I'm sorry. I'm sorry, everyone. Can we stop here?
                I'm not making a major life decision during a production number!
                All right. Take ten, everybody. Wrap it up, guys.
                I had virtually no rehearsal for that.
            """,
            author=user4_author,
            visibility='PUBLIC',
            page='http://localhost:8000'
        )

        user1_post1_comment1 = Comment.objects.create(
            author=user1_author,
            comment="# Im commenting on my first post.",
            contentType='text/markdown',
            id_url='{}api/authors/{}/commented/1'.format(NODEHOSTNAME, user1_author.id),
            post = user1_post_1
        )

        user2_post1_comment2 = Comment.objects.create(
            author=user2_author,
            comment="# Im commenting on john's first post.",
            contentType='text/plain',
            id_url='{}api/authors/{}/commented/2'.format(NODEHOSTNAME, user2_author.id),
            post = user1_post_1
        )

        user3_post1_comment3 = Comment.objects.create(
            author=user3_author,
            comment="Im commenting on John's first post too.",
            contentType='text/plain',
            id_url='{}api/authors/{}/commented/3'.format(NODEHOSTNAME, user3_author.id),
            post = user1_post_1
        )

        user1_post2_comment4 = Comment.objects.create(
            author=user1_author,
            comment="Im commenting on my second post now.",
            contentType='text/plain',
            id_url='{}api/authors/{}/commented/4'.format(NODEHOSTNAME, user1_author.id),
            post=user1_post_2
        )

        user2_post2_comment5 = Comment.objects.create(
            author=user2_author,
            comment="# Im commenting on john's second post.",
            contentType='text/markdown',
            id_url='{}api/authors/{}/commented/5'.format(NODEHOSTNAME, user2_author.id),
            post=user1_post_2
        )

        user3_post1_comment3 = Comment.objects.create(
            author=user3_author,
            comment="Im commenting on John's second post too.",
            contentType='text/plain',
            id_url='{}api/authors/{}/commented/6'.format(NODEHOSTNAME, user3_author.id),
            post=user1_post_2
        )

        user1_post3_comment7 = Comment.objects.create(
            author=user1_author,
            comment="Im tired of commenting on my own posts :(",
            contentType='text/plain',
            id_url='{}api/authors/{}/commented/7'.format(NODEHOSTNAME, user1_author.id),
            post=user1_post_3
        )

        user2_post3_comment8 = Comment.objects.create(
            author=user2_author,
            comment="Please stop posting john ion wanna comment no more.",
            contentType='text/plain',
            id_url='{}api/authors/{}/commented/8'.format(NODEHOSTNAME, user2_author.id),
            post=user1_post_3
        )

        user3_post3_comment9 = Comment.objects.create(
            author=user3_author,
            comment="Go kys john.",
            contentType='text/plain',
            id_url='{}api/authors/{}/commented/9'.format(NODEHOSTNAME, user3_author.id),
            post=user1_post_3
        )

        user1_post4_comment10 = Comment.objects.create(
            author=user1_author,
            comment="Go kys jacob.",
            contentType='text/plain',
            id_url='{}api/authors/{}/commented/10'.format(NODEHOSTNAME, user1_author.id),
            post=user1_post_4
        )

        user2_post4_comment11 = Comment.objects.create(
            author=user2_author,
            comment="Go kys jacob.",
            contentType='text/plain',
            id_url='{}api/authors/{}/commented/11'.format(NODEHOSTNAME, user2_author.id),
            post=user1_post_4
        )

        user3_post4_comment12 = Comment.objects.create(
            author=user3_author,
            comment="mannnnn",
            contentType='text/plain',
            id_url='{}api/authors/{}/commented/12'.format(NODEHOSTNAME, user3_author.id),
            post=user1_post_4
        )

        user1_post7_comment13 = Comment.objects.create(
            author=user1_author,
            comment="I wont even keep you-",
            contentType='text/plain',
            id_url='{}api/authors/{}/commented/13'.format(NODEHOSTNAME, user1_author.id),
            post=user1_post_7
        )

        user2_post7_comment14 = Comment.objects.create(
            author=user2_author,
            comment="I wont invite you to my second birthday party",
            contentType='text/plain',
            id_url='{}api/authors/{}/commented/14'.format(NODEHOSTNAME, user2_author.id),
            post=user1_post_7
        )

        user1_post1_like = Like.objects.create(
            author=user1_author,
            id_url='{}api/authors/{}/liked/1'.format(NODEHOSTNAME, user1_author.id),
            object=user1_post_1.id_url,
        )

        user2_post1_like = Like.objects.create(
            author=user2_author,
            id_url='{}api/authors/{}/liked/2'.format(NODEHOSTNAME, user2_author.id),
            object=user1_post_1.id_url,
        )

        user3_post1_like = Like.objects.create(
            author=user3_author,
            id_url='{}api/authors/{}/liked/3'.format(NODEHOSTNAME, user3_author.id),
            object=user1_post_1.id_url,
        )

        user1_post2_like = Like.objects.create(
            author=user1_author,
            id_url='{}api/authors/{}/liked/4'.format(NODEHOSTNAME, user1_author.id),
            object=user1_post_2.id_url,
        )

        user2_post2_like = Like.objects.create(
            author=user2_author,
            id_url='{}api/authors/{}/liked/5'.format(NODEHOSTNAME, user2_author.id),
            object=user1_post_2.id_url,
        )

        user3_post2_like = Like.objects.create(
            author=user3_author,
            id_url='{}api/authors/{}/liked/6'.format(NODEHOSTNAME, user3_author.id),
            object=user1_post_2.id_url,
        )

        admin_author_comment10_like = Like.objects.create(
            author=admin_author,
            id_url='{}api/authors/{}/liked/7'.format(NODEHOSTNAME, admin_author.id),
            object=user1_post4_comment10.id_url,
        )

        self.stdout.write(self.style.SUCCESS('Successfully added users and authors'))