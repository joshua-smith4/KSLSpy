from KSLSpyViewer.ksl_scraper_helper import get_query_results
from KSLSpyViewer.models import Campaign
campaigns = Campaign.objects.all()
print campaigns[0].queryJSON

for campaign in campaigns:
    for result in get_query_results(campaign.queryJSON):
        print result
