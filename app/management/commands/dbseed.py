from django.core.management.base import BaseCommand

from app.models import (
    User,
    Event,
)


class Command(BaseCommand):
    help = 'Seed the data'

    def handle(self, *args, **kwargs):
        print('Seeding Database...')

        super_user = User.objects.create_superuser('super', 'super@gifty.com', '123', first_name='Super', last_name='User')
        user = User.objects.create_user('normal@gifty.com', 'normal@gifty.com', '123', first_name='Normal', last_name="User")

        event = Event.objects.create(title="Tyler's Borthday", exchange_date="1994-09-15", organizer=super_user)
        event.members.add(user, super_user)

        for i in range(10):
            User.objects.create_user(f'user-{i}@test.com', f'user-{i}@test.com', '123', first_name=f'User{i}', last_name='Test')

        print('Seeded the datas!')