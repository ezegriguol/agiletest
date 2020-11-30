Requeriments to deploy the app.
1) GCP Account activated for billing.
2) Terraform in local machine.

Google Cloud Platform services used in this app:
1) Google Cloud Function (to run Python 3.7)
2) Google Firestore (as DB Cache)
3) Google Storage (save the Images)
4) Google Pub/Sub (for trigger the downloads)

The test was done in a cloud serverless environment using Google Cloud Platform.
The images are storage in a Google Storage bucket.
There are 2 endpoints:
	* search
	* downloadall (to be run the first time, download all the images into the storage and populate the DB).
		There is a internal download_detail function that is triggered by a message using pub/sub. Is configured to run only 5 instances in 				paralell (to avoid too many request at the same time to the AgileEngine server).

Example:
	https://us-central1-agileenginetest.cloudfunctions.net/search?tags=#life&camera="Nikon 705"

All the errors & debug information are stored in the GCP Logging service.

I also included the Terraform script with all the resources to deploy in one single click the solution.
Because a limitation of Terraform, the Firestore database should be enabled manually in GCP.
Also, it's necessary download a json security credential file and assign this to the script.
