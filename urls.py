from django.conf.urls.defaults import *


urlpatterns = patterns('podcast.views',
    # Show list of all shows
    url(r'^$', view='show_list', name='podcast_shows'),

    #added for pinax
    url(r'^__yours/$', view='yours', name='podcast_yours'),
    url(r'^__friends/$', view='friends', name='podcast_friends'),
    url(r'^__create/$', view='create', name='podcast_create'),
    url(r'^__update/(?P<slug>[-\w]+)/$', view='update', name='podcast_update'),

    url(r'^(?P<slug>[-\w]+)/add_episode/$', view='episode_add',\
            name='podcast_episode_add'),

    url(r'^(?P<show_slug>[-\w]+)/(?P<episode_slug>[-\w]+)/delete/$',\
            view='episode_delete', name='podcast_episode_delete'),

    url(r'^(?P<show_slug>[-\w]+)/(?P<episode_slug>[-\w]+)/add/$',\
            view='enclosure_add', name='podcast_enclosure_add'),




    # Episode list of one show
    url(r'^(?P<slug>[-\w]+)/$', view='episode_list', name='podcast_episodes'),

    # Episode list feed by show (RSS 2.0 and iTunes)
    url(r'^(?P<slug>[-\w]+)/feed/$', view='show_list_feed', name='podcast_feed'),

    # Episode list feed by show (Atom)
    url(r'^(?P<slug>[-\w]+)/atom/$', view='show_list_atom', name='podcast_atom'),

    # Episode list feed by show (Media RSS)
    url(r'^(?P<slug>[-\w]+)/media/$', view='show_list_media', name='podcast_media'),

    # Episode sitemap list of one show
    url(r'^(?P<slug>[-\w]+)/sitemap.xml$', view='episode_sitemap', name='podcast_sitemap'),

    # Episode detail of one show
    url(r'^(?P<show_slug>[-\w]+)/(?P<episode_slug>[-\w]+)/$', view='episode_detail', name='podcast_episode'),
)
