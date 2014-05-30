__author__ = 'Kevin Gleason'

from snowplow_tracker.tracker import Tracker
import contracts, requests

namespace = "tracker1"
app_id = "trackerTest"
context_vendor = "com.saggezza"
tracker = Tracker("d3rkrsqld9gmqf.cloudfront.net", namespace,\
                  app_id, context_vendor)
