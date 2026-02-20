import os
import django
import random
from django.contrib.auth.models import User
from octofit_tracker.models import Activity, Team

# Initialisation de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'octofit_tracker.settings')
django.setup()

def create_users(num_users=10):
    users = []
    for i in range(num_users):
        username = f'user{i+1}'
        email = f'user{i+1}@octofit.com'
        user, created = User.objects.get_or_create(username=username, defaults={'email': email})
        if created:
            user.set_password('password123')
            user.save()
        users.append(user)
    return users

def create_teams(users, num_teams=3):
    teams = []
    for i in range(num_teams):
        name = f'Team_{i+1}'
        team, _ = Team.objects.get_or_create(name=name)
        # Ajout de membres aléatoires
        members = random.sample(users, k=min(3, len(users)))
        for member in members:
            team.members.add(member)
        teams.append(team)
    return teams

def create_activities(users, num_activities=20):
    activity_types = ['Running', 'Cycling', 'Swimming', 'Yoga', 'Walking']
    for _ in range(num_activities):
        user = random.choice(users)
        activity_type = random.choice(activity_types)
        duration = random.randint(10, 120)  # minutes
        Activity.objects.create(user=user, type=activity_type, duration=duration)

def main():
    users = create_users()
    teams = create_teams(users)
    create_activities(users)
    print('Base de données peuplée avec des données de test.')

if __name__ == '__main__':
    main()
