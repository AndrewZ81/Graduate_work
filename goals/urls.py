from django.urls import path
from goals import views

urlpatterns = [
    # Пути для категорий
    path('goal_category/create', views.GoalCategoryCreateView.as_view(), name='category_create'),
    path('goal_category/list', views.GoalCategoryListView.as_view(), name='category_list'),
    path('goal_category/<int:pk>', views.GoalCategoryView.as_view(), name='category'),

    # Пути для целей
    path('goal/create', views.GoalCreateView.as_view(), name='goal_create'),
    path('goal/list', views.GoalListView.as_view(), name='goal_list'),
    path('goal/<int:pk>', views.GoalView.as_view(), name='goal'),

    # Пути для комментариев
    path('goal_comment/create', views.GoalCommentCreateView.as_view(), name='comment_create'),
    path('goal_comment/list', views.GoalCommentListView.as_view(), name='comment_list'),
    path('goal_comment/<int:pk>', views.GoalCommentView.as_view(), name='comment'),

    # Пути для общих досок целей
    path('board/create', views.BoardCreateView.as_view(), name='board_create'),
    path('board/list', views.BoardListView.as_view(), name='board_list'),
    path('board/<int:pk>', views.BoardView.as_view(), name='board'),
]
