from django.core.management.base import BaseCommand

from wizards.models import Wizard, Spell, Place

wizards = [
    ('Harry Blackstone Copperfield Dresden', 'Evocation'),
    ('Molly Carpenter', 'Illusion'),
]

places = [
    ('MacAnally\'s',),
    ('Carpenter House',)
]

spells = [
    ('Fuego', 'Makes stuff burn!')
]


class Command(BaseCommand):
    help = 'Creates initial data for each model'

    def handle(self, *args, **options):

        self.stdout.write('Creating wizards')
        for w in Wizard.objects.all():
            w.delete()
        for (name, school) in wizards:
            self.stdout.write('Creating {}'.format(name))
            Wizard.objects.create(name=name, school=school)

        self.stdout.write('Creating places')
        for p in Place.objects.all():
            p.delete()
        for (name,) in places:
            self.stdout.write('Creating {}'.format(name))
            Place.objects.create(name=name)

        self.stdout.write('Creating spells')
        for s in Spell.objects.all():
            s.delete()
        wizard = Wizard.objects.first()
        for (name, effect) in spells:
            self.stdout.write('Creating {}'.format(name))
            spell = Spell.objects.create(name=name, effect=effect)
            wizard.known_spells.add(spell)
            wizard.save()


        self.stdout.write(self.style.SUCCESS('All done!'))
