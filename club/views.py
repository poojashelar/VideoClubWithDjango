from django.http import Http404, JsonResponse
from django.views import generic
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.forms import formset_factory
from django.forms.utils import ErrorList
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Club, Video
from .forms import VideoForm, SearchForm
import urllib
import requests



YOUTUBE_API_KEY = 'abcdefg'

def home(request):
    '''Home view when user login to Video Club App'''
    recent_clubs = Club.objects.all().order_by('-id')[:3] # show last 3 clubs
    popular_clubs = [Club.objects.get(pk=3),Club.objects.get(pk=1)]
    return render(request, 'home.html',{'recent_clubs': recent_clubs, 'popular_clubs': popular_clubs})

@login_required # To access dashboard, user should login first.
def dashboard(request):
    ''' Dashboard view for user to see andperform CRUD opertions o Club and Videos'''
    clubs = Club.objects.filter(user=request.user) # User can see is own clubs only
    return render(request, 'dashboard.html', {'clubs': clubs})

@login_required # To access search functionality, user should login first.
def video_search(request):
    ''' Search Video on youtube using API Key'''
    search_form = SearchForm(request.GET)
    if search_form.is_valid():   
        encoded_search_term = urllib.parse.quote(search_form.cleaned_data['search_term'])
        response = requests.get(f'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=6&q={ encoded_search_term }&key={ YOUTUBE_API_KEY }')
        return JsonResponse(response.json())
    return JsonResponse({'error':'Not able to validate form'})

class DeleteVideo(LoginRequiredMixin, generic.DeleteView):
    '''
    # To delete video, user should login first.
    '''
    model = Video #table
    template_name = 'delete_video.html'
    success_url = reverse_lazy('dashboard') # On successful delete user should redirect to Dashboard.

    def get_object(self):
        ''' User can only delete videos which are added by himself.'''
        video = super(DeleteVideo, self).get_object()
        if not video.club.user == self.request.user:
            raise Http404
        return video

class SignUp(generic.CreateView):
    ''' Signup to Video Club app and Login automatically post signup'''
    form_class = UserCreationForm
    success_url = reverse_lazy('dashboard')
    template_name = 'registration/signup.html'

    #Form Validation
    def form_validate(self, form):
        view = super(SignUp, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1') # Form is created by Django
        user = authenticate(username=username, password=password)
        login(self.request, user) #Login automatically post signup
        return view

class CreateClub(LoginRequiredMixin, generic.CreateView):
    ''' Create Club of Videos to personalize the youtube'''
    model = Club
    fields = ['title'] # Provide title to create Club and user would be current login user
    template_name = 'create_club.html'
    success_url =  reverse_lazy('dashboard')
    
    #custom form validations
    def form_validate(self, form):
        form.instance.user = self.request.user
        super(CreateClub, self).form_valid(form)
        return redirect('dashboard')


class DetailClub(generic.DetailView):
    ''' Detail view of club'''
    model = Club
    template_name = 'detail_club.html'

class UpdateClub(LoginRequiredMixin, generic.UpdateView):
    ''' Update club'''
    model = Club
    template_name = 'update_club.html'
    fields = ['title']
    success_url =  reverse_lazy('dashboard')

    def get_object(self):
        ''' User can only update clubs which are created by himself.'''
        club = super(UpdateClub, self).get_object()
        if not club.user == self.request.user:
            raise Http404
        return club

class DeleteClub(LoginRequiredMixin, generic.DeleteView):
    '''Delete club view'''
    model = Club
    template_name = 'delete_club.html'
    fields = ['title']
    success_url =  reverse_lazy('dashboard')

    def get_object(self):
        ''' User can only delete clubs which are created by himself.'''
        club = super(DeleteClub, self).get_object()
        if not club.user == self.request.user:
            raise Http404
        return club

@login_required
def add_video(request, pk):
    ''' User can add videos post login '''
   # VideoFormSet = formset_factory(VideoForm, extra=5) - To crete multifile form on one page

    form = VideoForm()
    search_form = SearchForm()
    club = Club.objects.get(pk=pk)
    if not club.user == request.user:
        raise Http404
    if request.method == 'POST':
        #create
        form = VideoForm(request.POST)
        if form.is_valid():
            video = Video()
            video.url = form.cleaned_data['url'] # get URL which added on url textbox of Form
            video.club = club
            parsed_url = urllib.parse.urlparse(video.url) # Parse Youtube URL
            video_id  = urllib.parse.parse_qs(parsed_url.query).get('v') #Extract Id from url e.g : https://www.youtube.com/watch?v=SdTzwYmsgoU
            if video_id:
                video.youtube_id = video_id[0] # Assign youtube_id
               # video.title = filled_form.cleaned_data['title']
               
               # Make api call to Search particular video on youtube using id
                response = requests.get(f'https://youtube.googleapis.com/youtube/v3/videos?part=snippet&id={ video_id[0] }&key={ YOUTUBE_API_KEY}')
                json = response.json()
                title = json['items'][0]['snippet']['title'] #Extract title from response
                video.title = title
                video.save() # Save data in db
                return redirect('detail_club', pk)
            else:
                errors = form._errors.setdefault('url', ErrorList())
                errors.append('Needs to be Youtube URl')


    return render(request, 'add_video.html', {'form': form, 'search_form': search_form, 'club':club})