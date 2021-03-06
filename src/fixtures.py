from api.utils import get_random_date


def generate_presents(session):
    import random
    from models.present import Present
    from faker import Faker
    import datetime
    faker = Faker()
    friends_ids = list(range(1, 5000))
    client_ids = list(range(1, 3001))
    start_date = datetime.datetime(2015, 1, 1)
    end_date = datetime.datetime.now()
    for i in range(1, 2000):
        _from = random.choice(client_ids)
        to = random.choice(friends_ids)
        returned = random.choice([True, False])
        title = random.choice(faker.text().split(' '))
        present = Present()
        present.to = to
        present.returned = returned
        present._from = _from
        present.title = title
        present.date = get_random_date(start_date, end_date)
        session.add(present)
    session.commit()


def parse_profile(profile):
    username = profile['username']
    name = profile['name'].replace('Mr.', '').replace('Mrs.', '').strip().split(' ')[0]
    surname = ' '.join(profile['name'].replace('Mr.', '').replace('Mrs.', '').strip().split(' ')[1:])
    mail = profile['mail']
    address = profile['address']
    sex = profile['sex']
    birth_date = profile['birth_date']
    return username, name, surname, mail, address, sex, birth_date


def generate_profiles(session):
    from faker import Faker
    from models.profile import Profile
    from password_generator import PasswordGenerator
    faker = Faker()
    pwo = PasswordGenerator()
    usernames = []
    mails = []
    for i in range(0, 8000):
        profile = faker.simple_profile()
        while profile['username'] in usernames or profile['mail'] in mails:
            print('generating profile')
            profile = faker.simple_profile()
        username, name, surname, mail, address, sex, birth_date = parse_profile(profile)
        profile = Profile()
        profile.username = username
        profile.name = name
        profile.surname = surname
        profile.mail = mail
        profile.address = address
        profile.sex = sex
        profile.birth_date = birth_date
        profile.password = pwo.generate()
        profile.profile_id = i + 1
        session.add(profile)
        usernames.append(username)
        mails.append(mail)
    session.commit()


def generate_clients(session):
    from faker import Faker
    from models.client import Client
    import random
    faker = Faker()
    profile_ids_available = list(range(5001, 8001))
    profiles_used = []
    for i in range(1, 3001):
        profile_id = random.choice(profile_ids_available)
        while profile_id in profiles_used:
            profile_id = random.choice(profile_ids_available)
        client = Client()
        client.profile_id = profile_id
        client.client_id = i
        session.add(client)
        profiles_used.append(profile_id)

    session.commit()


def generate_friends(session):
    from faker import Faker
    import random
    from models.friend import Friend
    faker = Faker()
    profile_ids_available = list(range(1, 5001))
    profiles_used = []
    for i in range(1, 5001):
        profile_id = random.choice(profile_ids_available)
        while profile_id in profiles_used:
            profile_id = random.choice(profile_ids_available)
        friend = Friend()
        friend.friend_id = i
        friend.profile_id = profile_id
        session.add(friend)
        profiles_used.append(profile_id)
    session.commit()


def generate_friend_groups(session):
    from models.friend_group import FriendGroup
    for i in range(1, 2001):
        friend_group = FriendGroup()
        friend_group.friend_group_id = i
        session.add(friend_group)
    session.commit()


def generate_friend_group_records(session):
    from models.friend_group_record import FriendGroupRecord
    import random
    friends = list(range(1, 5001))
    groups = list(range(1, 2001))
    for i in range(4000):

        friends_selected = random.choices(friends, k=random.choice([2, 3, 4, 5, 6, 7, 8]))
        friend_group_id = random.choice(groups)
        for friend in friends_selected:
            friend_group_record = FriendGroupRecord()
            friend_group_record.friend_id = friend
            friend_group_record.friend_group_id = friend_group_id
            session.add(friend_group_record)
    session.commit()


def generate_client_groups(session):
    from models.client_group import ClientGroup
    for i in range(1, 2501):
        client_group = ClientGroup()
        client_group.client_group_id = i
        session.add(client_group)
    session.commit()


def generate_client_group_records(session):
    from models.client_group_record import ClientGroupRecord
    import random
    clients = list(range(1, 3001))
    groups = list(range(1, 2501))
    for i in range(4000):

        clients_selected = random.choices(clients, k=random.choice([2, 3, 4, 5, 6, 7, 8]))
        client_group_id = random.choice(groups)
        for client in clients_selected:
            client_group_record = ClientGroupRecord()
            client_group_record.client_id = client
            client_group_record.client_group_id = client_group_id
            session.add(client_group_record)
    session.commit()


def generate_complaints(session):
    import random
    from models.complaint import Complaint
    from faker import Faker

    faker = Faker()
    friends = list(range(1, 5001))
    client_groups = list(range(1, 2501))
    for i in range(1, 2501):
        complaint = Complaint()
        complaint.friend = random.choice(friends)
        client_group = random.choice(client_groups)
        complaint.client_group = client_group
        complaint.date = faker.date_between(start_date='-1y', end_date='today')
        complaint.complaint_id = i
        client_groups.remove(client_group)
        session.add(complaint)
    session.commit()


def generate_meetings(session):
    import random
    from models.meeting import Meeting
    from faker import Faker

    faker = Faker()
    clients = list(range(1, 3001))
    friend_groups = list(range(1, 2001))
    for i in range(1, 5000):
        meeting = Meeting()
        meeting.client_id = random.choice(clients)
        meeting.friend_group_id = random.choice(friend_groups)
        meeting.date = faker.date_between(start_date='-1y', end_date='today')
        session.add(meeting)
    session.commit()


def generate_holidays(session):
    import random
    from models.holiday import Holiday
    import datetime
    from faker import Faker

    faker = Faker()
    friends = list(range(1, 5001))
    for i in range(1, 4000):
        start_date = faker.date_between(start_date='-1y', end_date='today')
        end_date = faker.date_between(start_date=start_date, end_date='today')
        while end_date - start_date >= datetime.timedelta(days=30):
            start_date = faker.date_between(start_date='-1y', end_date='today')
            end_date = faker.date_between(start_date=start_date, end_date='today')
        holiday = Holiday()
        holiday.friend_id = random.choice(friends)
        holiday.start_date = start_date
        holiday.end_date = end_date
        session.add(holiday)
    session.commit()


def generate_users(session):
    import random
    from models.user import User
    clients = list(range(1, 3001))
    friends = list(range(1, 5001))
    for i in range(1, 8001):
        clients_or_friends = random.choice(['C', 'F'])

        if clients_or_friends == 'C' and len(clients) == 0:

            clients_or_friends = 'F'

        elif clients_or_friends == 'F' and len(friends) == 0:

            clients_or_friends = 'C'
        user = User()
        user.user_id = i
        if clients_or_friends == 'C':
            role_id = random.choice(clients)
            user.client_id = role_id
            clients.remove(role_id)

        if clients_or_friends == 'F':
            role_id = random.choice(friends)
            user.friend_id = role_id
            friends.remove(role_id)
        session.add(user)

    session.commit()
