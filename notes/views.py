from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Note
from .forms import NoteForm, SearchForm

class NoteListView(ListView):
    model = Note
    template_name = 'notes/note_list.html'
    context_object_name = 'notes'
    ordering = ['-created_at']  

class NoteDetailView(DetailView):
    model = Note
    template_name = 'notes/note_detail.html'
    context_object_name = 'note'

class NoteCreateView(CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'notes/note_form.html'
    success_url = reverse_lazy('note_list') 

class NoteUpdateView(UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'notes/note_form.html'
    
    def get_success_url(self):
        return reverse_lazy('note_detail', kwargs={'pk': self.object.pk})

class NoteDeleteView(DeleteView):
    model = Note
    template_name = 'notes/note_confirm_delete.html'
    success_url = reverse_lazy('note_list')

def search_notes(request):
    form = SearchForm()
    results = None
    query = None

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Note.objects.filter(title__icontains=query)

    return render(request, 'notes/search.html', {
        'form': form,
        'results': results,
        'query': query
    })