from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ....authors.models import Author
from ....follow.models import Follow
from ....posts.models import Post, Comment, Like

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

        # Create Authors
        admin_author = Author.objects.create(
            user=admin_user,
            displayName='admin',
            github='',
            profileImageURL='',
            page='',
            is_local=True,
            username='admin',
            state='ACTIVE',
            id_url='http://localhost:8000/api/authors/1',
        )

        user1_author = Author.objects.create(
            user=user1_user,
            displayName='John Doe',
            github='',
            profileImageURL='',
            page='',
            is_local=True,
            username='johndoe',
            state='ACTIVE',
            id_url='http://localhost:8000/api/authors/2'
        )

        user2_author = Author.objects.create(
            user=user2_user,
            displayName='Jane Doe',
            github='',
            profileImageURL='',
            page='',
            is_local=True,
            username='janedoe',
            state='ACTIVE',
            id_url='http://localhost:8000/api/authors/3'
        )

        user3_author = Author.objects.create(
            user=user3_user,
            displayName='Jacob',
            github='',
            profileImageURL='',
            page='',
            is_local=True,
            username='jacob',
            state='ACTIVE',
            id_url='http://localhost:8000/api/authors/4'
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
            id_url='http://localhost:8000/api/authors/2/posts/1',
            description='Post 1 description',
            contentType='text/plain',
            content='POST 1 Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
            author=user1_author,
            visibility='PUBLIC'
        )

        # public text/markdown post by user1
        user1_post_2 = Post.objects.create(
            title='Post 2',
            id_url='http://localhost:8000/api/authors/2/posts/2',
            description='Post 2 description',
            contentType='text/markdown',
            content='# POST 2 \n'+
                    '- Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
            author=user1_author,
            visibility='PUBLIC'
        )

        # public image/png;base64 post by user1
        user1_post_3 = Post.objects.create(
            title='Post 3',
            id_url='http://localhost:8000/api/authors/2/posts/3',
            description='Post 3 description',
            contentType='image/png;base64',
            content='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',
            author=user1_author,
            visibility='PUBLIC'
        )

        # Unlisted text/plain post by user1
        user1_post_4 = Post.objects.create(
            title='Post 4',
            id_url='http://localhost:8000/api/authors/2/posts/4',
            description='Post 4 description',
            contentType='text/plain',
            content='POST 1 Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
            author=user1_author,
            visibility='UNLISTED'
        )

        # public text/markdown post by user1
        user1_post_5 = Post.objects.create(
            title='Post 5',
            id_url='http://localhost:8000/api/authors/2/posts/5',
            description='Post 5 description',
            contentType='text/markdown',
            content='# POST 5 \n' +
                    '- Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
            author=user1_author,
            visibility='UNLISTED'
        )

        # public image/png;base64 post by user1
        user1_post_6 = Post.objects.create(
            title='Post 6',
            id_url='http://localhost:8000/api/authors/2/posts/6',
            description='Post 6 description',
            contentType='application/base64',
            content='UklGRs4SAABXRUJQVlA4IMISAABwXQCdASotAagAPpE+m0mloyKhKlBMiLASCWVu3V0SHMxso6sc8u8YPUyIFcxtWEFbiPQ2GGRUTSAezSmy7pDt0L9lCW+oqGeVnSYl4L2iar0dCGASnD3iXtey7nvRQE6UCIQ8+TCvbOriUcfjNgt2cYtq7DjSeCsoEymQBkpP/fywKJq4ZQ7RpN0zX7UXn0B2nzcN9A9zRI+yxslIirl/NiOnGyTlhga2ynbkksCq8QCCwYu6n12Edy37712iGoHixYoSaGwB1l8tOLKYeEqmESOSv7+C2HxvakY6rwvOOouKLc9E/61rfLWXxYIcWLINF/KV3byDOEuKOVp2V1Poy9ZrkPQTe2xchqXTdDl8CEt+sw0Wbt0zrHZKItEAT2H2gR6/7zY4oFmXrTKQ5h6ATSygNbMuU6AizX+lV/o/A5HEu9YN50jre7d4pROb5NedpN6f61fx4/uYDqeI5Fhdztr9rdmAIC22Oy8XEW67YuN2zthjsXwYdfiO6bfI/EVb4gJa4zeVsb5VQ7qG+0mgEr1jQgblBDu9qytWbcG/jlRESXei2ckAqZaRK0XpNvonpkpgmJLUfUFlfroj31PTVM4fyOQbhQ7HPfmHknp3GnuVWZ+uPfSOtUQvv/ueXLkxT23m3EaXYWXrwLvLMjcAZkpPOvehnriIrJtEIYyP66nyiI1E7ouAf0g89cP4idRbQ/QZ//+Kw/FBz9T3h3FSHfuOLCGIVDorszN9gL0EOK7JFxaO8WVVZynKGQyce2w9hfx5UCoHa8e9x45OLHvRNVbGVPzQuhVaOtjiaObhxywaiW1DXm8Va+Ez8MZUp5w9GZVioVuCpV8DA3F+0IDlqRJZsNMQj2HOZk8X3MFGkeLQSxl18hZzS48ffLr6DZ+HJKLl/aN4qdyNya73r6Kfw2vuPNa28S6z1nNwIwlGokptV15qfWCX2dgEYSOyul7BZC8LmLWPDE1EPgJD3iJiBul4fc/tO3ytavY6bCuuDSqpYugA/vtTmW/zpA+Nrd+9j3aNl7L0nvhYTxbfD+TgwmHIr23Q0S9Pz/4DkuH2/t2NCx/eFtC/KDvocF0xKK9k/TqugT02aEcbcgBXa3H5v0gyKBy6V9xoa7j3MPnSQmmPsAAXOf7Y2bFls1MipTjuHG10TGngNjFEZVNKLxx7OjFLNiCn5B4bgCttIexRFp/XRHer3bc4WOZy4JGBANuQr85iLUptz3kU22l2EpLl3YwWAxEsVYxB9SPZOMXZQf9nNlPTagOuv5YyA6j/oyeWBZHqytERbEQRjmE3zqZjdvjfUcYsYKo0BonxaSWtAIE3T72zf6Y2PKtlKVv4m0UXNwN2PF4vEaG3Lrf64pXaKJBh1Wt7XXC5VahRp4y/4saA1R81A2S5hP+ZwofWhihyqp+fSIPE2nay3BQRPa21A7FhJLnWNvc9zbaL+dU3xcWcOLoFq5DA8x5qMZ02tIKZjTD0YdqeSJpaenZo5yYoOBnY0kBpB7YhE8Qt2g+s+mTBaUdYzFpbB0Y7tHPE3WysyJYAx3WdEtzaj9krh3+TgT3p/Lg2qaxx3Ghg2PRR51eraRIuPdnwPw7ZI8NgxfqYxP5GJ4XZ9OpygFA7xBfdpbjxwEqHEzARnws/nh6y9StP5ECFjSBeyC+4QoJaEj3rsu9eTE3TEe9aEFHuC/0mOt7uGkBdN143fIDeqfLQ3KLWDQtXz/cP7sq9/vPcWdqi3yq+qrWq4DDiiFmj39i48yrFBZqrMcQ4ExJvnL/altqQNUcDIIkH34Jqx9vVOvOmX6lyB8CGdF3NNBEAUc2Lnm9SYUdTqLBPynsgMyTLASU15XsKh89QE7YvACduMfRlN/36dzngVHB6YYszJtYXBX0fhnm+h3fHKeblORIX8cYGK2sy6hidAzUJ3+y6x2jq+QZDjVH9B+4roNsFsNOryaDn3uNKatzW5GQrUMerx/mpNlOXDv3anx/Wl1N5I6mRXB1EctHNk8Q5Zgk4J5n9alD1s98oFuWPu1XfOWmthxJgc9CvfVmyHAOQCnlDO4JADEM7IrM8YQnaQDoumPUV9/feCef+ZxtBR7pzAny0q2hUZyxa/txn8b26eqcgBbQ3O7ScPw4CciSIMkfrjOBol0u+PbuTp+EPjrQ45eP1PV4Nc9hALVb9QH0A2Y+v+Vyt34nrziG/7sEPsRCWiM9n5FL7YaXYMYV1YG4c17G6V6DfcgL+8xHK1v0qqhf4Z3mxMxrziXbkLUikNuVm7y30SoLhDK+VqxAOoz4KPiT6Y/OQqzmd04JoEHLJs2nIdmE6EtU4YT6m3ObShmRs2XNpLPnINzO3BihemKD3EDqTRF/S/+ydrNhBER1C1QUEFgsfWwowkjOMax9L5WhcFq0H/Q5TAFEemaf2gqFtlP4hgk/dmHscL7ESNFCwnRo8BxQzh2htaxUHuwSQNs8oxQhuX4WG8HRD9XpyIeLlZk0JsgPgWQtDncYQE2Ny8nNqDcJPVJ/1RZkRxssayPOGH4+mlv66GefG5xw9hmOfE6PEz+/oUhFOQRaeXRw1/jeqk0geeAVw98AVKBhuxVEu6AzRSjW3KkAQMVPN8J+Tqm86zLPt5oCXJ7z7xxCtNB7gNB2SrEzozzW8JbanuKYzDS8wGbR3WUlt1MWCfSpDUGFJ+Aug46k2yrS3U3m7o3ZC+yhNxRP5wPBjQ96GvZpjhceOp6jarJdr60is6nZlw891E6C9+Dl8wblIM7bKhdJMGqOm41NbQHNagoFB3T6fvjPL9qmKAOvTiKwo/N9iW/DosnPqlDYvVe/JjSJVzE3VmKbgf8O7+wPFG4UyswJfdp29qKqhHQ13/mjrcpgQFV1jhbD8KqLZqCgwWmTKzJiYMEI0NcLoCpJ6SMnLYLQnYRi93kKmkXvGw4zCzsi0tXY/OQIieQAJk6sk6TD8eeogpf4I4r0+4SHXTQDELFBBbTvd7/lsrXuuLJzTlZ8ZdTN8ciymF7xbj3K1c0RYYNo+00Kjzexi/3RgO1LtMooyLsAiIIll1QZDVyYMM+dbbzbYLEjZzpycnxf4EDuV3XNeQ4/5a034ZMsRfXOEySTfB52gDIDgU0qdhIQZ0W754s5mr9JwkQB5WagpTKxgZko3hgLF4LneKsmJ3lIYj/M2kcWv7JztSPn6G3QNujEXRgAR9qLBQyABDyRtsIGNSqca/EyNi15eG8oGkxmB1YBz0q0WBbWGFIdqn62Jy0pKNHKuRUCF/DqHRuFYnG1v+2KuqDQKCoSAe4gkERjqBnFUWmA8ByHhhHHJ0qJEfFqrJ0psDOSXVj7zOitkj0+xIesVqIehZGh/vgHO13hX8xGT545yUj3kFM3yQbXHh7aZe7zTe8as/R9axusyvYXGZjXmDuRgeElX5xT5V5bK9eAuRYczJDJ8P6+qAx+8aP/12/9nSEmttZbDpO5QEaahs7W3j9tZuDrb009k7d/Z9ASUPtbtRm8nUORRU3x5pbBr1KjC8dO45ZZV/YrTqws1fwjXvB3U3fNtwXS8dwiTz3A6DFmBV/fWW8I5KbkwiElXI0P0LMyO5pxkYB2x62SFsvSTTJXdYvZRRgytlIZehsMIxtvVCwETaQiZbI1xmVd5vMeMiXpfD+1c8CW+m6UfKjeIV9FjraxEPvr+QhseHuNzgQ8nEmy8Xx6SMfJwTzG6uGRM18eKINWQbBq3go7ZqaFfa+zkiF39+APWeNJwDs58dZlCan6uvP3BZ8Ljf9KwKvN2CtCKhy+8wssvC3IY1Q+byIyyNsHgkdXU8BtEmIXjoCDySwGsJFos278jCCBC+kAWWzuqiXq538oaV4o8DsEoW/BoBQ6mtAdV5fM3cHI2hxj07TbqFT6iuAD+kwlfGH743rehLJPyPea8dzrmpcj7JV+jGlVr+DHiZ2N9VncabGidFRCON+9RPPBg7HR/duD1aRo20UIpeBU0nc22apdzPTgKDw64G+XyIgowujmrTao0WHltreXjZUfS9zS1Q5l/SNQzkXYpQ5d/oLik1gGVG/YzvvwqMzMMiElpf2FFFMDx0F0cp9C60RG6bejVJ3N4gQeSOIiCFA29XyIrE8fQfuiCimPnZPocAGw1LmNWSX/R0D+9LB/nYuD3tL0dJGAFzfMBez4LwVxs6GEQftZJJSfWxJtGIhyGlP9YpSSgT4G3DYKlZKEx1dY4Oj2M/XLPRPoSdpNG3oHhoncJNiZvSrUZ7psI4AOQWnu6HBaG4VcGC8NKiEbgOBpfeYsk+NRE1ptGmxz06s41MRb7Tk2x4DmTj+pgBs634Aa1AH9sVkMzi63BayDVYV/oohQHw2jQyFJG/9oL7euVtsF0X/r9y40DBeDQ8FpnxXYRgVIEvNEm3WresHxwjzfPytZSsbX6Em5I+6P1YxoJKzk7o1f9zDnGAiEy0SGAhvNfnmGjQIqtbJ5jn8lampXKvsT8fk2K0779AEhCuHHwqRBPzZPVfYlfI00AhDSHEKDh1xdOtpkDS9VWYA8ULHcIpY1pkyASi0QaCbbb95MVBPCDqgWN2oPocjkTVfQHOCFBl7vcks06VH5ewiUpqI5IbLlcT3UzjVCGSL371ucLPo3GW3hOzJzafKh9btFPUNLGA7zWXLCinWZKw03pqiis8Mw4EC8hrsSegwwEv7ufEd6HvsgUXvim/5NgVfXHvG9PS6KYL4eA6nqvMAEMMoyUK4Hdic//I0ubAv/2Uxk6nJooyXfoF47Op803DCU9iqJykiwl+Yo7bPjMVvInDwP/Rwv3kIWhJyFT3s9iM6lOePW/BZRS/aabRd77DMgYMWPO2Xo4xbFPd3U3c7Yi4moGP5lq4s8JHzIWm1gUv5E97oKjIl5QYPKOkasN62e9lLlh39XRlnNjP0dPKaAX4wdZGIss8zEXslXvh7ORQbEKeohE3eY5AuXwort+VQeKPcKzAUxTSZHYnLLs/naQLs3jf5C8TL0XE5/14lwzgFwX6W7WaOm4dT8o0ZGtu9wLncrmrkjm5Ft4e+YD4IXNmlnRM+bwON3NFXp9nAmehUETT5ssUtqBFrDvd91xrCZOdbaNedgxMm9LMnmSZZG7vT48SN1tncq8k3geBuRiPkEEyC8vh+PyRr4ayTMq19fXpjYYs7xKboSLz8lH3VZATGcDaOU0Wmr6C2vfwEfPil9RQPs2p3oKYiCCyEPLiCom6ZSW4uMe4u0WL40FHL5itGCyaZf6GIXxyT4yNQ4pdwpktQW/WdrAG/9HJjUnzZag/Uexb8NPztLDz49JlEjLwiLTP4BuV9JUjOetHpcCl0R9QXCTgmYh6FBOdQ25oPQtVFp7/viZbtuvLz6Qde5OcgsDHngaAM+PQ7FWyAePsNhX8Na7FxFe4gx+lV0pNIYLhicZoD0mS9l2/vX2nAhjHRxksEsMLfx2XmZix39sv91hS4nEsNvUwk27Zqa/FPow7aDIddwmzkxpVIk13ezM96RzCNOJOTJe3LYEbyDu6rRXpyaGu3XCizlsOGiLPzlPtWL+DRjY17tmLVB/4DZUxaTiCGUpBId7w5QnH+wjBvJS1ENWYwGl45kZ0vZFAd6zRddwA6QTBUYMvr6x6pnpmO9keSuYBkFjXXShyDDEChhCW1pA+mma+hqYVABt0O3LCgwE39B+xsKs4zN5ZCPUr3Ukzh/OFFFCb7M7NDxxyP5KjEZMfQe2eKDm/sy5zmfGHakxl/2gSHmD8CZZt2yqQf7iVHnFYnnTOe6+c3+lvLSzEhO/0tPQ+1zzsT+/pGj4a71a/Uc0d9Sb+U5W4mcfvPH9Jvsx3FRzqZFx+j/SHUxkvm+Ffn6icXujahsJCSlbMl7vnYEMVS5eQP1PR8VboYZfKLXbs1AdVBjHpM+GzL0nbjaQbrK2Wzo/HnIHOTcxMEhpHdYQ4rCEipuTba2mi9/S74s0reg91a3nYQMdZEgqYowODp85Z4R9m4/MKkUp832VGjqy/LGAOm+DVDkFK+4xcRlpCwyPg8ww+JVCGX/k8aoPt5gb59iEcY++pcCHVgna3se/khZHFAjkIBe3Y+k8d55mhUo22E04Edt8WI3GzB92fs3g7RWm6EEulSxwCpc4v+IswbFLy3RM6pt2un34E5M2S5jmWUkgHFOWF4JtFxlGJ7zRc0GbwCrXp8fZgJKU+Hi4C5UDVJfJ9U+zH90KcBqiQOAn2fQJkKB24D/wHxJ71YrzR+u4AifoKztl4TtA3wCKXaWHSI8FMJg4RvxoUeD+Tk2Ky7TPX1OQPYwKe5KSUaLby9pGM0pskahpwN83Rm3a/RNofHxwzfX2TdM4r6Ouc2Cu1PiV0B3INhIpp9fMrrifEUHqagXQt74oogfb8O6Ieoqn5eNgBaJtK1N/R52/gkokikUjFkr202EkQML1CM/ABoAAAA==',
            author=user1_author,
            visibility='UNLISTED'
        )

        user1_post_7 = Post.objects.create(
            title='Post 7',
            id_url='http://localhost:8000/api/authors/2/posts/7',
            description='Post 7 description',
            contentType='text/plain',
            content='POST 7 Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
            author=user1_author,
            visibility='FRIENDS'
        )

        user1_post_8 = Post.objects.create(
            title='Post 8',
            id_url='http://localhost:8000/api/authors/2/posts/8',
            description='Post 8 description',
            contentType='text/plain',
            content='POST 8 Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
            author=user1_author,
            visibility='DELETED'
        )

        user2_post_9 = Post.objects.create(
            title='Post 9',
            id_url='http://localhost:8000/api/authors/2/posts/9',
            description='Post 9 description',
            contentType='text/markdown',
            content='# POST 9 \n' +
                    '- Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
            author=user2_author,
            visibility='FRIENDS'
        )

        user3_post_10 = Post.objects.create(
            title='Post 10',
            id_url='http://localhost:8000/api/authors/2/posts/10',
            description='Post 10 description',
            contentType='text/markdown',
            content='# POST 10 \n' +
                    '- Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
            author=user3_author,
            visibility='DELETED'
        )

        self.stdout.write(self.style.SUCCESS('Successfully added users and authors'))