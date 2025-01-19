from django.contrib import admin,messages

from .models import Product, Category, Comment


class CommentInline(admin.TabularInline):
    model=Comment
    fields=['id', 'author','body', 'stars', 'status','active']
    extra=0
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('author','product')


class InventoryFilter(admin.SimpleListFilter):
    LESS_THAN_3 = '<3'
    BETWEEN_3_and_10 = '3<=10'
    MORE_THAN_10 = '>10'
    title = 'Critical Inventory Status'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            (InventoryFilter.LESS_THAN_3, 'High'),
            (InventoryFilter.BETWEEN_3_and_10, 'Medium'),
            (InventoryFilter.MORE_THAN_10, 'OK'),
        ]
    
    def queryset(self, request, queryset):
        if self.value() == InventoryFilter.LESS_THAN_3:
            return queryset.filter(inventory__lt=3)
        if self.value() == InventoryFilter.BETWEEN_3_and_10:
            return queryset.filter(inventory__range=(3, 10))
        if self.value() == InventoryFilter.MORE_THAN_10:
            return queryset.filter(inventory__gt=10)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['id', 'name', 'inventory', 'unit_price', 'inventory_status', 'category', 'active']
    prepopulated_fields={'slug': ['name',]}
    list_per_page=10
    list_editable=['unit_price']
    list_select_related=['category']
    list_filter=['datetime_created', InventoryFilter]
    search_fields=['name',]
    actions=['clear_inventory']
    inlines=[CommentInline]
    list_display_links=['id', 'name']

    def inventory_status(self, product):
        if product.inventory<10:
            return 'Low'
        elif product.inventory>50:
            return 'High'
        return 'Medium'
    
    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        update_count=queryset.update(inventory=0)
        self.message_user(request,f'{update_count} of products inventories cleared to zero', messages.ERROR)


admin.site.register(Category)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=['id', 'product', 'author', 'status','active']
    list_editable=['status', 'active']
    list_per_page=10
    autocomplete_fields=['product']
