from analysis.models import Corpus, MethodCategory
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Load the latest method definitions.'

    def handle(self, *args, **options) -> None:
        print('Attempting to set default methods')
        try:
            for category in MethodCategory.objects.all():
                print(f'Setting new defaults for category {category.name}')
                self.handle_category(category)
        except Exception as e:
            raise CommandError(e)
        finally:
            print('Setting new default methods complete')

    def handle_category(self, category: MethodCategory):
        new_method = category.definitions.latest()
        corpora = Corpus.objects.filter(method_category=category).exclude(default_method=new_method)
        print(f'Found {len(corpora)} corpora with older methods.')
        for corpus in corpora:
            old_method = corpus.default_method
            corpus.default_method = new_method
            corpus.save()
            print(f'Updated corpus {corpus.name} from {old_method.name if old_method else "None"} to {new_method.name}')
