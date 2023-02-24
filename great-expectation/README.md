# Great Expectations

It is a leading Python library that allows you to validate, document, and profile your data to make sure the data is as you expected.
Great Expectations go through a checklist to make sure the data passes all these tests before being used.


#Key Features

* __Expectations__ <br>
Expectations are assertions about your data. In Great Expectations, those assertions are expressed in a declarative language in the form of simple, human-readable Python methods.

* __Automated data profiling__ <br>
The library profiles your data to get basic statistics, and automatically generates a suite of Expectations based on what is observed in the data.

* __Data validation__ <br>
Great Expectations tells you whether each Expectation in an Expectation Suite passes or fails, and returns any unexpected values that failed a test, which can significantly speed up debugging data issues!

* __Data Docs__ <br>
Great Expectations renders Expectations to clean, human-readable documentation, which we call Data Docs.

* __Diverse Datasources and Store backends__ <br>
Various datasources such Pandas dataframes, Spark dataframes, and SQL databases via SQLAlchemy.


# Getting Started

1. **Expectations suite json**
 * [nexrad_suite](/great-expectation/great_expectations/expectations/nexrad_suite.json)
 * [goes18_suite](/great-expectation/great_expectations/expectations/goes18_suite.json)

2. **Data Docs html report**
[nexrad_suites](/great-expectation/great_expectations/uncommitted/data_docs/local_site/index.html)


## Dataset

* [metadata.csv](/great-expectation/great_expectations/data/metadata.csv)
* [nexrad.csv](/great-expectation/great_expectations/data/nexrad.csv)

# Step 01: Environment Setup and activation

```bash
python -m venv environment_name
```
```bash
source ./environment_name/bin/activate
```

## 1.0 Create a folder named `great-expectation` 

## 1.1 Install module `great_expectations`
```bash
pip install great_expectations
```

## 1.2 Verify the version
```bash
great_expectations --version
```

Output : `great_expectations, version 0.15.46`

## 02. Initialization at the base directory

```bash
great_expectations init
```


Change working directory to the newly created directory, great_expectations

```bash
cd great_expectations
```

## 03. Import data into the current repo
Copy the scv files into `great_expectations/data`

>metadata.csv
>nexrad.csv


# Step 02: Connect to the Datasource(data)
## 04.Launch Cli datasource process
```bash
great_expectations datasource new
```

Input following in the prompt
> `1`- Local file <br> `1`-Pandas <br> `data`-relative path to datasets

The first Jupyter notebook should opens<br>

* Change datasource_name to nexrad_datasource(goes18_datasource)
* Add \.csv to line 13 pattern: (.*)\.csv to ignore all other type of files

* Save the datasource Configuration
* Close Jupyter notebook
* Wait for terminal to show Saving file at /datasource_new.ipynb


# Step 03: Creating Expectations for data(nexrad and goes18)

## 3.1.Launch CLI suite
```bash
great_expectations suite new
```

Input the following choices
> '3'-Automatically,using a profiler 
> `1`-Select index for file : 
 1-metadata
 2-nexrad
> suite name:
`goes18_suite for metadata`
`nexrad_suite for nexrad`

* Opens up a Jupyter notebook,
* Check if the datasource_name is correct

* Run to create default expectations and analyze the results

* Wait for the terminal to show `Saving file at /edit_nexrad_suite.ipynb`

* Modify expectations as per your requirements 
* Modified the JSON file `great_expectations/expectations/nexrad_suite.json`

```bash
  great_expectations suite edit nexrad_suite
```

Input to the Prompt:
> '1'- Manually, without interacting with a sample batch of data


# Step 04:Validate Data

## 4.1. Create Checkpoint

```bash
great_expectations checkpoint new nexrad_checkpoint
```

This opens a Jupyter notebook,<br>

* Uncomment the last cell pf the Jupyter notebook
* Run all cells
* Report should pop up in the new page

# Step 05:Commit the following files and folders

* great_expectations/data

* great_expectations/expectations/*.json

* great_expectations/uncommitted/data_docs/*

* great_expectations/uncommitted/*.ipynb

# Step 06:Deploy using S3 Bucket

# Setup

Documentation : https://docs.greatexpectations.io/docs/deployment_patterns/how_to_use_gx_with_aws/how_to_use_gx_with_aws_using_cloud_storage_and_pandas/

## 6.1.1.Verify that the AWS CLI is installed

```bash
  aws --version
```

## 6.1.2.Verify that your AWS credentials are properly configured

```bash
aws sts get-caller-identity
```

# 6.2 Prepare a local installation of Great Expectations

## 6.2.1 Verify that your Python version meets requirements
```bash
python --version
```
## 6.2.2.Create virtual environment
```bash
python -m venv my_venv
```

## 6.2.3.Ensure your virtual environment is activated
```bash
source my_venv/bin/activate
```

## 6.2.3.Install boto3
```bash
python -m pip install boto3
```

# 6.4 Configure your Expectations Store on Amazon S3

## 6.4.1 Identify your Data Context Expectations Store

In your `great_expectations.yml` file, look for the following lines:
```bash
expectations_store_name: expectations_store

stores:
  expectations_store:
      class_name: ExpectationsStore
      store_backend:
          class_name: TupleFilesystemStoreBackend
          base_directory: expectations/
```

## 6.4.2 Update your configuration file to include a new Store for Expectations on Amazon S3
You can manually add an Expectations Store by adding the configuration shown below into the stores section of your great_expectations.yml file.
```bash
stores:
  expectations_S3_store:
      class_name: ExpectationsStore
      store_backend:
          class_name: TupleS3StoreBackend
          bucket: '<your_s3_bucket_name>'
          prefix: '<your_s3_bucket_folder_name>'
```

Please also note that the new Store's name is set to expectations_S3_store. This value can be any name you like as long as you also update the value of the expectations_store_name key to match the new Store's name.

```bash
expectations_store_name: expectations_S3_store
```
## 6.4.3 Verify that the new Amazon S3 Expectations Store has been added successfully
```bash
great_expectations store list
```
Terminal output
```bash
- name: expectations_S3_store
class_name: ExpectationsStore
store_backend:
  class_name: TupleS3StoreBackend
  bucket: '<your_s3_bucket_name>'
  prefix: '<your_s3_bucket_folder_name>'
```
## 6.4.4 (Optional) Copy existing Expectation JSON files to the Amazon S3 bucket

If you are converting an existing local Great Expectations deployment to one that works in AWS you may already have Expectations saved that you wish to keep and transfer to your S3 bucket.

One way to copy Expectations into Amazon S3 is by using the aws s3 sync command. As mentioned earlier, the base_directory is set to expectations/ by default.
```bash
aws s3 sync '<base_directory>' s3://'<your_s3_bucket_name>'/'<your_s3_bucket_folder_name>'
```

## 6.4.5 (Optional) Verify that copied Expectations can be accessed from Amazon S3

If you followed the optional step to copy your existing Expectations to the S3 bucket, you can confirm that Great Expectations can find them by running the command:
```bash
great_expectations suite list
```

```bash
Terminal output
2 Expectation Suites found:
- exp1
- exp2
```

# 6.5 Configure your Validation Results Store on Amazon S3
## 6.5.1 Identify your Data Context's Validation Results Store

Look for the following section in your Data Context's great_expectations.yml file:
File contents: great_expectations.yml

```bash
validations_store_name: validations_store

stores:
  validations_store:
      class_name: ValidationsStore
      store_backend:
          class_name: TupleFilesystemStoreBackend
          base_directory: uncommitted/validations/
```
## 6.5.2 Update your configuration file to include a new Store for Validation Results on Amazon S3

You can manually add a Validation Results Store by adding the configuration below to the stores section of your great_expectations.yml file:
```bash
stores:
  validations_S3_store:
      class_name: ValidationsStore
      store_backend:
          class_name: TupleS3StoreBackend
          bucket: '<your_s3_bucket_name>'
          prefix: '<your_s3_bucket_folder_name>'
```
Change the following in the files as before as well:
```bash
validations_store_name: validations_S3_store
```
## 6.5.3 Verify that the new Amazon S3 Validation Results Store has been added successfully
```bash
great_expectations store list
```
## 6.5.4 (Optional) Copy existing Validation results to the Amazon S3 bucket
You can copy Validation Results into Amazon S3 is by using the aws s3 sync command. As mentioned earlier, the base_directory is set to uncommitted/validations/ by default
```bash
aws s3 sync '<base_directory>' s3://'<your_s3_bucket_name>'/'<your_s3_bucket_folder_name>'

```
# 6.6 Configure Data Docs for hosting and sharing from Amazon S3

## 6.6.1 You can create an S3 bucket configured for a specific location using the AWS CLI. Make sure you modify the bucket name and region for your situation
You can create an S3 bucket configured for a specific location using the AWS CLI. Make sure you modify the bucket name and region for your situation

```bash
aws s3api create-bucket --bucket data-docs.my_org --region us-east-1
```
## 6.6.2 Configure your bucket policy to enable appropriate access
The example policy below enforces IP-based access - modify the bucket name and IP addresses for your situation. After you have customized the example policy to suit your situation, save it to a file called ip-policy.json in your local directory.

File content: ip-policy.json
```bash
{
    "Version": "2012-10-17",
    "Statement": [{
      "Sid": "Allow only based on source IP",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": [
        "arn:aws:s3:::data-docs.my_org",
        "arn:aws:s3:::data-docs.my_org/*"
      ],
      "Condition": {
        "IpAddress": {
          "aws:SourceIp": [
            "192.168.0.1/32",
            "2001:db8:1234:1234::/64"
          ]
        }
      }
    }
    ]
  }

```

## 6.6.3 Apply the access policy to your Data Docs' Amazon S3 bucket
```bash
aws s3api put-bucket-policy --bucket data-docs.my_org --policy file://ip-policy.json
```
## 6.6.4 Add a new Amazon S3 site to the data_docs_sites section of your great_expectations.yml

The below example shows the default local_site configuration that you will find in your great_expectations.yml file, followed by the s3_site configuration that you will need to add. You may optionally remove the default local_site configuration completely and replace it with the new s3_site configuration if you would only like to maintain a single S3 Data Docs site.
```bash
data_docs_sites:
  local_site:
    class_name: SiteBuilder
    show_how_to_buttons: true
    store_backend:
      class_name: TupleFilesystemStoreBackend
      base_directory: uncommitted/data_docs/local_site/
    site_index_builder:
      class_name: DefaultSiteIndexBuilder
  s3_site:  # this is a user-selected name - you may select your own
    class_name: SiteBuilder
    store_backend:
      class_name: TupleS3StoreBackend
      bucket: data-docs.my_org  # UPDATE the bucket name here to match the bucket you configured above.
    site_index_builder:
      class_name: DefaultSiteIndexBuilder
      show_cta_footer: true
```
## 6.6.5 Test that your Data Docs configuration is correct by building the site
Use the following CLI command: great_expectations docs build --site-name s3_site to build and open your newly configured S3 Data Docs site.
```bash
great_expectations docs build --site-name s3_site
```
You will be presented with the following prompt:
```bash
The following Data Docs sites will be built:

 - s3_site: https://s3.amazonaws.com/data-docs.my_org/index.html

Would you like to proceed? [Y/n]:

```
Signify that you would like to proceed by pressing the return key or entering Y. Once you have you will be presented with the following messages:
Output:
```bash
Building Data Docs...

Done building Data Docs
```

Our hosted site: http://data-great-expect.s3-website-us-east-1.amazonaws.com

#END