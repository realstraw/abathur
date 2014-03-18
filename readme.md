# Abathur

> "Look at flesh, see only potential. Strands, sequences, twisting,
> separating, joining. See how it could be better, Eat flesh, splinter bone.
> Inside me, can touch it. Weave it. Spin it. Make it great."
>
> -- Abathur (The evolution master) tells Sarah Kerrigan about his work

Abathur aims to be a easy-to-use automated machine learning and data
torturing toolkit to make the data talk.

## Feature Extraction

    usage: abathur extract [-h] [--query-param] param queries output

    Extract (aggregated) features from a sql database.

    positional arguments:
      param          the file with query params or the SQL query that finds the
                     params.
      queries        the set of queries and feature names to be executed.
      output         the output file.

    optional arguments:
      -h, --help     show this help message and exit
      --query-param  the given param file is a query file. by default we assume
                     it's a file that contains a list of query params.

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

    usage: abathur cluster [-h] [--ignore [IGNORE [IGNORE ...]]]
                             feat_filename output

    Perform clustering of the given data set.

    positional arguments:
      feat_filename         The input feature file
      output                The output file name

    optional arguments:
      -h, --help            show this help message and exit
      --ignore [IGNORE [IGNORE ...]]
                            The features (column names) to be ignored. Usually the
                            ID field.

`abathur cluster` takes a input feature file, and performs clustering. The
output is a file with code corresponding to the cluster id for each
corresponding row in the input feature file. It uses an information theoretic
approch detailed in [1] estimate the best number in of clusters. The algorithm
implemented slightly improves [1] by run the jump method multiple times and
gets the lowest number.

## Abathur Config

Abathur expects a config file in `~/.abathur.conf` with the following content:

    {
        "db_connection_string": "sqlalchemy_syle_connection_string"
    }

For more about sqlalchemy connection string see [SQLAlchemy Database URLS](http://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls)

## Reference

1. Catherine A. Sugar and Gareth M. James(2003). "[Finding the number of
   clusters in a data set: An information theoretic approach](http://www.tandfonline.com/doi/abs/10.1198/016214503000000666#.Uyfex9wRb1o)". Journal of the
   American Statistical Association 98 (January): 750-763. 
