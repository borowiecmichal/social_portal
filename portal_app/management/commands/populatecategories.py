from django.core.management.base import BaseCommand, CommandError

from portal_app.models import Category


class Command(BaseCommand):
    help = 'Creates default categories'


    def handle(self, *args, **options):
        cat1 = Category.objects.create(name='Motocykle')
        cat2 = Category.objects.create(name='Yamaha', upper_class_category=cat1)
        Category.objects.create(name='XJ6', upper_class_category=cat2)
        Category.objects.create(name='MT06', upper_class_category=cat2)
        Category.objects.create(name='R1', upper_class_category=cat2)
        Category.objects.create(name='Virago 535', upper_class_category=cat2)
        cat3 = Category.objects.create(name='Honda', upper_class_category=cat1)
        Category.objects.create(name='CBF500', upper_class_category=cat3)
        Category.objects.create(name='CBF600', upper_class_category=cat3)
        Category.objects.create(name='CB500F', upper_class_category=cat3)
        cat4 = Category.objects.create(name='KTM', upper_class_category=cat1)
        Category.objects.create(name='DUKE 390', upper_class_category=cat4)

        cat5 = Category.objects.create(name='Miasta')
        Category.objects.create(name='Rzeszów', upper_class_category=cat5)
        Category.objects.create(name='Warszawa', upper_class_category=cat5)
        Category.objects.create(name='Gdańsk', upper_class_category=cat5)
        Category.objects.create(name='Kraków', upper_class_category=cat5)

        self.stdout.write(self.style.SUCCESS('Successfully added categories'))
