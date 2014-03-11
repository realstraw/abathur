# Abathur

> "Look at flesh, see only potential. Strands, sequences, twisting,
> separating, joining. See how it could be better, Eat flesh, splinter bone.
> Inside me, can touch it. Weave it. Spin it. Make it great."
>
> -- Abathur (The evolution master) tells Sarah Kerrigan about his work

Abathur aims to be a easy-to-use automated machine learning and data
torturing toolkit to make the data talk. Currently only supports extract
features using exhaustive query execution.

## Feature Extraction

`abathur extract` is an adhoc feature extraction tool for relational (SQL)
databases, where every value in the feature is extracted with one query.
Although this is not efficient in terms of computation processing, but it does
the job and can be easily used to extract features for given set of targets.

### param file

`abathur extract` expects an *param file*. A *param file* can either be a CSV
file containing the query parameters or a SQL file which query parameters can
be obtained by an SQL query.

An example of CSV *ident file* content:

    ident,param_age
    1,35
    3,35
    12,35
    32,35

An exmample of query *ident file* content:

    select id as ident, 35 as param_age from users where age > 35

You need to add `--query-ident` option if the *param file* is an SQL file.

### query file

The second argument parsed to `abathur extract` is a *query file*. A query file
is a json file that specifies the feature name and the SQL query to extract the
feature. The SQL should contain {param\_key} as a placeholder for putting the
relevant parameters in the *param file*. 

An example of *query file* content:

    {
        "n_followers": "select count(*) from follow where follow_user_id={ident}",
        "n_follow": "select count(*) from follow where user_id={ident} and age>{param_age}"
    }

For help in commandline options:

    abathur extract --help

## Clustering

`abathur cluster`

## Abathur Config

Abathur expects a config file in `~/.abathur.conf` with the following content:

    {
        "db_connection_string": "sqlalchemy_syle_connection_string"
    }

For more about sqlalchemy connection string see [SQLAlchemy Database URLS](http://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls)
