output "vpc_id" {
  description = "A reference to the created VPC"
  value       = aws_vpc.this.id
}

output "public_subnets" {
  description = "A list of the public subnets"
  value       = [aws_subnet.public1.id, aws_subnet.public2.id]
}

output "public_subnet1" {
  description = "A reference to the public subnet in the 1st Availability Zone"
  value       = aws_subnet.public1.id
}

output "public_subnet2" {
  description = "A reference to the public subnet in the 2nd Availability Zone"
  value       = aws_subnet.public2.id
}

output "s3_bucket_name" {
  description = "The name of the created S3 bucket"
  value       = aws_s3_bucket.course_bucket.bucket
}
