from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from octofit_tracker.models import Team, Activity

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Nettoyage
        Activity.objects.all().delete()
        Team.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()

        # Création des utilisateurs super héros
        marvel_heroes = [
            {'username': 'ironman', 'email': 'ironman@marvel.com'},
            {'username': 'spiderman', 'email': 'spiderman@marvel.com'},
            {'username': 'captainamerica', 'email': 'captainamerica@marvel.com'},
        ]
        dc_heroes = [
            {'username': 'batman', 'email': 'batman@dc.com'},
            {'username': 'superman', 'email': 'superman@dc.com'},
            {'username': 'wonderwoman', 'email': 'wonderwoman@dc.com'},
        ]
        users = []
        for hero in marvel_heroes + dc_heroes:
            user, _ = User.objects.get_or_create(username=hero['username'], defaults={'email': hero['email']})
            user.set_password('password123')
            user.save()
            users.append(user)

        # Création des équipes
        marvel_team = Team.objects.create(name='Marvel')
        dc_team = Team.objects.create(name='DC')
        for user in users[:3]:
            marvel_team.members.add(user)
        for user in users[3:]:
            dc_team.members.add(user)

        # Création d'activités
        activities = [
            {'user': users[0], 'type': 'Running', 'duration': 30},
            {'user': users[1], 'type': 'Cycling', 'duration': 45},
            {'user': users[2], 'type': 'Swimming', 'duration': 60},
            {'user': users[3], 'type': 'Yoga', 'duration': 40},
            {'user': users[4], 'type': 'Walking', 'duration': 20},
            {'user': users[5], 'type': 'Running', 'duration': 50},
        ]
        for act in activities:
            Activity.objects.create(**act)

        self.stdout.write(self.style.SUCCESS('octofit_db a été peuplée avec des données de test super héros!'))
