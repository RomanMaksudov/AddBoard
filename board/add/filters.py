from django.forms import DateTimeInput
from django_filters import FilterSet, DateTimeFilter, ModelChoiceFilter
from .models import Post, UserResponse


class PostFilter(FilterSet):
    added_after = DateTimeFilter(
        field_name='dateCreation',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
        }


class ResponseFilter(FilterSet):
    class Meta:
        model = UserResponse
        fields = [
            'post'
        ]

    def __init__(self, *args, **kwargs):
        super(ResponseFilter, self).__init__(*args, **kwargs)
        self.filters['post'].queryset = Post.objects.filter(to_user_id=self.request)
