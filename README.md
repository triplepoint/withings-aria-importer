# Intro
So you've got weight and body fat data in Fitbit that you'd like to export to Withings.

Fitbit and Withings have an [integration set up to export your activity tracker data](https://www.withings.com/us/en/switch-to-withings), but nothing to handle weight data.

With a little manual work, you can do it yourself.

# Procedure
## Fitbit Full Account Archive
Log into your Fitbit account and ask them to "[export your account archive](https://www.fitbit.com/settings/data/export)"

This will take some time depending on the amount of data they have.  You can watch the percentage on that page, or just wait for them to email you when it's done.  Note you can only do this once every 24 hours, so make sure all the data you want is in their database before you request the dump.

## Generate Withings Uploadable CSV files
Once you've got the `MyFitbitData.zip` file from Fitbit, clone this repository to a working directory somewhere, and copy the fitbit .zip file into it.  Unzip the archive, and you should have a directory something like `SomeUserName`.

Run the script (this contacts no external services, and is safe to run):
``` sh
./generate_csv_files.py <path_to_folder_with_fitbit_files>
```
Example:
```
./generate_csv_files.py "./SomeUserName/user-site-export/"
```

This will cull through the downloaded Fitbit archive data, pull out your weight data, and reorganize it into a set of `weight_dataN.csv` files, which it creates in the same directory as the script ran.  Note that it creates several instead of one, because Withings states a 300 line maximum per file.

## Upload the CSV files to Withings
Log into [the Health Mate dashboard](https://healthmate.withings.com).

Click your "Account" in the top right hand corner, click "settings", and then click your user icon to bring up your user preferences.

Click `import my data`, and click the `Browse...` button in the Weight section.

Find the first generated weight data file, `weight_data1.csv`, and upload it.  Wait for the page to refresh.

Repeat for the remaining generated `weight_dataN.csv` files.

## Verify the Data
Once you're done here, you can verify the historical data is in place by going to the Weight section of the Health Mate website, and clicking "All" at the bottom of the screen.  You should see your historical Fitbit data.
