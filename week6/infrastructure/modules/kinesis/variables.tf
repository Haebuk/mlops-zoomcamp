variable "stream_name"  {
    type = string
    description = "Kinesis stream name"
}

variable "shard_count" {
  type        = number
  description = "Kinisis stream shard count"
}

variable "retention_period" {
  type        = number
  description = "Kinisis stream retention period"
}

variable "shard_level_metrics" {
  type        = list(string)
  default     = [
    "IncomingBytes",
    "OutgoingBytes",
    "IncomingRecords",
    "OutgoingRecords",
    "WriteProvisionedThroughputExceeded",
    "ReadProvisionedThroughputExceeded",
    "IteratorAgeMilliseconds",
  ]
  description = "Kinisis stream shard level metrics"
}

variable "tags" {
  type        = string
  default     = "mlops-zoomcamp"
  description = "Tags for the Kinisis stream"
}
