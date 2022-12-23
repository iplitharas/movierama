import random


from django.core.management.base import BaseCommand
from movies.models import Movie
from config.settings import BASE_DIR
from django.core.files.base import File
from random import choice
from pathlib import Path
from dataclasses import dataclass
from django.contrib.auth import get_user_model


@dataclass
class SampleData:
    title: str
    file_path: Path
    desc: str
    genre: str
    year: str


class Command(BaseCommand):
    help = "Command for creating sample users and samples movies"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Cleaning previous sample movies.."))
        User = get_user_model()
        default_password = "password123"
        sample_usernames = ["bob", "alice", "france", "olivia"]

        User.objects.filter(username__in=sample_usernames).delete()
        random.shuffle(sample_usernames)
        sample_users = []
        for sample_username in sample_usernames:
            user = User(username=sample_username)
            user.set_password(default_password)
            user.save()
            sample_users.append(user)

        self.stdout.write(
            self.style.WARNING(
                f"Samples usernames: {sample_users} with password: {default_password}"
            )
        )
        samples_movies = [
            SampleData(
                title="Harry Potter and the Deathly Hallows: Part 2",
                file_path=BASE_DIR / "sample_data/covers/harry-potter.jpeg",
                desc="A clash between good and evil awaits as young Harry (Daniel Radcliffe),"
                " Ron (Rupert Grint) and Hermione (Emma Watson) prepare for a final battle against L"
                "ord Voldemort (Ralph Fiennes). Harry has grown into a steely lad on a mission to rid the "
                "world of evil. The friends must search for the Horcruxes that keep the dastardly w"
                "izard immortal. Harry and Voldemort meet at Hogwarts Castle for an epic showdown "
                "where the forces of darkness may finally meet their match.",
                genre="Fantasy",
                year="2011",
            ),
            SampleData(
                title="Star Wars: The Rise of Skywalker",
                file_path=BASE_DIR / "sample_data/covers/star-wars.png",
                desc="When it's discovered that the evil Emperor Palpatine did not die at the hands of Darth Vader, "
                "the rebels must race against the clock to find out his whereabouts. Finn and Poe lead the"
                " Resistance to put a stop to the First Order's plans to form a new Empire,"
                " while Rey anticipates her inevitable confrontation with Kylo Ren. Warning:"
                " Some flashing-lights scenes in this film may affect photosensitive viewers.",
                genre="Sci-fi/Action",
                year="2019",
            ),
            SampleData(
                title="Avengers: Endgame",
                file_path=BASE_DIR / "sample_data/covers/avengers.png",
                desc="Adrift in space with no food or water, Tony Stark sends a message to Pepper Potts as"
                " his oxygen supply starts to dwindle. Meanwhile, the remaining Avengers -- "
                "Thor, Black Widow, Captain America and Bruce Banner -- must figure out a way to bring b"
                "ack their vanquished allies for an epic showdown with Thanos -- "
                "the evil demigod who decimated the planet and the universe.",
                year="2019",
                genre="Action/Adventure",
            ),
            SampleData(
                title="Dr. No",
                file_path=BASE_DIR / "sample_data/covers/dr-no.png",
                desc="In the film that launched the James Bond saga, Agent 007 (Sean Connery) battles mysterious "
                "Dr. No,"
                " a scientific genius bent on destroying the U.S. space program."
                " As the countdown to disaster begins,"
                " Bond must go to Jamaica, where he encounters beautiful "
                "Honey Ryder (Ursula Andress), "
                "to confront a megalomaniacal villain in his massive island headquarters..",
                year="1962",
                genre="Action/Adventure",
            ),
            SampleData(
                title="Home Alone",
                file_path=BASE_DIR / "sample_data/covers/home-alone.png",
                desc="When bratty 8-year-old Kevin McCallister (Macaulay Culkin) acts out the night before a family"
                " trip to Paris, his mother (Catherine O'Hara) makes him sleep in the attic. After the "
                "McCallisters mistakenly leave for the airport without Kevin, he awakens "
                "to an empty house and assumes his wish to have no family has come true."
                " But his excitement sours when he realizes that two con men (Joe Pesci, Daniel Stern)"
                " plan to rob the McCallister residence, and that he alone must protect the family home.",
                year="1990",
                genre="Comedy",
            ),
            SampleData(
                title="The Grand Budapest Hotel",
                file_path=BASE_DIR / "sample_data/covers/budapest-hotel.png",
                desc="In the 1930s, the Grand Budapest Hotel is a popular European ski resort, "
                "presided over by concierge Gustave H. "
                "(Ralph Fiennes). Zero, a junior lobby boy, "
                "becomes Gustave's friend and protege. Gustave prides himself on providing "
                "first-class service to the hotel's guests, including satisfying the sexual needs "
                "of the many elderly women who stay there. When one of Gustave's lovers dies mysteriously,"
                " Gustave finds himself the recipient of a priceless painting and the chief suspect in her murder.",
                year="2014",
                genre="Comedy/Drama",
            ),
            SampleData(
                title="Interstellar",
                file_path=BASE_DIR / "sample_data/covers/interstellar.png",
                desc="In Earth's future, a global crop blight and second Dust Bowl are slowly rendering the "
                "planet uninhabitable. Professor Brand (Michael Caine), "
                "a brilliant NASA physicist, is working on plans to save mankind by transporting "
                "Earth's population to a new home via a wormhole. But first, Brand must send former "
                "NASA pilot Cooper (Matthew McConaughey) and a team of researchers through the wormhole"
                " and across the galaxy to find out which of three planets could be mankind's new home.",
                year="2014",
                genre=" Sci-fi/Adventure ",
            ),
            SampleData(
                title="The Imitation Game",
                file_path=BASE_DIR / "sample_data/covers/imitation.png",
                desc="In 1939, newly created British intelligence agency MI6 recruits Cambridge mathematics alumnus "
                "Alan Turing (Benedict Cumberbatch) to crack Nazi codes, including Enigma --"
                " which cryptanalysts had thought unbreakable. Turing's team, including Joan Clarke "
                "(Keira Knightley), analyze Enigma messages while he builds a machine to decipher them."
                " Turing and team finally succeed and become heroes, but in 1952, the quiet genius encounters"
                " disgrace when authorities reveal he is gay and send him to prison.",
                year="2014",
                genre="War/Drama",
            ),
            SampleData(
                title="The Theory of Everything",
                file_path=BASE_DIR / "sample_data/covers/theory-of-everything.png",
                desc="In the 1960s, Cambridge University student and future physicist Stephen Hawking (Eddie Redmayne)"
                " falls in love with fellow collegian Jane Wilde (Felicity Jones)."
                " At 21, Hawking learns that he has motor neuron disease. "
                "Despite this -- and with Jane at his side -- he begins an ambitious study of time, "
                "of which he has very little left, according to his doctor."
                " He and Jane defy terrible odds and break new ground in the "
                "fields of medicine and science, achieving more than either could hope to imagine.",
                year="2014",
                genre="Romance/Drama",
            ),
            SampleData(
                title="The Great Gatsby",
                file_path=BASE_DIR / "sample_data/covers/gatsby.png",
                desc="Midwest native Nick Carraway (Tobey Maguire) arrives in 1922"
                " New York in search of the American dream. Nick, a would-be writer, moves in next-door to "
                "millionaire Jay Gatsby (Leonardo DiCaprio) and across the bay from his cousin Daisy ("
                "Carey Mulligan) and her philandering husband, Tom (Joel Edgerton). Thus, Nick becomes "
                "drawn into the captivating world of the wealthy and -- "
                "as he bears witness to their illusions and deceits -- pens a tale of impossible "
                "love, dreams, and tragedy.",
                genre="Romance/Drama",
                year="2013",
            ),
            SampleData(
                title="The King's Speech",
                file_path=BASE_DIR / "sample_data/covers/the-kings-speech.png",
                desc="England's Prince Albert (Colin Firth) must ascend the throne as King George VI, "
                "but he has a speech impediment. Knowing that the country needs her husband to"
                " be able to communicate effectively, Elizabeth (Helena Bonham Carter) "
                "hires Lionel Logue (Geoffrey Rush), an Australian actor and speech therapist, "
                "to help him overcome his stammer. An extraordinary friendship develops between "
                "the two men, as Logue uses unconventional means to teach the monarch how to"
                " speak with confidence.",
                year="2010",
                genre="History/Drama",
            ),
            SampleData(
                title="Fight Club",
                file_path=BASE_DIR / "sample_data/covers/fight-club.png",
                desc="A depressed man (Edward Norton) suffering from insomnia meets a strange soap salesman named "
                "Tyler Durden (Brad Pitt) and soon finds himself living in his squalid "
                "house after his perfect apartment is destroyed. The two bored men form an "
                "underground club with strict rules and fight other men who are fed up with their"
                " mundane lives. Their perfect partnership frays when Marla (Helena Bonham Carter),"
                " a fellow support group crasher, attracts Tyler's attention.",
                year="1999",
                genre="Thriller/Drama",
            ),
        ]

        random.shuffle(samples_movies)
        for sample_movie in samples_movies:
            with sample_movie.file_path.open(mode="rb") as file:
                movie = Movie.objects.create(
                    author=choice(sample_users),
                    title=sample_movie.title,
                    desc=sample_movie.desc,
                    genre=sample_movie.genre,
                    year=sample_movie.year,
                )
                movie.cover = File(file, name=sample_movie.file_path.name)
                movie.save()

        self.stdout.write(
            self.style.SUCCESS("Successfully created #%d sample movies")
            % len(samples_movies),
        )
