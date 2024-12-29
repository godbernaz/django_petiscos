from django.contrib import admin
from .models import Category, Customer, Product, Order, Profile, Review
from django.contrib.auth.models import User
from django import forms

admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Profile)

class ProfileInline(admin.StackedInline):
    model = Profile
    
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']
    inlines = [ProfileInline]
    
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

class ReviewAdminForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = '__all__'
        
    # Limitar o campo rating a um dropdown com opções de 0 a 5
    RATING_CHOICES = [(i, str(i)) for i in range(0, 6)]  # Opções de 0 a 5
    rating = forms.ChoiceField(choices=RATING_CHOICES)
    
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')  # Colunas visíveis na lista
    list_filter = ('rating', 'created_at')  # Filtros laterais
    search_fields = ('product__name', 'user__username')  # Campos de pesquisa
    ordering = ('-created_at',)  # Ordenação por data, mais recentes primeiro