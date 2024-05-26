from Settings.models import Org

def OrgData(request):
    Web = Org.objects.first()
    if not Web:
        Web = Org.objects.create(
            name="Default Org Name",
        )
    
    data = {
        'Web': Web
    }
    return (data)
