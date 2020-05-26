from urllib.parse import quote_plus
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect,Http404
from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone

from comments.forms import CommentForm
from comments.models import Comments
from .forms import PostForm
from .models import Post
from .utils import get_read_time,count_words


def post_list(request):
    # the below line is alternative for model Manager but not suitable at every time
    # queryset = Post.objects.filter(draft=False).filter(publish__lte=timezone.now()) #all().order_by('-id') #.order_by('-timestamp')
    today = timezone.now()
    queryset = Post.objects.active() # added in ch-36
    if request.user.is_staff or request.user.is_superuser: # added in ch-36
        queryset = Post.objects.all() # added in ch-36

    query = request.GET.get('q')
    if query:
        queryset = Post.objects.filter(
            Q(title__icontains=query)|
            Q(content__icontains=query)|
            Q(user__first_name__icontains=query)|
            Q(user__last_name__icontains=query)).filter(draft=False).distinct()

    paginator = Paginator(queryset, 5) # Show 5 contents per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'object_list' : page_obj,
        'page_obj': page_obj,
        'today':today
    }
    return render(request,'blog_app/post_list.html',context)


def post_details(request,slug = None, pk=None):
    # instance = get_object_or_404(Post,pk=pk)
    instance = get_object_or_404(Post,slug=slug)
    if instance.draft or instance.publish > timezone.now():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(instance.content)
    # print(get_read_time(instance.content))
    # print(count_words(instance.content))
    
    initial_data = {
        'content_type' : instance.get_content_type,
        'object_id':instance.id
    }
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid() and request.user.is_authenticated():
        
        c_type = form.cleaned_data.get('content_type')
        content_type = ContentType.objects.get_for_model(instance.__class__)
        # content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get('object_id')
        content_data = form.cleaned_data.get('content')
        parent_obj = None
        try:
            parent_id = int(request.POST.get('parent_id'))
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comments.objects.filter(id = parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()

        # print(form.cleaned_data)
        new_comment, created = Comments.objects.get_or_create(
            user = request.user,
            content_type = content_type,
            object_id = obj_id,
            content = content_data,
            parent = parent_obj
        )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())
     
    comments = instance.comments 
    context = {
        'obj_details':instance,
        'share_string':share_string,
        'comments':comments,
        'comment_form':form
    }
    return render(request,'blog_app/post_details.html',context)


def post_create(request):
    # if not request.user.is_staff or not request.user.is_supperuser:
        # raise Http404

    # if not request.user.is_authenticated:
    #     raise Http404

    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request,'Succesfuly created')
        return HttpResponseRedirect(instance.get_absolute_url())
    # else:
    #     messages.error(request,'Not succesfully created')    
    context = {
        'form':form
    }
    return render(request, 'blog_app/post_create.html',context)



def post_update(request, id=None):
    # if not request.user.is_staff or not request.user.is_supperuser:
    #     raise Http404

    # if not request.user.is_authenticated:
    #     raise Http404
    
    instance = get_object_or_404(Post,id=id) #This instance should pass through form to update
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request,'<a href="">Item</a> Succesfuly changed',extra_tags='html_safe') #extra tag is used to create different classes in html
        return HttpResponseRedirect(instance.get_absolute_url()) #redirecting the url is must and should once after saved the form
    # else:
    #     messages.error(request,'Not succesfully changed')

    context = {
        'form':form
    }
    return render(request, 'blog_app/post_create.html',context)


def post_delete(request,id=None):
    if not request.user.is_staff or not request.user.is_supperuser:
        raise Http404
    instance = get_object_or_404(Post,id=id)
    instance.delete()
    messages.success(request, "Succesfully deleted")
    return redirect('blog_app:post_list')



