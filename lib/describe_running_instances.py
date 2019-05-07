"""This script is only meant to give a quick view into an account and give an 
overview of running instances for further troubleshooting."""
import boto3
import itertools
import json

client = boto3.client('ec2')

def instances():
  """
  Return a list of instances in the account.
  
  :return: list of instances
  """
  response = client.describe_instances()
  if not response:
    raise Exception("There are no instances in this environment.")
  r_instances = [r['Instances'] for r in response['Reservations']]
  return list(itertools.chain.from_iterable(r_instances))

def print_result(result):
  """
  Print the results grouped by their instance state.
  
  :param result: dict of instance states and instance ids
  """
  print('*' * 15 + "\nInstance States\n" + '*' * 15)
  
  for state in result:
    print(
      '=' * 15 + '\n{} x {}\n'.format(state, len(result[state])) + '=' * 15
    )
    state_instances = (result[state])
    for i in state_instances:
      print(i)

def collect_results(instances):
  """
  Organize the given instances by their state and return the result.
  
  :param instances: list of instances
  :return: dict of instance states and instance ids
  """
  result = {}
  for i in instances:
    instance_id = i['InstanceId']
    state = i['State']['Name']
    if state not in result:
      result[state] = []
    result[state].append(instance_id)
  return result

def main():
  """Main entry point for the script."""
  print_result(collect_results(instances()))

if __name__ == '__main__':
  main()