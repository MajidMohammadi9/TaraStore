from django.shortcuts import render
from django.db.models import Q
from django.utils.translation import get_language
from django.http import JsonResponse

from .models import FAQCategory, FAQCategoryTrans, FAQ

def faq_list_view(request):
    categories = FAQCategory.objects.prefetch_related('faqs').filter(faqs__active=True).distinct()
    query = request.GET.get('q')

    if query:
        categories = FAQCategory.objects.filter(Q(faqs__question__icontains=query) | Q(faqs__answer__icontains=query))

    return render(request, 'faq/faq_list.html', {'categories': categories, 'query': query})


def faq_list_view_Trans(request):
    categories = FAQCategoryTrans.objects.prefetch_related('faqs').filter(faqs__active=True).distinct()
    query = request.GET.get('q')
    language = get_language()  # زبان فعلی سایت را دریافت می‌کنیم

    if query:
        categories = FAQCategoryTrans.objects.filter(
            Q(faqs__question_en__icontains=query) | Q(faqs__answer_en__icontains=query) |
            Q(faqs__question_fa__icontains=query) | Q(faqs__answer_fa__icontains=query) |
            Q(faqs__question_ar__icontains=query) | Q(faqs__answer_ar__icontains=query)
        )
    
    return render(request, 'faq/faq_list_trans.html', {
        'categories': categories, 
        'query': query,
        'language': language
    })

def faq_search_api(request):
    query = request.GET.get('q', '')
    results = []

    if len(query) >= 2:
        faqs = FAQ.objects.filter(
            Q(question__icontains=query) | Q(answer__icontains=query),
            active=True
        ).select_related('category')

        for faq in faqs:
            results.append({
                'question': faq.question,
                'answer': faq.answer,
                'category': faq.category.title,
            })

    return JsonResponse({'results': results})