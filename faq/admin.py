from django.contrib import admin

from .models import FAQ, FAQCategory, FAQTrans, FAQCategoryTrans


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer', 'datetime_created', 'active']
    list_filter = ['active']
    search_fields = ['question', 'answer']


@admin.register(FAQCategory)
class FAQCategoryAdmin(admin.ModelAdmin):
    list_display = ['id','title', ]
    search_fields = ['title']



@admin.register(FAQTrans)
class FAQTransAdmin(admin.ModelAdmin):
    list_display = ['question_en', 'question_fa', 'question_ar', 'answer_en', 'answer_fa', 'answer_ar', 'datetime_created', 'active']
    list_filter = ['active']
    search_fields = ['question_en', 'question_fa', 'question_ar', 'answer_en', 'answer_fa', 'answer_ar']

    # def question_en(self, obj):
    #     return obj.question_en
    # question_en.short_description = 'Question (English)'

    # def question_fa(self, obj):
    #     return obj.question_fa
    # question_fa.short_description = 'Question (Persian)'

    # def question_ar(self, obj):
    #     return obj.question_ar
    # question_ar.short_description = 'Question (Arabic)'

    # def answer_en(self, obj):
    #     return obj.answer_en
    # answer_en.short_description = 'Answer (English)'

    # def answer_fa(self, obj):
    #     return obj.answer_fa
    # answer_fa.short_description = 'Answer (Persian)'

    # def answer_ar(self, obj):
    #     return obj.answer_ar
    # answer_ar.short_description = 'Answer (Arabic)'


@admin.register(FAQCategoryTrans)
class FAQCategoryTransAdmin(admin.ModelAdmin):
    list_display = ['id', 'title_en', 'title_fa', 'title_ar']
    search_fields = ['title_en', 'title_fa', 'title_ar']

    # def title_en(self, obj):
    #     return obj.title_en
    # title_en.short_description = 'Category Title (English)'

    # def title_fa(self, obj):
    #     return obj.title_fa
    # title_fa.short_description = 'Category Title (Persian)'

    # def title_ar(self, obj):
    #     return obj.title_ar
    # title_ar.short_description = 'Category Title (Arabic)'
