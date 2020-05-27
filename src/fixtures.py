def generate_presents(session):
    import random
    from models.present import Present
    from faker import Faker
    faker = Faker()
    friends_ids = list(range(1, 5000))
    client_ids = list(range(1, 2500))
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
        session.add(present)
    session.commit()


def parse_profile(profile):
    username = profile['username']
    name = profile['name'].split(' ')[0]
    surname = ' '.join(profile['name'].split(' ')[1:])
    mail = profile['mail']
    address = profile['address']
    sex = profile['sex']
    birth_date = profile['birth_date']
    return username, name, surname, mail, address, sex, birth_date


def generate_clients(session):
    from faker import Faker
    from models.client import Client
    faker = Faker()
    usernames = []
    mailes = []
    for i in range(1, 2501):

        profile = faker.simple_profile()
        while profile['username'] in usernames or profile['mail'] in mailes:
            print('generating profile')
            profile = faker.simple_profile()
        username, name, surname, mail, address, sex, birth_date = parse_profile(profile)
        client = Client()
        client.username = username
        client.name = name
        client.surname = surname
        client.mail = mail
        client.address = address
        client.sex = sex
        client.birth_date = birth_date
        client.client_id = i
        session.add(client)
        usernames.append(username)
        mailes.append(mail)
    session.commit()


def generate_friends(session):
    from faker import Faker
    from models.friend import Friend
    faker = Faker()
    usernames = []
    mails = []
    for i in range(1, 5001):

        profile = faker.simple_profile()
        while profile['username'] in usernames or profile['mail'] in mails:
            print('generating profile')
            profile = faker.simple_profile()
        username, name, surname, mail, address, sex, birth_date = parse_profile(profile)
        friend = Friend()
        friend.username = username
        friend.name = name
        friend.surname = surname
        friend.mail = mail
        friend.address = address
        friend.sex = sex
        friend.birth_date = birth_date
        friend.friend_id = i
        session.add(friend)
        usernames.append(username)
        mails.append(mail)
    session.commit()


def generate_friend_groups(session):
    from models.friend_group import FriendGroup
    for i in range(2000):
        friend_group = FriendGroup()
        friend_group.friend_group_id = i
        session.add(friend_group)
    session.commit()


def generate_friend_group_records(session):
    from models.friend_group_record import FriendGroupRecord
    import random
    friends = list(range(1, 5001))
    groups = list(range(1, 2000))
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
    for i in range(1, 2500):
        client_group = ClientGroup()
        client_group.client_group_id = i
        session.add(client_group)
    session.commit()


def generate_client_group_records(session):
    from models.client_group_record import ClientGroupRecord
    import random
    clients = list(range(1, 2501))
    groups = list(range(1, 2500))
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
    client_groups = list(range(1, 2500))
    for i in range(1, 2500):
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
    clients = list(range(1, 2501))
    friend_groups = list(range(1, 2000))
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
