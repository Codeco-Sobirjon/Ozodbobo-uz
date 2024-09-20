from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from apps.blog.models import Categories, Blog, BlogImage, BlogComment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def basePageView(request):
    context = {}

    context['categories'] = Categories.objects.all().order_by('-id')

    print(context['categories'])

    return render(request, 'base.html', context)


def indexPageView(request):
    # Query the 5 most viewed blogs
    most_viewed_blogs = Blog.objects.order_by('-is_seen')[:5]

    # Get images for the most viewed blogs
    blogs_with_images = []
    for blog in most_viewed_blogs:
        blog_images = BlogImage.objects.filter(blog=blog).first()
        blogs_with_images.append({
            'blog': blog,
            'images': blog_images
        })

    new_nine_blogs = []
    new_nine_blog = Blog.objects.all().order_by('-id')[:10]
    for blog in new_nine_blog:
        blog_images = BlogImage.objects.filter(blog=blog).first()
        new_nine_blogs.append({
            'blog': blog,
            'images': blog_images
        })

    context = {
        'blogs_with_images': blogs_with_images,
        'new_nine_blogs': new_nine_blogs,
    }

    return render(request, 'index.html', context)


def categoryPageView(request, id):
    category = get_object_or_404(Categories, id=id)
    blogs = Blog.objects.filter(category=category)

    # Pagination setup
    paginator = Paginator(blogs, 4)  # Show 10 blogs per page
    page = request.GET.get('page')
    try:
        blogs_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        blogs_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        blogs_page = paginator.page(paginator.num_pages)

    blogs_with_images = []
    for blog in blogs_page:
        blog_images = BlogImage.objects.filter(blog=blog).first()
        blogs_with_images.append({
            'blog': blog,
            'images': blog_images
        })

    context = {
        'blogs_with_images': blogs_with_images,
        'page_obj': blogs_page,
        'paginator': paginator,
    }
    return render(request, 'category.html', context)


def detailPageView(request, id):
    blog_detail = get_object_or_404(Blog, id=id)

    blog_detail.is_seen += 1
    blog_detail.save()
    blog_images = BlogImage.objects.filter(blog=blog_detail)
    blog_comment_count = BlogComment.objects.select_related('blog').filter(blog=blog_detail).count()
    blog_comment = BlogComment.objects.select_related('blog').filter(blog=blog_detail)
    categories = Categories.objects.all().order_by('-id')
    last_blogs = Blog.objects.order_by('-id')[:5]
    last_blog = []
    for blog in last_blogs:
        blog_image = BlogImage.objects.filter(blog=blog).first()
        last_blog.append({
            'blog': blog,
            'images': blog_image
        })

    context = {
        'blog': blog_detail,
        'images': blog_images,
        'blog_comment_count': blog_comment_count,
        'categories': categories,
        'last_blog': last_blog,
        'blog_comment': blog_comment,
        'video_url': blog_detail.video
    }
    return render(request, 'detail.html', context)


def commentPageView(request, id):
    # Get the blog object
    blog_detail = get_object_or_404(Blog, id=id)

    if request.method == 'POST':
        # Get data from the form
        full_name = request.POST.get('name')
        phone = request.POST.get('text')  # Ensure this matches the 'name' attribute in the HTML form
        comment_text = request.POST.get('comment')

        # Create and save the comment
        BlogComment.objects.create(
            full_name=full_name,
            phone=phone,
            comment=comment_text,
            blog=blog_detail
        )

        # Redirect back to the blog detail page
        return HttpResponseRedirect(reverse('detail-blog', args=[blog_detail.id]))

    return HttpResponseRedirect(reverse('detail-blog', args=[blog_detail.id]))


def passs(request):

    pass