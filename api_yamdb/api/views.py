from reviews.models import Review, Comment
from .serializers import (CommentSerializer, ReviewSerializer)
from django.shortcuts import get_object_or_404
from rest_framework import viewsets


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        # Получаем id отзыва из эндпоинта
        title_id = self.kwargs.get('title_id')
        # И отбираем только нужные комментарии
        new_queryset = Review.objects.filter(title=title_id)
        return new_queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, review=title)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)
        super(ReviewViewSet, self).perform_update(serializer)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    # queryset во вьюсете не указываем
    # Нам тут нужны не все комментарии,
    # а только связанные с отзывом id=review_id
    # Поэтому нужно переопределить метод get_queryset и применить фильтр

    def get_queryset(self):
        # Получаем id отзыва из эндпоинта
        review_id = self.kwargs.get('review_id')
        # И отбираем только нужные комментарии
        new_queryset = Comment.objects.filter(review=review_id)
        return new_queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)
        super(CommentViewSet, self).perform_update(serializer)
