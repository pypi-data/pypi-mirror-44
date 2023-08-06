import logging

import boto3
import cfnresponse

log = logging.getLogger()


def run(event, context):
    log.info('Event %s', event)

    ec2 = boto3.client('ec2')
    destinationCidrBlock = event['ResourceProperties']['DestinationCidrBlock']
    transitGatewayId = event['ResourceProperties']['TransitGatewayId']
    routeTable1 = event['ResourceProperties']['RouteTable1']
    if 'RouteTable2' not in event['ResourceProperties'].keys():
        rts = [routeTable1]
    else:
        rts = [routeTable1, event['ResourceProperties']['RouteTable2']]

    if event['RequestType'] in ['Create', 'Update']:
        physicalResId = 'keep'
        for i in rts:
            try:
                r = ec2.create_route(
                    DestinationCidrBlock=destinationCidrBlock,
                    TransitGatewayId=transitGatewayId,
                    RouteTableId=i
                )
                log.info('create_route response: %s', r)
            except Exception as e:
                log.exception(e)
                cfnresponse.send(event, context, cfnresponse.FAILED, {'Message': 'Route create/update failed'}, physicalResId)
                return 1
        cfnresponse.send(event, context, cfnresponse.SUCCESS, {'Message': 'Create/Update successful!'}, physicalResId)
    else:
        physicalResId = 'remove'
        for i in rts:
            try:
                r = ec2.delete_route(
                    DestinationCidrBlock=destinationCidrBlock,
                    RouteTableId=i
                )
                log.info('delete_route response: %s', r)
            except Exception as e:
                log.exception(e)
                cfnresponse.send(event, context, cfnresponse.FAILED, {'Message': 'Route delete failed'}, physicalResId)
                return 1
        cfnresponse.send(event, context, cfnresponse.SUCCESS, {'Message': 'Delete successful!'}, physicalResId)
    return 0
