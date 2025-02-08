# Tool usage
In this section, the usage of the tool will be described both locally and CI integrated.

## Local usage
Local usage or our tool is an important aspect for debugging and development. This can be done by doing the following:

1. Configuring a local MongoDB instance through their documentation: <https://www.mongodb.com/docs/manual/administration/install-community/>
2. Have a local version (clone) of an experiment
3. Clone this repository and install its dependencies (in venv if you want)
4. Create a .env file based on the .env-local file in the repository
6. Run the following command: `python main.py <relative_path_to_experiment>`
7. Metadata should be in the local MongoDB

## CI Integrated usage
The extraction tool is best used as an automated CI step. This will result in metadata creation, even while the experiment is still in development. Based on the tool in this repository, a demo repository has bee created: <https://github.com/Thijsrausch/pos-metadata-extractor-demo>. To create a CI integrated setup through GitHub Actions, such as in the demo repository, follow the steps below.

1. Create a hosted MongoDB, there is a free tier in MongoDB atlas: <https://www.mongodb.com/docs/atlas/getting-started/>
2. Create a database in your hosted instance with a collection to store the metadata (remember this for step 5).
3. Create a repository with an experiment or fork / use an existing experiment
4. Add the custom action configuration and metadata extraction tool to the experiment repository, see for example this commit: <https://github.com/gallenmu/pos-artifacts/commit/331f95c7da5498360d2813d74d20a9cb7dd02e95>
5. Set environment variables in the repository based on the .env-github-action file that is within this repository. This file contains the required variables for the GitHub Action to run. They are used for setting up a connection to MongoDB. The following variables are required:
  * MONGO_URI: get the URI from your hosted environment
  * DATABASE_NAME: the name you want your database to get or already has
  * CURRENT_COLLECTION_NAME: the name you want your collection to get or already has
* ACTION=true: this is used to indicate that we are running the metadata extractor in a GitHub action and not locally
6. Push to the repository and check that the action is running and data is being outputted to your MongoDB instance.
