from django.db.models import Avg, F
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from .models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer to represent Category model
    """
    class Meta:
        fields = ('name', 'slug', )
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """
    Serializer to represent Genre model
    """
    class Meta:
        fields = ('name', 'slug', )
        model = Genre


class GenreField(serializers.SlugRelatedField):
    """
    Custom field for Genre
    """
    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(**{self.slug_field: data})
        except (TypeError, ValueError):
            self.fail('invalid')

    def to_representation(self, value):
        return GenreSerializer(value).data


class CategoryField(serializers.SlugRelatedField):
    """
    Custom field for Category
    """
    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(**{self.slug_field: data})
        except (TypeError, ValueError):
            self.fail('invalid')

    def to_representation(self, value):
        return CategorySerializer(value).data


class TitleSerializer(serializers.ModelSerializer):
    """
    Serializer to represent Title model

    Additional calculated field - title rating
    """
    genre = GenreField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )

    category = CategoryField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    rating = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        model = Title

    def get_rating(self, obj):
        return obj.review.aggregate(avgs=Avg(F('score'))).get('avgs', None)


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer to represent Review model.
    Validate score and constraint unique titel-review.
    """
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date',)
        model = Review

    def validate(self, data):
        get_object_or_404(
            Title,
            id=self.context.get('view').kwargs.get('title_id')
        )
        if 1 > data.get('score') > 10:
            raise serializers.ValidationError(
                {'detail': 'Значение должно быть от 1 до 10'}
            )
        title = self.context.get('view').kwargs.get('title_id')
        author = self.context['request'].user
        if (self.context.get('request').method == 'POST'
            and Review.objects.filter(
                title=title, author_id=author.id).exists()):
            raise serializers.ValidationError(
                {'detail': 'Вы уже оставили отзыв'})
        return data


class CommentsSerializer(serializers.ModelSerializer):
    """
    Serializer to represent Comment model
    """
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
