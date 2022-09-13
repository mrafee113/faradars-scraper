from courses.models import Course, Tutor
from utils.scrapy_pipeline import Pipeline


class FaradarsMainPipeline(Pipeline):
    store_temporarily = True
    temporary_storage = 'cache'
    cache_key = 'faradars_main'
    item_type = list

    @classmethod
    def item_to_db_map(cls) -> dict:
        return {k: k for k in {
            'title', 'link', 'number_of_students', 'tutor', 'duration'
        }}

    @classmethod
    def export_to_db(cls, items: list[dict]):
        tutors_name_to_id = {name: idx for name, idx in Tutor.objects.values_list('name', 'id')}
        tutor_objs = list()
        for item in items:
            if item['tutor'] not in tutors_name_to_id:
                tutor_objs.append(Tutor(name=item['tutor']))
        Tutor.objects.bulk_create(tutor_objs, ignore_conflicts=True)
        tutors_name_to_id = {name: idx for name, idx in Tutor.objects.values_list('name', 'id')}

        objs = list()
        for item in items:
            item['tutor_id'] = tutors_name_to_id[item['tutor']]
            del item['tutor']
            item['provider'] = 'faradars'
            objs.append(Course(**item))

        Course.objects.bulk_create(objs, ignore_conflicts=True)
