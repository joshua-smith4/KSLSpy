from KSLSpyViewer.ksl_scraper_helper import get_query_results
from KSLSpyViewer.models import Campaign
campaigns = Campaign.objects.all()


for result in get_query_results({'hello':'world'}):
    print result
