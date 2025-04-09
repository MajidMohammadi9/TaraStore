from django.db import models
from django.utils.translation import get_language, gettext_lazy as _


class FAQCategory(models.Model):
    title=models.CharField(max_length=100, verbose_name=_('Category Title'))

    def __str__(self):
        return self.title

class FAQ(models.Model):
    category=models.ForeignKey(FAQCategory, on_delete=models.CASCADE, related_name='faqs', verbose_name=_('Category'))
    question=models.CharField(max_length=255, verbose_name=_('Question'))
    answer=models.TextField(verbose_name=_('Answer'))
    datetime_created=models.DateTimeField(auto_now_add=True, verbose_name=_('Date Time Created'))
    datetime_modified=models.DateTimeField(auto_now=True, verbose_name=_('Date Time Modified'))
    active=models.BooleanField(default=True, verbose_name=_('Active'))

    def __str__(self):
        return self.question
    

class FAQCategoryTrans(models.Model):
    title_en = models.CharField(max_length=100, verbose_name=_('CategoryTitle (English)'))
    title_fa = models.CharField(max_length=100, verbose_name=_('CategoryTitle (Persian)'))
    title_ar = models.CharField(max_length=100, verbose_name=_('CategoryTitle (Arabic)'))

    def __str__(self):
        if hasattr(self, 'title_' + get_language()):
            return getattr(self, 'title_' + get_language())
        return self.title_en  

class FAQTrans(models.Model):
    category = models.ForeignKey(FAQCategoryTrans, on_delete=models.CASCADE, related_name='faqs', verbose_name=_('Category'))
    question_en = models.CharField(max_length=255, verbose_name=_('Question (English)'))
    question_fa = models.CharField(max_length=255, verbose_name=_('Question (Persian)'))
    question_ar = models.CharField(max_length=255, verbose_name=_('Question (Arabic)'))
    
    answer_en = models.TextField(verbose_name=_('Answer (English)'))
    answer_fa = models.TextField(verbose_name=_('Answer (Persian)'))
    answer_ar = models.TextField(verbose_name=_('Answer (Arabic)'))
    
    datetime_created = models.DateTimeField(auto_now_add=True, verbose_name=_('Date Time Created'))
    datetime_modified = models.DateTimeField(auto_now=True, verbose_name=_('Date Time Modified'))
    active = models.BooleanField(default=True, verbose_name=_('Active'))

    def __str__(self):
        if hasattr(self, 'question_' + get_language()):
            return getattr(self, 'question_' + get_language())
        return self.question_en
