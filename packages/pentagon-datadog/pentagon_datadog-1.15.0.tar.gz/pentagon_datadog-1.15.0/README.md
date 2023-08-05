# rodd
ReactiveOps best practices and sane defaults for dashboards and monitoring of Kubernetes infrastructure with Datadog.

## Requirements
- python >= 2.7
- $DATADOG_API_KEY and $DATADOG_APP_KEY
- [Pentagon](https://github.com/reactiveops/pentagon):
  - `pip install git+https://github.com/reactiveops/pentagon.git`

## Installation
`rodd` is a [Pentagon component](https://github.com/reactiveops/pentagon/blob/master/docs/components.md) so you'll need to have Pentagon installed.

`rodd` is based on terraform, so plan to create your rodd monitors in an appropriate directory. Enter that terraform directory and initialize by running: `pentagon add datadog -o$(pwd)`. This will create `datadog.tf` and the directory `datadog` that will contain an `rodd-example.yml` to get you up and running. `datadog.tf` will define the provider and module to be included in your terraform directory. The `datadog` directory will contain the terraform files that define monitors and dashboards.

## Usage
### [Monitors](docs/monitors.md)

We create a template with all the monitors we want to use. You can see the current monitors(yaml files) under [monitors](/monitors/). Later on, we talk about how to create our own monitors.

Have a look at [rodd-example.yml](/pentagon_datadog/files/datadog/rodd-example.yaml) here we define(under definitions) variables we want to use such as `cluster`. Then under `monitors` we call out the monitors we want to use. Finally, when ready run:

`pentagon add datadog.monitors -f rodd-example.yml`

Which creates a terraform module for each monitor.

#### Native Monitors and Monitor Families
There are several monitor included in this module and those are broken up into families. `kubernetes`, `rds` etc. See below for a comprehensive list. If you wish to deploy all monitors in a family, you can simply call out the family name in the yaml file. The following snippet will create a terraform file for each of the monitors in the `kubernetes` family.

```yaml
monitors:
  - source: kubernetes
```

You can override individual values in the monitor as necessary. A complete list of fields is declared [below](#monitor-fields).

This example will use all the defaults from the `kubernetes.cluster_bytes_received` monitor but override the `thresholds` and `timeout` fields.

```yaml
monitors:
  - source: kubernetes.cluster_bytes_received
    thresholds: {critical: 50, warning: 25}
    timeout_h: 3
```
#### Custom Monitors
If the monitor you want doesn't exist as a native monitor in a monitor family. You can define any monitor you want inline in the yaml file. This will create

```yaml
definitions:
  environment: "production"
  cluster: "production.cluster"
  notifications: "@pagerduty"
monitors:
  - notify_audit: false
    locked: false
    name: '[${environment}] Increase in network errors'
    tags: [network, '${environment}', reactiveops]
    include_tags: false
    no_data_timeframe: null
    silenced: {}
    new_host_delay: 300
    require_full_window: true
    notify_no_data: false
    renotify_interval: 0
    escalation_message: ''
    query: avg(last_15m):avg:kubernetes.network.rx_errors{kubernetescluster:${cluster}} + avg:kubernetes.network.tx_errors{kubernetescluster:${cluster}} > 10
    message: |
      {{#is_alert}}
      We are getting increasing network errors
      {{/is_alert}}
      ${notifications}
    type: metric alert
    thresholds: {critical: 10, warning: 5}
    timeout_h: 0
```

#### Monitor Definitions
Alluded to above, in each monitor there are certain fields that need to be defined; `environment`, `cluster` are two examples.
They are denoted by `${<name>}` in the template and are referred to as "definitions". You can define definitions at a global level.

```yaml
definitions:
  cluster: working.cluster
  environment: production
monitors:
  - source: kubernetes
```
or at an individual monitor level to override the global value.

```yaml
definitions:
  cluster: working.cluster
  environment: production
monitors:
  - source: kubernetes
    definitions:
      environment: staging # this will override the global value
```

#### Namespaced Monitors

Datadog does not support multiple namespaces in monitor query filters. As a workaround, Rodd monitors that include a namespace filter can generate multiple namespace specific monitors from a single monitor definition.

The underlying Rodd monitor must have `vary_by_namespace: true` set. The monitor's namespace definition value can be a string or a list. Each namespace definition value will produce a separate monitor and Terraform file.

```yaml
definitions:
  cluster: working.cluster
  environment: production
monitors:
  - source: kubernetes.deploy_replica_alert
    definitions:
      namespace: ['infra', 'kube-system', 'rbac-manager']
```

#### Exceptions
Sometimes you'll want to apply all the monitors or dashboards in a family of except one or two. In this case, you can can use a list of `exceptions` at the root of the YAML document. All the monitors or dashboards in that family will be templated except the ones listed in `exceptions`. The full path of the monitor is required:

```yaml
monitors:
  - source: kubernetes
exceptions:
  - kubernetes.cluster_bytes_received
```

This is not the path of the .tf file that is generated by rodd. This is the path of the monitor in the rodd monitors directory. Ie:

```yaml
monitors:
  - source: kubernetes
exceptions:
  - kubernetes.cluster_iops
# - kubernetes.(production_)high_number_of_total_iops_on_host
# NOT THIS ^
```

### Dashboards
Usage is exactly the same for Datadog Dashboards. They are `timeboard` type dashboards.

`pentagon add datadog.dashboards -f rodd/pentagon_datadog/files/rodd-example.yml`

NOTE: Dashboards do not support tags.


### Downtime
Usage is the same for Datadog downtimes.

`pentagon add datadog.downtimes -f rodd/pentagon_datadog/files/rodd-example.yml`

## Converting your own Monitors

You can export monitors from datadog and using `convert.py` create your own monitors.

## Monitor Fields
 Complete list of fields as taken from datadog tf [provider](https://www.terraform.io/docs/providers/datadog/r/monitor.html)
- notify_audit
- locked
- name
- tags
- include_tags
- no_data_timeframe
- silence
- new_host_delay
- require_full_window
- notify_no_data
- renotify_interval
- escalation_message
- query
- message
- type
- thresholds
- timeout_h

## Dashboard Fields
 Complete list of fields as taken from datadog tf [provider](https://www.terraform.io/docs/providers/datadog/r/timeboard.html)
- read_only
- description
- title
- graphs
- template_variables

## Downtime Fields
 Complete list of fields are taken from datadog tf [provider](https://www.terraform.io/docs/providers/datadog/r/downtime.html)
 - name - descriptive name for the downtime (not part of the downtime definition)
 - scope
 - active
 - start
 - end
 - start_date
 - end_date
 - recurrence_type
 - recurrence_period
 - recurrence_week_days
 - recurrence_until
 - message
 - monitor_id

## References:
- https://www.terraform.io/docs/providers/datadog/index.html
- https://github.com/reactiveops/pentagon
- https://github.com/reactiveops/pentagon/blob/master/docs/components.md
- https://docs.datadoghq.com/monitors/
