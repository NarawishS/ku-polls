"""Register models to show in admin here."""
from django.contrib import admin
from mysite.polls.models import Choice, Question


class ChoiceInline(admin.TabularInline):
    """Show detail of Choice in Question."""

    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    """Show detail of Question."""

    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date', 'end_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'end_date', 'was_published_recently', 'can_vote')
    list_filter = ['pub_date', 'end_date']
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
