# VPC
resource "aws_vpc" "this" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name   = var.environment_name
    course = "dataEngineeringCourse"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "this" {
  vpc_id = aws_vpc.this.id

  tags = {
    Name   = var.environment_name
    course = "dataEngineeringCourse"
  }
}

# Subnets
data "aws_availability_zones" "available" {}

resource "aws_subnet" "public1" {
  vpc_id                  = aws_vpc.this.id
  cidr_block              = var.public_subnet1_cidr
  availability_zone       = data.aws_availability_zones.available.names[0]
  map_public_ip_on_launch = true

  tags = {
    Name   = "${var.environment_name} Public Subnet (AZ1)"
    course = "dataEngineeringCourse"
  }
}

resource "aws_subnet" "public2" {
  vpc_id                  = aws_vpc.this.id
  cidr_block              = var.public_subnet2_cidr
  availability_zone       = data.aws_availability_zones.available.names[1]
  map_public_ip_on_launch = true

  tags = {
    Name   = "${var.environment_name} Public Subnet (AZ2)"
    course = "dataEngineeringCourse"
  }
}

# Route table + associations
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.this.id

  tags = {
    Name   = "${var.environment_name} Public Routes"
    course = "dataEngineeringCourse"
  }
}

resource "aws_route" "default_public" {
  route_table_id         = aws_route_table.public.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.this.id
}

resource "aws_route_table_association" "assoc_public1" {
  subnet_id      = aws_subnet.public1.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "assoc_public2" {
  subnet_id      = aws_subnet.public2.id
  route_table_id = aws_route_table.public.id
}

# S3 Bucket
resource "aws_s3_bucket" "course_bucket" {
  bucket = var.s3_bucket_for_course

  tags = {
    course = "dataEngineeringCourse"
  }
}

# Optionally block public access to S3 (best practice)
resource "aws_s3_bucket_public_access_block" "course_bucket_block" {
  bucket = aws_s3_bucket.course_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
