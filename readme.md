# Abathur

> "Look at flesh, see only potential. Strands, sequences, twisting,
> separating, joining. See how it could be better, Eat flesh, splinter bone.
> Inside me, can touch it. Weave it. Spin it. Make it great."
>
> -- Abathur (The evolution master) tells Sarah Kerrigan about his work

Abathur aim to be a comprehensive automated machine learning and data
torturing toolkit to make the data talk. Currently only supports extract
features using exhaustive query execution.

## Feature Extraction

`abathur extract` is an adhoc feature extraction tool for relational (SQL)
databases, where every value in the feature is extracted with one query.
Although this is not efficient in terms of computation processing, but it does
the job and can be easily used to extract features for given set of targets.

### ident file

`abathur extract` expects an *ident file*. An *ident file* can either be a file
with each line as identifiers (of the target instances) or an file containing
SQL command to query the set of identifiers.

An example of identifier *ident file* content:

    1
    3
    12
    32

An exmample of query *ident file* content:

    select id from users where age > 35

You need to add `--query-ident` option if the *ident file* is an sql file.

### query file

The second argument parsed to `abathur extract` is a *query file*. A query file
is a json file that specifies the feature name and the SQL query to extract the
feature. The SQL should contain {ident} as a placeholder for putting the
identifier for the target instance. 

An example of *query file* content:

    {
        "n_followers": "select count(*) from follow where follow_user_id={ident}",
        "n_follow": "select count(*) from follow where user_id={ident}"
    }

For help in commandline options:

    abathur extract --help

Feature extraction is a two step work. First it needs to generate an file
containing a set of IDs. The IDs are normally customer IDs, a set of dates, or
a set of asset IDs, which is a unique identifier for each row.

## Abathur Config

Abathur expects a config file in `~/.abathur.conf` with the following content:

    {
        "db_connection_string": "sqlalchemy_syle_connection_string"
    }

For more about sqlalchemy connection string see [SQLAlchemy Database URLS](http://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls)
