from sqladmin import ModelView

from src.models import SubjectCombinationSpecialties


class SubjectCombinationSpecialtiesAdmin(ModelView, model=SubjectCombinationSpecialties):
    column_list = [
        SubjectCombinationSpecialties.subject_combination_id,
        SubjectCombinationSpecialties.specialty_id,
    ]

    column_details_list = [
        SubjectCombinationSpecialties.subject_combination_id,
        SubjectCombinationSpecialties.specialty_id,
    ]

    column_filters = [
        SubjectCombinationSpecialties.subject_combination_id,
        SubjectCombinationSpecialties.specialty_id,
    ]
    column_searchable_list = [
    ]
    column_sortable_list = [
        SubjectCombinationSpecialties.subject_combination_id,
        SubjectCombinationSpecialties.specialty_id,
    ]
    form_include_pk = True
