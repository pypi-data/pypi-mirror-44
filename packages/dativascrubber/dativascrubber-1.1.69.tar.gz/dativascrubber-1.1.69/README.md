# Dativa Scrubber

The Scrubber class runs a set of cleansing rules specified in the config parameter on a pandas [DataFrame](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html) that is passed to it.

It can run basic data type validation, session validation, duplication checks, and verification against external reference lists. When data does not meet the validation rules, the library can attempt to automatically fix the data or quarantine it for later investigation.

The library returns a report object that contains details on the cleansing that has been done on the DataFrame. The entries within this report can be logged locally, used to create an email report, or logged centrally to a centralized logging stack like the [Elastic stack](https://www.elastic.co/products) or CloudWatch.

## Basic usage

You can instantiate a Scrubber class with no parameters and then call the run() function with a suitable config and the DataFrame you want to have cleansed:

```python
from dativa.scrubber import Scrubber
import pandas as pd

scrubber = Scrubber()
df = pd.read_csv("path/to/file.csv")

report = scrubber.run(df,
                config={"rules": [
                 {
                     "rule_type": "String",
                     "field": "Name",
                     "params": {
                         "fallback_mode": "remove_record",
                         "maximum_length": 40,
                         "minimum_length": 1
                     },
                 }]})

for entry in report:
    print (entry)
    print (entry.df.describe())

```

The config parameter contains a JSON-style object structured as follows:

* **rules** - an array containing the rules
    - **rule** - an object containing the configuration of each rule
        + **field** - the number or name of the field to which this rule is applied for single field rules
        + **rule_type** - the type of the rule
        + **append_results** - set to True if the results of the rule should be appended to the source DataFrame as a new column
        + **params** - the parameters specific to the rule

An example rule to process  a single field called "Name", and remove blanks records is shown below:

```python
config = {
    "rules": [
        {
            "rule_type": "String",
            "field": "Name",
            "params": {
                "fallback_mode": "remove_record",
                "maximum_length": 40,
                "minimum_length": 1
            },
        }
    ]
},
```

The parameters vary according to the type of rule. The following values for "rule_type" are supported:

* Single column rules
    - "String" - validates string data
    - "Number" - validates numbers
    - "Date" - validates dates
    - "Lookup" - checks fields against a separate dataset
* Multiple column rules
    * "Session" - validates session data
    * "Uniqueness" - validates the uniqueness of fields

## Validating basic data types

The basic data type validation rules are String, Number, and Date.

### rule_type: "String"

String rules validates a field as a string, according to its length and optionally using a regular expression.

It takes the following parameters:

* **minimum_length** - the minimum length of the string, defaults to  0
* **maximum_length** - the maximum allowed length of the string, defaults to  1024
* **regex** - a regular expression to be applied to validate the string. This is processed using the standard Python regular expression processor and supports all syntax documented [here](https://docs.python.org/3/library/re.html). It defaults to ".*"

The example below validates that a string is between 1 and 40 characters and contains only alphanumeric characters:

```python
config = {
    "rules": [
        {
            "rule_type": "String",
            "field": "Name",
            "params": {
                "fallback_mode": "remove_record",
                "maximum_length": 40,
                "minimum_length": 1,
                "regex": "\w*"
            },
        }
    ]
},
```

### rule_type: "Number"

Number rules validate a field as a number, according to the number of decimal places and its size.

It takes the following parameters:

* **minimum_value** - the minimum allowed value of the number, defaults to  0
* **maximum_value** - the maximum allowed value of the number, defaults to  65535
* **decimal_places** - the number of decimal places the number should contain, required
* **fix_decimal_places** - if set to True, the default value, the rule will automatically fix all records to the same number of decimal places, 
                            rather than applying the fallback if the number of decimal places does not match.

If the column of the passed DataFrame is of dtype float then decimal places validation is 

The example below validates that a number is between 0 and 255 and contains no decimal places. Any invalid decimal places are fixed automatically.

```python
config = {
    "rules": [
        {
            "rule_type": "Number",
            "field": "Name",
            "params": {
                "fallback_mode": "remove_record",
                "minimum_value": 0,
                "maximum_value": 255,
                "decimal_places": 0,
                "fix_decimal_places": True
            },
        }
    ]
},
```

### rule_type: "Date"

Date rules validate the field as a date, date format and the range of the dates.

It takes the following parameters:

* **date_format** - the format of the date parameter. This is based on the standard [strftime](http://strftime.org) parameters with the addition of the format '%s' represents an integer epoch time in seconds.
* **range_check** -  this can be set to the following values:
    -  **none** -  in which case the date is not checked
    -  **fixed** - in which case the field is validated to lie between two fixed dates
    -  **rolling** in which case the field is validated against a rolling window of days.
* **range_minimum** - if range_check is set to "fixed" then this represents the start of the date range. If the range check is set to "rolling" it represents the offset from the current time, in days, that should be used as the earliest point in the range. The default value is '2000-01-01 00:00:00'
* **range_maximum** - if range_check is set to "fixed" then this represents the end of the date range. If the range check is set to "rolling" it represents the offset from the current time, in days, that should be used as the latest point in the range. The default value is '2020-01-01 00:00:00'

The example below validates that a date is in epoch time and within the last week of whenever the rule is run:

```python
config = {
    "rules": [
        {
            "rule_type": "Date",
            "field": "Name",
            "params": {
                "fallback_mode": "remove_record",
                "date_format": "%s",
                "range_check": "rolling",
                "range_minimum": -7,
                "range_maximum": 0
            },
        }
    ]
},
```

## Reporting

The run() method returns a dictionary of ReportEntry objects. The report entry object contains a number of different objects:

* ReportEntry.date - a python datetime object for when the entry was created
* ReportEntry.field - a string representing the name of the field which was processed
* ReportEntry.number_records - the number of records effected
* ReportEntry.category - a string categorizing the type of action applied to the rows
* ReportEntry.description - a string with more detail on the action taken
* ReportEntry.df - a pandas DataFrame containing any records that did not pass validation, and any values they were replaced with

The ReportEntry class serializes to a human readable log file, but it is more common for it to be post-processed into a machine readable format and for the DataFrames to be saved to disk for later review.

## Handling invalid data

If the data does not validate then a fall back option is applied depending on the specification of the following params:

* **fallback_mode** - specifies what should be done if the data does not comply with the rules, and can take the following values:
    - **"remove_entry"** - the record is removed and quarantined in a dataframe sent to the Logger object passed to the Scrubber class
    - **"use_default"** - the record is removed and replaced with whatever is specified in the "default_value" field
    - **"do_not_replace"** - the record is left unchanged but still logged to the Logger object.
* **default_value** - The value that records that do not validate should be set to if fallback_mode is set to use_default. Defaults to ''.

For String, Number, and Date fields,  there are two additional methods that can be applied for handling invalid data.

The best match options search the other values in the field that meet the validation rule and replaces the invalid value with one that is sufficiently similar. This is controlled by these two parameters:

* **attempt_closest_match** - Specifies whether entries that do not validate should be replaced with the value of the closest matching record in the dataset. If a sufficiently close match, as specified by the string_distance_threshold is not found then the fallback_mode is still applied. Defaults to False
* **string_distance_threshold** - This specifies the default distance threshold for closest matches to be applied. This is a variant of the Jaro [Winkler distance](https://en.wikipedia.org/wiki/Jaro–Winkler_distance) and defaults to 0.7

The best matching is not possible where invalid data is blank. In this case an additional option is available to replace a field with a value from the record that is most similar in its other fields. This is known as a lookalike model and is most useful for filling in blank records.

It is enabled with the single parameter:

* **lookalike_match** - This specifies whether entries that do not validates should be replaced with value from the record that looks most similar to the other records. This implements a nearest neighbor algorithm based on the similarity of other fields in the dataset. It is useful for filling in blank records and defaults to False

## Anonymising data

Two different forms of data anonymisation are supported:

* Hashing - where the data is replaced with a hash using the SHA512 hashing algorithm with customisable salt
* Encryption - where data is encrypted with a public certificate

Hashing provides a second irreversible mechanism for anonymisation but collisions may occur so the hashes cannot be guaranteed to be unique. The salt applied to the hash can also be keyed from a date making the hashes persistent only for a limited period of time.

Encryption provides full reversible anonymization for those with the private certificate. Encryption supports the PKCS1 algorithm optimal asymmetric encryption padding 'OAEP'. The padding adds randomness to the encrypted output and we can either use a truly random number for continuously changing encrypted values, a fixed value for static encrypted values, or a fixed number based on a data field allowing for pseudo-rotating-tokens with different encrypted values for each time period.

### Hashing

String fields can be hashed by setting the **hash** parameter to True. Hashes are constructed from a SHA512 hash algorithm with a salt of up to 16 bytes added. The salt can be constructed from a date field to allow rotating hashes.

The following rule would hash an email address in a hash:

```python
rules={
  "rule_type": "String",
  "field": "email_address",
  "params": {
      "minimum_length": 5,
      "maximum_length": 1024,
      "regex": "[^@]+@[^\\.]..*[^\\.]",
      "fallback_mode": "remove_record",
      "hash": True,
      "salt": "XY@4242SSS"
  }}
```

This rule would hash an email address with salt that changes daily:

```python
rules={
"rule_type": "String",
"field": "from",
"params": {
  "minimum_length": 5,
  "maximum_length": 1024,
  "regex": "[^@]+@[^\\.]..*[^\\.]",
  "fallback_mode": "remove_record",
  "hash": True,
  "salt": "XY@4242SSS%y%m%d",
  "salt_date_field": "date",
  "salt_date_format": "%Y-%m-%d %H:%M:%S"
}},
```

The full parameters for hashing are:

* **hash** - specifies whether the field should be hashed
* **hash_length** - the length of the hash to use, defaults to 16 characters. Can be up to 128 characters. The longer the hash, the fewer hash collisions will occur.
* **salt** - the salt to be used in the hash, up to 16 bytes in length. This can contain strftime data format parameters to create a rotating salt
* **salt_date_field** - if specified, then a date is parsed from this field using the data format and applied to the salt using strftime formatting. This allows for rotating hashes
* **salt_date_format** - must be specified if salt_date_field is specified. This date format is used to parse the date from the salt_date_field

### Encryption

Encryption can be enabled by setting the **encrypt** parameter on a string rule. Encryption uses OAEP padding to ensure the encryption is irreversible. If you want consistent encrypted values from source values then set **random_string** to a fixed value, or apply time-wise rotation on this value to create rotating encryption.

* **encrypt** - specifies whether the field should be hashed
* **public_key** - the public key to be used in encryption
* **random_string** - defaults to "random" in which case a random string is generated according to the standard PKCS1 AOEP algorithm. If this is set then this string (padded to 20 bytes) is used as the random string in the PKCS1 AOEP algorithm. If this is fixed then it will results in consistent values for all time.
* **random_string_date_field** - if specified, then a date is parsed from this field using the data format and applied to the random using strftime formatting. This allows for rotating encryption
* **random_string_date_format** - must be specified if random_string_date_field is specified. This date format is used to parse the date from the random_string_date_field

The following rule would encrypt an email address with different value each time it is encrypted:

```python
rules={
"rule_type": "String",
"field": "email_address",
"params": {
  "minimum_length": 5,
  "maximum_length": 1024,
  "regex": "[^@]+@[^\\.]..*[^\\.]",
  "fallback_mode": "remove_record",
  "encrypt": True,
  "public_key": """-----BEGIN PUBLIC KEY-----
                   MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDDmPPm5UC8rXn4uX37m4tN/j4T
                   MAhUVyxN7V7QxMF3HDg5rkl/Ju53DPJbv59TCvlTCXw1ihp9asVyyYpCqrsKCh10
                   sZI0kIrkizlKaB/20Q4P1kYOCgv4Cwds7Iu2y0TFwDosK9a7MPR9IksL7QRWKjD0
                   DoNemKEpyCt2dZTaQwIDAQAB
                   -----END PUBLIC KEY-----"""
}}
```

The following rule would encrypt an email address with different value for each day:

```python
rules={
"rule_type": "String",
"field": "email_address",
"params": {
  "minimum_length": 5,
  "maximum_length": 1024,
  "regex": "[^@]+@[^\\.]..*[^\\.]",
  "fallback_mode": "remove_record",
  "encrypt": True,
  "public_key": """-----BEGIN PUBLIC KEY-----
                   MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDDmPPm5UC8rXn4uX37m4tN/j4T
                   MAhUVyxN7V7QxMF3HDg5rkl/Ju53DPJbv59TCvlTCXw1ihp9asVyyYpCqrsKCh10
                   sZI0kIrkizlKaB/20Q4P1kYOCgv4Cwds7Iu2y0TFwDosK9a7MPR9IksL7QRWKjD0
                   DoNemKEpyCt2dZTaQwIDAQAB
                   -----END PUBLIC KEY-----""",
  "random_string": "XY@4242SSS%y%m%d",
  "random_string_date_field": "date",
  "random_string_date_format": "%Y-%m-%d %H:%M:%S"
}}
```

## Validating against a separate dataset

Some fields can be validated with reference to a known dataset. This includes unique identifiers, primary keys in database ETL, and categorical datasets.

In order to implement this, additional reference dataframe(s) need to be passed to Scrubber.run() in the df_dict parameter and a rule of **rule_type**="Lookup" used.

The lookup rules have the following parameters:

* **original_reference** - specifies the entry in the df_dict dictionary containing the reference dataframe
* **reference_field** - the name or number of the column in the reference DataFrame that contains the values that this field should be validated against.
* **attempt_closest_match** - Specifies whether entries that do not validate should be replaced with the value of the closest matching record in the _reference DataFrame_. If a sufficiently close match, as specified by the string_distance_threshold is not found then the fallback_mode is still applied. Defaults to False
* **string_distance_threshold** - This specifies the default distance threshold for closest matches to be applied. This is a variant of the Jaro [Winkler distance](https://en.wikipedia.org/wiki/Jaro–Winkler_distance) and defaults to 0.7

```python
from dativa.scrubber import Scrubber
import pandas as pd

scrubber = Scrubber()
df = pd.read_csv("path/to/file.csv")
db_df = pd.read_csv("path/to/products.csv")


report = scrubber.run(df,
                config={"rules": [
                 {
                     "rule_type": "Lookup",
                     "field": "product_guid",
                     "params": {
                         "fallback_mode": "remove_record",
                       "original_reference": "product_db_df",
                         "reference_field": "guid"
                     },
                 }]},
                 df_dict= {"product_db_df": db_df})

for entry in report:
    print (entry)
    print (entry.df.describe())

```

Note in the above example, the key of the DataFrame in the df_dict is the same as the value of the **original_reference** field.

## Checking for duplication

Duplication can be checked on String, Number, and Date fields by setting the parameter is_unique:

* **is_unique** - specifies whether this column should only contain unique values, defaults to False

In additional, Uniqueness rules can be set up which check for uniqueness across multiple sets of columns. These have the **rule_type**="Uniqueness" and automatically quarantine any data that does not meet the criteria.

They take the following parameters:

* **unique_fields** - a comma separated list of the fields that should be checked for uniqueness, e.g "device_id,date"
* **use_last_value** - specifies whether the the first or last duplicate value should be taken. Defaults to False

Note that "rule_type": "Uniqueness" does not use the "field" parameter:

```python
config = {
    "rules": [
        {
            "rule_type": "Uniqueness",
            "params": {
                "unique_fields": "device_id,date"
            },
        }
    ]
},
```

## Handling blanks

Sometimes it's fine to have blanks in a file, and in this case you can specify the **skip_blank** parameter in the config:

* **skip_blank** - specified whether blank values in this field should be checked or whether they can be skipped, defaults to False


```python
config = {
    "rules": [
        {
            "rule_type": "Date",
            "field": "Name",
            "params": {
                "fallback_mode": "remove_record",
                "date_format": "%s",
                "range_check": "rolling",
                "range_minimum": -7,
                "range_maximum": 0,
                "skip_blank": True
            },
        }
    ]
},
```

Where there are significant blanks in categorical data, you can use the lookalike match field to fill these automatically:

* **lookalike_match** - This specifies whether entries that do not validates should be replaced with value from the record that looks most similar to the other records. This implements a nearest neighbor algorithm based on the similarity of other fields in the dataset. It is useful for filling in blank records and defaults to False

## Working with session data

As session data is common in IOT applications, we have a special rule to validate session data, removing overlapping sessions and filling any gaps. **rule_type**="Session" provides special functionality to handle session data:

* **key_field** - specifies the field that keys the session. For most IOT applications is would be th device ID. If two sessions overlap on the same value of key_field then they will be truncated. Defaults to None
* **start_field** - specifies the field that controls the start of the session. Defaults to None
* **end_field** - specifies the field that controls the end of the session.  Defaults to None
* **date_format** -  the format of the date parameter. This is based on the standard [strftime](http://strftime.org) parameters with the addition of the format '%s' represents an integer epoch time in seconds
* **overlaps_option** - specifies how overlaps should be handled:
    -  "**ignore**" - overlaps are not processed
    -  "**truncate_start**" - the overlap is resolved by truncating the start of the next session
    -  "**truncate_end**" - the overlap is resolved by truncating the end of the previous session
* **gaps_option** - specifies how overlaps should be handled:
    - "**ignore**" - gaps are ignored
    - "**extend_start**" - the gaps are resolved by extending the start of the next session
    - "**extend_end**" - the gaps are resolved by extending the end of the previous session
    - "**insert_new**" - the gaps are resolved by inserting a new session as specified in the "template_for_new" parameter
* **template_for_new** -  contains a comma separated list of values that will be used a a template for a new row in the DataFrame to fill the gap. The key_field, start_field, and end_field will be replaced with appropriate vlaues to fill any gaps.
* **allowed_gap_seconds** -  specifies how many seconds of a gap are allowed before the gap options are implemented, defaults to 1
* **allowed_overlap_seconds** - specifies how many seconds of overlap are allowed before the overlap options are implemented,  defaults to 1
* **remove_zero_length** -  specifies whether zero length sessions should be removed. defaults to True

## Altering the profile

The file processor contains a profile specifying the number of records that can be processed, with the following defaults:

* **maximum_records** = 2,000,000 - the maximum number of records to process in a single DataFrame
* **maximum_records_closest_matches** = 5000 - the maximum number of records that the closest match will be applied to in a single run
* **maximum_records_lookalike** = 5000 - the maximum number of of records that will be fixed by lookalike in a single DataFrame
* **maximum_file_records_lookalike** = 500000 - the maximum number of records in the DataFrame 
* **lookalike_number_records** = 5 - the number of records the lookalike match uses to finalize the lookalike match

These defaults can easily be adjusted according to the memory and CPU available on the server and are customized by passing a custom profile to the Scrubber class:

```python
from dativa.scrubber import Scrubber, DefaultProfile
import pandas as pd

big_profile = DefaultProfile()
big_profile.maximum_records = 100e6

scrubber = Scrubber(profile = big_profile)

df = pd.read_csv("path/to/big_file.csv")

report = scrubber.run(df,
                config={"rules": [
                 {
                     "rule_type": "String",
                     "field": "name",
                     "params": {
                         "fallback_mode": "remove_record",
                         "regex": "[\w\s]*"
                     },
                 }]})
```

## Custom reporting

By default the Scrubber class uses the DefaultReportWriter() class that aggregated ReportEntry() classes and returns them in a list at the end of the project.

In order to write your own custom reporting class you need to implement a class with two interfaces: log_history, and get_report.

Here is an example that simply logs all information to stdout:

```python
from dativa.scrubber import Scrubber
import pandas as pd
from datetime import datetime

class MyReportWriter:

    def log_history(self,
                    rule,
                    field,
                    dataframe,
                    category,
                    description
                    ):
        print("{0}, Field {1}: {2} {3} {4}/{5}".format(datetime.now(),
                                                    field,
                                                    rule,
                                                    dataframe.shape[0],
                                                    category,
                                                    description))

    @staticmethod
    def reset_report():
        pass

    @staticmethod
    def get_report():
        return None

scrubber = Scrubber(report_writer = MyReportWriter())

df = pd.read_csv("path/to/file.csv")

report = scrubber.run(df,
                config={"rules": [
                 {
                     "rule_type": "String",
                     "field": "name",
                     "params": {
                         "fallback_mode": "remove_record",
                         "regex": "[\w\s]*"
                     },
                 }]})


```

## Example configuration

The following is a more sophisticated configuration that demonstrates how multiple fields can be processed. This configuration is included in the test suite for the package.

```python
config={"rules": [
    {
        "params": {
            "attempt_closest_match": True,
            "default_value": "N/A",
            "fallback_mode": "do_not_replace",
            "lookalike_match": False,
            "original_reference": "generic/TV_Titles_Master_50000_records.csv",
            "reference_field": "0"
        },
        "rule_type": "Lookup",
        "field": "0"
    },
    {
        "params": {
            "attempt_closest_match": True,
            "default_value": "N/A",
            "fallback_mode": "do_not_replace",
            "lookalike_match": False,
            "original_reference": "generic/TV_Titles_Master_50000_records.csv",
            "reference_field": "0"
        },
        "rule_type": "Lookup",
        "field": "1"
    },
    {
        "params": {
            "attempt_closest_match": True,
            "default_value": "N/A",
            "fallback_mode": "use_default",
            "lookalike_match": False,
            "maximum_length": 1000,
            "minimum_length": 0,
            "regex": "^0$"
        },
        "rule_type": "String",
        "field": "2"
    },
    {
        "params": {
            "attempt_closest_match": True,
            "default_value": "N/A",
            "fallback_mode": "use_default",
            "lookalike_match": False,
            "maximum_length": 1000,
            "minimum_length": 0,
            "regex": ".+"
        },
        "rule_type": "String",
        "field": "3"
    },
    {
        "params": {
            "attempt_closest_match": True,
            "default_value": "Banana",
            "fallback_mode": "do_not_replace",
            "lookalike_match": False,
            "original_reference": "generic/Genres_Master.csv",
            "reference_field": "0"
        },
        "rule_type": "Lookup",
        "field": "7"
    },
    {
        "params": {
            "attempt_closest_match": True,
            "default_value": "Banana",
            "fallback_mode": "do_not_replace",
            "lookalike_match": False,
            "original_reference": "generic/Genres_Master.csv",
            "reference_field": "0"
        },
        "rule_type": "Lookup",
        "field": "8"
    },
    {
        "params": {
            "attempt_closest_match": True,
            "default_value": "Banana",
            "fallback_mode": "do_not_replace",
            "lookalike_match": False,
            "original_reference": "generic/Genres_Master.csv",
            "reference_field": "0"
        },
        "rule_type": "Lookup",
        "field": "9"
    },
    {
        "params": {
            "attempt_closest_match": True,
            "default_value": "Banana",
            "fallback_mode": "do_not_replace",
            "lookalike_match": False,
            "original_reference": "generic/Genres_Master.csv",
            "reference_field": "0"
        },
        "rule_type": "Lookup",
        "field": "10"
    },
    {
        "params": {
            "attempt_closest_match": True,
            "default_value": "Banana",
            "fallback_mode": "do_not_replace",
            "lookalike_match": False,
            "original_reference": "generic/Genres_Master.csv",
            "reference_field": "0"
        },
        "rule_type": "Lookup",
        "field": "11"
    },
    {
        "params": {
            "attempt_closest_match": True,
            "default_value": "Banana",
            "fallback_mode": "do_not_replace",
            "lookalike_match": False,
            "original_reference": "generic/Genres_Master.csv",
            "reference_field": "0"
        },
        "rule_type": "Lookup",
        "field": "12"
    },
    {
        "params": {
            "attempt_closest_match": True,
            "default_value": "Banana",
            "fallback_mode": "do_not_replace",
            "lookalike_match": False,
            "original_reference": "generic/Genres_Master.csv",
            "reference_field": "0"
        },
        "rule_type": "Lookup",
        "field": "13"
    },
    {
        "params": {
            "attempt_closest_match": True,
            "default_value": "Banana",
            "fallback_mode": "do_not_replace",
            "lookalike_match": False,
            "original_reference": "generic/Genres_Master.csv",
            "reference_field": "0"
        },
        "rule_type": "Lookup",
        "field": "14"
    }
]}
```

## Configuration reference

### String rules

* **minimum_length** - the minimum length of the string, required
* **maximum_length** - the maximum allowed length of the string, required
* **regex** - a regular expression to be applied to validate the string. This is processed using the standard Python regular expression processor and supports all syntax documented [here](https://docs.python.org/3/library/re.html). It default to  ".*"
* **is_unique** - specifies whether this column should only contain unique values, defaults to False
* **skip_blank** - specified whether blank values in this field should be checked or whether they can be skipped, defaults to False
* **fallback_mode** - specifies what should be done if the data does not comply with the rules, and can take the following values:
    - **"remove_record"** - the default value, the record is removed and quarantined in a dataframe sent to the Logger object passed to the Scrubber class
    - **"use_default"** - the record is removed and replaced with whatever is specified in the "default_value" field
    - **"do_not_replace"** - the record is left unchanged but still logged to the Logger object.
* **default_value** - The value that records that do not validate should be set to if fallback_mode is set to use_default. Defaults to ''.
* **attempt_closest_match** - Specifies whether entries that do not validate should be replaced with the value of the closest matching record in the dataset. If a sufficiently close match, as specified by the string_distance_threshold is not found then the fallback_mode is still applied. Defaults to False
* **string_distance_threshold** - This specifies the default distance threshold for closest matches to be applied. This is a variant of the [Jaro Winkler distance](https://en.wikipedia.org/wiki/Jaro–Winkler_distance) and defaults to 0.7
* **lookalike_match** - This specifies whether entries that do not validates should be replaced with value from the record that looks most similar to the other records. This implements a nearest neighbor algorithm based on the similarity of other fields in the dataset. It is useful for filling in blank records and defaults to False

### Number rules

* **minimum_value** - the minimum allowed value of the number, defaults to  0
* **maximum_value** - the maximum allowed value of the number, defaults to  65535
* **decimal_places** - the number of decimal places the number should contains, defaults to  0
* **fix_decimal_places** - if set to True, the default value, the rule will automatically fix all records to the same number of decimal places
* **is_unique** - specifies whether this column should only contain unique values, defaults to False
* **skip_blank** - specified whether blank values in this field should be checked or whether they can be skipped, defaults to False
* **fallback_mode** - specifies what should be done if the data does not comply with the rules, and can take the following values:
    - **"remove_record"** - the default value, the record is removed and quarantined in a dataframe sent to the Logger object passed to the Scrubber class
    - **"use_default"** - the record is removed and replaced with whatever is specified in the "default_value" field
    - **"do_not_replace"** - the record is left unchanged but still logged to the Logger object.
* **default_value** - The value that records that do not validate should be set to if fallback_mode is set to use_default. Defaults to ''.
* **attempt_closest_match** - Specifies whether entries that do not validate should be replaced with the value of the closest matching record in the dataset. If a sufficiently close match, as specified by the string_distance_threshold is not found then the fallback_mode is still applied. Defaults to False
* **string_distance_threshold** - This specifies the default distance threshold for closest matches to be applied. This is a variant of the Jaro [Winkler distance](https://en.wikipedia.org/wiki/Jaro–Winkler_distance) and defaults to 0.7
* **lookalike_match** - This specifies whether entries that do not validates should be replaced with value from the record that looks most similar to the other records. This implements a nearest neighbor algorithm based on the similarity of other fields in the dataset. It is useful for filling in blank records and defaults to False

### Date rules

* **date_format** - the format of the date parameter. This is based on the standard [strftime](http://strftime.org) parameters with the addition of the format '%s' represents an integer epoch time in seconds.
* **range_check** -  this can be set to the following values:
    -  **none** -  in which case the date is not checked
    -  **fixed** - in which case the field is validated to lie between two fixed dates
    -  **rolling** in which case the field is validated against a rolling window of days.
* **range_minimum** - if range_check is set to "fixed" then this represents the start of the date range. If the range check is set to "rolling" it represents the offset from the current time, in days, that should be used as the earliest point in the range. The default value is '2000-01-01 00:00:00'
* **range_maximum** - if range_check is set to "fixed" then this represents the end of the date range. If the range check is set to "rolling" it represents the offset from the current time, in days, that should be used as the latest point in the range. The default value is '2020-01-01 00:00:00'
* **is_unique** - specifies whether this column should only contain unique values, defaults to False
* **skip_blank** - specified whether blank values in this field should be checked or whether they can be skipped, defaults to False
* **fallback_mode** - specifies what should be done if the data does not comply with the rules, and can take the following values:
    - **"remove_record"** - the default value, the record is removed and quarantined in a dataframe sent to the Logger object passed to the Scrubber class
    - **"use_default"** - the record is removed and replaced with whatever is specified in the "default_value" field
    - **"do_not_replace"** - the record is left unchanged but still logged to the Logger object.
* **default_value** - The value that records that do not validate should be set to if fallback_mode is set to use_default. Defaults to ''.
* **attempt_closest_match** - Specifies whether entries that do not validate should be replaced with the value of the closest matching record in the dataset. If a sufficiently close match, as specified by the string_distance_threshold is not found then the fallback_mode is still applied. Defaults to False
* **string_distance_threshold** - This specifies the default distance threshold for closest matches to be applied. This is a variant of the Jaro [Winkler distance](https://en.wikipedia.org/wiki/Jaro–Winkler_distance) and defaults to 0.7
* **lookalike_match** - This specifies whether entries that do not validates should be replaced with value from the record that looks most similar to the other records. This implements a nearest neighbor algorithm based on the similarity of other fields in the dataset. It is useful for filling in blank records and defaults to False

### Lookup rules

* **original_reference** - specifies the entry in the df_dict dictionary containing the reference dataframe
* **reference_field** - the name or number of the column in the reference DataFrame that contains the values that this field should be validated against.
* **attempt_closest_match** - Specifies whether entries that do not validate should be replaced with the value of the closest matching record in the _reference DataFrame_. If a sufficiently close match, as specified by the string_distance_threshold is not found then the fallback_mode is still applied. Defaults to True
* **string_distance_threshold** - This specifies the default distance threshold for closest matches to be applied. This is a variant of the Jaro [Winkler distance](https://en.wikipedia.org/wiki/Jaro–Winkler_distance) and defaults to 0.7
* **skip_blank** - specified whether blank values in this field should be checked or whether they can be skipped, defaults to False
* **fallback_mode** - specifies what should be done if the data does not comply with the rules, and can take the following values:
    - **"remove_record"** - the default value, the record is removed and quarantined in a dataframe sent to the Logger object passed to the Scrubber class
    - **"use_default"** - the record is removed and replaced with whatever is specified in the "default_value" field
    - **"do_not_replace"** - the record is left unchanged but still logged to the Logger object.
* **default_value** - The value that records that do not validate should be set to if fallback_mode is set to use_default. Defaults to ''.
* **lookalike_match** - This specifies whether entries that do not validates should be replaced with value from the record that looks most similar to the other records. This implements a nearest neighbor algorithm based on the similarity of other fields in the dataset. It is useful for filling in blank records and defaults to False

### Uniqueness rules

* **unique_fields** - a comma separated list of the fields that should be checked for uniqueness, e.g "device_id,date"
* **use_last_value** - specifies whether the the first or last duplicate value should be taken. Defaults to False

### Session rules

* **key_field** - specifies the field that keys the session. For most IOT applications is would be th device ID. If two sessions overlap on the same value of key_field then they will be truncated. Defaults to None
* **start_field** - specifies the field that controls the start of the session. Defaults to None
* **end_field** - specifies the field that controls the end of the session.  Defaults to None
* **date_format** -  required parameter based on the [strftime](http://strftime.org) parameters
* **overlaps_option** - specifies how overlaps should be handled:
    -  "**ignore**" - overlaps are not processed
    -  "**truncate_start**" - the overlap is resolved by truncating the start of the next session
    -  "**truncate_end**" - the overlap is resolved by truncating the end of the previous session
* **gaps_option** - specifies how overlaps should be handled:
    - "**ignore**" - gaps are ignored
    - "**extend_start**" - the gaps are resolved by extending the start of the next session
    - "**extend_end**" - the gaps are resolved by extending the end of the previous session
    - "**insert_new**" - the gaps are resolved by inserting a new session as specified in the "template_for_new" parameter
* **template_for_new** -  contains a comma separated list of values that will be used a a template for a new row in the DataFrame to fill the gap. The key_field, start_field, and end_field will be replaced with appropriate vlaues to fill any gaps.
* **allowed_gap_seconds** -  specifies how many seconds of a gap are allowed before the gap options are implemented, defaults to 1
* **allowed_overlap_seconds** - specifies how many seconds of overlap are allowed before the overlap options are implemented,  defaults to 1
* **remove_zero_length** -  specifies whether zero length sessions should be removed. defaults to True

# Dativa File Analyser

The file analyser provides tools for analyzing CSV files and in particular creating configurations for use with the Dativa Scrubber.

## Installation

You can install using one of the following

```bash

# using bitbucket username and password:

pip install --upgrade git+http://bitbucket.org/dativa4data/file-processing@master

# using bitbucket SSH key:
pip install --upgrade git+ssh://bitbucket.org/dativa4data/file-processing@master
```

## Command Line Toool

The file analyzer installs a command line tool fanalyzer which takes a CSV file and produces a description of the fields and configuration for the Scrubber:

### Examples

```bash

fanalyzer my_csv.csv

fanalyzer --csv_delimeter=\| pip_delimited.csv
```

### Positional arguments

* csv_file :the file to parse

### optional arguments

* csv_delimiter CSV_DELIMITER : the csv delimiter (default: ,)
* maximum_string_length MAXIMUM_STRING_LENGTH : the maximum length of string allowed (default: 1024)
* large_sample_size LARGE_SAMPLE_SIZE : the number of rows to sample (default: 10000)
* small_sample_size SMALL_SAMPLE_SIZE : the number of rows to sample for memory intensive operations (default: 1000)
* clean_threshold CLEAN_THRESHOLD : the % of rows that must meet the criteria (default: 0.95)
* outlier_threshold OUTLIER_THRESHOLD : the number of standard deviations for an outlier to be ignored (default: 2)
* min_occurences MIN_OCCURENCES : the minimum number of times an item must appear to be considered a lookup item (default: 5)
* min_references MIN_REFERENCES : the minimum number of items to be classified as a lookup, lower than this will be treated using a regex (default: 20)
* max_references MAX_REFERENCES : the maximum number of items to be classified as a lookup (default: 1000)

## Using in a program

```python

import pandas as pd
from dativa.analyzer import AutoConfig
from dativa.tools.pandas import CSVHandler

file = "test.csv"

csv = CSVHandler()
df = csv.get_dataframe(file, force_dtype=pd.np.str)  # always load as a string when using the file analyzer
ac = AutoConfig()

auto_config, df_dict = ac.create_config(df)
```

# PersistentFieldLogger

The PersistentFieldLogger can be used like a python logger but takes keyword arguments. These keyword arguments are logged as a JSON object. Any keyword arguments specified when creating the PersistentFieldLogger will be persisted.

```
logger = logging.getLogger("dativa.espn")

# create a field logger that persists the value of the field "file"
field_logger = PersistentFieldLogger(logger, {"file": ""})

field_logger.info(file="test", message="the knights")
field_logger.info(message="who say Ni")
```

This should log:
INFO - {"file": "test", "message" : "the knights"}
INFO - {"file": "test", "message" : "who say Ni"}

The persistent field logger is normally used with the LoggingReportWriter class