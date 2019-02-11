from django.shortcuts import render

# Create your views here.
def upload_post(request):
    if request.method=='POST':
        form=PlayListForm(request.POST)
    else:
        form=PlayListForm()
    return render(request,'playlists/upload.html',{'form':form})
        
def search_keyword(request):
    pass


        
    
