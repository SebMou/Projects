<h2>General considerations</h2>

Pipeline for model refreshing (possibly airflow):
How often is the documentation updated?
    Everyday - Daily refresh the model
    Not that often - Monthly/Weekly refresh the model
    Ideally - Refresh everytime there is a change in documentation

Data storage configuration:
    https://confluence.atlassian.com/doc/configuring-s3-object-storage-1206794554.html
    Store data in a bucket and define IAM for any sensitive data
    Show the documentation in Confluence for ease of reading
    Will we have several document formats and can we store them in the bucket?

High level workflow:
    Fetch data from confluence to train the model, host a page with a Chatbot/search bar which answers your questions and
    provides links to confluence pages

Extra steps:
    Test/select other models
    Fine tuning
    Better UI
    Save model to be reused between questions


<h2>Running the program</h2>
In order to run the program simply call the script which will ask the questions from the proposed scenario
and print the answers. It will also run a nonsense question to show how it will react to questions it
is not able to answer:
```
python RAG.py
```

<h2>Testing</h2>
Unfortunately I was unable to run the tests, as the security definitions would not allow me to do so, but the
general process would look like this.
To run the tests cd to the correct directory:
```
cd tests
```

Then run:
```
promptfoo eval
```

Afterwards, you can view the results by running `promptfoo view`
