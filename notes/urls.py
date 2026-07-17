from django.urls import path
from . import views

urlpatterns = [
    path('', views.NoteListView.as_view(), name='note_list'),
    path('note/<int:pk>/', views.NoteDetailView.as_view(), name='note_detail'),
    path('note/add/', views.NoteCreateView.as_view(), name='note_create'),
    path('note/<int:pk>/edit/', views.NoteUpdateView.as_view(), name='note_update'),
    path('note/<int:pk>/delete/', views.NoteDeleteView.as_view(), name='note_delete'),
    path('search/', views.search_notes, name='note_search'),  # FBV Поиск
]