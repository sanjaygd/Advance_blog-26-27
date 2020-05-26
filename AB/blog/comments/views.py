from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render,get_object_or_404,reverse,Http404

from .forms import CommentForm
from .models import Comments

@login_required(login_url='/login/')
def comment_delete(request,id):
    # obj = get_object_or_404(Comments,id=id)
    try:
        obj = Comments.objects.get(id=id)
    except:
        raise Http404

    

    if obj.user != request.user:
        response = HttpResponse('You donot have the permission to delete the comment')
        response.status_code = 403
        return response
    if request.method == 'POST':
        parent_obj_url = obj.content_object.get_absolute_url()
        print(obj.content_object)
        print(obj.id)
        print(parent_obj_url)
        msg_info = obj.content
        obj.delete()
        messages.success(request,msg_info)
        return HttpResponseRedirect(parent_obj_url)
    context = {
        'object':obj
    }
    return render(request, 'blog_app/comment_delete.html',context)


@login_required(login_url='/login/')
def comment_thread(request,id):
    # obj = get_object_or_404(Comments,id=id)
    try:
        obj = Comments.objects.get(id=id)
    except:
        raise Http404
    
    if not obj.is_parent:
        obj = obj.parent

    initial_data = {
        'content_type':obj.content_type,
        'object_id':obj.id
    }
    form = CommentForm(request.POST or None, initial=initial_data)
    # print(dir(form))
    # print(form.errors)
    if form.is_valid() and request.user.is_authenticated():
        c_type = form.cleaned_data.get('content_type')
        content_type = ContentType.objects.get_for_model(obj.__class__)
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
        # return reverse(new_comment.content_object.get_absolute_url())
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())
    context = {
        'comment':obj,
        'form':form
    }
    return render(request,'blog_app/comment_thread.html', context)
