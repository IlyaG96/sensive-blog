from django.shortcuts import render
from blog.models import Post, Tag
from django.http import HttpResponse


def serialize_post(post):

    serialized_tags = [serialize_tag(tag) for tag in post.tags.all()]

    return {
        'title': post.title,
        'teaser_text': post.text[:200],
        'author': post.author.username,
        'comments_amount': post.comments_count,
        'image_url': post.image.url if post.image else None,
        'published_at': post.published_at,
        'slug': post.slug,
        'tags': serialized_tags,
        'first_tag_title': serialized_tags[0]['title'],
    }


def serialize_tag(tag):
    return {
        'title': tag.title,
        'posts_with_tag': tag.related_post_num,
    }


def index(request):
    most_popular_posts = (Post.objects
                          .prefetch_related_tags()
                          .popular()[:5]
                          .select_related('author')
                          .fetch_with_comments_count()
                          )

    most_fresh_posts = (Post.objects
                        .prefetch_related_tags()
                        .fresh()[:5]
                        .fetch_with_comments_count()
                        )

    most_popular_tags = Tag.objects.popular()[:5]

    context = {
        'most_popular_posts': [
            serialize_post(post) for post in most_popular_posts
        ],
        'page_posts': [serialize_post(post) for post in most_fresh_posts],
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
    }
    return render(request, 'index.html', context)


def post_detail(request, slug):

    try:
        post = (Post.objects
                .prefetch_related_tags()
                .popular()
                .select_related('author')
                .get(slug=slug)
                )
    except Post.DoesNotExist:
        response = ('<html>'
                    '<body>'
                    'Такого поста не существует'
                    '<p><a href = "/">На главную</a></p>'
                    '</body>'
                    '</html>')
        return HttpResponse(response)

    comments = (post.comments
                .prefetch_related('post')
                .select_related('author')
                )

    serialized_comments = [
        {'text': comment.text,
         'published_at': comment.published_at,
         'author': comment.author.username,
         } for comment in comments
    ]

    serialized_post = {
        'title': post.title,
        'text': post.text,
        'author': post.author.username,
        'comments': serialized_comments,
        'likes_amount': post.likes_amount,
        'image_url': post.image.url if post.image else None,
        'published_at': post.published_at,
        'slug': post.slug,
        'tags': [serialize_tag(tag) for tag in post.tags.all()],
    }

    most_popular_tags = Tag.objects.popular()[:5]

    most_popular_posts = (Post.objects
                          .popular()[:5]
                          .prefetch_related('author')
                          .prefetch_related_tags()
                          .fetch_with_comments_count()
                          )

    context = {
        'post': serialized_post,
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
        'most_popular_posts': [
            serialize_post(post) for post in most_popular_posts
        ],
    }
    return render(request, 'post-details.html', context)


def tag_filter(request, tag_title):
    try:
        tag = Tag.objects.get(title=tag_title)
    except Tag.DoesNotExist:
        response = ('<html>'
                    '<body>'
                    'Такого тега не существует'
                    '<p><a href = "/">На главную</a></p>'
                    '</body>'
                    '</html>')
        return HttpResponse(response)

    most_popular_tags = Tag.objects.popular()[:5]

    most_popular_posts = (Post.objects
                          .popular()[:5]
                          .prefetch_related('author')
                          .prefetch_related_tags()
                          .fetch_with_comments_count()
                          )

    related_posts = (tag.posts
                        .prefetch_related('author')
                        .prefetch_related_tags()
                        .fetch_with_comments_count()[:20])

    context = {
        'tag': tag.title,
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
        'posts': [serialize_post(post) for post in related_posts],
        'most_popular_posts': [
            serialize_post(post) for post in most_popular_posts
        ],
    }
    return render(request, 'posts-list.html', context)


def contacts(request):
    # позже здесь будет код для статистики заходов на эту страницу
    # и для записи фидбека
    return render(request, 'contacts.html', {})
