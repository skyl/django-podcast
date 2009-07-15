from django.views.generic.list_detail import object_list
from django.views.generic.list_detail import object_detail
from podcast.models import Episode, Show, Enclosure

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

from django.views.generic.create_update import create_object, update_object, delete_object


from podcast.forms import ShowForm, EpisodeForm, EnclosureForm

from random import choice

def episode_detail(request, show_slug, episode_slug):
    """
    Episode detail

    Template:  ``podcast/episode_detail.html``
    Context:
        object_detail
            Detail of episode.
    """

    try:
        show = Show.objects.get(slug = show_slug, author=request.user)
        is_me = True
    except:
        show = Show.objects.get(slug = show_slug)
        is_me = False

    context={ 'enclosure_list': Enclosure.objects.filter(episode__show__slug__exact=show_slug).filter(episode__slug__exact=episode_slug).order_by('-episode__date'),\
              'show':show, 'is_me': is_me, }

    return object_detail(
        request,
        queryset=Episode.objects.published().filter(show__slug__exact=show_slug),
        slug=episode_slug,
        slug_field='slug',
        template_name='podcast/episode_detail.html',
        extra_context = context)


def episode_list(request, slug):
    """
    Episode list

    Template:  ``podcast/episode_list.html``
    Context:
        object_list
            List of episodes.
    """

    try:
        show = Show.objects.get(slug=slug, author=request.user)
        is_me = True
    except:
        try:
            show = Show.objects.get(slug=slug)
            is_me = False
        except:
            return HttpResponseRedirect(reverse('podcast_shows'))

    context = {'is_me': is_me, 'show':show}

    return object_list(
        request,
        queryset=Episode.objects.published().filter(show__slug__exact=slug),
        template_name='podcast/episode_list.html', extra_context=context)


def episode_sitemap(request, slug):
    """
    Episode sitemap

    Template:  ``podcast/episode_sitemap.html``
    Context:
        object_list
            List of episodes.
    """
    return object_list(
        request,
        mimetype='application/xml',
        queryset=Episode.objects.published().filter(show__slug__exact=slug).order_by('-date'),
        extra_context={
            'enclosure_list': Enclosure.objects.filter(episode__show__slug__exact=slug).order_by('-episode__date')},
        template_name='podcast/episode_sitemap.html')


def show_list(request):
    """
    Episode list

    Template:  ``podcast/show_list.html``
    Context:
        object_list
            List of shows.
    """
    return object_list(
        request,
        queryset=Show.objects.all().order_by('title'),
        template_name='podcast/show_list.html')


def show_list_feed(request, slug):
    """
    Episode feed by show

    Template:  ``podcast/show_feed.html``
    Context:
        object_list
            List of episodes by show.
    """
    return object_list(
        request,
        mimetype='application/rss+xml',
        queryset=Episode.objects.filter(show__slug__exact=slug).order_by('-date')[0:21],
        template_name='podcast/show_feed.html')


def show_list_media(request, slug):
    """
    Episode feed by show

    Template:  ``podcast/show_feed_media.html``
    Context:
        object_list
            List of episodes by show.
    """
    return object_list(
        request,
        mimetype='application/rss+xml',
        queryset=Episode.objects.filter(show__slug__exact=slug).order_by('-date')[0:21],
        extra_context={
            'enclosure_list': Enclosure.objects.filter(episode__show__slug__exact=slug).order_by('-episode__date')},
        template_name='podcast/show_feed_media.html')


def show_list_atom(request, slug):
    """
    Episode feed by show

    Template:  ``podcast/show_feed_atom.html``
    Context:
        object_list
            List of episodes by show.
    """
    return object_list(
        request,
        mimetype='application/rss+xml',
        queryset=Episode.objects.filter(show__slug__exact=slug).order_by('-date')[0:21],
        extra_context={
            'enclosure_list': Enclosure.objects.filter(episode__show__slug__exact=slug).order_by('-episode__date')},
        template_name='podcast/show_feed_atom.html')

@login_required
def yours(request):
    context={}
    return object_list(request, template_name = 'podcast/yours.html',\
            queryset = Show.objects.filter(author=request.user),
            extra_context = context)

@login_required
def friends(request):
    context={}
    return object_list('podcast/friends.html', context,\
            context_instance=RequestContext(request))


@login_required
def create(request):
    if request.method == 'POST':
        form = ShowForm(request.POST)
        if form.is_valid():
            s = form.save(commit=False)
            s.webmaster = request.user
            s.author = request.user
            s.slug = slugify(s.title)
            s.save()
            #except:
            #    s.slug = slugify(s.title) +\
            #            ''.join([choice('0123456789-_') for i in range(7)])
            #    s.save()

            #finally:
            return HttpResponseRedirect(reverse('podcast_shows'))
    else:
        context={}
        return create_object(request, form_class=ShowForm, template_name="podcast/create_show.html")


@login_required
def update(request, slug):
    context={}

    return update_object(request, model=Show, slug=slug, slug_field='slug',\
            login_required=True, template_name="podcast/update_show.html",\
            extra_context=context)


def episode_add(request, slug):
    ''' create a new episode '''
    try:
        show = Show.objects.get(slug=slug, author=request.user)
    except:
        return HttpResponseRedirect(reverse('podcast_shows'))

    if request.method == 'POST':
        form = EpisodeForm(request.POST)
        if form.is_valid():
            e = form.save(commit=False)
            e.show = show
            e.slug = slugify(e.title)
            e.save()
            #except:
            #    e.slug = slugify(e.title) + \
                    #            ''.join([choice('0123456789-_') for i in range(7)])
            #    e.save()
            #finally:
            return HttpResponseRedirect(reverse('podcast_episodes', args=[slug]))


    context={'show':show}
    return create_object(request, form_class=EpisodeForm,\
            template_name="podcast/create_episode.html", \
            extra_context=context)

def enclosure_add(request, show_slug, episode_slug):
    ''' create a new enclosure for an episode '''
    try:
        show = Show.objects.get(slug=show_slug, author=request.user)
        episode = Episode.objects.get(slug=episode_slug)
    except:
        return HttpResponseRedirect(reverse('podcast_shows'))

    if request.method == 'POST':
        form = EnclosureForm(request.POST)
        if form.is_valid():
            en = form.save(commit=False)
            en.episode = episode
            en.save()
            return HttpResponseRedirect(reverse('podcast_episode',\
                    args=[show_slug, episode_slug]))

    context={'show':show, 'episode':episode, }
    return create_object(request, form_class = EnclosureForm,\
            template_name="podcast/create_enclosure.html",\
            extra_context = context)


@login_required
def episode_delete(request, show_slug, episode_slug):
    #e = Episode.objects.get(slug=slug)
    #if e.show.author == request.user:

    return delete_object(request, model=Episode, slug=episode_slug, slug_field='slug',\
            post_delete_redirect=reverse('podcast_episodes', args=[show_slug]),
            template_name="podcast/confirm_delete.html")


