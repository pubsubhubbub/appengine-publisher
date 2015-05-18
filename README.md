This is a Google AppEngine application that publishes an Atom feed and pings
a PubSubHubbub hub whenever an item is added to it.

In order to deploy this application, create a new application on AppEngine and
deploy like this:

```
$ appcfg.py update . -A s~your-app-id
08:01 PM Application: s~your-app-id (was: auto); version: auto
08:01 PM Host: appengine.google.com
08:01 PM
Starting update of app: s~your-app-id, version: auto
08:01 PM Getting current resource limits.
08:01 PM Scanning files on local disk.
08:01 PM Cloning 4 application files.
08:01 PM Uploading 1 files and blobs.
08:01 PM Uploaded 1 files and blobs.
08:01 PM Compilation starting.
08:02 PM Compilation completed.
08:02 PM Starting deployment.
08:02 PM Checking if deployment succeeded.
08:02 PM Deployment successful.
08:02 PM Checking if updated app version is serving.
08:02 PM Completed update of app: s~your-app-id, version: auto
```

It will serve

* a browser interface for adding entries to the feed at http://your-app-id.appspot.com/
* the Atom feed at http://your-app-id.appspot.com/feed
