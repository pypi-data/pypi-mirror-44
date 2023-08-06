# redis-tracker

Cli tool that redirect redis key values to stdout and/or [prometheus](http://prometheus.io)

    $ redis-tracker set zset text --prometheus 9090
    sending stats to prometheus: localhost:9090
    set                                                       84
    zset                                                      19
    text                                                  hello!

## Prometheus

The example above would produce these prometheus stats:

    # HELP redis_track redis key value tracking
    # TYPE redis_track gauge
    redis_track{key="set",source="redis@localhost/0:6379",type="set"} 1.0
    redis_track{key="zset",source="redis@localhost/0:6379",type="zset"} 1.0
    # HELP redis_track_info redis key value tracking
    # TYPE redis_track_info gauge
    redis_track_info{key="text",source="redis@localhost/0:6379",text="hello!",type="string"} 1.0
    
In other words:
    
* `sets` produce gauges that track their length
* `zsets` same as sets
* `string` produces `info`

## Usage

    $ redis-tracker --help                                                                                               
    Usage: redis-tracker [OPTIONS] [KEYS]...

      track redis keys to stdout and/or prometheus

    Options:
      --from-set TEXT       take keys from set key
      --prometheus INTEGER  enable prometheus polling on port
      --tick-rate INTEGER   how often to check in seconds  [default: 1]
      --no-color            disable output color
      -h TEXT               redis hoststring  [default: localhost]
      -p INTEGER            redis port  [default: 6379]
      -a TEXT               redis password
      -db INTEGER           redis host  [default: 0]
      --help                Show this message and exit.

## Install

    pip install redis-tracker
