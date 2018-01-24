

def is_rds_db_snapshot_attr_public_access(rds_db_snapshot_attribute):
    """
    Checks whether a RDS snapshot attribute is:

    {
        "AttributeName": "restore",
        "AttributeValues": ["random_aws_account_id", "any"]
    }

    >>> is_rds_db_snapshot_attr_public_access({"AttributeName": "restore", "AttributeValues": ["any"]})
    True
    >>> is_rds_db_snapshot_attr_public_access({"AttributeName": "restore", "AttributeValues": ["aws_account_id"]})
    False
    >>> is_rds_db_snapshot_attr_public_access({"AttributeName": "restore", "AttributeValues": []})
    False
    >>> is_rds_db_snapshot_attr_public_access({"AttributeName": "blorg", "AttributeValues": ["any"]})
    False
    >>> is_rds_db_snapshot_attr_public_access([])
    Traceback (most recent call last):
    ...
    TypeError: list indices must be integers or slices, not str
    >>> is_rds_db_snapshot_attr_public_access(0)
    Traceback (most recent call last):
    ...
    TypeError: 'int' object is not subscriptable
    >>> is_rds_db_snapshot_attr_public_access(None)
    Traceback (most recent call last):
    ...
    TypeError: 'NoneType' object is not subscriptable
    """
    return rds_db_snapshot_attribute['AttributeName'] == 'restore' \
      and 'any' in rds_db_snapshot_attribute['AttributeValues']


def does_rds_db_security_group_grant_public_access(sg):
    """
    Checks an RDS instance for a DB security group with CIDRIP 0.0.0.0/0

    >>> does_rds_db_security_group_grant_public_access({"IPRanges": [{"CIDRIP": "127.0.0.1/32", "Status": "authorized"}, {"CIDRIP": "0.0.0.0/0", "Status": "authorized"}]})
    True
    >>> does_rds_db_security_group_grant_public_access({"IPRanges": []})
    False
    """
    return any(ipr['CIDRIP'] == '0.0.0.0/0' and ipr['Status'] == 'authorized' for ipr in sg['IPRanges'])


def does_vpc_security_group_grant_public_access(sg):
    """
    Checks an RDS instance for a VPC security groups with ingress permission ipv4 range 0.0.0.0/0 or ipv6 range :::/0

    >>> does_vpc_security_group_grant_public_access({'IpPermissions': [{'Ipv6Ranges': [], 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}]})
    True
    >>> does_vpc_security_group_grant_public_access({'IpPermissions': [{'Ipv6Ranges': [], 'IpRanges': []}]})
    False
    >>> does_vpc_security_group_grant_public_access({'IpPermissions': [{'Ipv6Ranges': [], 'IpRanges': [{'CidrIp': '192.168.1.0/0'}]}]})
    False
    """
    return any(ipr['CidrIp'] == '::/0' for ipp in sg['IpPermissions'] for ipr in ipp['Ipv6Ranges']) or \
      any(ipr['CidrIp'] == '0.0.0.0/0' for ipp in sg['IpPermissions'] for ipr in ipp['IpRanges'])


def is_rds_db_instance_encrypted(rds_db_instance):
    """
    Checks the RDS instance 'StorageEncrypted' value.

    >>> is_rds_db_instance_encrypted({'StorageEncrypted': True})
    True
    >>> is_rds_db_instance_encrypted({'StorageEncrypted': False})
    False
    >>> is_rds_db_instance_encrypted({})
    Traceback (most recent call last):
    ...
    KeyError: 'StorageEncrypted'
    >>> is_rds_db_instance_encrypted(0)
    Traceback (most recent call last):
    ...
    TypeError: 'int' object is not subscriptable
    >>> is_rds_db_instance_encrypted(None)
    Traceback (most recent call last):
    ...
    TypeError: 'NoneType' object is not subscriptable
    """
    return bool(rds_db_instance['StorageEncrypted'])


def is_rds_db_snapshot_encrypted(rds_db_snapshot):
    """
    Checks the RDS snapshot 'Encrypted' value.

    >>> is_rds_db_snapshot_encrypted({'Encrypted': True})
    True
    >>> is_rds_db_snapshot_encrypted({'Encrypted': False})
    False
    >>> is_rds_db_snapshot_encrypted({})
    Traceback (most recent call last):
    ...
    KeyError: 'Encrypted'
    >>> is_rds_db_snapshot_encrypted(0)
    Traceback (most recent call last):
    ...
    TypeError: 'int' object is not subscriptable
    >>> is_rds_db_snapshot_encrypted(None)
    Traceback (most recent call last):
    ...
    TypeError: 'NoneType' object is not subscriptable
    """
    return bool(rds_db_snapshot['Encrypted'])
